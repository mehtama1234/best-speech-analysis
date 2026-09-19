#!/usr/bin/env python3
"""Build a 30-day route through every reviewed video."""

from __future__ import annotations

import json
import html
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITINERARY = ROOT / "research/corpus-video-learning-itinerary.json"
OUT = ROOT / "research/corpus-30-day-study-route.json"
MD = ROOT / "writeups/corpus-30-day-study-route.md"
HTML = ROOT / "writeups/corpus-30-day-study-route.html"


def build() -> dict:
    entries = json.loads(ITINERARY.read_text())["entries"]
    by_job = defaultdict(deque)
    for entry in entries:
        by_job[entry["canonical_job"]].append(entry)
    jobs = sorted(by_job)
    ordered = []
    while any(by_job.values()):
        for job in jobs:
            if by_job[job]:
                ordered.append(by_job[job].popleft())
    days = []
    for offset in range(0, len(ordered), 14):
        chunk = ordered[offset:offset + 14]
        day_number = len(days) + 1
        days.append({
            "day": day_number,
            "video_count": len(chunk),
            "video_ids": [entry["video_id"] for entry in chunk],
            "entries": [{
                "video_id": entry["video_id"], "title": entry["title"], "canonical_job": entry["canonical_job"],
                "writeup": entry.get("writeup"), "phrase_handle_count": len(entry.get("phrase_handles", [])),
                "exact_evidence_count": len(entry.get("exact_evidence", [])),
                "delivery_status": entry.get("delivery_proxy", {}).get("status"),
            } for entry in chunk],
            "practice": "Read the exact evidence for two entries, name the listener problem and repeatable move, then adapt one move in your own words. Ask for a one-sentence restatement and record one non-fit or revision.",
            "self_check": "Can you explain what changed, what remains uncertain and why the move fits this situation without copying the speaker's identity or certainty?",
        })
    route = {
        "schema_version": "1.0", "route_id": "corpus-30-day-study-route", "status": "complete_corpus_route_transcript_derived_not_validated",
        "claim_boundary": "This route schedules inspection and practice of every reviewed video. It is not validation evidence and does not rank videos, establish effectiveness, or replace independent review and listener/learner testing.",
        "source": "research/corpus-video-learning-itinerary.json", "video_count": len(entries), "day_count": len(days), "max_videos_per_day": max(day["video_count"] for day in days), "days": days,
    }
    OUT.write_text(json.dumps(route, ensure_ascii=False, indent=2) + "\n")
    lines = ["# 30-day route through the full speech corpus", "", "Status: **every reviewed video scheduled for inspection and practice; not validation evidence**.", "", route["claim_boundary"], "", f"Videos: **{route['video_count']}** · days: **{route['day_count']}** · maximum videos in one day: **{route['max_videos_per_day']}**.", "", "## Daily loop", "", "1. Read the exact evidence for two listed videos and open the linked writeup.", "2. Name the listener problem and the observed move before looking at the phrase handle.", "3. Rewrite one repeatable form in your own relationship, evidence level and access mode.", "4. Try it once; ask for a listener restatement when possible.", "5. Record the non-fit, safety/accessibility issue and next revision in the local practice log.", "", "## Route", "", "The route deliberately rotates canonical jobs so the month does not become a single-speaker or single-style imitation exercise.", ""]
    for day in days:
        lines += [f"### Day {day['day']} — {day['video_count']} videos", "", day["practice"], "", f"**Self-check:** {day['self_check']}", "", "| Video | Job | Exact evidence | Phrase handles | Delivery |", "|---|---|---:|---:|---|"]
        for entry in day["entries"]:
            title = entry["title"].replace("|", "\\|")
            lines.append(f"| `{entry['video_id']}` {title} | `{entry['canonical_job']}` | {entry['exact_evidence_count']} | {entry['phrase_handle_count']} | `{entry['delivery_status']}` |")
        lines.append("")
    lines += ["Use the [searchable itinerary](corpus-video-learning-itinerary.html) for the full card, source link and delivery inspection details. The [practice log](corpus-learner-card-inventory.html) is local and does not establish learner or listener outcomes.", ""]
    MD.write_text("\n".join(lines))
    day_articles = []
    for day in days:
        entries = "".join(f"<li><a href='../{html.escape(entry['writeup'])}'>{html.escape(entry['title'])}</a> · <code>{html.escape(entry['video_id'])}</code> · <code>{html.escape(entry['canonical_job'])}</code> · evidence {entry['exact_evidence_count']} · phrases {entry['phrase_handle_count']}</li>" if entry.get("writeup") else f"<li>{html.escape(entry['title'])} · <code>{html.escape(entry['video_id'])}</code> · <code>{html.escape(entry['canonical_job'])}</code></li>" for entry in day["entries"])
        day_articles.append(f"<article class='day' data-day='{day['day']}' data-search='{html.escape(' '.join(str(x) for x in day.values()), quote=True)}'><h2>Day {day['day']} · {day['video_count']} videos</h2><p>{html.escape(day['practice'])}</p><p><b>Self-check:</b> {html.escape(day['self_check'])}</p><ol>{entries}</ol></article>")
    HTML.write_text("""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>30-day corpus study route</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select{font:inherit;padding:.7rem;margin:1rem .5rem 1rem 0}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.day{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.day h2{margin:.1rem 0}code{overflow-wrap:anywhere}</style><main><h1>30-day corpus study route</h1><div class='notice'><b>Practice route, not proof.</b> All 395 reviewed videos are scheduled once. Read exact context, adapt one move, ask for restatement, and record non-fit or revision.</div><label>Day <select id='day'><option value=''>All days</option>__DAYS__</select></label><label>Search <input id='search' type='search' placeholder='video, title, job or day'></label><p id='count' aria-live='polite'></p><section id='route'>__DAYS_CONTENT__</section></main><script>const days=[...document.querySelectorAll('.day')],day=document.querySelector('#day'),search=document.querySelector('#search'),count=document.querySelector('#count');function filter(){const q=search.value.toLowerCase(),d=day.value;let n=0;days.forEach(x=>{const ok=(!d||x.dataset.day===d)&&(!q||x.dataset.search.toLowerCase().includes(q));x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${days.length} days`}day.onchange=filter;search.oninput=filter;filter()</script>""".replace("__DAYS__", "".join(f"<option>{day['day']}</option>" for day in days)).replace("__DAYS_CONTENT__", "\n".join(day_articles)))
    return route


if __name__ == "__main__":
    route = build()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": route["video_count"], "day_count": route["day_count"]}, indent=2))
