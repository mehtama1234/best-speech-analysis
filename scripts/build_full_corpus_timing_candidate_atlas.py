#!/usr/bin/env python3
"""Build a bounded full-local-media atlas of transcript/audio timing candidates."""

from __future__ import annotations

import json
import html
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/full-reading-queue.json"
FEATURE_DIR = ROOT / "data/features"
OUT = ROOT / "research/full-corpus-timing-candidate-atlas.json"
MD = ROOT / "writeups/full-corpus-timing-candidate-atlas.md"
HTML = ROOT / "writeups/full-corpus-timing-candidate-atlas.html"


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    source_by_video = {row.get("video_id") or row.get("id"): row for row in queue.get("videos", queue.get("items", []))}
    candidates = []
    raw_counts = Counter()
    aligned_video_count = 0
    aligned_segment_count = 0
    density_selected = Counter()
    for path in sorted(FEATURE_DIR.glob("*.json")):
        report = json.loads(path.read_text())
        video_id = report.get("video_id")
        rows = [row for row in report.get("aligned_transcript", []) if row.get("evidence_id")]
        if not rows:
            continue
        aligned_video_count += 1
        aligned_segment_count += len(rows)
        source = source_by_video.get(video_id, {})
        url = source.get("url") or source.get("source_url") or f"https://www.youtube.com/watch?v={video_id}"
        title = source.get("title") or video_id

        def add(row: dict, reason: str, selected: bool = True) -> None:
            if not selected:
                return
            candidates.append({
                "candidate_id": f"{video_id}:{row['evidence_id'].split(':')[-1]}:{reason}",
                "video_id": video_id,
                "title": title,
                "source_url": url,
                "evidence_id": row["evidence_id"],
                "start_seconds": row.get("start_seconds"),
                "end_seconds": row.get("end_seconds"),
                "text": row.get("text", ""),
                "candidate_reason": reason,
                "words_per_second_proxy": row.get("words_per_second_proxy"),
                "transcript_gap_before_seconds": row.get("transcript_gap_before_seconds"),
                "transcript_gap_after_seconds": row.get("transcript_gap_after_seconds"),
                "mean_rms_db": row.get("mean_rms_db"),
                "speech_activity_fraction": row.get("speech_activity_fraction"),
                "feature_file": str(path.relative_to(ROOT)),
                "status": "proxy_candidate_requires_full_media_and_manual_listening",
            })

        for row in rows:
            before = row.get("transcript_gap_before_seconds")
            after = row.get("transcript_gap_after_seconds")
            if before is not None and before >= 1.0:
                raw_counts["gap_before"] += 1
                add(row, "gap_before_captioned_unit")
            if after is not None and after >= 1.0:
                raw_counts["gap_after"] += 1
                add(row, "gap_after_captioned_unit")

        # Density is highly confounded by caption segmentation. Retain only
        # the three lowest and three highest eligible rows per video, while
        # reporting the unbounded raw counts separately.
        density_rows = [row for row in rows if row.get("words_per_second_proxy") is not None and (row.get("word_count") or 0) >= 5]
        low = [row for row in density_rows if row["words_per_second_proxy"] <= 1.5]
        high = [row for row in density_rows if row["words_per_second_proxy"] >= 4.0]
        raw_counts["low_density"] += len(low)
        raw_counts["high_density"] += len(high)
        for row in sorted(low, key=lambda x: (x["words_per_second_proxy"], x["evidence_id"]))[:3]:
            density_selected["low_density"] += 1
            add(row, "lower_caption_density_proxy")
        for row in sorted(high, key=lambda x: (-x["words_per_second_proxy"], x["evidence_id"]))[:3]:
            density_selected["high_density"] += 1
            add(row, "higher_caption_density_proxy")

    # A segment can satisfy multiple candidate reasons; preserve each reason
    # because the review question differs for a boundary and density flag.
    report = {
        "schema_version": "1.0",
        "report_id": "full-corpus-timing-candidate-atlas",
        "status": "full_local_feature_proxy_atlas_manual_listening_pending",
        "source_queue": "research/full-reading-queue.json",
        "source_feature_directory": "data/features",
        "claim_boundary": "This atlas routes transcript/audio feature candidates for navigation. Caption gaps may reflect editing, missing captions, music, turn changes or silence; density reflects retained caption segmentation. No row establishes an intentional pause, pace choice, vocal meaning, identity, alignment, effectiveness or listener outcome.",
        "eligibility": "Feature reports with at least one aligned retained transcript row; density rows require at least five retained words and retain at most three low and three high rows per video.",
        "thresholds": {"gap_candidate_seconds": 1.0, "lower_density_words_per_second": 1.5, "higher_density_words_per_second": 4.0, "density_word_count_minimum": 5, "density_rows_per_video_per_side": 3},
        "coverage": {"aligned_video_count": aligned_video_count, "aligned_segment_count": aligned_segment_count, "candidate_record_count": len(candidates), "candidate_video_count": len({row["video_id"] for row in candidates}), "raw_tag_counts": dict(raw_counts), "selected_density_counts": dict(density_selected)},
        "items": candidates,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    reasons = Counter(row["candidate_reason"] for row in candidates)
    lines = ["# Full-corpus timing candidate atlas", "", "Status: **full local feature proxy atlas; manual listening and independent review pending**.", "", report["claim_boundary"], "", f"Aligned feature coverage: **{aligned_video_count} videos / {aligned_segment_count} caption rows** · routed candidate records: **{len(candidates)}** across **{report['coverage']['candidate_video_count']} videos**.", "", "| Candidate reason | Routed records | Raw matches before density cap |", "|---|---:|---:|"]
    for reason in ("gap_before_captioned_unit", "gap_after_captioned_unit", "lower_caption_density_proxy", "higher_caption_density_proxy"):
        raw_key = {"gap_before_captioned_unit": "gap_before", "gap_after_captioned_unit": "gap_after", "lower_caption_density_proxy": "low_density", "higher_caption_density_proxy": "high_density"}[reason]
        lines.append(f"| `{reason}` | {reasons[reason]} | {raw_counts[raw_key]} |")
    lines += ["", "## Review rule", "", "Open the linked source interval and inspect the complete captioned unit. Decide whether the boundary or density comes from speech, silence, an edit, music, a turn change, caption segmentation or missing data. Preserve `indeterminate` when the source cannot establish the cause. The atlas is a navigation surface, not a best-practice ranking.", ""]
    MD.write_text("\n".join(lines))
    cards = []
    for row in candidates:
        cards.append(
            "<article class='card' data-reason='{}' data-video='{}' data-search='{}'>"
            "<h2>{}</h2><p><a target='_blank' rel='noreferrer' href='{}'>Open source at timestamp</a> · <code>{}</code></p>"
            "<p class='excerpt'>{}</p><p class='metrics'>reason: <code>{}</code> · W/s: {} · gap before: {} · gap after: {} · RMS: {}</p>"
            "<button type='button' class='review-button'>Review locally</button></article>".format(
                html.escape(row["candidate_reason"]), html.escape(row["video_id"]),
                html.escape((row["title"] + " " + row["video_id"] + " " + row["candidate_reason"] + " " + row["text"]).lower()),
                html.escape(row["title"]), html.escape(row["source_url"]), html.escape(row["evidence_id"]),
                html.escape(row["text"]), html.escape(row["candidate_reason"]), row["words_per_second_proxy"],
                row["transcript_gap_before_seconds"], row["transcript_gap_after_seconds"], row["mean_rms_db"],
            )
        )
    jobs = sorted({row["candidate_reason"] for row in candidates})
    html_page = """<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Full-corpus timing candidate atlas</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1180px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select,textarea,button{font:inherit;padding:.6rem;margin:.3rem .5rem .7rem 0}input{width:min(620px,100%)}textarea{width:min(800px,100%);min-height:4rem;display:block}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:.8rem}.review{border:2px solid #426b8a;border-radius:8px;padding:1rem;margin:1rem 0;background:#f4f8fb}.card{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.card h2{font-size:1rem;margin:.1rem 0 .4rem}.excerpt{color:#36454f}.metrics{font-family:ui-monospace,monospace;font-size:.86rem}code{overflow-wrap:anywhere}</style><main><h1>Full-corpus timing candidate atlas</h1><div class='notice'><strong>Review queue, not a score.</strong> These records are transcript/audio proxy candidates across locally aligned videos. A gap may be speech, editing, music, a turn, caption segmentation or missing data. Reviews stay in this browser's local storage until exported; nothing is uploaded. Validate exports with <code>scripts/validate_timing_candidate_reviews.py</code>.</div><p id='count' aria-live='polite'></p><label>Reason <select id='reason'><option value=''>All reasons</option></select></label><label>Search <input id='search' type='search' placeholder='video, title, evidence or wording'></label><section id='review' class='review' hidden><h2>Local timing review</h2><p id='selected'></p><label>Reviewer code <input id='reviewer' autocomplete='off'></label><label>Transcript/audio alignment <select id='alignment'><option value='not_reviewed'>not reviewed</option><option value='clear'>clear</option><option value='partial'>partial</option><option value='misaligned'>misaligned</option></select></label><label>Observed cause <select id='cause'><option value='not_reviewed'>not reviewed</option><option value='speech_pause_or_boundary'>speech pause or boundary</option><option value='editing_or_cut'>editing or cut</option><option value='music_or_ambience'>music or ambience</option><option value='turn_or_response'>turn or response</option><option value='caption_segmentation'>caption segmentation</option><option value='missing_or_unclear'>missing or unclear</option></select></label><label>Observation / uncertainty<textarea id='observation'></textarea></label><label>Accessibility or modality note<textarea id='accessibility'></textarea></label><button id='save' type='button'>Save local review</button> <button id='export' type='button'>Export local reviews</button> <span id='saved' aria-live='polite'></span></section><section id='cards'>""" + "\n".join(cards) + """</section></main><script>const cards=[...document.querySelectorAll('.card')],reason=document.querySelector('#reason'),search=document.querySelector('#search'),count=document.querySelector('#count'),review=document.querySelector('#review'),selected=document.querySelector('#selected'),saved=document.querySelector('#saved');let current=null;const fields=['reviewer','alignment','cause','observation','accessibility'];let reviews=JSON.parse(localStorage.getItem('full_corpus_timing_reviews')||'{}');const reasons=[...new Set(cards.map(x=>x.dataset.reason))].sort();reasons.forEach(x=>{let o=document.createElement('option');o.value=x;o.textContent=x;reason.append(o)});function filter(){let q=search.value.toLowerCase(),r=reason.value,n=0;cards.forEach(x=>{let ok=(!r||x.dataset.reason===r)&&(!q||x.dataset.search.includes(q));x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${cards.length} timing candidates`}function openReview(card){current=card;review.hidden=false;selected.textContent=card.querySelector('h2').innerText+' — '+card.dataset.video+' — '+card.querySelector('code').innerText;let old=reviews[card.querySelector('code').innerText]||{};fields.forEach(id=>{document.querySelector('#'+id).value=old[id]||document.querySelector('#'+id).value});saved.textContent=reviews[card.querySelector('code').innerText]?'Existing local review loaded.':'';review.scrollIntoView({behavior:'smooth',block:'start'})}cards.forEach(card=>card.querySelector('.review-button').onclick=()=>openReview(card));document.querySelector('#save').onclick=()=>{if(!current)return;let id=current.querySelector('code').innerText,row={candidate_id:id,updated_at:new Date().toISOString()};fields.forEach(x=>row[x]=document.querySelector('#'+x).value);reviews[id]=row;localStorage.setItem('full_corpus_timing_reviews',JSON.stringify(reviews));saved.textContent=`Saved ${Object.keys(reviews).length} local review(s).`};document.querySelector('#export').onclick=()=>{let blob=new Blob([JSON.stringify(Object.values(reviews),null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='full-corpus-timing-reviews.json';a.click();URL.revokeObjectURL(a.href)};reason.onchange=filter;search.oninput=filter;filter()</script>"""
    HTML.write_text(html_page)
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "aligned_videos": aligned_video_count, "aligned_segments": aligned_segment_count, "candidate_records": len(candidates), "candidate_videos": report["coverage"]["candidate_video_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
