#!/usr/bin/env python3
"""Build a blank independent review workbook for exact phrase forms."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "research/corpus-phrase-form-inventory.json"
OUT_JSON = ROOT / "research/corpus-phrase-form-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/corpus-phrase-form-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/corpus-phrase-form-independent-review-workbook.html"
OUT_REQUEST = ROOT / "writeups/corpus-phrase-form-independent-review-request.md"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    inventory = json.loads(INVENTORY.read_text())
    items = []
    for form in inventory["forms"]:
        examples = form["examples"][:2]
        items.append({
            "review_item_id": f"phrase-form:{form['family']}:{form['phrase_form']}",
            "phrase_form": form["phrase_form"],
            "family": form["family"],
            "matched_pattern": form["matched_pattern"],
            "occurrence_count": form["occurrence_count"],
            "video_count": form["video_count"],
            "train_video_count": form["train_video_count"],
            "holdout_video_count": form["holdout_video_count"],
            "examples": examples,
            "review": {
                "form_match_decision": None,
                "primary_function": None,
                "alternate_function": None,
                "speaker_event_identity": None,
                "duplicate_or_compilation_risk": None,
                "recurrence_decision": None,
                "reason": None,
            },
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "corpus-phrase-form-independent-review-workbook",
        "status": "template_not_completed",
        "source_inventory": "research/corpus-phrase-form-inventory.json",
        "item_count": len(items),
        "claim_boundary": "This review tests whether the listed exact transcript form is actually present and whether the sampled contexts support a proposed communication-function and recurrence interpretation. It does not establish delivery effectiveness, speaker intent, audience outcomes, causality or universal best practice.",
        "sampling_rule": "The inventory supplies up to two exact-source examples per form, preserving train/holdout labels when available. A reviewer may request more examples when these are insufficient.",
        "independence_requirement": "Reviewer must not have created the phrase inventory, regex families, candidate mechanisms or workbook.",
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "decision_vocabulary": {
            "form_match_decision": ["confirmed", "not_exact", "unclear"],
            "primary_function": ["opening", "definition", "explanation", "example", "story", "contrast", "correction", "question", "answer", "repair", "qualification", "transition", "callback", "humour_or_rapport", "persuasion", "call_to_action", "closing", "other", "indeterminate"],
            "speaker_event_identity": ["distinct_event", "same_event_as_another_item", "compilation_or_clip", "unclear"],
            "duplicate_or_compilation_risk": ["low", "medium", "high", "unclear"],
            "recurrence_decision": ["admit_as_candidate", "exclude", "indeterminate"],
        },
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Exact phrase-form independent review workbook", "",
        "Status: **template not completed**; no independent judgments are present.", "",
        workbook["claim_boundary"], "", f"Items: **{len(items)} exact forms**.", "",
        "| # | Exact form | Family | Train videos | Holdout videos | Sample contexts | Decision |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    for number, item in enumerate(items, 1):
        lines.append(f"| {number} | `{item['phrase_form']}` | `{item['family']}` | {item['train_video_count']} | {item['holdout_video_count']} | {len(item['examples'])} |  |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fields = []
    for number, item in enumerate(items, 1):
        examples = "".join(f'<li><b>{esc(ex["event_split"])}</b> · {esc(ex["evidence_id"])} · {esc(ex["text"])} · <a href="{esc(ex["source_url"])}" target="_blank" rel="noopener">source</a></li>' for ex in item["examples"])
        fields.append(f'''<fieldset><legend>{number}. <code>{esc(item["phrase_form"])}</code> · {esc(item["family"])}</legend><p>Regex: <code>{esc(item["matched_pattern"])}</code> · {item["occurrence_count"]} occurrences in {item["video_count"]} videos ({item["train_video_count"]} train / {item["holdout_video_count"]} holdout).</p><ol>{examples}</ol><label>Exact form confirmed in sampled contexts?<select required name="item_{number}_form_match_decision"><option value="">Choose</option><option>confirmed</option><option>not_exact</option><option>unclear</option></select></label><label>Primary function<select required name="item_{number}_primary_function"><option value="">Choose</option>{''.join(f'<option>{esc(v)}</option>' for v in workbook["decision_vocabulary"]["primary_function"])}</select></label><label>Speaker/event identity<select required name="item_{number}_speaker_event_identity"><option value="">Choose</option><option>distinct_event</option><option>same_event_as_another_item</option><option>compilation_or_clip</option><option>unclear</option></select></label><label>Duplicate/compilation risk<select required name="item_{number}_duplicate_or_compilation_risk"><option value="">Choose</option><option>low</option><option>medium</option><option>high</option><option>unclear</option></select></label><label>Recurrence decision<select required name="item_{number}_recurrence_decision"><option value="">Choose</option><option>admit_as_candidate</option><option>exclude</option><option>indeterminate</option></select></label><label>Alternate function or explanation<textarea required name="item_{number}_alternate_function" rows="2"></textarea></label><label>Reason and evidence limits<textarea required name="item_{number}_reason" rows="2"></textarea></label></fieldset>''')
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Exact phrase-form independent review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style></head><body><h1>Exact phrase-form independent review</h1><div class="notice"><strong>Boundary:</strong> Exact transcript form, sampled function, identity/duplication and recurrence eligibility only. Do not infer delivery effectiveness, speaker intent or audience outcomes.</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of inventory and candidate-label creation.</label></fieldset>{''.join(fields)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'corpus_phrase_form_independent_review',workbook_id:'corpus-phrase-form-independent-review-workbook',claim_boundary:'Exact transcript form and sampled recurrence eligibility only; not delivery effectiveness or audience outcomes.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='corpus-phrase-form-independent-review.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    OUT_REQUEST.write_text("""# Exact phrase-form independent review request\n\nPlease review the 50 exact phrase forms without having created the inventory or candidate labels. For each form, verify the sampled transcript matches the form, label the primary function, flag alternate functions, identify duplicate/compilation risk, and decide whether it is eligible as a recurrence candidate. Preserve `indeterminate` decisions and disagreements.\n\nThis review does not test delivery, speaker intent, audience outcomes, causality or universal best practice.\n\n- Workbook: `research/corpus-phrase-form-independent-review-workbook.json`\n- Browser form: `writeups/corpus-phrase-form-independent-review-workbook.html`\n- Required export validator: to be added before any results are promoted.\n""")
    OUT_REQUEST.write_text(OUT_REQUEST.read_text().replace("- Required export validator: to be added before any results are promoted.", "- Required export validator: `scripts/validate_corpus_phrase_form_review.py`\n- Disagreement comparator: `scripts/compare_corpus_phrase_form_reviews.py`"))
    print(f"wrote exact phrase-form workbook and views ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
