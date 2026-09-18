#!/usr/bin/env python3
"""Build a blank independent-review workbook from the five packet records."""
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = ["contrast-or-disagreement", "example", "story", "uncertainty", "conclusion"]
OUT_JSON = ROOT / "research/vertical-slice-01-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/vertical-slice-01-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/vertical-slice-01-independent-review-workbook.html"


def packet_items(packet):
    items = [("representative", item) for item in packet.get("representative_examples", [])]
    items.extend(("counterexample", item) for item in packet.get("counterexamples", []))
    for key, value in packet.get("counterexample_status", {}).items():
        if isinstance(value, list):
            items.extend((key, item) for item in value if isinstance(item, dict) and "evidence_id" in item)
    return items


def build():
    items = []
    for name in NAMES:
        packet = json.loads((ROOT / f"research/vertical-slice-01-{name}.json").read_text())
        for role, item in packet_items(packet):
            items.append({
                "review_item_id": f"{name}:{item['evidence_id']}:{role}",
                "packet": f"research/vertical-slice-01-{name}.json",
                "pattern_id": packet["pattern_id"],
                "role": role,
                "evidence_id": item["evidence_id"],
                "video_id": item["video_id"],
                "title": item.get("title"),
                "text": item.get("text"),
                "start_seconds": item.get("start_seconds"),
                "end_seconds": item.get("end_seconds"),
                "url": item.get("url"),
                "review": {
                    "boundary": None,
                    "speech_function": None,
                    "pattern_decision": None,
                    "interpretation_decision": None,
                    "audio_proxy_wording": None,
                    "alternative_explanation": None,
                    "safety_decision": None,
                    "reason": None,
                    "disagreement": None,
                    "new_counterexample_requested": None,
                },
            })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "vertical-slice-01-independent-review-workbook",
        "status": "template_not_completed",
        "independence_requirement": "Reviewer must not be the packet creator or original interpreter.",
        "claim_boundary": "A completed review evaluates evidence boundaries and interpretations; it does not establish listener outcomes or causal communication effects.",
        "reviewer": {"name": None, "role": None, "date": None, "modality": None, "conflict_statement": None},
        "decision_vocabulary": {
            "boundary": ["correct", "needs_revision", "indeterminate"],
            "pattern_decision": ["supported", "unsupported", "indeterminate"],
            "safety_decision": ["safe_as_written", "needs_boundary", "unsafe"],
        },
        "required_packet_checks": [
            "speech-function label",
            "counterexample adequacy",
            "speaker/event independence claim",
            "audio-proxy wording",
            "alternative explanations",
            "accessibility and safety boundary",
        ],
        "item_count": len(items),
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vertical slice 01 independent-review workbook",
        "",
        "Status: **template not completed**. This workbook contains no reviewer judgments.",
        "",
        "The reviewer must be independent of packet creation and must record "
        "identity, date, modality, conflicts, per-item decisions, reasons, "
        "disagreements and new counterexamples. `indeterminate` is a valid decision.",
        "",
        f"Items: **{len(items)}** across five packets.",
        "",
        "| # | Packet | Role | Evidence ID | Text | Boundary | Pattern decision | Safety | Reason/disagreement |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, item in enumerate(items, 1):
        text = " ".join((item.get("text") or "").split()).replace("|", "\\|")
        if len(text) > 110:
            text = text[:107] + "..."
        lines.append(
            f"| {index} | `{item['pattern_id']}` | {item['role']} | `{item['evidence_id']}` | {text} |  |  |  |  |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")
    item_json = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vertical slice 01 independent review workbook</title>
