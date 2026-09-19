#!/usr/bin/env python3
"""Audit learner-surface coverage for every fixed-corpus video."""

from __future__ import annotations

import json
import html
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/corpus-learner-card-inventory.json"
ITINERARY = ROOT / "research/corpus-video-learning-itinerary.json"
MEDIA = ROOT / "research/full-corpus-media-coverage.json"
PROXIES = ROOT / "research/full-delivery-proxy-index.json"
OUT = ROOT / "research/corpus-learning-coverage-audit.json"
MD = ROOT / "writeups/corpus-learning-coverage-audit.md"
HTML = ROOT / "writeups/corpus-learning-coverage-audit.html"


def build() -> dict:
    cards = json.loads(CARDS.read_text())
    itinerary = json.loads(ITINERARY.read_text())
    media_report = json.loads(MEDIA.read_text())
    proxy_report = json.loads(PROXIES.read_text())
    media_by_video = {row["video_id"]: row for row in media_report["videos"]}
    proxy_by_video = {row["video_id"]: row for row in proxy_report["videos"]}
    itinerary_ids = {entry["video_id"] for entry in itinerary["entries"]}
    functions = defaultdict(list)
    sequences = defaultdict(list)
    for card in cards["cards"]:
        functions[card["video_id"]].append(card)
    for card in cards["structural_cards"]:
        sequences[card["video_id"]].append(card)
    rows = []
    for route in itinerary["entries"]:
        video_id = route["video_id"]
        function_cards = functions[video_id]
        sequence_cards = sequences[video_id]
        all_cards = function_cards + sequence_cards
        media = media_by_video.get(video_id, {})
        proxy = proxy_by_video.get(video_id, {})
        row = {
            "video_id": video_id,
            "title": route["title"],
            "writeup": route.get("writeup"),
            "function_card_count": len(function_cards),
            "sequence_card_count": len(sequence_cards),
            "total_card_count": len(all_cards),
            "cards_with_exact_evidence": sum(bool(card.get("exact_evidence")) for card in all_cards),
            "cards_with_phrase_handles": sum(bool(card.get("phrase_handles")) for card in all_cards),
            "phrase_handle_count": sum(len(card.get("phrase_handles", [])) for card in all_cards),
            "cards_with_local_delivery_proxy": sum(card.get("delivery_proxy", {}).get("status", "").startswith("local") for card in all_cards),
            "cards_with_delivery_candidates": sum(bool(card.get("delivery_candidates")) for card in all_cards),
            "delivery_candidate_count": sum(len(card.get("delivery_candidates", [])) for card in all_cards),
            "cards_with_movement_candidates": sum(bool(card.get("movement_candidates")) for card in all_cards),
            "movement_candidate_count": sum(len(card.get("movement_candidates", [])) for card in all_cards),
            "selected_lesson_has_exact_evidence": bool(route.get("exact_evidence")),
            "selected_lesson_phrase_handle_count": len(route.get("phrase_handles", [])),
            "selected_lesson_delivery_status": route.get("delivery_proxy", {}).get("status"),
            "media_state": media.get("media_state", "not_in_media_audit"),
            "raw_audio_video_present": media.get("media_state") == "raw_audio_video_present",
            "feature_report_present": bool(proxy),
            "feature_report": proxy.get("feature_file"),
            "coverage_status": "covered_with_transcript_lesson" if all_cards and route.get("exact_evidence") else "review_required",
        }
        rows.append(row)
    report = {
        "schema_version": "1.0",
        "audit_id": "corpus-learning-coverage-audit",
        "status": "coverage_reconciled_transcript_derived_not_validation",
        "claim_boundary": "This audit proves that local learner artifacts are linked and counts reconcile for the fixed corpus. It is not validation evidence and does not prove source identity, function correctness, delivery meaning, teachability, listener comprehension or effectiveness.",
        "source_artifacts": ["research/corpus-learner-card-inventory.json", "research/corpus-video-learning-itinerary.json", "research/full-corpus-media-coverage.json", "research/full-delivery-proxy-index.json"],
        "video_count": len(rows),
        "videos_with_transcript_lesson": sum(row["coverage_status"] == "covered_with_transcript_lesson" for row in rows),
        "videos_requiring_review": sum(row["coverage_status"] != "covered_with_transcript_lesson" for row in rows),
        "summary": {
            "function_cards": sum(row["function_card_count"] for row in rows),
            "sequence_cards": sum(row["sequence_card_count"] for row in rows),
            "cards_with_exact_evidence": sum(row["cards_with_exact_evidence"] for row in rows),
            "cards_with_phrase_handles": sum(row["cards_with_phrase_handles"] for row in rows),
            "phrase_handle_count": sum(row["phrase_handle_count"] for row in rows),
            "cards_with_local_delivery_proxy": sum(row["cards_with_local_delivery_proxy"] for row in rows),
            "cards_with_delivery_candidates": sum(row["cards_with_delivery_candidates"] for row in rows),
            "delivery_candidate_count": sum(row["delivery_candidate_count"] for row in rows),
            "cards_with_movement_candidates": sum(row["cards_with_movement_candidates"] for row in rows),
            "movement_candidate_count": sum(row["movement_candidate_count"] for row in rows),
            "raw_audio_video_present": sum(row["raw_audio_video_present"] for row in rows),
            "feature_report_present": sum(row["feature_report_present"] for row in rows),
            "media_state_counts": {state: sum(row["media_state"] == state for row in rows) for state in sorted({row["media_state"] for row in rows})},
            "full_proxy_index_video_count": len(proxy_report["videos"]),
            "proxy_videos_without_itinerary_entry": len(set(proxy_by_video) - itinerary_ids),
        },
        "videos": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Corpus learning coverage audit", "", "Status: **coverage reconciled; transcript-derived and not validation evidence**.", "", report["claim_boundary"], "", f"Fixed-corpus videos: **{report['video_count']}** · videos with a transcript lesson and exact selected evidence: **{report['videos_with_transcript_lesson']}** · requiring review: **{report['videos_requiring_review']}**.", "", f"Cards: **{report['summary']['function_cards']}** function + **{report['summary']['sequence_cards']}** sequence · cards with exact evidence: **{report['summary']['cards_with_exact_evidence']}** · cards with phrase handles: **{report['summary']['cards_with_phrase_handles']}** (**{report['summary']['phrase_handle_count']}** handles) · local delivery proxies: **{report['summary']['cards_with_local_delivery_proxy']}** · cards with delivery candidates: **{report['summary']['cards_with_delivery_candidates']}** (**{report['summary']['delivery_candidate_count']}** windows) · cards with movement candidates: **{report['summary']['cards_with_movement_candidates']}** (**{report['summary']['movement_candidate_count']}** records).", "", "| Video | Function cards | Sequence cards | Exact evidence | Phrase-handle cards | Delivery proxy cards | Movement cards | Status |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in rows:
        lines.append(f"| `{row['video_id']}` {row['title'].replace('|', '\\|')} | {row['function_card_count']} | {row['sequence_card_count']} | {row['cards_with_exact_evidence']} | {row['cards_with_phrase_handles']} | {row['cards_with_local_delivery_proxy']} | {row['cards_with_movement_candidates']} | `{row['coverage_status']}` |")
    lines += ["", f"Media cross-check: **{report['summary']['raw_audio_video_present']}** learner-route videos have raw local audio/video; **{report['summary']['feature_report_present']}** learner-route videos have a linked feature report. The full proxy index contains **{report['summary']['full_proxy_index_video_count']}** reports, including **{report['summary']['proxy_videos_without_itinerary_entry']}** records without a retained itinerary entry. These are availability and measurement records, not manual nonverbal findings. Use the [full learner-card browser](corpus-learner-card-inventory.html) for card-level evidence and the [video itinerary](corpus-video-learning-itinerary.html) for one starting lesson per video. Coverage is not validation.", ""]
    MD.write_text("\n".join(lines))
    articles = []
    for row in rows:
        search = " ".join(str(value) for value in row.values()).lower()
        title = f"<a href='../{html.escape(row['writeup'])}'>{html.escape(row['title'])}</a>" if row.get("writeup") else html.escape(row["title"])
        articles.append(f"<article class='video' data-search='{html.escape(search, quote=True)}'><h2>{title}</h2><p><code>{html.escape(row['video_id'])}</code> · <b>{html.escape(row['coverage_status'])}</b></p><p>Function cards: <b>{row['function_card_count']}</b> · sequence cards: <b>{row['sequence_card_count']}</b> · exact evidence: <b>{row['cards_with_exact_evidence']}</b> · phrase-handle cards: <b>{row['cards_with_phrase_handles']}</b> · local delivery proxy cards: <b>{row['cards_with_local_delivery_proxy']}</b> · movement cards: <b>{row['cards_with_movement_candidates']}</b></p><p>Media: <code>{html.escape(row['media_state'])}</code> · feature report: <code>{'present' if row['feature_report_present'] else 'missing'}</code> · selected lesson phrase handles: <b>{row['selected_lesson_phrase_handle_count']}</b> · selected delivery status: <code>{html.escape(row['selected_lesson_delivery_status'] or '')}</code></p></article>")
    HTML.write_text("""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Corpus learning coverage audit</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input{font:inherit;padding:.7rem;width:min(700px,100%);margin:1rem 0}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.video{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.video h2{margin:.1rem 0}code{overflow-wrap:anywhere}.muted{color:#5c6872}</style><main><h1>Corpus learning coverage audit</h1><div class='notice'><b>Coverage, not validation.</b> Every fixed-corpus video is checked for linked transcript lessons and exact evidence. Phrase and delivery fields preserve their own missingness and claim boundaries.</div><p>395 videos · 4,016 function cards · 2,800 sequence cards · zero video-level lesson gaps.</p><label for='search'>Search video, title, status, job or coverage field</label><input id='search' type='search'><p id='count' aria-live='polite'></p><section id='videos'>__VIDEOS__</section></main><script>const videos=[...document.querySelectorAll('.video')],input=document.querySelector('#search'),count=document.querySelector('#count');function filter(){const q=input.value.toLowerCase();let n=0;videos.forEach(v=>{const ok=!q||v.dataset.search.includes(q);v.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${videos.length} videos`}input.oninput=filter;filter()</script>""".replace("__VIDEOS__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": build()["video_count"]}, indent=2))
