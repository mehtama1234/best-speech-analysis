#!/usr/bin/env python3
"""Build the explicit adjudication form used after independent stimulus reviews."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"
OUT = ROOT / "writeups/communication-job-listener-stimulus-adjudication.html"


def main() -> int:
    workbook = json.loads(WORKBOOK.read_text())
    fieldsets = []
    for number, item in enumerate(workbook["items"], 1):
        fieldsets.append(
            f"<fieldset><legend>{number}. {html.escape(item['canonical_job'])} · {html.escape(item['stimulus_id'])}</legend>"
            f"<p><b>Proposition:</b> {html.escape(item['proposition'])}</p>"
            f"<p><b>Control:</b> {html.escape(item['control_text'])}</p>"
            f"<p><b>Pattern-informed:</b> {html.escape(item['pattern_informed_text'])}</p>"
            f"<label>Final decision<select required name='item_{number}_final_decision'><option value=''>Choose</option><option>lock_for_pilot</option><option>hold_for_revision</option><option>exclude_pair</option></select></label>"
            f"<label>Accessibility/safety decision<select required name='item_{number}_accessibility_safety'><option value=''>Choose</option><option>pass</option><option>revise</option><option>exclude</option></select></label>"
            f"<label>Adjudication rationale<textarea required name='item_{number}_rationale' rows='3'></textarea></label></fieldset>"
        )
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Listener stimulus adjudication</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style></head><body><h1>Listener stimulus adjudication</h1><div class="notice">This form records the adjudicator’s explicit lock/revise/exclude decision after two distinct independent stimulus reviews. A lock is a pilot-readiness decision only; it is not listener outcome evidence, communication-effectiveness evidence or proof of equivalence.</div><form id="adjudication"><fieldset><legend>Adjudicator record</legend><label>Adjudicator code<input required name="adjudicator_code"></label><label>Date<input required type="date" name="adjudication_date"></label><label>Independent review A code<input required name="review_a_code"></label><label>Independent review B code<input required name="review_b_code"></label><label>Review A export path or ID<input required name="source_review_a"></label><label>Review B export path or ID<input required name="source_review_b"></label></fieldset>{''.join(fieldsets)}<p id="export-status" aria-live="polite"></p><button type="button" id="download">Download adjudication JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#adjudication');if(!f.reportValidity())return;const r={{schema_version:'1.0',record_type:'listener_stimulus_adjudication',workbook_id:'listener-stimulus-review-workbook',claim_boundary:'Explicit stimulus lock decision after independent review; lock is pilot readiness only, not listener outcome or communication-effectiveness evidence.',responses:{{}}}};for(const e of f.elements)if(e.name){{if(e.name.startsWith('item_'))r.responses[e.name]=e.value;else r[e.name]=e.type==='checkbox'?e.checked:e.value}}const b=new Blob([JSON.stringify(r,null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='listener-stimulus-adjudication.json';a.click();URL.revokeObjectURL(u);document.querySelector('#export-status').textContent='Adjudication JSON downloaded locally.'}};</script></body></html>'''
    OUT.write_text(html_doc)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(workbook['items'])} pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
