#!/usr/bin/env python3
"""Build an independent manual-review workbook for the 18 listener stimulus pairs."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "research/communication-job-listener-stimuli-draft.json"
PREFLIGHT = ROOT / "research/communication-job-stimuli-preflight.json"
OUT_JSON = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"
OUT_MD = ROOT / "writeups/communication-job-listener-stimulus-review-workbook.md"
OUT_HTML = ROOT / "writeups/communication-job-listener-stimulus-review-workbook.html"
OUT_REQUEST = ROOT / "writeups/communication-job-listener-stimulus-review-request.md"


def main() -> int:
    draft = json.loads(DRAFT.read_text())
    preflight = json.loads(PREFLIGHT.read_text())
    preflight_by_id = {row["stimulus_id"]: row for row in preflight["records"]}
    items = []
    for row in draft["records"]:
        audit = preflight_by_id[row["stimulus_id"]]
        items.append({
            "review_item_id": f"stimulus-review:{row['stimulus_id']}",
            "stimulus_id": row["stimulus_id"],
            "card_id": row["card_id"],
            "canonical_job": row["canonical_job"],
            "topic": row["topic"],
            "proposition": row["proposition"],
            "control_text": row["control_text"],
            "pattern_informed_text": row["pattern_informed_text"],
            "word_count_delta": row["word_count_delta"],
            "automated_preflight": audit,
            "review": {
                "proposition_equivalence": None,
                "readability_match": None,
                "target_isolation": None,
                "accessibility": None,
                "safety": None,
                "condition_order_or_blinding": None,
                "lock_decision": None,
                "rationale_and_revision": None,
                "reviewer_code": None,
            },
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "listener-stimulus-review-workbook",
        "status": "manual_equivalence_review_pending",
        "source_draft": "research/communication-job-listener-stimuli-draft.json",
        "source_preflight": "research/communication-job-stimuli-preflight.json",
        "item_count": len(items),
        "claim_boundary": "This workbook checks whether newly authored matched stimulus pairs are suitable for a blinded listener study. It does not establish that a communication pattern works, improves understanding, or causes any listener outcome.",
        "independence_requirement": "Reviewer must not be the person who authored the stimulus pairs or target-pattern labels.",
        "decision_vocabulary": {
            "proposition_equivalence": ["equivalent", "extra_claim_in_one_condition", "not_equivalent", "unclear"],
            "readability_match": ["matched", "control_harder", "pattern_harder", "unclear"],
            "target_isolation": ["isolated", "leakage", "not_decidable"],
            "accessibility": ["pass", "revise", "unclear"],
            "safety": ["pass", "revise", "unclear"],
            "condition_order_or_blinding": ["adequate", "needs_revision", "not_applicable"],
            "lock_decision": ["lock_for_pilot", "hold_for_revision", "exclude_pair"],
        },
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Listener stimulus manual-review workbook", "", "Status: **manual equivalence review pending**; no pairs are locked.", "", workbook["claim_boundary"], "", f"Pairs: **{len(items)}**.", "", "| # | Job | Stimulus | Word delta | Automated target screen | Manual lock |", "|---:|---|---|---:|---|---|"]
    for n, item in enumerate(items, 1):
        lines.append(f"| {n} | `{item['canonical_job']}` | `{item['stimulus_id']}` | {item['word_count_delta']} | `{item['automated_preflight']['target_marker_status']}` | pending |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    vocab = workbook["decision_vocabulary"]
    fieldsets = []
    for n, item in enumerate(items, 1):
        choices = "".join(f'<label>{html.escape(k)}<select required name="item_{n}_{k}"><option value="">Choose</option>{"".join(f"<option>{html.escape(v)}</option>" for v in values)}</select></label>' for k, values in vocab.items())
        fieldsets.append(f'<fieldset><legend>{n}. {html.escape(item["canonical_job"])} · {html.escape(item["stimulus_id"])}</legend><p><b>Proposition:</b> {html.escape(item["proposition"])}</p><p><b>Control:</b> {html.escape(item["control_text"])}</p><p><b>Pattern-informed:</b> {html.escape(item["pattern_informed_text"])}</p><p><small>Automated screen: target markers {html.escape(item["automated_preflight"]["target_marker_status"])}; word delta {item["word_count_delta"]}. Automated screen does not prove equivalence.</small></p>{choices}<label>Reviewer code<input required name="item_{n}_reviewer_code"></label><label>Rationale/revision<textarea required name="item_{n}_rationale_and_revision" rows="3"></textarea></label></fieldset>')
    OUT_HTML.write_text(f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Listener stimulus review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.4rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style><h1>Listener stimulus manual review</h1><div class="notice">{html.escape(workbook["claim_boundary"])}</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<textarea required name="review_modality" rows="2"></textarea></label><label>Conflict statement<textarea required name="conflict_statement" rows="2"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of stimulus authorship and target labels.</label></fieldset>{''.join(fieldsets)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'listener_stimulus_independent_review',workbook_id:'listener-stimulus-review-workbook',claim_boundary:'Stimulus suitability review only; not listener outcome evidence.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='listener-stimulus-independent-review.json';a.click();URL.revokeObjectURL(u)}};</script>''')
    OUT_REQUEST.write_text("""# Listener stimulus review request\n\nReview all 18 newly authored matched pairs independently. Check proposition equivalence, readability, target isolation, accessibility, safety and blinding/order. Use `hold_for_revision` or `exclude_pair` when needed; do not lock a pair because an automated preflight passed.\n\n- Workbook: `research/communication-job-listener-stimulus-review-workbook.json`\n- Browser form: `writeups/communication-job-listener-stimulus-review-workbook.html`\n- Validator: `scripts/validate_listener_stimulus_review.py`\n\nA locked stimulus set is a prerequisite for listener outcome records; this review itself is not outcome evidence.\n""")
    print(f"wrote listener stimulus review workbook ({len(items)} pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
