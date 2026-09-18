#!/usr/bin/env python3
"""Build a blank independent workbook for transcript recurrence candidates."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
OUT_JSON = ROOT / "research/corpus-recurrence-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/corpus-recurrence-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/corpus-recurrence-independent-review-workbook.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    atlas = json.loads(ATLAS.read_text())
    items = []
    for item in atlas["recurrence_review_queue"]["items"]:
        items.append({
            "review_item_id": item["queue_item_id"],
            "phrase_family": item["phrase_family"],
            "event_split": item["event_split"],
            "video_id": item["video_id"],
            "title": item["title"],
            "evidence_id": item["evidence_id"],
            "start_seconds": item["start_seconds"],
            "end_seconds": item["end_seconds"],
            "transcript_text": item["text"],
            "matched_forms": item["matched_forms"],
            "source_url": f"https://www.youtube.com/watch?v={item['video_id']}",
            "internal_reviewed_evidence": item["reviewed_evidence"],
            "review": {
                "context_decision": None,
                "phrase_role_decision": None,
                "primary_function": None,
                "recurrence_include_decision": None,
                "alternative_function": None,
                "reason": None,
                "identity_or_duplicate_note": None,
            },
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "corpus-recurrence-independent-review-workbook",
        "status": "template_not_completed",
        "source_atlas": "research/corpus-pattern-atlas.json",
        "item_count": len(items),
        "claim_boundary": "This review tests whether exact transcript phrase hits support a proposed speech-function label in context. It does not establish delivery effectiveness, audience outcomes, speaker intent or causal effects.",
        "independence_requirement": "Reviewer must not have created the atlas, phrase queue or candidate labels.",
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "decision_vocabulary": {
            "context_decision": ["supports", "alternate_function", "not_enough_context", "not_relevant"],
            "phrase_role_decision": ["central", "incidental", "quoted_or_repeated", "unclear"],
            "primary_function": ["opening", "definition", "explanation", "example", "story", "contrast", "correction", "question", "answer", "repair", "qualification", "transition", "callback", "humour_or_rapport", "persuasion", "call_to_action", "closing", "other", "indeterminate"],
            "recurrence_include_decision": ["include", "exclude", "indeterminate"],
        },
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Corpus recurrence independent-review workbook", "",
        "Status: **template not completed**; no independent judgments are present.", "",
        workbook["claim_boundary"], "", f"Items: **{len(items)}**.", "",
        "| # | Split | Phrase family | Video | Evidence | Text | Independent decision |",
        "|---:|---|---|---|---|---|---|",
    ]
    for number, item in enumerate(items, 1):
        text = " ".join(item["transcript_text"].split()).replace("|", "\\|")
        lines.append(f"| {number} | `{item['event_split']}` | `{item['phrase_family']}` | `{item['video_id']}` | `{item['evidence_id']}` | {text[:110]} |  |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fields = []
    for number, item in enumerate(items, 1):
        fields.append(f'''<fieldset><legend>{number}. {esc(item['phrase_family'])} · {esc(item['event_split'])} · {esc(item['video_id'])}</legend><p><b>{esc(item['evidence_id'])}</b> · {esc(item['start_seconds'])}–{esc(item['end_seconds'])}s<br>{esc(item['transcript_text'])}<br><small>Matched forms: {esc(', '.join(item['matched_forms']))} · <a href="{esc(item['source_url'])}" target="_blank" rel="noopener">source URL</a></small></p><label>Context decision<select required name="item_{number}_context_decision"><option value="">Choose</option><option>supports</option><option>alternate_function</option><option>not_enough_context</option><option>not_relevant</option></select></label><label>Phrase role<select required name="item_{number}_phrase_role_decision"><option value="">Choose</option><option>central</option><option>incidental</option><option>quoted_or_repeated</option><option>unclear</option></select></label><label>Primary function<select required name="item_{number}_primary_function"><option value="">Choose</option>{''.join(f'<option>{esc(v)}</option>' for v in workbook['decision_vocabulary']['primary_function'])}</select></label><label>Include as recurrence evidence?<select required name="item_{number}_recurrence_include_decision"><option value="">Choose</option><option>include</option><option>exclude</option><option>indeterminate</option></select></label><label>Alternative function or explanation<textarea required name="item_{number}_alternative_function" rows="2"></textarea></label><label>Reason<textarea required name="item_{number}_reason" rows="2"></textarea></label><label>Identity/duplicate note<textarea name="item_{number}_identity_or_duplicate_note" rows="2"></textarea></label></fieldset>''')
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Corpus recurrence independent review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style></head><body><h1>Corpus recurrence independent review</h1><div class="notice"><strong>Boundary:</strong> Review transcript function and recurrence eligibility only. Do not infer delivery effectiveness, intent or audience outcomes. Use “indeterminate” when context is insufficient.</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of atlas and candidate-label creation.</label></fieldset>{''.join(fields)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'corpus_recurrence_independent_review',workbook_id:'corpus-recurrence-independent-review-workbook',claim_boundary:'Transcript-function and recurrence eligibility only; not delivery effectiveness or audience outcomes.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='corpus-recurrence-independent-review.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
