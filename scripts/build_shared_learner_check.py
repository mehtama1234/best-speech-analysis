#!/usr/bin/env python3
"""Build one consent-aware learner instrument for all current draft lessons."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/shared-provisional-curriculum.json"
SLICE_01_BANK = ROOT / "research/vertical-slice-01-learner-task-bank.json"
SLICE_02_BANK = ROOT / "research/vertical-slice-02-learner-task-bank.json"
OUT_JSON = ROOT / "research/shared-learner-check.json"
OUT_HTML = ROOT / "writeups/shared-learner-check.html"
OUT_MD = ROOT / "writeups/shared-learner-check.md"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    index = json.loads(INDEX.read_text())
    banks = [json.loads(SLICE_01_BANK.read_text()), json.loads(SLICE_02_BANK.read_text())]
    tasks = []
    for bank in banks:
        for task in bank["tasks"]:
            tasks.append({**task, "source_task_bank": bank.get("task_bank_id", bank.get("bank_id"))})
    pattern_rows = index["lessons"]
    grouped: dict[str, list[dict]] = {}
    for task in tasks:
        grouped.setdefault(task["pattern_id"], []).append(task)
    pattern_by_id = {row["pattern_id"]: row for row in pattern_rows}
    patterns = []
    for pattern_id in grouped:
        row = pattern_by_id[pattern_id]
        patterns.append({
            "pattern_id": pattern_id,
            "slice": row["slice"],
            "communication_job": row["communication_job"],
            "lesson": row["lesson"],
            "packet": row["packet"],
            "task_count": len(grouped[pattern_id]),
            "status": "draft_not_validated",
        })
    protocol = {
        "schema_version": "1.0",
        "protocol_id": "shared-learner-check",
        "status": "protocol_drafted_not_run",
        "purpose": "Test whether learners can recognize, explain, transfer and safely bound all eight current draft communication patterns.",
        "claim_boundary": "This protocol tests teachability of draft lessons, not whether any speech pattern improves trust, memory, persuasion, engagement or action.",
        "consent_and_accessibility": "Use a pseudonym; allow written, typed, captioned, asynchronous or spoken responses; do not require personal disclosure; store no recording without explicit separate consent.",
        "source_task_banks": [
            "research/vertical-slice-01-learner-task-bank.json",
            "research/vertical-slice-02-learner-task-bank.json",
        ],
        "lesson_index": "research/shared-provisional-curriculum.json",
        "task_count": len(tasks),
        "pattern_count": len(patterns),
        "patterns": patterns,
        "tasks": tasks,
        "procedure": ["baseline", "lesson exposure", "new-example recognition", "transfer", "non-fit judgment", "listener restatement", "revision after feedback", "matched post-task"],
        "rubric": {
            "scale": "0=missing or misleading; 1=partial; 2=clear and bounded",
            "dimensions": ["communication job identified", "underlying choice transferred", "alternative explanation or limit", "misuse/non-fit detection", "privacy/accessibility/safety boundary", "listener restatement"],
            "safety_rule": "Do not average away a safety or privacy failure; retain it as a boundary finding.",
            "control": "Include a plain-communication or no-marker comparison task where the source bank provides one.",
        },
        "outcome_boundary": "Learner observations can show whether the lesson is understandable and usable; they do not establish audience outcomes of the original speech patterns.",
    }
    OUT_JSON.write_text(json.dumps(protocol, ensure_ascii=False, indent=2) + "\n")

    sections = []
    for number, pattern_id in enumerate(grouped, 1):
        row = pattern_by_id[pattern_id]
        task_markup = []
        for task in grouped[pattern_id]:
            stimulus = f"<p><b>Stimulus:</b> {esc(task['stimulus'])}</p>" if task.get("stimulus") else ""
            name = f"p{number}_{task['task_id']}"
            task_markup.append(
                f'<div class="task"><strong>{esc(task["phase"])} — {esc(task["task_id"])}</strong>'
                f'{stimulus}<p>{esc(task["prompt"])}</p>'
                f'<label>Response<textarea required name="{esc(name)}" rows="4"></textarea></label></div>'
            )
        ids = ",".join(task["task_id"] for task in grouped[pattern_id])
        sections.append(
            f'<fieldset><legend>{number}. {esc(pattern_id)}</legend>'
            f'<p><b>Communication job:</b> {esc(row["communication_job"])}</p>'
            f'<p><a href="{esc(row["lesson"])}">Open draft lesson</a> · <a href="{esc(row["packet"])}">Open evidence packet</a></p>'
            f'<input type="hidden" name="p{number}_task_bank_ids" value="{esc(ids)}">'
            + "".join(task_markup)
            + f'<label>Listener restatement<textarea required name="p{number}_listener_restatement" rows="3"></textarea></label>'
            + f'<label>Revision after feedback<textarea required name="p{number}_revision" rows="3"></textarea></label>'
            + f'<label>Boundary, safety or non-fit note<textarea required name="p{number}_boundary_note" rows="3"></textarea></label></fieldset>'
        )
    task_ids = [task["task_id"] for task in tasks]
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shared learner check</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#17202a}}fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1.5rem 0;padding:1rem}}legend{{font-weight:700;padding:0 .4rem}}label{{display:block;margin:.7rem 0}}textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}input[type=text],input[type=date]{{max-width:24rem;padding:.35rem}}button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0}}.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}}.task{{background:#eef5fb;border-left:4px solid #39739d;padding:.6rem;margin:.7rem 0}}</style></head><body><h1>Shared learner check</h1><div class="notice"><strong>Research boundary:</strong> This instrument tests whether draft lessons are understandable and usable. It does not test whether the original speech patterns cause trust, memory, persuasion, engagement or action. Do not enter identifying or sensitive personal information. Written, typed, captioned and asynchronous responses are allowed.</div><form id="check"><fieldset><legend>Session record</legend><label>Pseudonym or participant code<input required type="text" name="participant_code"></label><label>Date<input required type="date" name="date"></label><label>Lesson version<input required type="text" name="lesson_version" value="shared-curriculum-draft"></label><label>Accessibility needs or modality<textarea name="accessibility" rows="2"></textarea></label><label><input required type="checkbox" name="consent"> I consent to this local teachability record being saved for the stated purpose.</label></fieldset>{''.join(sections)}<fieldset><legend>Facilitator record</legend><label>Feedback given<textarea name="facilitator_feedback" rows="4"></textarea></label><label>Accommodations or unresolved disagreement<textarea name="facilitator_notes" rows="3"></textarea></label></fieldset><button type="button" id="download">Download JSON record</button><button type="reset">Clear form</button></form><script type="application/json" id="task-bank">{json.dumps(task_ids, ensure_ascii=False)}</script><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#check');if(!f.reportValidity())return;const responses={{}};for(const e of f.elements)if(e.name)responses[e.name]=e.type==='checkbox'?e.checked:e.value;const record={{schema_version:'1.0',protocol_id:'shared-learner-check',record_type:'learner_observation',claim_boundary:'Teachability observations only; not listener outcomes or communication-effectiveness evidence.',task_bank_ids:JSON.parse(document.querySelector('#task-bank').textContent),responses}};const blob=new Blob([JSON.stringify(record,null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='shared-learner-record-'+responses.participant_code+'.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    lines = ["# Shared learner check", "", "Status: **protocol drafted, not run**.", "", protocol["claim_boundary"], "", f"Patterns: **{len(patterns)}** · fixed tasks: **{len(tasks)}**.", "", "| Pattern | Slice | Tasks | Lesson status |", "|---|---|---:|---|"]
    lines += [f"| `{p['pattern_id']}` | `{p['slice']}` | {p['task_count']} | `{p['status']}` |" for p in patterns]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_HTML.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)} ({len(patterns)} patterns, {len(tasks)} tasks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
