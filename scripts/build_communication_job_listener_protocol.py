#!/usr/bin/env python3
"""Build a separate listener-outcome design for all 18 communication jobs."""

from __future__ import annotations

import html
import json
from pathlib import Path


TASKS = [
    ("main_point_recall", "State the speaker's main point in your own words without seeing the script.", "blind rubric score 0–2"),
    ("evidence_or_example_identification", "Name the example, reason or evidence the speaker used, if any.", "blind rubric score 0–2"),
    ("limit_or_condition_identification", "State one limit, uncertainty or condition included by the speaker, or say that none was clear.", "blind rubric score 0–2"),
    ("requested_action_or_role", "What action or role, if any, did the speaker invite? Include owner or condition if stated.", "blind rubric score 0–2"),
    ("confusion_and_load", "Report what was confusing, rushed, emotionally difficult or easy to follow; agreement is not required.", "coded response plus optional rating"),
    ("delayed_recall", "After a defined delay, restate the main point and one supporting detail.", "blind rubric score 0–2; only when feasible and consented"),
]

SCORE_LABELS = {
    0: "not recalled, incorrect or not scorable",
    1: "partial or materially incomplete",
    2: "accurate and sufficiently complete",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    cards = json.loads((root / "research/communication-job-cards.json").read_text())["cards"]
    stimuli = json.loads((root / "research/communication-job-listener-stimuli-draft.json").read_text())
    preflight = json.loads((root / "research/communication-job-stimuli-preflight.json").read_text())
    lock_path = root / "research/communication-job-listener-stimulus-lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else None
    stimuli_locked = bool(lock and lock.get("status") == "locked_for_pilot" and lock.get("locked_pair_count") == stimuli["pair_count"])
    stimuli_by_card = {item["card_id"]: item for item in stimuli["records"]}
    patterns = []
    for card in cards:
        patterns.append({
            "pattern_id": card["card_id"],
            "canonical_job": card["canonical_job"],
            "communication_job": card["problem"],
            "pattern_informed_form": card["form"],
            "draft_stimulus_id": stimuli_by_card[card["card_id"]]["stimulus_id"],
            "draft_stimulus_status": stimuli_by_card[card["card_id"]]["status"],
            "stimulus_requirement": "one newly authored matched pair; same proposition, topic, vocabulary, modality and length range; no source-speaker identity",
        })
    return {
        "schema_version": "1.0",
        "protocol_id": "communication-job-listener-outcome-protocol",
        "status": "design_locked_not_run" if stimuli_locked else "design_complete_not_run",
        "purpose": "Test comprehension, recall and reported cognitive load for matched control versus pattern-informed versions of the 18 provisional communication-job cards.",
        "claim_boundary": "A result can show differences in the measured task for the authored stimuli and tested population. It cannot establish that a celebrity's delivery or a speech form causes trust, long-term memory, persuasion, engagement or action generally.",
        "source": "research/communication-job-cards.json",
        "stimulus_bank": "research/communication-job-listener-stimuli-draft.json",
        "stimulus_preflight": "research/communication-job-stimuli-preflight.json",
        "stimulus_preflight_status": preflight["status"],
        "stimulus_pairs_locked": stimuli_locked,
        "stimulus_lock_audit": "research/communication-job-listener-stimulus-lock.json" if stimuli_locked else None,
        "stimulus_pair_count": stimuli["pair_count"],
        "patterns": patterns,
        "listener_tasks": [{"task_id": task_id, "prompt": prompt, "measure": measure} for task_id, prompt, measure in TASKS],
        "design": {
            "unit": "listener-session-by-stimulus",
            "comparison": "randomized matched control versus pattern-informed version",
            "assignment": "randomize version and pattern order; keep scorer blind to condition where practical",
            "holdout": "Lock a new authored stimulus set before unblinding and reserve some pairs for holdout.",
            "primary_outcome": "pre-registered main-point recall score",
            "secondary_outcomes": ["evidence identification", "limit/condition identification", "requested action/role", "confusion/load", "delayed recall"],
        },
        "controls": [
            "Keep proposition, topic, vocabulary, length and modality matched.",
            "Do not use source celebrity identity or copied quotations as the manipulation.",
            "Pretest readability, captions, audio levels and accessibility.",
            "Record topic familiarity and agreement separately from comprehension.",
            "Do not treat liking, trust or agreement as comprehension proxies.",
        ],
        "consent_and_accessibility": [
            "Use plain-language consent and allow withdrawal without penalty.",
            "Offer text, captioned audio/video and screen-reader-compatible response modes.",
            "Do not require trauma, medical, political or personal disclosure.",
            "Minimize retention of recordings; obtain separate permission for recording.",
        ],
        "scoring_schema": {
            "scale": "0-2",
            "labels": {str(key): value for key, value in SCORE_LABELS.items()},
            "score_field_prefix": "score_",
            "missing_value": None,
            "missing_value_rule": "Use null only when the task was not feasible, not administered or was inaccessible; record the reason separately.",
            "scorer_instruction": "Score against a pre-registered answer key while blind to condition where practical; do not score agreement, liking or trust.",
        },
        "record_schema": {
            "required": ["participant_code", "date", "protocol_version", "consent", "modality", "stimulus_id", "condition", "task_responses", "scorer_id_or_blind_code"],
            "condition_values": ["control", "pattern_informed", "unknown_or_blinded"],
            "score_values": [0, 1, 2, None],
            "accessibility_issue_values": ["yes", "no"],
        },
        "record_form": "writeups/communication-job-listener-record.html",
        "analysis_plan": [
            "Report item-level and aggregate comprehension/recall with uncertainty and missingness.",
            "Compare conditions within stimulus and, where possible, within participant.",
            "Inspect null results, reversals, topic interactions and accessibility failures.",
            "Pre-register primary task and exclusions before unblinding.",
            "Treat results as local to the authored stimuli and tested population until replicated.",
        ],
        "not_run_reason": "Matched stimulus pairs are locked for pilot review, but no consented listener observations are present." if stimuli_locked else "No matched stimulus pairs or consented listener observations are present.",
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    protocol = build(root)
    (root / "research/communication-job-listener-outcome-protocol.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n")
    status_label = "design locked, not run" if protocol["stimulus_pairs_locked"] else "design complete, not run"
    lock_label = "yes" if protocol["stimulus_pairs_locked"] else "no"
    lines = ["# Communication-job listener-outcome protocol", "", f"Status: **{status_label}**.", "", protocol["claim_boundary"], "", f"Jobs: **{len(protocol['patterns'])}** · common listener tasks: **{len(protocol['listener_tasks'])}** · stimulus pairs locked: **{lock_label}**.", "", "## Listener tasks", "", "| Task | Measure |", "|---|---|"]
    lines += [f"| `{task['task_id']}` | {task['measure']} |" for task in protocol["listener_tasks"]]
    lines += ["", "## Stimulus requirement", "", "Each job requires a newly authored matched control/pattern-informed pair. Source celebrity identity and copied quotations are not experimental manipulations.", "", "## Safety and accessibility", ""] + [f"- {item}" for item in protocol["consent_and_accessibility"]] + ["", "## Not yet evidence", "", protocol["not_run_reason"], ""]
    (root / "writeups/communication-job-listener-outcome-protocol.md").write_text("\n".join(lines))
    task_markup = "".join(f"<label>{esc(task['task_id'])}<textarea required name='task_{esc(task['task_id'])}' rows='3' placeholder='{esc(task['prompt'])}'></textarea><span>Blind score: <select required name='score_{esc(task['task_id'])}'><option value=''>Choose</option><option value='0'>0 — not recalled, incorrect or not scorable</option><option value='1'>1 — partial or materially incomplete</option><option value='2'>2 — accurate and sufficiently complete</option><option value='null'>Not feasible / inaccessible</option></select></span></label>" for task in protocol["listener_tasks"])
    html_doc = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Communication-job listener record</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#17202a}}fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1.5rem 0;padding:1rem}}label{{display:block;margin:.7rem 0}}textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}input,select{{padding:.35rem}}button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0}}.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}}</style></head><body><h1>Communication-job listener outcome record</h1><div class='notice'><strong>Not an effectiveness claim.</strong> Use only after matched stimuli are authored, pretested and locked. This form measures local comprehension/recall tasks, not trust, liking, persuasion or behavior.</div><form id='record'><fieldset><legend>Session</legend><label>Participant code<input required name='participant_code'></label><label>Date<input required type='date' name='date'></label><label>Protocol version<input required name='protocol_version' value='communication-job-listener-outcome-v1'></label><label>Modality<input required name='modality'></label><label>Stimulus ID<input required name='stimulus_id'></label><label>Condition<select required name='condition'><option value=''>Choose</option><option>control</option><option>pattern_informed</option><option>unknown_or_blinded</option></select></label><label>Blind scorer code<input required name='scorer_id_or_blind_code'></label><label><input required type='checkbox' name='consent'> Consent recorded for this session.</label></fieldset><fieldset><legend>Listener responses and blind scores</legend>{task_markup}</fieldset><fieldset><legend>Optional notes</legend><label>Accessibility issue or missing task reason<select required name='accessibility_issue'><option value=''>Choose</option><option>no</option><option>yes</option></select></label><label>Prior topic familiarity<textarea name='prior_topic_familiarity' rows='2'></textarea></label><label>Agreement or confidence<textarea name='agreement_or_confidence' rows='2'></textarea></label><label>Accessibility accommodation or missing reason<textarea name='accessibility_or_missing_reason' rows='2'></textarea></label></fieldset><button type='button' id='download'>Download JSON record</button><button type='reset'>Clear</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#record');if(!f.reportValidity())return;const r={{schema_version:'1.0',protocol_id:'communication-job-listener-outcome-protocol',record_type:'communication_job_listener_outcome_observation',claim_boundary:'Local listener comprehension/recall observation only; not general effectiveness evidence.',responses:{{}}}};for(const e of f.elements)if(e.name){{let v=e.type==='checkbox'?e.checked:e.value;if(e.name.startsWith('score_')&&v==='null')v=null;else if(e.name.startsWith('score_')&&v!=='')v=Number(v);r.responses[e.name]=v}}const b=new Blob([JSON.stringify(r,null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='communication-job-listener-record-'+r.responses.participant_code+'.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>"""
    draft_controls = "<section class='draft-controls'><p><b>Local draft:</b> save and resume this listener session in this browser only; it is not outcome evidence until stimuli are locked and records are validated.</p><button type='button' id='save-draft'>Save local draft</button><button type='button' id='restore-draft'>Restore local draft</button><button type='button' id='clear-draft'>Clear local draft</button><span id='draft-status' aria-live='polite'></span></section>"
    draft_script = "const draftKey='communication_job_listener_outcome_draft_v1',draftStatus=document.querySelector('#draft-status'),draftFields=()=>[...document.querySelectorAll('#record input[name],#record textarea[name],#record select[name]')],readDraft=()=>{try{return JSON.parse(localStorage.getItem(draftKey)||'null')}catch(_){return null}},collectDraft=()=>Object.fromEntries(draftFields().map(e=>[e.name,e.type==='checkbox'?e.checked:e.value])),applyDraft=d=>{if(!d)return;for(const e of draftFields())if(Object.hasOwn(d,e.name)){if(e.type==='checkbox')e.checked=Boolean(d[e.name]);else e.value=d[e.name]}},saveDraft=()=>{localStorage.setItem(draftKey,JSON.stringify(collectDraft()));draftStatus.textContent='Saved in this browser only.'};document.querySelector('#save-draft').onclick=saveDraft;document.querySelector('#restore-draft').onclick=()=>{const d=readDraft();if(!d){draftStatus.textContent='No local draft found.';return}applyDraft(d);draftStatus.textContent='Restored from this browser only.'};document.querySelector('#clear-draft').onclick=()=>{localStorage.removeItem(draftKey);draftStatus.textContent='Local draft cleared.'};if(readDraft())draftStatus.textContent='A local draft is available; restore it when ready.';"
    html_doc = html_doc.replace("<button type='button' id='download'>", draft_controls + "<button type='button' id='download'>")
    html_doc = html_doc.replace("<button type='button' id='download'>", "<p id='export-status' aria-live='polite'></p><button type='button' id='download'>", 1)
    html_doc = html_doc.replace("URL.revokeObjectURL(u)};", "URL.revokeObjectURL(u);document.querySelector('#export-status').textContent='Listener record downloaded locally.'};")
    html_doc = html_doc.replace('</script></body></html>', draft_script + '</script></body></html>')
    (root / "writeups/communication-job-listener-record.html").write_text(html_doc)
    return protocol


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps({"pattern_count": len(result["patterns"]), "task_count": len(result["listener_tasks"]), "status": result["status"]}, indent=2))
