#!/usr/bin/env python3
"""Build label-blinded packets for independent transcript review."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/blinded-review-packet.json"
KEY = ROOT / "research/blinded-review-packet-key.json"
MD = ROOT / "writeups/blinded-review-packet.md"
HTML = ROOT / "writeups/blinded-review-packet.html"


def blind_id(gate: str, source_id: str) -> str:
    digest = hashlib.sha256(f"{gate}:{source_id}".encode()).hexdigest()[:12]
    return f"blind-{gate}-{digest}"


def main() -> int:
    function = json.loads((ROOT / "research/corpus-function-independent-review-workbook.json").read_text())
    recurrence = json.loads((ROOT / "research/corpus-recurrence-independent-review-workbook.json").read_text())
    phrase = json.loads((ROOT / "research/corpus-phrase-form-independent-review-workbook.json").read_text())
    packet = {"schema_version": "1.0", "packet_id": "blinded-corpus-transcript-review", "status": "blinded_operational_packet_no_human_records", "claim_boundary": "This packet removes internal candidate labels and decisions for independent transcript review. It is an instrument, not evidence that any label, recurrence or phrase form is correct or effective.", "independence_instruction": "The reviewer must not be the analyst who created the source labels, phrase families or packet.", "gates": {}}
    key = {"schema_version": "1.0", "key_id": "blinded-corpus-transcript-review-key", "status": "internal_mapping_do_not_send_with_packet", "claim_boundary": "This key maps blinded IDs to internal source labels for later adjudication; it is not independent evidence.", "items": []}

    function_items = []
    for item in function["items"]:
        bid = blind_id("function", item["review_item_id"])
        function_items.append({"blind_item_id": bid, "video_id": item["video_id"], "title": item["title"], "evidence_id": item["evidence_id"], "start_seconds": item["start_seconds"], "end_seconds": item["end_seconds"], "transcript_text": item["transcript_text"], "source_url": item["source_url"], "event_split": item.get("event_split"), "review_prompt": "Read the surrounding context. Does this segment perform a distinct communication function? Name the primary function in your own words, an alternate if relevant, and whether the segment is interpretable."})
        key["items"].append({"blind_item_id": bid, "gate": "function", "source_review_item_id": item["review_item_id"], "internal_candidate_function": item.get("candidate_function")})
    packet["gates"]["function"] = {"item_count": len(function_items), "source_workbook": "research/corpus-function-independent-review-workbook.json", "items": sorted(function_items, key=lambda x: x["blind_item_id"])}

    recurrence_items = []
    for item in recurrence["items"]:
        bid = blind_id("recurrence", item["review_item_id"])
        recurrence_items.append({"blind_item_id": bid, "video_id": item["video_id"], "title": item["title"], "evidence_id": item["evidence_id"], "start_seconds": item["start_seconds"], "end_seconds": item["end_seconds"], "transcript_text": item["transcript_text"], "source_url": item["source_url"], "event_split": item.get("event_split"), "review_prompt": "Read the surrounding context. Describe what role the retrieved wording plays, whether another function is more plausible, and whether this occurrence should count for a recurrence comparison."})
        key["items"].append({"blind_item_id": bid, "gate": "recurrence", "source_review_item_id": item["review_item_id"], "internal_phrase_family": item.get("phrase_family"), "internal_matched_forms": item.get("matched_forms")})
    packet["gates"]["recurrence"] = {"item_count": len(recurrence_items), "source_workbook": "research/corpus-recurrence-independent-review-workbook.json", "items": sorted(recurrence_items, key=lambda x: x["blind_item_id"])}

    phrase_items = []
    for item in phrase["items"]:
        bid = blind_id("phrase", item["review_item_id"])
        examples = [{key: example.get(key) for key in ("evidence_id", "video_id", "title", "start_seconds", "end_seconds", "text", "event_split", "source_url")} for example in item.get("examples", [])]
        phrase_items.append({"blind_item_id": bid, "phrase_form": item["phrase_form"], "matched_pattern": item["matched_pattern"], "examples": examples, "review_prompt": "Check whether the exact form matches the retained examples, whether its context supports the retrieved family, and whether the sample supports inclusion in recurrence counting. Record ambiguity or duplication risk."})
        key["items"].append({"blind_item_id": bid, "gate": "phrase_form", "source_review_item_id": item["review_item_id"], "internal_family": item.get("family"), "internal_counts": {key: item.get(key) for key in ("occurrence_count", "video_count", "train_video_count", "holdout_video_count")}})
    packet["gates"]["phrase_form"] = {"item_count": len(phrase_items), "source_workbook": "research/corpus-phrase-form-independent-review-workbook.json", "items": sorted(phrase_items, key=lambda x: x["blind_item_id"])}
    key["items"].sort(key=lambda x: x["blind_item_id"])
    OUT.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    KEY.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Blinded transcript-review packet", "", "Status: **operational packet; no human records received**.", "", packet["claim_boundary"], "", "Send the packet without the key. The reviewer should use the exact source links and surrounding context, record uncertainty and disagreement, and return a separate coded export. Do not treat a completed packet as effectiveness evidence.", "", "| Gate | Items | Internal labels hidden |", "|---|---:|---|", f"| function | {len(function_items)} | candidate function and internal review state |", f"| recurrence | {len(recurrence_items)} | phrase family, matched-form list and internal review state |", f"| phrase form | {len(phrase_items)} | family, counts and internal review state |", "", "Files:", "", "- Browser form to send: `writeups/blinded-review-packet.html`", "- Machine packet: `research/blinded-review-packet.json`", "- Internal key: `research/blinded-review-packet-key.json` (do not send)", "- Returned export validator: `scripts/validate_blinded_review_export.py`", "- Source workbooks remain the authoritative response schemas and validators.", "", "Review boundaries:", "", "- Inspect complete context and source identity; use indeterminate when needed.", "- Do not infer speaker intent, delivery meaning, audience outcome or effectiveness.", "- Preserve disagreement and conflict statements.", "- Keep the internal key separate until adjudication.", ""]
    MD.write_text("\n".join(lines))
    all_items = [("function", item) for item in packet["gates"]["function"]["items"]] + [("recurrence", item) for item in packet["gates"]["recurrence"]["items"]] + [("phrase_form", item) for item in packet["gates"]["phrase_form"]["items"]]
    fieldsets = []
    for number, (gate, item) in enumerate(all_items, 1):
        if gate == "phrase_form":
            examples = "".join(f"<blockquote><code>{html.escape(example.get('evidence_id') or '')}</code> {html.escape(example.get('text') or '')}<br><a href='{html.escape(example.get('source_url') or '', quote=True)}'>source</a></blockquote>" for example in item.get("examples", []))
            context = f"<p><b>Exact form:</b> <code>{html.escape(item['phrase_form'])}</code> · pattern <code>{html.escape(item['matched_pattern'])}</code></p>{examples}"
        else:
            context = f"<p><code>{html.escape(item['evidence_id'])}</code> · {html.escape(item['transcript_text'])}</p><p><a href='{html.escape(item['source_url'], quote=True)}'>source at timestamp</a></p>"
        fieldsets.append(f"<fieldset><legend>{number}. {html.escape(gate)} · <code>{html.escape(item['blind_item_id'])}</code></legend>{context}<p>{html.escape(item['review_prompt'])}</p><label>Decision<select required name='item_{number}_decision'><option value=''>Choose</option><option>supports</option><option>alternate_function</option><option>not_enough_context</option><option>indeterminate</option><option>include</option><option>exclude</option></select></label><label>Primary function or role<textarea required name='item_{number}_primary_function' rows='2'></textarea></label><label>Alternate explanation<textarea required name='item_{number}_alternate' rows='2'></textarea></label><label>Reason and context note<textarea required name='item_{number}_reason' rows='2'></textarea></label><label>Identity, duplication or accessibility note<textarea required name='item_{number}_identity_note' rows='2'></textarea></label></fieldset>")
    html_doc = """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Blinded transcript review</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#17202a}fieldset{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}label{display:block;margin:.6rem 0}textarea{width:100%;box-sizing:border-box}select,input,button{font:inherit;padding:.55rem}button{cursor:pointer;background:#173f5f;color:white;border:0;border-radius:4px}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem}.muted{color:#5c6872}.draft-controls{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0}.draft-controls button{background:#4b5563}.draft-status{color:#4b5563}</style></head><body><h1>Blinded transcript review</h1><div class='notice'><b>Independent review instrument, not a result.</b> Internal candidate labels are intentionally hidden. Inspect the surrounding context and source, use indeterminate when needed, and do not infer intent, delivery meaning, audience outcome or effectiveness. Drafts stay in this browser only and are not evidence until exported and independently validated.</div><form id='review'><fieldset><legend>Reviewer metadata</legend><label>Reviewer code<input required name='reviewer_code'></label><label>Role<input required name='reviewer_role'></label><label>Date<input required type='date' name='review_date'></label><label>Conflict statement<textarea required name='conflict_statement' rows='2'></textarea></label><label><input required type='checkbox' name='independent_attestation'> I am independent of the analyst who created the labels and packet.</label></fieldset>__ITEMS__<div class='draft-controls'><button type='button' id='save-draft'>Save local draft</button><button type='button' id='restore-draft'>Restore local draft</button><button type='button' id='clear-draft'>Clear local draft</button><span id='draft-status' class='draft-status' role='status' aria-live='polite'></span></div><button type='button' id='download'>Download blinded review export</button></form><script>const form=document.querySelector('#review'),draftKey='blinded_transcript_review_draft_v1',status=document.querySelector('#draft-status');function snapshot(){const values={};for(const e of form.elements)if(e.name)values[e.name]=e.type==='checkbox'?e.checked:e.value;return values}function restore(values){for(const e of form.elements)if(e.name&&Object.prototype.hasOwnProperty.call(values,e.name)){if(e.type==='checkbox')e.checked=Boolean(values[e.name]);else e.value=values[e.name]}}document.querySelector('#save-draft').onclick=()=>{localStorage.setItem(draftKey,JSON.stringify(snapshot()));status.textContent='Draft saved in this browser.'};document.querySelector('#restore-draft').onclick=()=>{const raw=localStorage.getItem(draftKey);if(!raw){status.textContent='No local draft found.';return}try{restore(JSON.parse(raw));status.textContent='Draft restored from this browser.'}catch{status.textContent='Local draft could not be restored.'}};document.querySelector('#clear-draft').onclick=()=>{localStorage.removeItem(draftKey);status.textContent='Local draft cleared.'};document.querySelector('#download').onclick=()=>{if(!form.reportValidity())return;const responses={};for(const e of form.elements)if(e.name)responses[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({schema_version:'1.0',record_type:'blinded_transcript_review',packet_id:'blinded-corpus-transcript-review',claim_boundary:'Independent transcript review instrument; not effectiveness evidence.',responses},null,2)+'\\n'],{type:'application/json'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='blinded-transcript-review.json';a.click();URL.revokeObjectURL(u)}</script></body></html>""".replace("__ITEMS__", "\n".join(fieldsets))
    HTML.write_text(html_doc)
    print(json.dumps({"packet": str(OUT.relative_to(ROOT)), "key": str(KEY.relative_to(ROOT)), "html": str(HTML.relative_to(ROOT)), "function": len(function_items), "recurrence": len(recurrence_items), "phrase_form": len(phrase_items)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
