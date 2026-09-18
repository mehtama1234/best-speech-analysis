#!/usr/bin/env python3
"""Build a text/caption-friendly listener-outcome record form."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/listener-outcome-protocol.json"
OUT = ROOT / "writeups/listener-outcome-record.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    protocol = json.loads(PROTOCOL.read_text())
    tasks = protocol["listener_tasks"]
    fields = []
    for task in tasks:
        task_id = task["task_id"]
        fields.append(
            f'<fieldset><legend>{esc(task_id)}</legend><p>{esc(task["prompt"])}</p>'
            f'<label>Response<textarea required name="response_{esc(task_id)}" rows="4"></textarea></label>'
            f'<label>Blind rubric score<select required name="score_{esc(task_id)}"><option value="">Choose</option><option value="0">0 — missing/misleading</option><option value="1">1 — partial</option><option value="2">2 — clear/bounded</option><option value="NA">Not scorable</option></select></label></fieldset>'
        )
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Listener outcome record</title><style>body{{font:16px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#17202a}}fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1rem 0;padding:1rem}}label{{display:block;margin:.7rem 0}}textarea{{display:block;width:100%;box-sizing:border-box;margin-top:.3rem}}input,select{{font:inherit;padding:.35rem;max-width:28rem}}button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0}}.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}}</style></head><body><h1>Listener outcome record</h1><div class="notice"><b>Protocol boundary:</b> This form records comprehension/recall observations for a predefined stimulus. It does not measure trust, persuasion, liking or behavior, and it does not deliver or store recordings. Do not use it until stimuli, condition assignment and consent procedures are locked.</div><form id="record"><fieldset><legend>Session</legend><label>Participant code<input required name="participant_code"></label><label>Date<input required type="date" name="date"></label><label>Protocol version<input required name="protocol_version" value="listener-outcome-protocol-v1"></label><label>Stimulus ID<input required name="stimulus_id"></label><label>Condition<select required name="condition"><option value="">Choose</option><option value="control">Control</option><option value="pattern_informed">Pattern-informed</option><option value="unknown_or_blinded">Unknown/blinded</option></select></label><label>Modality<input required name="modality" placeholder="text, captioned audio, etc."></label><label>Scorer/blind code<input required name="scorer_id_or_blind_code"></label><label>Prior topic familiarity<textarea name="prior_topic_familiarity" rows="2"></textarea></label><label>Accessibility accommodation<textarea name="accessibility_accommodation" rows="2"></textarea></label><label><input required type="checkbox" name="consent"> I consent to this local listener-observation record for the stated protocol purpose.</label></fieldset>{''.join(fields)}<fieldset><legend>Session notes</legend><label>Confidence or uncertainty<textarea name="confidence" rows="2"></textarea></label><label>Missing response or withdrawal reason<textarea name="withdrawal_or_missing_reason" rows="2"></textarea></label></fieldset><button type="button" id="download">Download JSON record</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#record');if(!f.reportValidity())return;const responses={{}},tasks={{}};for(const e of f.elements){{if(!e.name)continue;if(e.name.startsWith('response_'))tasks[e.name.slice(9)]={{response:e.value,score:f.elements['score_'+e.name.slice(9)].value}};else if(!e.name.startsWith('score_'))responses[e.name]=e.type==='checkbox'?e.checked:e.value}}responses.task_responses=tasks;const record={{schema_version:'1.0',record_type:'listener_outcome_observation',protocol_id:'listener-outcome-protocol',claim_boundary:'Comprehension and recall observations only; not trust, persuasion, behavior or general effectiveness.',responses}};const blob=new Blob([JSON.stringify(record,null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='listener-outcome-'+responses.participant_code+'.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT.write_text(document)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(tasks)} listener tasks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
