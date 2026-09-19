#!/usr/bin/env python3
"""Build the blank counterexample library for all provisional communication jobs."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/communication-job-cards.json"
OUT_JSON = ROOT / "research/communication-job-counterexample-workbook.json"
OUT_MD = ROOT / "writeups/communication-job-counterexample-workbook.md"
OUT_HTML = ROOT / "writeups/communication-job-counterexample-workbook.html"
OUT_REQUEST = ROOT / "writeups/communication-job-counterexample-review-request.md"

COUNTEREXAMPLE_TYPES = [
    ("absent_but_speech_works", "Find a comparable communication job where the proposed form is absent but the speech still works; record what other choice may explain it."),
    ("present_but_speech_fails", "Find a case where the proposed form is present but the speech is unclear, unsafe, ineffective-looking or otherwise fails for an observable reason; do not infer audience outcomes."),
    ("alternate_function", "Find a case where the same words or behavior serve a different communication job than the proposed one."),
    ("confound_or_setting", "Find a case where topic, editing, microphone, audience, room, genre, speaker identity or caption quality could explain the observation."),
    ("misuse_or_copying_risk", "Record a source-grounded or reviewer-grounded situation where copying the form would be unnatural, coercive, inaccessible, unsafe or privacy-invasive."),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    cards = json.loads(CARDS.read_text())["cards"]
    items = []
    for card in cards:
        for kind, requirement in COUNTEREXAMPLE_TYPES:
            items.append({
                "review_item_id": f"counterexample:{card['canonical_job']}:{kind}",
                "card_id": card["card_id"],
                "canonical_job": card["canonical_job"],
                "counterexample_type": kind,
                "requirement": requirement,
                "candidate": {"evidence_id": None, "video_id": None, "title": None, "start_seconds": None, "end_seconds": None, "source_url": None, "transcript_excerpt": None},
                "review": {"evidence_status": None, "function_decision": None, "identity_status": None, "context_note": None, "alternative_explanation": None, "safety_or_accessibility_note": None, "reviewer_code": None},
            })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "communication-job-counterexample-workbook",
        "status": "template_not_completed",
        "source_cards": "research/communication-job-cards.json",
        "item_count": len(items),
        "job_count": len(cards),
        "counterexample_types_per_job": len(COUNTEREXAMPLE_TYPES),
        "claim_boundary": "This workbook collects counterexamples, alternate functions, confounds and misuse limits for provisional transcript-derived practice hypotheses. Blank slots are not evidence. Completed records do not establish delivery effectiveness, speaker intent, audience outcomes, causality or universal best practice.",
        "independence_requirement": "Reviewer must not be the person who created the original card interpretation or candidate counterexample selection.",
        "decision_vocabulary": {
            "evidence_status": ["confirmed_counterexample", "candidate_requires_check", "not_a_counterexample", "insufficient_context", "no_candidate_found"],
            "function_decision": ["same_job", "alternate_job", "mixed_jobs", "not_decidable"],
            "identity_status": ["distinct_event", "duplicate_or_compilation", "unclear"],
        },
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job counterexample workbook", "", "Status: **template not completed**; no counterexample judgments are present.", "", workbook["claim_boundary"], "", f"Jobs: **{len(cards)}** · required counterexample slots: **{len(items)}**.", "", "| # | Job | Required counterexample type | Evidence | Decision |", "|---:|---|---|---|---|"]
    for n, item in enumerate(items, 1):
        lines.append(f"| {n} | `{item['canonical_job']}` | `{item['counterexample_type']}` |  |  |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fieldsets = []
    for n, item in enumerate(items, 1):
        vocab = workbook["decision_vocabulary"]
        fieldsets.append(f'''<fieldset><legend>{n}. {esc(item['canonical_job'])} · {esc(item['counterexample_type'])}</legend><p>{esc(item['requirement'])}</p><label>Evidence ID (or blank if no candidate)<input name="item_{n}_evidence_id"></label><label>Video ID<input name="item_{n}_video_id"></label><label>Title<input name="item_{n}_title"></label><label>Start/end seconds<input name="item_{n}_time"></label><label>Source URL<input name="item_{n}_source_url" type="url"></label><label>Transcript excerpt<textarea name="item_{n}_transcript_excerpt" rows="2"></textarea></label><label>Evidence status<select required name="item_{n}_evidence_status"><option value="">Choose</option>{''.join(f'<option>{esc(v)}</option>' for v in vocab['evidence_status'])}</select></label><label>Function decision<select required name="item_{n}_function_decision"><option value="">Choose</option>{''.join(f'<option>{esc(v)}</option>' for v in vocab['function_decision'])}</select></label><label>Identity status<select required name="item_{n}_identity_status"><option value="">Choose</option>{''.join(f'<option>{esc(v)}</option>' for v in vocab['identity_status'])}</select></label><label>Context note<textarea required name="item_{n}_context_note" rows="2"></textarea></label><label>Alternative explanation<textarea required name="item_{n}_alternative_explanation" rows="2"></textarea></label><label>Safety/accessibility note<textarea required name="item_{n}_safety_or_accessibility_note" rows="2"></textarea></label><label>Reviewer code<input required name="item_{n}_reviewer_code"></label></fieldset>''')
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication-job counterexample review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style></head><body><h1>Communication-job counterexample review</h1><div class="notice"><strong>Boundary:</strong> Counterexample and limitation review only. Do not infer effectiveness, intent or audience outcomes. A blank or “no candidate found” slot is an honest result.</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of the original card interpretation and candidate selection.</label></fieldset>{''.join(fieldsets)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'communication_job_counterexample_review',workbook_id:'communication-job-counterexample-workbook',claim_boundary:'Counterexample and limitation review only; not delivery effectiveness or audience outcomes.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='communication-job-counterexample-review.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    OUT_REQUEST.write_text("""# Communication-job counterexample review request\n\nReview all 90 slots independently: five required counterexample types for each of the 18 provisional communication jobs. Preserve `no_candidate_found`, `insufficient_context` and disagreement decisions; do not force a counterexample.\n\n- Workbook: `research/communication-job-counterexample-workbook.json`\n- Browser form: `writeups/communication-job-counterexample-workbook.html`\n- Validator: `scripts/validate_communication_job_counterexample_review.py`\n\nThis review does not establish delivery effectiveness, speaker intent, audience outcomes, causality or universal best practice.\n""")
    print(f"wrote counterexample workbook and views ({len(items)} slots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
