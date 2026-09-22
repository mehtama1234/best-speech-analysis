#!/usr/bin/env python3
"""Build a local browser for the bounded recovered-pattern priority packet."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research/recovered-pattern-priority-review.json"
OUT = ROOT / "writeups/recovered-pattern-priority-review.html"


def main() -> int:
    packet = json.loads(PACKET.read_text())
    items = json.dumps(packet["items"], ensure_ascii=False).replace("<", "\\u003c")
    html = f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Recovered pattern priority review</title>
<style>body{{font:15px/1.45 system-ui,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#17202a}}.notice{{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}}.controls{{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0}}button,select,input,textarea{{font:inherit;padding:.55rem}}button{{cursor:pointer;background:#173f5f;color:white;border:0;border-radius:4px}}button.secondary{{background:#4b5563}}label{{display:block;margin:.65rem 0}}textarea{{width:100%;box-sizing:border-box}}.evidence{{background:#f4f8fb;border-left:4px solid #39739d;padding:.7rem;margin:.5rem 0}}.muted{{color:#5c6872}}.status{{color:#4b5563}}a{{overflow-wrap:anywhere}}</style></head>
<body><h1>Recovered pattern priority review</h1>
<div class='notice'><b>This is a review form, not a finding.</b> Each item shows the proposed move to check, but hides its internal pattern name, category and card ID. Open the source and read the surrounding context before deciding. If you cannot tell, say so; do not guess. You may return a partial review. Blank answers stay blank. This review cannot show whether a move is common or effective. Drafts stay in this browser on this device.</div>
<fieldset><legend>Reviewer metadata</legend><label>Reviewer code <input id='reviewer_code' required></label><label>Reviewer role <input id='reviewer_role' required></label><label>Review date <input id='review_date' type='date' required></label><label>Conflict statement <textarea id='conflict_statement' rows='2' required></textarea><label><input id='independent_attestation' type='checkbox'> I did not create these candidate cards or labels, have not seen the internal key or another reviewer’s decisions, and can review this packet independently.</label></fieldset>
<div class='controls'><button id='previous' type='button' class='secondary'>Previous</button><button id='next' type='button'>Next</button><button id='save' type='button' class='secondary'>Save local draft</button><button id='restore' type='button' class='secondary'>Restore draft</button><button id='download' type='button'>Download review export</button><span class='status' id='status' role='status' aria-live='polite'></span></div>
<p id='progress' class='muted'></p><main id='item'></main>
<script id='items' type='application/json'>{items}</script>
<script>
const items=JSON.parse(document.querySelector('#items').textContent), state={{index:0,responses:{{}}}}, key='recovered_pattern_priority_review_draft_v1';
const fields=['decision','primary_function','alternate_explanation','context_note','identity_note','uncertainty_note'];
const el=id=>document.getElementById(id), status=message=>el('status').textContent=message;
function current(){{return items[state.index]}}
function capture(){{const response={{}};for(const field of fields){{const node=el(field);if(node)response[field]=node.value}}state.responses[current().blind_item_id]=response}}
function escapeHtml(value){{return String(value??'').replace(/[&<>"']/g,x=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[x]))}}
function escapeAttr(value){{return escapeHtml(value).replace(/`/g,'&#96;')}}
function excerpt(e,item){{const timed=e.start!==null&&e.start!==undefined&&Number.isFinite(Number(e.start)),link=timed?`<a href="${{escapeAttr(item.source_url+'&t='+Math.floor(Number(e.start))+'s')}}" target="_blank" rel="noreferrer">Open at excerpt</a>`:'';return `<div class="evidence"><b>${{e.start ?? 'untimed'}}–${{e.end ?? ''}}</b> ${{link}}<br>${{escapeHtml(e.text)}}</div>`}}
function sourceLinks(item){{const label=item.evidence_layer==='alternate_source'?'Open alternate transcript source':'Open transcript source';const original=item.original_source_url?` · <a href="${{escapeAttr(item.original_source_url)}}" target="_blank" rel="noreferrer">Open original catalog source (identity check)</a>`:'';return `<p><a href="${{escapeAttr(item.source_url)}}" target="_blank" rel="noreferrer">${{label}}</a>${{original}}</p>`}}
function sourceBasis(item){{return {{direct_audio:'Transcript made from the linked video’s audio',alternate_source:'Transcript from an alternate video source',external_transcript:'Transcript from an outside source'}}[item.evidence_layer]||'Transcript source not classified'}}
function render(){{const item=current(), response=state.responses[item.blind_item_id]||{{}};el('progress').textContent=`Item ${{state.index+1}} of ${{items.length}}`;let evidence=item.evidence.map(e=>excerpt(e,item)).join(''),originalNote=item.original_source_url?'<p class="muted">The title identifies the original catalog item; the linked alternate source is shown separately.</p>':'';const choices=[['supports_candidate','Yes — the excerpt shows this move'],['alternate_function','No — the speaker is doing something else'],['not_enough_context','I cannot tell from the available context'],['indeterminate','I am unsure for another reason'],['identity_mismatch','The speaker or source may be misidentified'],['duplicate_or_compilation','This appears to be a duplicate or compilation clip']];el('item').innerHTML=`<h2>${{escapeHtml(item.title||'Source excerpt')}}</h2><p><strong>Proposed move to check:</strong> ${{escapeHtml(item.proposed_move)}}</p><p class="muted">${{sourceBasis(item)}}. Check the linked source: machine transcripts can contain errors.</p>${{sourceLinks(item)}}${{originalNote}}<p>${{escapeHtml(item.review_prompt)}}</p>${{evidence}}<label>What is your decision?<select id="decision" required><option value="">Choose one</option>${{choices.map(([value,label])=>`<option value="${{value}}" ${{response.decision===value?'selected':''}}>${{label}}</option>`).join('')}}</select></label><label>What is the speaker doing here?<textarea id="primary_function" rows="2" required>${{escapeHtml(response.primary_function||'')}}</textarea></label><label>What is another plausible explanation?<textarea id="alternate_explanation" rows="2" required>${{escapeHtml(response.alternate_explanation||'')}}</textarea></label><label>What surrounding context matters?<textarea id="context_note" rows="3" required>${{escapeHtml(response.context_note||'')}}</textarea></label><label>Any concern about the source, repetition or access?<textarea id="identity_note" rows="2" required>${{escapeHtml(response.identity_note||'')}}</textarea></label><label>What are you unsure about?<textarea id="uncertainty_note" rows="2" required>${{escapeHtml(response.uncertainty_note||'')}}</textarea></label>`}}
el('previous').onclick=()=>{{capture();if(state.index>0)state.index--;render()}};el('next').onclick=()=>{{capture();if(state.index<items.length-1)state.index++;render()}};
function snapshot(){{capture();return {{schema_version:'1.0',record_type:'recovered_pattern_priority_review',review_packet_id:'recovered-pattern-priority-review',claim_boundary:'Independent review instrument; not effectiveness evidence.',reviewer:{{reviewer_code:el('reviewer_code').value,reviewer_role:el('reviewer_role').value,review_date:el('review_date').value,conflict_statement:el('conflict_statement').value,independent_attestation:el('independent_attestation').checked}},responses:state.responses}}}}
el('save').onclick=()=>{{localStorage.setItem(key,JSON.stringify(snapshot()));status('Draft saved locally.')}};el('restore').onclick=()=>{{const raw=localStorage.getItem(key);if(!raw)return status('No local draft found.');const data=JSON.parse(raw);Object.assign(state.responses,data.responses||{{}});for(const [id,value] of Object.entries({{reviewer_code:data.reviewer?.reviewer_code||'',reviewer_role:data.reviewer?.reviewer_role||'',review_date:data.reviewer?.review_date||'',conflict_statement:data.reviewer?.conflict_statement||''}}))el(id).value=value;el('independent_attestation').checked=Boolean(data.reviewer?.independent_attestation);render();status('Draft restored locally.')}};
el('download').onclick=()=>{{const data=snapshot();if(!data.reviewer.independent_attestation)return status('Independent attestation is required.');const blob=new Blob([JSON.stringify(data,null,2)+'\\n'],{{type:'application/json'}}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='recovered-pattern-priority-review.json';a.click();URL.revokeObjectURL(url);status('Export downloaded. Run the validator to see decision and note coverage; missing fields are not inferred.')}};render();
</script></body></html>"""
    OUT.write_text(html)
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "item_count": len(packet["items"]), "pattern_count": packet["pattern_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
