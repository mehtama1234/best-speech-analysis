#!/usr/bin/env python3
"""Build a blank independent workbook for corpus speech-function candidates."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
OUT_JSON = ROOT / "research/corpus-function-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/corpus-function-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/corpus-function-independent-review-workbook.html"

PRIMARY_FUNCTIONS = [
    "opening", "definition", "explanation", "example", "story", "contrast",
    "correction", "question", "answer", "repair", "qualification", "transition",
    "callback", "humour_or_rapport", "persuasion", "call_to_action", "closing",
    "other", "indeterminate",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    atlas = json.loads(ATLAS.read_text())
    items = []
    for item in atlas["candidate_function_review_queue"]["items"]:
        items.append({
            "review_item_id": item["queue_item_id"],
            "candidate_function": item["candidate_function"],
            "event_split": item["event_split"],
            "video_id": item["video_id"],
            "title": item["title"],
            "evidence_id": item["evidence_id"],
            "start_seconds": item["start_seconds"],
            "end_seconds": item["end_seconds"],
            "transcript_text": item["text"],
            "source_url": f"https://www.youtube.com/watch?v={item['video_id']}",
            "internal_reviewed_evidence": item["reviewed_evidence"],
            "review": {
                "context_decision": None,
                "primary_function": None,
                "candidate_label_decision": None,
                "alternate_function": None,
                "reason": None,
                "identity_or_duplicate_note": None,
            },
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "corpus-function-independent-review-workbook",
        "status": "template_not_completed",
        "source_atlas": "research/corpus-pattern-atlas.json",
        "item_count": len(items),
        "claim_boundary": "This review tests transcript speech-function labels in surrounding context. It does not establish delivery effectiveness, audience outcomes, speaker intent or causal effects.",
        "independence_requirement": "Reviewer must not have created the atlas, candidate labels or review queue.",
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "decision_vocabulary": {
            "context_decision": ["supports", "alternate_function", "not_enough_context", "not_relevant"],
            "primary_function": PRIMARY_FUNCTIONS,
            "candidate_label_decision": ["supported", "alternate_function", "indeterminate", "not_relevant"],
        },
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Corpus speech-function independent-review workbook", "",
        "Status: **template not completed**; no independent judgments are present.", "",
        workbook["claim_boundary"], "", f"Items: **{len(items)}**.", "",
        "| # | Split | Candidate label | Video | Evidence | Text | Independent decision |",
        "|---:|---|---|---|---|---|---|",
    ]
    for number, item in enumerate(items, 1):
        text = " ".join(item["transcript_text"].split()).replace("|", "\\|")
        lines.append(f"| {number} | `{item['event_split']}` | `{item['candidate_function']}` | `{item['video_id']}` | `{item['evidence_id']}` | {text[:110]} |  |")
    OUT_MD.write_text("\n".join(lines) + "\n")

    fields = []
    for number, item in enumerate(items, 1):
        options = "".join(f"<option>{esc(value)}</option>" for value in PRIMARY_FUNCTIONS)
        fields.append(
            f'<fieldset><legend>{number}. {esc(item["candidate_function"])} · {esc(item["event_split"])} · {esc(item["video_id"])}</legend>'
            f'<p><b>{esc(item["evidence_id"])}</b> · {esc(item["start_seconds"])}–{esc(item["end_seconds"])}s<br>{esc(item["transcript_text"])}<br>'
            f'<small><a href="{esc(item["source_url"])}" target="_blank" rel="noopener">source URL</a></small></p>'
            f'<label>Context decision<select required name="item_{number}_context_decision"><option value="">Choose</option><option>supports</option><option>alternate_function</option><option>not_enough_context</option><option>not_relevant</option></select></label>'
            f'<label>Primary function<select required name="item_{number}_primary_function"><option value="">Choose</option>{options}</select></label>'
            f'<label>Candidate label decision<select required name="item_{number}_candidate_label_decision"><option value="">Choose</option><option>supported</option><option>alternate_function</option><option>indeterminate</option><option>not_relevant</option></select></label>'
            f'<label>Alternative function or explanation<textarea required name="item_{number}_alternate_function" rows="2"></textarea></label>'
            f'<label>Reason<textarea required name="item_{number}_reason" rows="2"></textarea></label>'
            f'<label>Identity/duplicate note<textarea name="item_{number}_identity_or_duplicate_note" rows="2"></textarea></label></fieldset>'
        )
    html_doc = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Corpus speech-function independent review</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}fieldset{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}label{display:block;margin:.5rem 0}textarea{width:100%;box-sizing:border-box}.notice{background:#fff6d6;padding:.8rem}</style></head><body>'
        '<h1>Corpus speech-function independent review</h1><div class="notice"><strong>Boundary:</strong> Review transcript function and candidate-label fit only. Do not infer delivery effectiveness, intent or audience outcomes.</div>'
        '<form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of atlas and candidate-label creation.</label></fieldset>'
        + "".join(fields)
        + '<button type="button" id="download">Download review JSON</button></form><script>document.querySelector("#download").onclick=()=>{const f=document.querySelector("#review");if(!f.reportValidity())return;const r={};for(const e of f.elements)if(e.name)r[e.name]=e.type==="checkbox"?e.checked:e.value;const blob=new Blob([JSON.stringify({schema_version:"1.0",record_type:"corpus_function_independent_review",workbook_id:"corpus-function-independent-review-workbook",claim_boundary:"Transcript speech-function labels only; not delivery effectiveness or audience outcomes.",responses:r},null,2)+"\\n"],{type:"application/json"}),u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download="corpus-function-independent-review.json";a.click();URL.revokeObjectURL(u)}</script></body></html>'
    )
    OUT_HTML.write_text(html_doc)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
