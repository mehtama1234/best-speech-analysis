#!/usr/bin/env python3
"""Build a fixed, consent-aware teachability instrument for 18 job cards."""

from __future__ import annotations

import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


JOB_TO_PHRASE_FAMILY = {
    "closing": "conclusion_or_summary",
    "question": "question",
    "story_or_personal_experience": "story_or_personal_experience",
    "example_or_case": "example",
    "contrast_or_disagreement": "contrast_or_disagreement",
    "qualification_or_boundary": "uncertainty_or_qualification",
    "definition_or_explanation": "definition",
    "call_to_action_or_audience_role": "call_to_action",
}


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    cards = json.loads((root / "research/communication-job-cards.json").read_text())["cards"]
    phrase_inventory = json.loads((root / "research/corpus-phrase-form-inventory.json").read_text())
    forms_by_family = {}
    for form in phrase_inventory["forms"]:
        forms_by_family.setdefault(form["family"], []).append({"phrase_form": form["phrase_form"], "matched_pattern": form["matched_pattern"], "status": form["status"] if "status" in form else form["mechanism_status"], "mechanism_hypothesis": form["mechanism_hypothesis"]})
    tasks = []
    card_rows = []
    for card in cards:
        job = card["canonical_job"]
        family = JOB_TO_PHRASE_FAMILY.get(job)
        phrase_forms = forms_by_family.get(family, [])
        form_text = ", ".join(f"‘{form['phrase_form']}’" for form in phrase_forms) if phrase_forms else "No direct exact-form family match is currently indexed for this job; do not invent one."
        card_rows.append({"card_id": card["card_id"], "canonical_job": job, "task_count": 4, "status": "draft_not_validated", "phrase_form_family": family, "phrase_forms": phrase_forms, "phrase_form_coverage_status": "indexed_family_match" if phrase_forms else "no_direct_family_match", "scoring_dimensions": ["recognition", "explanation", "transfer", "non_fit", "listener_restatement", "revision"]})
        tasks.extend([
            {
                "task_id": f"{job}-recognition-01",
                "card_id": card["card_id"],
                "canonical_job": job,
                "phase": "new_example_recognition",
                "prompt": f"A speaker is trying to do this: {card['problem']} Read this repeatable form: ‘{card['form']}’ and compare it with these indexed exact forms where available: {form_text}. Does the response perform the job {job}? Identify the words that support your judgment and one alternative explanation.",
                "required_features": ["job judgment", "textual evidence", "alternative explanation", "exact-form boundary"],
                "boundary": "A plausible form is not proof that a listener understood or benefited.",
            },
            {
                "task_id": f"{job}-explanation-01",
                "card_id": card["card_id"],
                "canonical_job": job,
                "phase": "plain_language_explanation",
                "prompt": f"Explain the underlying communication choice for {job} to a new learner in two or three sentences. If you use one of these exact forms ({form_text}), explain what job it is doing rather than treating the words as magic. Do not imitate a celebrity’s accent, personality or mannerism.",
                "required_features": ["plain-language explanation", "underlying choice separated from persona", "limit or condition", "form/function distinction"],
                "boundary": "Explain a practice hypothesis, not a proven effectiveness claim.",
            },
            {
                "task_id": f"{job}-transfer-01",
                "card_id": card["card_id"],
                "canonical_job": job,
                "phase": "transfer",
                "prompt": card["practice"],
                "required_features": ["new situation", "underlying choice used", "bounded claim"],
                "boundary": "The learner may use a hypothetical, anonymous or direct example; personal disclosure is optional.",
            },
            {
                "task_id": f"{job}-non-fit-01",
                "card_id": card["card_id"],
                "canonical_job": job,
                "phase": "misuse_non_fit",
                "prompt": f"When should this job not be used? Start with this warning: {card['non_fit']} Give one ordinary scenario where a different communication choice would be safer or clearer.",
                "required_features": ["non-fit identified", "alternative choice", "safety or consent boundary"],
                "boundary": card["non_fit"],
            },
        ])
    return {
        "schema_version": "1.0",
        "protocol_id": "communication-job-learner-check",
        "status": "protocol_drafted_not_run",
        "purpose": "Test whether learners can recognize, explain, transfer and safely bound all 18 provisional communication-job cards.",
        "claim_boundary": "This protocol tests teachability and usability of draft cards. It does not establish that a speech form improves trust, memory, persuasion, engagement, delivery, listener outcomes or action.",
        "consent_and_accessibility": "Use a pseudonym; allow written, typed, captioned, asynchronous or spoken responses; do not require personal disclosure; do not upload recordings through this form; store no sensitive information.",
        "source": "research/communication-job-cards.json",
        "phrase_form_inventory": "research/corpus-phrase-form-inventory.json",
        "phrase_form_family_map": JOB_TO_PHRASE_FAMILY,
        "exact_phrase_form_count": len(phrase_inventory["forms"]),
        "card_count": len(cards),
        "task_count": len(tasks),
        "cards": card_rows,
        "tasks": tasks,
        "procedure": ["baseline recognition", "lesson exposure", "new-example recognition", "plain-language explanation", "transfer", "non-fit judgment", "listener restatement", "revision after feedback"],
        "rubric": {
            "scale": "0=missing or misleading; 1=partial; 2=clear and bounded",
            "dimensions": ["job identified", "underlying choice explained", "transfer to new situation", "non-fit detection", "privacy/accessibility/safety boundary", "listener restatement", "revision after feedback"],
            "safety_rule": "Do not average away a privacy, consent or safety failure; retain it as a boundary finding.",
            "facilitator_scoring": "For each card, score recognition, explanation, transfer, non-fit, listener restatement and revision as 0=missing/misleading, 1=partial, 2=clear and bounded; record a separate safety/privacy issue flag.",
        },
        "outcome_boundary": "Learner observations show whether the cards are understandable and usable; they do not establish original speech-pattern effectiveness or listener outcomes.",
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    protocol = build(root)
    (root / "research/communication-job-learner-check.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n")
    sections = []
    for number, card in enumerate(protocol["cards"], 1):
        tasks = [task for task in protocol["tasks"] if task["card_id"] == card["card_id"]]
        markup = []
        for task in tasks:
            name = task["task_id"]
            markup.append(f"<div class='task'><strong>{esc(task['phase'])} — {esc(name)}</strong><p>{esc(task['prompt'])}</p><label>Response<textarea required name='{esc(name)}' rows='4'></textarea></label></div>")
        scoring = "".join(f"<label>{esc(dimension)} score<select required name='{esc(card['card_id'])}_score_{esc(dimension)}'><option value=''>Choose</option><option value='0'>0 — missing or misleading</option><option value='1'>1 — partial</option><option value='2'>2 — clear and bounded</option></select></label>" for dimension in card["scoring_dimensions"])
        sections.append(f"<fieldset><legend>{number}. {esc(card['canonical_job'])}</legend><input type='hidden' name='{esc(card['card_id'])}_task_ids' value='{esc(','.join(t['task_id'] for t in tasks))}'>{''.join(markup)}<label>Listener restatement<textarea required name='{esc(card['card_id'])}_listener_restatement' rows='3'></textarea></label><label>Revision after feedback<textarea required name='{esc(card['card_id'])}_revision' rows='3'></textarea></label><label>Boundary or safety note<textarea required name='{esc(card['card_id'])}_boundary_note' rows='3'></textarea></label><h3>Facilitator scoring</h3>{scoring}<label>Safety/privacy/accessibility issue?<select required name='{esc(card['card_id'])}_safety_issue'><option value=''>Choose</option><option>yes</option><option>no</option></select></label></fieldset>")
    ids = [task["task_id"] for task in protocol["tasks"]]
    html_doc = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Communication-job learner check</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#17202a}}fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1.5rem 0;padding:1rem}}legend{{font-weight:700}}label{{display:block;margin:.7rem 0}}textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}input[type=text],input[type=date]{{max-width:24rem;padding:.35rem}}button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0}}.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}}.task{{background:#eef5fb;border-left:4px solid #39739d;padding:.7rem;margin:.7rem 0}}</style></head><body><h1>Communication-job learner check</h1><div class='notice'><strong>Teachability only:</strong> This instrument tests whether draft cards are understandable and usable. It does not test whether the original speech forms cause trust, memory, persuasion, engagement or action. Do not enter identifying or sensitive information. Written, typed, captioned and asynchronous responses are allowed.</div><form id='check'><fieldset><legend>Session record</legend><label>Pseudonym or participant code<input required type='text' name='participant_code'></label><label>Date<input required type='date' name='date'></label><label>Lesson version<input required type='text' name='lesson_version' value='communication-job-cards-draft'></label><label>Accessibility or response modality<textarea name='accessibility' rows='2'></textarea></label><label><input required type='checkbox' name='consent'> I consent to this local teachability record being saved for the stated purpose.</label></fieldset>{''.join(sections)}<fieldset><legend>Facilitator record</legend><label>Feedback given<textarea name='facilitator_feedback' rows='4'></textarea></label><label>Accommodations or unresolved disagreement<textarea name='facilitator_notes' rows='3'></textarea></label></fieldset><button type='button' id='download'>Download JSON record</button><button type='reset'>Clear form</button></form><script type='application/json' id='task-bank'>{json.dumps(ids)}</script><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#check');if(!f.reportValidity())return;const responses={{}};for(const e of f.elements)if(e.name)responses[e.name]=e.type==='checkbox'?e.checked:e.value;const record={{schema_version:'1.0',protocol_id:'communication-job-learner-check',record_type:'communication_job_learner_observation',claim_boundary:'Teachability observations only; not listener outcomes or communication-effectiveness evidence.',task_bank_ids:JSON.parse(document.querySelector('#task-bank').textContent),responses}};const blob=new Blob([JSON.stringify(record,null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='communication-job-learner-record-'+responses.participant_code+'.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>"""
    (root / "writeups/communication-job-learner-check.html").write_text(html_doc)
    lines = ["# Communication-job learner check", "", "Status: **protocol drafted, not run**.", "", protocol["claim_boundary"], "", f"Cards: **{protocol['card_count']}** · fixed tasks: **{protocol['task_count']}**.", "", "| Job | Tasks | Status |", "|---|---:|---|"]
    lines += [f"| `{card['canonical_job']}` | {card['task_count']} | `{card['status']}` |" for card in protocol["cards"]]
    (root / "writeups/communication-job-learner-check.md").write_text("\n".join(lines) + "\n")
    return protocol


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps({"card_count": result["card_count"], "task_count": result["task_count"], "status": result["status"]}, indent=2))
