#!/usr/bin/env python3
"""Build an all-video delivery inspection queue without interpreting proxies."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "research/full-corpus-media-coverage.json"
PROXY = ROOT / "research/full-delivery-proxy-index.json"
ITINERARY = ROOT / "research/corpus-video-learning-itinerary.json"
OUT = ROOT / "research/full-corpus-delivery-inspection.json"
MD = ROOT / "writeups/full-corpus-delivery-inspection.md"
HTML = ROOT / "writeups/full-corpus-delivery-inspection.html"


def build() -> dict:
    media = {row["video_id"]: row for row in json.loads(MEDIA.read_text())["videos"]}
    proxy = {row["video_id"]: row for row in json.loads(PROXY.read_text())["videos"]}
    itinerary = {row["video_id"]: row for row in json.loads(ITINERARY.read_text())["entries"]}
    rows = []
    for video_id in sorted(media):
        m = media[video_id]
        p = proxy.get(video_id, {})
        route = itinerary.get(video_id, {})
        state = m.get("media_state", "not_in_media_audit")
        if state == "raw_audio_video_present":
            inspection_status = "raw_media_available_manual_review_pending"
        elif p:
            inspection_status = "proxy_available_raw_media_missing_manual_review_pending"
        else:
            inspection_status = "media_unavailable_manual_review_not_possible_locally"
        rows.append({
            "video_id": video_id,
            "title": m.get("title") or route.get("title"),
            "source_url": m.get("source_url"),
            "writeup": route.get("writeup"),
            "learning_track": route.get("learning_track"),
            "media_state": state,
            "inspection_status": inspection_status,
            "raw_media_files": m.get("video_files", []) + m.get("audio_files", []),
            "feature_report": p.get("feature_file"),
            "aligned_transcript_segment_count": p.get("aligned_transcript_segment_count", 0),
            "sampled_frame_count": p.get("sampled_frame_count", 0),
            "claim_boundary": "This is an inspection queue. Raw media and local features establish availability or measurable proxies only; they do not establish intentional delivery, emotion, gesture meaning, speaker identity, audience response, comprehension or effectiveness.",
            "review_prompt": "Listen/watch the exact evidence window if available. Record only observable timing, vocal change, visible action, setting, edit, accessibility and missingness; preserve indeterminate judgments.",
        })
    report = {
        "schema_version": "1.0",
        "queue_id": "full-corpus-delivery-inspection",
        "status": "all_video_delivery_inspection_queue_proxy_only_manual_review_pending",
        "claim_boundary": "This queue routes delivery inspection for every fixed-corpus video. It is not a set of nonverbal findings or effectiveness evidence.",
        "source_artifacts": ["research/full-corpus-media-coverage.json", "research/full-delivery-proxy-index.json", "research/corpus-video-learning-itinerary.json"],
        "video_count": len(rows),
        "inspection_status_counts": {status: sum(row["inspection_status"] == status for row in rows) for status in sorted({row["inspection_status"] for row in rows})},
        "media_state_counts": {state: sum(row["media_state"] == state for row in rows) for state in sorted({row["media_state"] for row in rows})},
        "feature_report_count": sum(bool(row["feature_report"]) for row in rows),
        "rows": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Full-corpus delivery inspection queue", "", "Status: **all 395 videos routed; manual delivery review pending; proxies are not findings**.", "", report["claim_boundary"], "", f"Videos: **{len(rows)}** · feature reports linked: **{report['feature_report_count']}**.", "", "| Video | Media state | Inspection status | Feature report | Learning track |", "|---|---|---|---|---|"]
    for row in rows:
        title = (row["title"] or "").replace("|", "\\|")
        source = f"[{title}]({row['source_url']})" if row.get("source_url") else title
        lines.append(f"| `{row['video_id']}` {source} | `{row['media_state']}` | `{row['inspection_status']}` | `{row['feature_report'] or 'none'}` | `{row['learning_track'] or 'unrouted'}` |")
    lines += ["", "For a manual pass, open the source and linked full-context writeup, then record observable timing, vocal change, visible action, setting, editing, accessibility and missingness. Do not infer emotion, intent, confidence or effectiveness from a proxy or a single frame.", ""]
    MD.write_text("\n".join(lines))
    articles = []
    for row in rows:
        search = " ".join(str(value) for value in row.values()).lower()
        title = html.escape(row["title"] or row["video_id"])
        links = []
        if row.get("source_url"):
            links.append(f"<a href='{html.escape(row['source_url'], quote=True)}'>source</a>")
        if row.get("writeup"):
            links.append(f"<a href='../{html.escape(row['writeup'])}'>full writeup</a>")
        articles.append(f"<article class='video' data-state='{html.escape(row['media_state'], quote=True)}' data-search='{html.escape(search, quote=True)}'><h2>{title}</h2><p><code>{html.escape(row['video_id'])}</code> · {' · '.join(links)}</p><p><b>Media:</b> <code>{html.escape(row['media_state'])}</code> · <b>Inspection:</b> <code>{html.escape(row['inspection_status'])}</code> · <b>Track:</b> <code>{html.escape(row['learning_track'] or 'unrouted')}</code></p><p><b>Feature report:</b> <code>{html.escape(row['feature_report'] or 'none')}</code> · aligned transcript segments: {row['aligned_transcript_segment_count']} · sampled frames: {row['sampled_frame_count']}</p><p>{html.escape(row['review_prompt'])}</p><p class='boundary'>{html.escape(row['claim_boundary'])}</p></article>")
    HTML.write_text("""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Full-corpus delivery inspection queue</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select{font:inherit;padding:.7rem;margin:1rem .5rem 1rem 0}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.video{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.video h2{margin:.1rem 0}.boundary{color:#5c6872;font-size:.92rem}code{overflow-wrap:anywhere}</style><main><h1>Full-corpus delivery inspection queue</h1><div class='notice'><b>Inspection queue, not findings.</b> All 395 fixed-corpus videos are routed. Raw media and local features establish availability or measurable proxies only; they do not establish meaning, intent or effectiveness.</div><p>Open a source, inspect the exact context, and record observable timing, vocal change, visible action, setting, editing, accessibility and missingness.</p><label>Media state <select id='state'><option value=''>All states</option><option>raw_audio_video_present</option><option>derived_features_only</option><option>transcript_only_no_local_media</option><option>video_only</option></select></label><label>Search <input id='search' type='search' placeholder='video, title, status, track or feature'></label><p id='count' aria-live='polite'></p><section id='videos'>__VIDEOS__</section></main><script>const videos=[...document.querySelectorAll('.video')],state=document.querySelector('#state'),input=document.querySelector('#search'),count=document.querySelector('#count');function filter(){const s=state.value,q=input.value.toLowerCase();let n=0;videos.forEach(x=>{const ok=(!s||x.dataset.state===s)&&(!q||x.dataset.search.includes(q));x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${videos.length} videos`}state.onchange=filter;input.oninput=filter;filter()</script>""".replace("__VIDEOS__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    report = build()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": report["video_count"]}, indent=2))
