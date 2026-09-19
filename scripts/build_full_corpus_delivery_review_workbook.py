#!/usr/bin/env python3
"""Build a blank manual delivery-review workbook for every fixed-corpus video."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/full-corpus-delivery-inspection.json"
ITINERARY = ROOT / "research/corpus-video-learning-itinerary.json"
OUT = ROOT / "research/full-corpus-delivery-review-workbook.json"
HTML = ROOT / "writeups/full-corpus-delivery-review-workbook.html"

DECISIONS = ["observed_and_bounded", "indeterminate", "not_available", "needs_followup"]


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def build() -> dict:
    queue = json.loads(QUEUE.read_text())
    itinerary = {row["video_id"]: row for row in json.loads(ITINERARY.read_text())["entries"]}
    items = []
    for row in queue["rows"]:
        lesson = itinerary.get(row["video_id"], {})
        evidence = lesson.get("exact_evidence", [])
        first = evidence[0] if evidence else {}
        items.append({
            "review_item_id": f"delivery:{row['video_id']}",
            "video_id": row["video_id"],
            "title": row["title"],
            "source_url": row.get("source_url"),
            "writeup": row.get("writeup"),
            "learning_track": row.get("learning_track"),
            "media_state": row["media_state"],
            "feature_report": row.get("feature_report"),
            "evidence_id": first.get("evidence_id"),
            "evidence_start_seconds": first.get("start_seconds"),
            "evidence_end_seconds": first.get("end_seconds"),
            "evidence_text": first.get("text"),
            "review": None,
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "full-corpus-delivery-review-workbook",
        "status": "blank_manual_review_workbook_no_human_records",
        "claim_boundary": "Blank review infrastructure is not delivery evidence. Completed records must describe observable timing, vocal change, visible action, setting, editing, accessibility and missingness without inferring emotion, intent, identity, comprehension or effectiveness.",
        "independence_requirement": "For independent promotion review, the reviewer must not be the person who created the transcript interpretation or proxy candidate selection.",
        "video_count": len(items),
        "completed_review_count": 0,
        "decision_vocabulary": DECISIONS,
        "reviewer": None,
        "items": items,
    }
    OUT.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    fieldsets = []
    for number, item in enumerate(items, 1):
        links = []
        if item.get("source_url"):
            links.append(f"<a href='{esc(item['source_url'])}'>source</a>")
        if item.get("writeup"):
            links.append(f"<a href='../{esc(item['writeup'])}'>full writeup</a>")
        evidence = f"<blockquote><code>{esc(item['evidence_id'])}</code> {esc(item['evidence_text'])}<br>{esc(item['evidence_start_seconds'])}–{esc(item['evidence_end_seconds'])} seconds</blockquote>" if item.get("evidence_id") else "<p>No retained evidence window is linked; record media availability only.</p>"
        options = "".join(f"<option>{esc(value)}</option>" for value in DECISIONS)
        fieldsets.append(f"<fieldset data-state='{esc(item['media_state'])}' data-search='{esc(' '.join(str(v) for v in item.values()))}'><legend>{number}. {esc(item['video_id'])} · {esc(item['title'])}</legend><p>{' · '.join(links)} · media <code>{esc(item['media_state'])}</code> · track <code>{esc(item['learning_track'] or 'unrouted')}</code></p>{evidence}<label>Decision<select required name='item_{number}_decision'><option value=''>Choose</option>{options}</select></label><label>Observable timing / pauses<textarea required name='item_{number}_timing' rows='2'></textarea></label><label>Observable vocal change<textarea required name='item_{number}_vocal' rows='2'></textarea></label><label>Visible action / orientation<textarea required name='item_{number}_visible' rows='2'></textarea></label><label>Setting / edit / music<textarea required name='item_{number}_setting' rows='2'></textarea></label><label>Accessibility / missingness / uncertainty<textarea required name='item_{number}_access' rows='2'></textarea></label><label>Reviewer note<textarea required name='item_{number}_note' rows='2'></textarea></label></fieldset>")
    html_doc = """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Full-corpus delivery review workbook</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select,textarea{font:inherit;padding:.5rem;margin:.25rem 0;box-sizing:border-box}input,select,textarea{width:100%}fieldset{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}legend{font-weight:700}.notice{background:#fff6d6;border-left:4px solid #b8860b;padding:1rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem}.controls{position:sticky;top:0;background:white;padding:.5rem 0;border-bottom:1px solid #ccd3da}button{font:inherit;padding:.6rem .8rem;cursor:pointer}</style></head><body><h1>Full-corpus delivery review workbook</h1><div class='notice'><b>Blank workbook, not evidence.</b> Record only observable timing, vocal change, visible action, setting, editing, accessibility and missingness. Use <code>indeterminate</code> or <code>not_available</code> rather than inferring emotion, intent, identity, comprehension or effectiveness. Independent review requires a reviewer separate from the original interpretation.</div><form id='review'><fieldset><legend>Reviewer</legend><label>Name or code<input required name='reviewer_name'></label><label>Role<input required name='reviewer_role'></label><label>Date<input required type='date' name='review_date'></label><label>Modality and tools<input required name='review_modality'></label><label>Conflict statement<textarea required name='conflict_statement' rows='2'></textarea></label><label><input required type='checkbox' name='independent_attestation'> I am independent of the original interpretation and proxy selection.</label></fieldset><div class='controls'><label>Search<input id='search' type='search' placeholder='video, title, media state or track'></label><label>Media state<select id='state'><option value=''>All states</option><option>raw_audio_video_present</option><option>derived_features_only</option><option>transcript_only_no_local_media</option><option>video_only</option></select></label><button type='button' id='download'>Download review JSON</button><span id='count'></span></div>__FIELDSETS__</form><script>const form=document.querySelector('#review'),sets=[...document.querySelectorAll('fieldset[data-state]')],search=document.querySelector('#search'),state=document.querySelector('#state'),count=document.querySelector('#count');function filter(){const q=search.value.toLowerCase(),s=state.value;let n=0;sets.forEach(x=>{const ok=(!s||x.dataset.state===s)&&(!q||x.dataset.search.toLowerCase().includes(q));x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${sets.length} items`}search.oninput=filter;state.onchange=filter;document.querySelector('#download').onclick=()=>{if(!form.reportValidity())return;const reviewer={};for(const e of form.elements)if(e.name&&e.name.startsWith('reviewer_'))reviewer[e.name]=e.type==='checkbox'?e.checked:e.value;const responses={};for(const e of form.elements)if(e.name&&e.name.startsWith('item_'))responses[e.name]=e.value;const output={schema_version:'1.0',record_type:'full_corpus_delivery_review',workbook_id:'full-corpus-delivery-review-workbook',claim_boundary:'Completed records describe observable delivery only; they do not establish intent, emotion, comprehension or effectiveness.',reviewer,responses};const blob=new Blob([JSON.stringify(output,null,2)+'\\n'],{type:'application/json'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='full-corpus-delivery-review.json';a.click();URL.revokeObjectURL(u)};filter()</script></body></html>""".replace("__FIELDSETS__", "\n".join(fieldsets))
    HTML.write_text(html_doc)
    return workbook


if __name__ == "__main__":
    workbook = build()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": workbook["video_count"]}, indent=2))
