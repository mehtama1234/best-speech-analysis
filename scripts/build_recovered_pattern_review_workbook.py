#!/usr/bin/env python3
"""Build a label-blinded review workbook for recovered pattern cards."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/recovered-pattern-candidate-cards.json"
PACKET = ROOT / "research/recovered-pattern-independent-review-workbook.json"
KEY = ROOT / "research/recovered-pattern-independent-review-key.json"
REPORT = ROOT / "writeups/recovered-pattern-independent-review.md"
HTML = ROOT / "writeups/recovered-pattern-independent-review.html"


def blind_id(card_id: str) -> str:
    return "blind-recovered-" + hashlib.sha256(card_id.encode()).hexdigest()[:14]


def main() -> int:
    cards = json.loads(CARDS.read_text())["cards"]
    items = []
    key_items = []
    for card in cards:
        bid = blind_id(card["card_id"])
        item = {
            "blind_item_id": bid,
            "video_id": card["video_id"],
            "candidate_video_id": card.get("candidate_video_id"),
            "title": card.get("title"),
            "evidence_layer": card["evidence_layer"],
            "source_url": f"https://www.youtube.com/watch?v={card['candidate_video_id'] or card['video_id']}",
            "evidence": card["evidence"],
            "review_prompt": (
                "Read the excerpt and surrounding source context. Decide whether "
                "the excerpt performs the retrieved communication move, another "
                "move, or cannot be interpreted from the available evidence. "
                "Check source identity, duplication and caption quality."
            ),
        }
        items.append(item)
        key_items.append({
            "blind_item_id": bid,
            "card_id": card["card_id"],
            "pattern_id": card["pattern_id"],
            "category": card["category"],
            "candidate_form": card["candidate_form"],
            "quality_flags": card.get("quality_flags", []),
            "quality_disposition": card.get("quality_disposition"),
        })
    items.sort(key=lambda item: item["blind_item_id"])
    key_items.sort(key=lambda item: item["blind_item_id"])
    packet = {
        "schema_version": "1.0",
        "workbook_id": "recovered-pattern-independent-review",
        "status": "operational_packet_no_human_records",
        "independence_requirement": "Reviewer must not be the analyst who created the recovered cards or internal key.",
        "claim_boundary": (
            "This workbook is an independent review instrument for recovered "
            "transcript candidates. It does not establish semantic accuracy, "
            "source identity, recurrence, delivery meaning, or effectiveness."
        ),
        "decision_vocabulary": [
            "supports_candidate",
            "alternate_function",
            "not_enough_context",
            "indeterminate",
            "identity_mismatch",
            "duplicate_or_compilation",
        ],
        "item_count": len(items),
        "items": items,
    }
    key = {
        "schema_version": "1.0",
        "key_id": "recovered-pattern-independent-review-key",
        "status": "internal_mapping_do_not_send_with_packet",
        "claim_boundary": "Internal mapping only; it is not independent evidence.",
        "items": key_items,
    }
    PACKET.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    KEY.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    REPORT.write_text(
        "\n".join([
            "# Recovered pattern independent-review workbook",
            "",
            "Status: **operational packet; no human records received**.",
            "",
            packet["claim_boundary"],
            "",
            f"- Blinded review items: **{len(items)}**",
            "- Candidate pattern labels are withheld from the packet and retained in the internal key.",
            "- Exact excerpts, source layer, timestamps and source URLs remain visible for review.",
            "",
            "## Files",
            "",
            "- Packet to send: `research/recovered-pattern-independent-review-workbook.json`",
            "- Internal key: `research/recovered-pattern-independent-review-key.json` (do not send)",
            "- Return records must include reviewer identity, independence attestation, decision, context note, identity/duplication note and uncertainty.",
            "",
            "## Decision boundary",
            "",
            "A completed review can support or reject a candidate retrieval. It cannot by itself prove cross-speaker recurrence, delivery meaning, learner transfer, listener outcomes or effectiveness.",
            "",
            "## Reproducibility",
            "",
            "```bash",
            "python3 scripts/build_recovered_pattern_review_workbook.py",
            "```",
        ]) + "\n"
    )
    embedded = json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")
    html = f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Recovered pattern independent review</title>
<style>body{{font:15px/1.45 system-ui,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#17202a}}.notice{{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}}.controls{{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0}}button,select,input,textarea{{font:inherit;padding:.55rem}}button{{cursor:pointer;background:#173f5f;color:white;border:0;border-radius:4px}}button.secondary{{background:#4b5563}}label{{display:block;margin:.65rem 0}}textarea{{width:100%;box-sizing:border-box}}.evidence{{background:#f4f8fb;border-left:4px solid #39739d;padding:.7rem;margin:.5rem 0}}.muted{{color:#5c6872}}.status{{color:#4b5563}}a{{overflow-wrap:anywhere}}</style></head>
<body><h1>Recovered pattern independent review</h1>
<div class='notice'><b>Independent review instrument, not a result.</b> Candidate pattern labels are hidden. Read the excerpt and surrounding context, use indeterminate when needed, and do not infer effectiveness or audience outcomes. Drafts remain local to this browser.</div>
<fieldset><legend>Reviewer metadata</legend><label>Reviewer code <input id='reviewer_code' required></label><label>Reviewer role <input id='reviewer_role' required></label><label>Review date <input id='review_date' type='date' required></label><label>Conflict statement <textarea id='conflict_statement' rows='2' required></textarea><label><input id='independent_attestation' type='checkbox'> I am independent of the analyst who created these cards.</label></fieldset>
<div class='controls'><button id='previous' type='button' class='secondary'>Previous</button><button id='next' type='button'>Next</button><button id='save' type='button' class='secondary'>Save local draft</button><button id='restore' type='button' class='secondary'>Restore draft</button><button id='download' type='button'>Download review export</button><span class='status' id='status' role='status' aria-live='polite'></span></div>
<p id='progress' class='muted'></p><main id='item'></main>
<script id='items' type='application/json'>{embedded}</script>
<script>
const items=JSON.parse(document.querySelector('#items').textContent), state={{index:0,responses:{{}}}}, key='recovered_pattern_review_draft_v1';
const fields=['decision','primary_function','alternate_explanation','context_note','identity_note','uncertainty_note'];
const el=id=>document.getElementById(id), status=message=>el('status').textContent=message;
function current(){{return items[state.index]}}
function capture(){{const response={{}};for(const field of fields){{const node=el(field);if(node)response[field]=node.value}}state.responses[current().blind_item_id]=response}}
function render(){{const item=current(), response=state.responses[item.blind_item_id]||{{}};el('progress').textContent=`Item ${{state.index+1}} of ${{items.length}} · ${{item.evidence_layer}} · ${{item.video_id}}`;let evidence=item.evidence.map(e=>`<div class="evidence"><b>${{e.start ?? 'untimed'}}–${{e.end ?? ''}}</b><br>${{escapeHtml(e.text)}} </div>`).join('');el('item').innerHTML=`<h2>${{escapeHtml(item.title||'Recovered source')}}</h2><p><a href="${{escapeAttr(item.source_url)}}" target="_blank" rel="noreferrer">Open source</a></p><p>${{escapeHtml(item.review_prompt)}}</p>${{evidence}}<label>Decision<select id="decision" required><option value="">Choose</option>${{['supports_candidate','alternate_function','not_enough_context','indeterminate','identity_mismatch','duplicate_or_compilation'].map(x=>`<option ${{response.decision===x?'selected':''}}>${{x}}</option>`).join('')}}</select></label><label>Primary function or role<textarea id="primary_function" rows="2" required>${{escapeHtml(response.primary_function||'')}}</textarea></label><label>Alternate explanation<textarea id="alternate_explanation" rows="2" required>${{escapeHtml(response.alternate_explanation||'')}}</textarea></label><label>Context note<textarea id="context_note" rows="3" required>${{escapeHtml(response.context_note||'')}}</textarea></label><label>Identity, duplication or accessibility note<textarea id="identity_note" rows="2" required>${{escapeHtml(response.identity_note||'')}}</textarea></label><label>Uncertainty note<textarea id="uncertainty_note" rows="2" required>${{escapeHtml(response.uncertainty_note||'')}}</textarea></label>`}}
function escapeHtml(value){{return String(value??'').replace(/[&<>"']/g,x=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[x]))}}
function escapeAttr(value){{return escapeHtml(value).replace(/`/g,'&#96;')}}
el('previous').onclick=()=>{{capture();if(state.index>0)state.index--;render()}};el('next').onclick=()=>{{capture();if(state.index<items.length-1)state.index++;render()}};
function snapshot(){{capture();return {{schema_version:'1.0',record_type:'recovered_pattern_independent_review',workbook_id:'recovered-pattern-independent-review',claim_boundary:'Independent review instrument; not effectiveness evidence.',reviewer:{{reviewer_code:el('reviewer_code').value,reviewer_role:el('reviewer_role').value,review_date:el('review_date').value,conflict_statement:el('conflict_statement').value,independent_attestation:el('independent_attestation').checked}},responses:state.responses}}}}
el('save').onclick=()=>{{localStorage.setItem(key,JSON.stringify(snapshot()));status('Draft saved locally.')}};el('restore').onclick=()=>{{const raw=localStorage.getItem(key);if(!raw)return status('No local draft found.');const data=JSON.parse(raw);Object.assign(state.responses,data.responses||{{}});for(const [id,value] of Object.entries({{reviewer_code:data.reviewer?.reviewer_code||'',reviewer_role:data.reviewer?.reviewer_role||'',review_date:data.reviewer?.review_date||'',conflict_statement:data.reviewer?.conflict_statement||''}}))el(id).value=value;el('independent_attestation').checked=Boolean(data.reviewer?.independent_attestation);render();status('Draft restored locally.')}};
el('download').onclick=()=>{{const data=snapshot();if(!data.reviewer.independent_attestation)return status('Independent attestation is required.');const blob=new Blob([JSON.stringify(data,null,2)+'\\n'],{{type:'application/json'}}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='recovered-pattern-independent-review.json';a.click();URL.revokeObjectURL(url)}};render();
</script></body></html>"""
    HTML.write_text(html)
    print(json.dumps({
        "packet": str(PACKET.relative_to(ROOT)),
        "key": str(KEY.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
        "html": str(HTML.relative_to(ROOT)),
        "item_count": len(items),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
