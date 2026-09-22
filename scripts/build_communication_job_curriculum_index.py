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
CANDIDATE_QUEUE = ROOT / "research/communication-job-counterexample-candidate-queue.json"
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
    candidate_queue = json.loads(CANDIDATE_QUEUE.read_text())
    learner_by_job = {row["canonical_job"]: row for row in learner["cards"]}
    listener_by_job = {row["canonical_job"]: row for row in listener["patterns"]}
    delivery_by_job = {}
    for item in delivery["items"]:
        delivery_by_job.setdefault(item["canonical_job"], []).append(item)
    measurement_by_sample = {item["sample_id"]: item for item in measurement["items"]}
    counter_by_job = {}
    for item in counterexamples["items"]:
        counter_by_job.setdefault(item["canonical_job"], []).append(item)
    candidates_by_job = {}
    for item in candidate_queue["items"]:
        candidates_by_job.setdefault(item["canonical_job"], []).append(item)
    lessons = []

    def modality_for(state: str) -> str:
        if state.startswith("raw_audio_video_present"):
            return "audio_video"
        if "derived" in state or "proxy" in state:
            return "derived_proxy"
        if "audio" in state:
            return "audio"
        return "transcript_only"

    def source_quality_for(rows: list[dict]) -> str:
        modalities = {modality_for(row.get("raw_media_state", "")) for row in rows}
        if "audio_video" in modalities:
            return "transcript_plus_raw_av"
        if "derived_proxy" in modalities or "audio" in modalities:
            return "transcript_plus_proxy"
        return "transcript_only"

    for card in cards:
        job = card["canonical_job"]
        learner_row = learner_by_job[job]
        listener_row = listener_by_job[job]
        delivery_rows = []
        for item in delivery_by_job.get(job, []):
            delivery_rows.append({**item, "measurement": measurement_by_sample.get(item["sample_id"])})
        facets = {
            "function": [job],
            "modality": sorted({modality_for(row.get("raw_media_state", "")) for row in delivery_rows}) or ["transcript_only"],
            "setting": ["unclassified"],
            "difficulty": ["guided"],
            "source_quality": [source_quality_for(delivery_rows)],
            "confidence": ["provisional"],
        }
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
            "counterexample_candidates": [
                {
                    "counterexample_type": item["counterexample_type"],
                    "candidate_status": item["candidate_status"],
                    "evidence_id": item["candidate"].get("evidence_id"),
                    "transcript_excerpt": item["candidate"].get("transcript_excerpt"),
                    "claim_boundary": item["claim_boundary"],
                }
                for item in candidates_by_job.get(job, [])
            ],
            "practice": card["practice"],
            "self_check": card["self_check"],
            "non_fit": card["non_fit"],
            "learner": {"task_count": learner_row["task_count"], "status": learner_row["status"]},
            "listener": {"pattern_id": listener_row["pattern_id"], "stimulus_status": listener_row["draft_stimulus_status"], "protocol_status": listener["status"]},
            "validation": card["validation"],
            "facets": facets,
        })
    index = {
        "schema_version": "1.0",
        "index_id": "communication-job-curriculum-index",
        "status": "18_job_provisional_curriculum_not_validated",
        "lesson_count": len(lessons),
        "claim_boundary": "This index is a provisional learning surface joining transcript examples, exact phrase forms, delivery measurement queues, counterexample slots, practice, learner tasks and listener protocols. It does not present any pattern as effective, independently recurrent, teachable or outcome-producing.",
        "sources": ["research/communication-job-cards.json", "research/corpus-phrase-form-inventory.json", "research/communication-job-delivery-sampling.json", "research/communication-job-delivery-measurement-preflight.json", "research/communication-job-counterexample-workbook.json", "research/communication-job-counterexample-candidate-queue.json", "research/communication-job-learner-check.json", "research/communication-job-listener-outcome-protocol.json"],
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
        candidate_rows = "".join(
            f"<li><b>{html.escape(c['counterexample_type'])}</b> · {html.escape(c['candidate_status'])} · "
            f"{html.escape(c['evidence_id'] or 'reviewer must select or record none')}"
            f"{(' — ' + html.escape(c['transcript_excerpt'] or '')) if c['transcript_excerpt'] else ''}</li>"
            for c in lesson["counterexample_candidates"]
        )
        facet_attrs = " ".join(f"data-{key}=\"{html.escape(' '.join(values), quote=True)}\"" for key, values in lesson["facets"].items())
        facet_text = html.escape(", ".join(f"{key}={'/'.join(values)}" for key, values in lesson["facets"].items()))
        articles.append(f"<article class='lesson' {facet_attrs} data-search='{html.escape((lesson['canonical_job']+' '+lesson['communication_problem']+' '+lesson['repeatable_form']).lower(), quote=True)}'><h2>{html.escape(lesson['canonical_job'])}</h2><p><b>Problem:</b> {html.escape(lesson['communication_problem'])}</p><p><b>Mechanism hypothesis:</b> {html.escape(lesson['mechanism_hypothesis'])}</p><p><b>Repeatable form:</b> {html.escape(lesson['repeatable_form'])}</p><p><b>Indexed exact forms:</b> {forms}</p><p><b>Facets:</b> {facet_text}</p><details><summary>Exact transcript examples ({len(lesson['exact_examples'])})</summary><ol>{examples}</ol></details><details><summary>Delivery and measurement queue ({len(lesson['delivery_samples'])})</summary><ul>{delivery_rows}</ul></details><details><summary>Counterexample and limit queue</summary><ul>{counter}</ul><p class='muted'>Machine-routed candidates are source-linked review targets, not confirmed counterexamples.</p><ul>{candidate_rows}</ul></details><p><b>Practice:</b> {html.escape(lesson['practice'])}</p><p><b>Self-check:</b> {html.escape(lesson['self_check'])}</p><p><b>When not to use:</b> {html.escape(lesson['non_fit'])}</p><p><b>Learner:</b> {lesson['learner']['task_count']} tasks; {html.escape(lesson['learner']['status'])}. <b>Listener:</b> {html.escape(lesson['listener']['protocol_status'])}; stimulus {html.escape(lesson['listener']['stimulus_status'])}.</p></article>")
    def options(values: set[str]) -> str:
        return "<option value=\"\">All</option>" + "".join(f"<option value=\"{html.escape(value, quote=True)}\">{html.escape(value)}</option>" for value in sorted(values))

    all_facets = {key: {value for lesson in lessons for value in lesson["facets"][key]} for key in ("function", "modality", "setting", "difficulty", "source_quality", "confidence")}
    controls = "".join(f"<label for=\"filter-{label}\">{label.replace('_', ' ').title()} <select id=\"filter-{label}\">{options(all_facets[label])}</select></label>" for label in all_facets)
    document = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication-job curriculum</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}}input,select{{box-sizing:border-box;padding:.55rem;font:inherit;margin:.35rem .5rem .35rem 0;max-width:100%;min-width:0}}input{{width:min(100%,620px)}}.controls{{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0;min-width:0;overflow:hidden}}.controls label{{flex:1 1 12rem;min-width:0;overflow:hidden}}.controls select{{width:100%}}.notice{{background:#fff6d6;padding:1rem;border-left:4px solid #b8860b}}.lesson{{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0;overflow-wrap:anywhere}}blockquote{{background:#f5f7f9;padding:.7rem;margin:.5rem 0;overflow-wrap:anywhere}}code{{overflow-wrap:anywhere}}</style><main><h1>Communication-job curriculum</h1><div class="notice">{html.escape(index["claim_boundary"])} Facets explicitly marked <b>unclassified</b> or <b>provisional</b> are missing evidence, not hidden certainty.</div><div class="controls"><label>Search <input id="search" type="search" placeholder="Search a communication job or problem"></label>{controls}</div><p id="count"></p>{''.join(articles)}</main><script>const input=document.querySelector('#search'),cards=[...document.querySelectorAll('.lesson')],count=document.querySelector('#count'),filters=[...document.querySelectorAll('select[id^=filter-]')];function filter(){{const q=input.value.toLowerCase();let n=0;for(const card of cards){{const facets=filters.every(x=>!x.value||card.dataset[x.id.slice(7)]?.split(' ').includes(x.value));const show=facets&&(!q||card.dataset.search.includes(q));card.hidden=!show;if(show)n++}}count.textContent=`Showing ${{n}} of ${{cards.length}} jobs`}}input.oninput=filter;filters.forEach(x=>x.onchange=filter);filter()</script>'''
    document = document.replace('<!doctype html><meta', '<!doctype html><html lang="en"><head><meta')
    document = document.replace('<main>', '</head><body><main>', 1)
    document = document.replace('<label>Search <input id="search"', '<label for="search">Search <input id="search"')
    document = document.replace('<p id="count">', '<p id="count" aria-live="polite">')
    document = document.replace('</main><script>', '<script>')
    document = document.replace('</script>', '</script></main></body></html>')
    OUT_HTML.write_text(document)
    print(f"wrote integrated communication-job curriculum ({len(lessons)} jobs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