<style>
body{{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}}
fieldset{{border:1px solid #9aa7b2;border-radius:.5rem;margin:1rem 0;padding:1rem}} legend{{font-weight:700}}
label{{display:block;margin:.55rem 0}} input,select,textarea{{max-width:100%;padding:.35rem;box-sizing:border-box}} textarea{{width:100%}}
.item{{background:#f6f8fa}} .evidence{{background:white;padding:.6rem;border-left:4px solid #778899}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.5rem}} button{{padding:.6rem 1rem;margin:.5rem .5rem .5rem 0}}
.notice{{background:#fff6d6;border-left:4px solid #c88a00;padding:.8rem}} #result{{display:none;white-space:pre-wrap;background:#f3f5f7;padding:1rem}}
</style></head><body>
<h1>Vertical slice 01 independent review</h1>
<div class="notice"><strong>Independence rule:</strong> use this form only if you did not create the packet or original interpretation. This review evaluates evidence boundaries and safety; it does not establish listener outcomes or causal effects. <strong>Indeterminate is valid.</strong></div>
<form id="review"><fieldset><legend>Reviewer identity</legend>
<div class="grid"><label>Name or reviewer code<input required name="reviewer_name"></label><label>Role/affiliation<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<input required name="review_modality"></label></div>
<label>Conflict statement<textarea required name="conflict_statement" rows="2"></textarea></label>
<label><input required type="checkbox" name="independent_attestation"> I am independent of packet creation and original interpretation.</label>
</fieldset><div id="items"></div>
<button type="button" id="download">Download review JSON</button><button type="reset">Clear form</button></form><pre id="result" aria-live="polite"></pre>
<script type="application/json" id="items">{item_json}</script>
<script>
const items=JSON.parse(document.querySelector('#items').textContent), host=document.querySelector('#items');
const options=(name,values)=>`<label>${{name}}<select required name="${{name.toLowerCase().replaceAll(' ','_')}}"><option value="">Choose…</option>${{values.map(v=>`<option>${{v}}</option>`).join('')}}</select></label>`;
items.forEach((item,index)=>{{const n=index+1, p=document.createElement('fieldset'); p.className='item';
 const timing=item.start_seconds!==null&&item.start_seconds!==undefined?`<br>Time: ${{item.start_seconds}}–${{item.end_seconds||''}}s`:'';
 const source=item.url?`<br><a href="${{item.url}}" target="_blank" rel="noopener">Open source at evidence timestamp</a>`:'';
 p.innerHTML=`<legend>${{n}}. ${{item.pattern_id}} — ${{item.role}}</legend><div class="evidence"><strong>${{item.evidence_id}}</strong><br>${{item.title||''}}${{timing}}${{source}}<br>${{item.text||''}}</div>
 <div class="grid">${{options('Boundary',['correct','needs_revision','indeterminate'])}}${{options('Pattern decision',['supported','unsupported','indeterminate'])}}${{options('Speech-function',['plausible','needs_revision','indeterminate'])}}${{options('Safety decision',['safe_as_written','needs_boundary','unsafe'])}}</div>
 <label>Audio-proxy wording<textarea required name="item_${{n}}_audio_proxy" rows="2"></textarea></label>
 <label>Alternative explanation<textarea required name="item_${{n}}_alternative" rows="2"></textarea></label>
 <label>Reason and disagreement<textarea required name="item_${{n}}_reason" rows="2"></textarea></label>
 <label>New counterexample requested<textarea name="item_${{n}}_counterexample" rows="2"></textarea></label>`;
 // Scope select names by item after templating.
 p.querySelectorAll('select').forEach((select)=>{{select.name=`item_${{n}}_${{select.name}}`;}}); host.appendChild(p);}});
document.querySelector('#download').addEventListener('click',()=>{{const form=document.querySelector('#review');if(!form.reportValidity())return;
 const responses={{}};for(const el of form.elements)if(el.name)responses[el.name]=el.type==='checkbox'?el.checked:el.value;
 const record={{schema_version:'1.0',record_type:'independent_review',workbook_id:'vertical-slice-01-independent-review-workbook',claim_boundary:'Evidence review only; not listener outcomes.',responses}};
 const blob=new Blob([JSON.stringify(record,null,2)+'\\n'],{{type:'application/json'}}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='vertical-slice-01-independent-review-'+responses.reviewer_name+'.json';a.click();URL.revokeObjectURL(url);
 const result=document.querySelector('#result');result.style.display='block';result.textContent='Review record prepared. Verify reviewer identity and keep the code non-identifying.';}});
</script></body></html>"""
    OUT_HTML.write_text(document)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} ({len(items)} items)")
    return workbook


if __name__ == "__main__":
    build()
