#!/usr/bin/env python3
"""Build an adjudicator form from a joined blinded-review input."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path


def render(data: dict) -> str:
    fieldsets = []
    for number, item in enumerate(data.get("items", []), 1):
        internal = html.escape(json.dumps(item.get("internal_reference", {}), ensure_ascii=False))
        response = html.escape(json.dumps(item.get("reviewer_response", {}), ensure_ascii=False))
        fieldsets.append(f"<fieldset><legend>{number}. {html.escape(item.get('gate', ''))} · <code>{html.escape(item.get('blind_item_id', ''))}</code></legend><p><b>Source review item:</b> <code>{html.escape(item.get('source_review_item_id', ''))}</code></p><p><b>Internal reference:</b> <code>{internal}</code></p><p><b>Reviewer response:</b> <code>{response}</code></p><label>Adjudication decision<select required name='item_{number}_final_decision'><option value=''>Choose</option><option>retain</option><option>revise</option><option>reject</option><option>indeterminate</option></select></label><label>Adjudicator rationale<textarea required name='item_{number}_rationale' rows='3'></textarea></label><label>Safety, accessibility or privacy note<textarea required name='item_{number}_safety_note' rows='2'></textarea></label></fieldset>")
    return """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Blinded review adjudication</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}fieldset{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}label{display:block;margin:.6rem 0}textarea{width:100%;box-sizing:border-box}select,input,button{font:inherit;padding:.55rem}button{cursor:pointer;background:#173f5f;color:white;border:0;border-radius:4px}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}code{overflow-wrap:anywhere}</style></head><body><h1>Blinded review adjudication</h1><div class='notice'><b>Adjudication only.</b> Compare the independent response with the internal reference, preserve disagreement, and use indeterminate when the evidence does not support a decision. This form does not establish effectiveness or listener outcomes.</div><form id='adjudication'><fieldset><legend>Adjudicator metadata</legend><label>Adjudicator code<input required name='adjudicator_code'></label><label>Role<input required name='adjudicator_role'></label><label>Date<input required type='date' name='adjudication_date'></label><label>Conflict statement<textarea required name='conflict_statement' rows='2'></textarea></label></fieldset>__ITEMS__<button type='button' id='download'>Download adjudication export</button></form><script>document.querySelector('#download').onclick=()=>{const f=document.querySelector('#adjudication');if(!f.reportValidity())return;const responses={};for(const e of f.elements)if(e.name)responses[e.name]=e.value;const blob=new Blob([JSON.stringify({schema_version:'1.0',record_type:'blinded_review_adjudication',status:'adjudicator_record_not_effectiveness_evidence',claim_boundary:'Adjudication records preserve decisions about source interpretation; they do not establish communication effectiveness or listener outcomes.',responses},null,2)+'\\n'],{type:'application/json'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='blinded-review-adjudication.json';a.click();URL.revokeObjectURL(u)}</script></body></html>""".replace("__ITEMS__", "\n".join(fieldsets))


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: build_blinded_adjudication_form.py ADJUDICATION_INPUT_JSON [OUTPUT_HTML]", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text())
    if data.get("record_type") != "blinded_review_adjudication_input":
        print("input is not a reducer output", file=sys.stderr)
        return 1
    output = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("blinded-review-adjudication.html")
    output.write_text(render(data))
    print(f"wrote {output}: {len(data.get('items', []))} adjudication items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
