#!/usr/bin/env python3
"""Build the shared curriculum index from the current 18-job curriculum."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows_from_curriculum(curriculum: dict) -> list[dict]:
    rows = []
    for lesson in curriculum["lessons"]:
        rows.append({
            "pattern_id": lesson["pattern_id"],
            "slice": "communication-job-curriculum",
            "communication_job": lesson["communication_problem"],
            "practice_hypothesis": lesson["mechanism_hypothesis"],
            "evidence_level": "provisional_practice_hypothesis",
            "packet": "research/communication-job-cards.json",
            "lesson": "writeups/communication-job-curriculum.html",
            "practice_flows": "research/communication-job-mobile-lessons.json",
            "learner_check": "research/communication-job-learner-check.json",
            "lesson_status": lesson["status"],
            "packet_status": "provisional_not_validated",
            "independent_review_status": lesson["validation"].get("independent_function_review", "pending"),
            "learner_status": lesson["validation"].get("learner_check", "not_run"),
            "representative_example_count": len(lesson.get("exact_examples", [])),
            "counterexample_count": len(lesson.get("counterexample_slots", [])),
            "source_limit": "Transcript and queued delivery evidence remain provisional; independent review and outcome evidence are pending.",
            "multimodal_status": "delivery_queue_manual_observation_pending",
        })
    return rows


def main() -> int:
    curriculum = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text())
    rows = rows_from_curriculum(curriculum)
    payload = {
        "schema_version": "1.0",
        "index_id": "shared-provisional-curriculum",
        "status": "18_draft_lessons_not_validated",
        "evidence_level": "provisional_practice_hypotheses",
        "lesson_count": len(rows),
        "claim_boundary": "This index links transcript evidence, queued delivery evidence and draft practice tasks. It does not present patterns as proven communication effects or claim that learners have completed the tasks.",
        "shared_learner_check": "research/communication-job-learner-check.json",
        "shared_learner_check_html": "writeups/communication-job-learner-check.html",
        "shared_learner_check_validator": "scripts/validate_communication_job_learner_record.py",
        "shared_lesson_cards": "research/shared-lesson-cards.json",
        "shared_lesson_cards_html": "writeups/shared-lesson-cards.html",
        "lessons": rows,
        "validation_gates": {
            "independent_review": "pending",
            "learner_observations": "not_started",
            "listener_outcomes": "not_tested",
            "full_corpus_audiovisual_coverage": "not_complete",
        },
    }
    out = ROOT / "research/shared-provisional-curriculum.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Best Speech Analysis — Provisional Curriculum</title><style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#202938}}.notice{{background:#fff7d6;border:1px solid #d8bd61;padding:1rem;border-radius:8px}}.controls{{display:flex;gap:1rem;margin:1rem 0;flex-wrap:wrap}}input,select{{font:inherit;padding:.5rem}}article{{border:1px solid #d7d0c5;border-radius:8px;padding:1rem;margin:1rem 0}}.meta{{color:#5b6570;font-size:.9rem}}a{{color:#075985}}</style></head><body><h1>Provisional communication curriculum</h1><div class="notice"><b>18 draft lessons.</b> Independent review, delivery observations, learner observations and listener outcomes remain incomplete.</div><div class="controls"><label>Search <input id="search" type="search"></label><label>Slice <select id="slice"><option value="">All</option><option value="communication-job-curriculum">Current 18-job curriculum</option></select></label></div><p id="count"></p><main id="lessons"></main><script id="data" type="application/json">{data}</script><script>const rows=JSON.parse(document.getElementById('data').textContent),q=document.getElementById('search'),s=document.getElementById('slice'),out=document.getElementById('lessons'),count=document.getElementById('count');const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));function render(){{const term=q.value.toLowerCase(),xs=rows.filter(x=>(!term||JSON.stringify(x).toLowerCase().includes(term))&&(!s.value||x.slice===s.value));count.textContent=xs.length+' of '+rows.length+' lessons';out.innerHTML=xs.map(x=>'<article><div class="meta">'+esc(x.pattern_id)+' · '+esc(x.lesson_status)+'</div><h2>'+esc(x.communication_job)+'</h2><p>'+esc(x.practice_hypothesis)+'</p><p>'+x.representative_example_count+' exact examples · '+x.counterexample_count+' counterexample slots · '+esc(x.independent_review_status)+'</p><p><a href="../writeups/communication-job-curriculum.html">Open integrated curriculum</a> · <a href="../research/communication-job-cards.json">Evidence cards</a> · <a href="../research/communication-job-mobile-lessons.json">Mobile payload</a></p></article>').join('')||'<p>No matching lesson.</p>'}}q.oninput=render;s.onchange=render;render();</script></body></html>'''
    (ROOT / "writeups/shared-provisional-curriculum.html").write_text(page)
    lines = ["# Shared provisional curriculum", "", "The current shared model contains 18 draft communication-job lessons. It is a curriculum index, not a promotion claim.", "", "| Pattern | Lesson status | Independent review | Learner status |", "|---|---|---|---|"]
    lines.extend(f"| `{row['pattern_id']}` | `{row['lesson_status']}` | `{row['independent_review_status']}` | `{row['learner_status']}` |" for row in rows)
    lines += ["", "The shared lesson-card model is `research/shared-lesson-cards.json`; the mobile payload is `research/communication-job-mobile-lessons.json`.", ""]
    (ROOT / "writeups/shared-provisional-curriculum.md").write_text("\n".join(lines))
    print(json.dumps({"json": str(out.relative_to(ROOT)), "lessons": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
