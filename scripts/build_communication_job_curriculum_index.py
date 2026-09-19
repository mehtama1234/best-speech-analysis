#!/usr/bin/env python3
"""Build the integrated, provisional 18-job learning surface."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/communication-job-cards.json"
LEARNER = ROOT / "research/communication-job-learner-check.json"
LISTENER = ROOT / "research/communication-job-listener-outcome-protocol.json"
DELIVERY = ROOT / "research/communication-job-delivery-sampling.json"
MEASUREMENTS = ROOT / "research/communication-job-delivery-measurement-preflight.json"
COUNTEREXAMPLES = ROOT / "research/communication-job-counterexample-workbook.json"
OUT_JSON = ROOT / "research/communication-job-curriculum-index.json"
OUT_MD = ROOT / "writeups/communication-job-curriculum-index.md"
OUT_HTML = ROOT / "writeups/communication-job-curriculum.html"


def main() -> int:
    cards = json.loads(CARDS.read_text())["cards"]
    learner = json.loads(LEARNER.read_text())
    listener = json.loads(LISTENER.read_text())
    delivery = json.loads(DELIVERY.read_text())
    measurement = json.loads(MEASUREMENTS.read_text())
    counterexamples = json.loads(COUNTEREXAMPLES.read_text())
    learner_by_job = {row["canonical_job"]: row for row in learner["cards"]}
    listener_by_job = {row["canonical_job"]: row for row in listener["patterns"]}
    delivery_by_job = {}
    for item in delivery["items"]:
        delivery_by_job.setdefault(item["canonical_job"], []).append(item)
    measurement_by_sample = {item["sample_id"]: item for item in measurement["items"]}
    counter_by_job = {}
    for item in counterexamples["items"]:
        counter_by_job.setdefault(item["canonical_job"], []).append(item)
    lessons = []
    for card in cards:
        job = card["canonical_job"]
        learner_row = learner_by_job[job]
        listener_row = listener_by_job[job]
        delivery_rows = []
        for item in delivery_by_job.get(job, []):
            delivery_rows.append({**item, "measurement": measurement_by_sample.get(item["sample_id"])})
        lessons.append({
            "pattern_id": card["card_id"],
            "canonical_job": job,
            "status": "provisional_not_validated",
            "communication_problem": card["problem"],
            "mechanism_hypothesis": card["mechanism"],
            "repeatable_form": card["form"],
            "exact_examples": card["exact_examples"],
            "recurrence": card["recurrence"],
            "phrase_forms": learner_row["phrase_forms"],
            "phrase_form_coverage_status": learner_row["phrase_form_coverage_status"],
            "delivery_samples": delivery_rows,
            "counterexample_slots": [{"counterexample_type": item["counterexample_type"], "status": item["review"]["evidence_status"] or "pending"} for item in counter_by_job[job]],
            "practice": card["practice"],
            "self_check": card["self_check"],
            "non_fit": card["non_fit"],
            "learner": {"task_count": learner_row["task_count"], "status": learner_row["status"]},
            "listener": {"pattern_id": listener_row["pattern_id"], "stimulus_status": listener_row["draft_stimulus_status"], "protocol_status": listener["status"]},
            "validation": card["validation"],
        })
    index = {
        "schema_version": "1.0",
        "index_id": "communication-job-curriculum-index",
        "status": "18_job_provisional_curriculum_not_validated",
        "lesson_count": len(lessons),
        "claim_boundary": "This index is a provisional learning surface joining transcript examples, exact phrase forms, delivery measurement queues, counterexample slots, practice, learner tasks and listener protocols. It does not present any pattern as effective, independently recurrent, teachable or outcome-producing.",
        "sources": ["research/communication-job-cards.json", "research/corpus-phrase-form-inventory.json", "research/communication-job-delivery-sampling.json", "research/communication-job-delivery-measurement-preflight.json", "research/communication-job-counterexample-workbook.json", "research/communication-job-learner-check.json", "research/communication-job-listener-outcome-protocol.json"],
        "lessons": lessons,
        "validation_gates": ["independent function and phrase-form review", "speaker/event identity", "manual and independent delivery review", "counterexample completion", "learner observations", "locked listener stimuli and listener outcomes"],
    }
    OUT_JSON.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job curriculum index", "", "Status: **18-job provisional curriculum; not validated**.", "", index["claim_boundary"], "", "| Job | Exact forms | Examples | Delivery samples | Counterexample slots | Learner tasks | Listener |", "|---|---:|---:|---:|---:|---:|---|"]
    for lesson in lessons:
        lines.append(f"| `{lesson['canonical_job']}` | {len(lesson['phrase_forms'])} | {len(lesson['exact_examples'])} | {len(lesson['delivery_samples'])} | {len(lesson['counterexample_slots'])} pending | {lesson['learner']['task_count']} | `{lesson['listener']['stimulus_status']}` |")
    lines += ["", "The browser surface keeps transcript wording, proxy measurements, missing media, blank counterexample slots and unrun learner/listener gates visible.", ""]
    OUT_MD.write_text("\n".join(lines))
    articles = []
    for lesson in lessons:
        examples = "".join(f"<li><a href='{html.escape(e['source_url'], quote=True)}'>{html.escape(e['title'])}</a><blockquote>{html.escape(' '.join(s['text'] for s in e['exact_segments']))}</blockquote></li>" for e in lesson["exact_examples"])
        forms = ", ".join(html.escape(f["phrase_form"]) for f in lesson["phrase_forms"]) or "No direct exact-form family match indexed."
        delivery_rows = "".join(f"<li><code>{html.escape(d['sample_id'])}</code> · {html.escape(d['raw_media_state'])} · matched feature segments: {len((d.get('measurement') or {}).get('evidence_ids_matched', []))} · manual observation pending</li>" for d in lesson["delivery_samples"])
        counter = "".join(f"<li>{html.escape(c['counterexample_type'])}: <b>{html.escape(c['status'])}</b></li>" for c in lesson["counterexample_slots"])
        articles.append(f"<article class='lesson' data-search='{html.escape((lesson['canonical_job']+' '+lesson['communication_problem']+' '+lesson['repeatable_form']).lower(), quote=True)}'><h2>{html.escape(lesson['canonical_job'])}</h2><p><b>Problem:</b> {html.escape(lesson['communication_problem'])}</p><p><b>Mechanism hypothesis:</b> {html.escape(lesson['mechanism_hypothesis'])}</p><p><b>Repeatable form:</b> {html.escape(lesson['repeatable_form'])}</p><p><b>Indexed exact forms:</b> {forms}</p><details><summary>Exact transcript examples ({len(lesson['exact_examples'])})</summary><ol>{examples}</ol></details><details><summary>Delivery and measurement queue ({len(lesson['delivery_samples'])})</summary><ul>{delivery_rows}</ul></details><details><summary>Counterexample and limit queue</summary><ul>{counter}</ul></details><p><b>Practice:</b> {html.escape(lesson['practice'])}</p><p><b>Self-check:</b> {html.escape(lesson['self_check'])}</p><p><b>When not to use:</b> {html.escape(lesson['non_fit'])}</p><p><b>Learner:</b> {lesson['learner']['task_count']} tasks; {html.escape(lesson['learner']['status'])}. <b>Listener:</b> {html.escape(lesson['listener']['protocol_status'])}; stimulus {html.escape(lesson['listener']['stimulus_status'])}.</p></article>")
    OUT_HTML.write_text(f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication-job curriculum</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}}input{{width:100%;box-sizing:border-box;padding:.7rem;font:inherit;margin:1rem 0}}.notice{{background:#fff6d6;padding:1rem;border-left:4px solid #b8860b}}.lesson{{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}}blockquote{{background:#f5f7f9;padding:.7rem;margin:.5rem 0}}code{{overflow-wrap:anywhere}}</style><main><h1>Communication-job curriculum</h1><div class="notice">{html.escape(index["claim_boundary"])}</div><input id="search" type="search" placeholder="Search a communication job or problem"><p id="count"></p>{''.join(articles)}</main><script>const input=document.querySelector('#search'),cards=[...document.querySelectorAll('.lesson')],count=document.querySelector('#count');function filter(){{const q=input.value.toLowerCase();let n=0;for(const card of cards){{const show=!q||card.dataset.search.includes(q);card.hidden=!show;if(show)n++}}count.textContent=`Showing ${{n}} of ${{cards.length}} jobs`}}input.oninput=filter;filter()</script>''')
    print(f"wrote integrated communication-job curriculum ({len(lessons)} jobs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
