#!/usr/bin/env python3
"""Build a blank independent-review workbook for second-slice draft packets."""

from __future__ import annotations

import json
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKETS = ["question", "definition", "call-to-action"]
OUT_JSON = ROOT / "research/vertical-slice-02-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/vertical-slice-02-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/vertical-slice-02-independent-review-workbook.html"


def build() -> dict:
    items = []
    for name in PACKETS:
        packet = json.loads((ROOT / f"research/vertical-slice-02-{name}-draft.json").read_text())
        for role, group in (("representative", "representative_examples"), ("counterexample", "counterexamples")):
            for item in packet[group]:
                items.append({
                    "review_item_id": f"{name}:{item['evidence_id']}:{role}",
                    "packet": f"research/vertical-slice-02-{name}-draft.json",
                    "pattern_id": packet["pattern_id"],
                    "role": role,
                    "evidence_id": item["evidence_id"],
                    "video_id": item["video_id"],
                    "text": item.get("text"),
                    "start_seconds": item.get("start_seconds"),
                    "end_seconds": item.get("end_seconds"),
                    "url": item.get("url"),
                    "review": {
                        "boundary": None,
                        "speech_function": None,
                        "pattern_decision": None,
                        "audio_visual_alignment": None,
                        "alternative_explanation": None,
                        "safety_decision": None,
                        "reason": None,
                        "disagreement": None,
                        "new_counterexample_requested": None,
                    },
                })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "vertical-slice-02-independent-review-workbook",
        "status": "template_not_completed",
        "independence_requirement": "Reviewer must not be the draft packet creator or original interpreter.",
        "claim_boundary": "A completed review evaluates evidence boundaries and interpretations; it does not establish listener outcomes or causal communication effects.",
        "reviewer": {"name": None, "role": None, "date": None, "modality": None, "conflict_statement": None},
        "decision_vocabulary": {
            "boundary": ["correct", "needs_revision", "indeterminate"],
            "pattern_decision": ["supported", "unsupported", "indeterminate"],
            "safety_decision": ["safe_as_written", "needs_boundary", "unsafe"],
        },
        "required_packet_checks": [
            "question or definition/action function",
            "counterexample adequacy",
            "speaker/event independence claim",
            "audio/video alignment wording",
            "alternative explanations",
            "accessibility and safety boundary",
        ],
        "item_count": len(items),
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vertical slice 02 independent-review workbook",
        "",
        "Status: **template not completed**. This workbook contains no reviewer judgments.",
        "",
        "The reviewer must be independent of draft creation and must record identity,",
        "date, modality, conflicts, per-item decisions, reasons and disagreements.",
        "`indeterminate` is a valid decision.",
        "",
        f"Items: **{len(items)}** across three candidate packets.",
        "",
        "| # | Candidate | Role | Evidence ID | Text | Boundary | Pattern decision | Safety | Reason/disagreement |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for i, item in enumerate(items, 1):
        text = " ".join((item.get("text") or "").split()).replace("|", "\\|")
        if len(text) > 110:
            text = text[:107] + "..."
        lines.append(f"| {i} | `{item['pattern_id']}` | {item['role']} | `{item['evidence_id']}` | {text} |  |  |  |  |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fields = []
    for i, item in enumerate(items, 1):
        evidence = html.escape(item.get("text") or "")
        timing = "" if item.get("start_seconds") is None else f"<br>Time: {item['start_seconds']}–{item.get('end_seconds', '')}s"
        link = "" if not item.get("url") else f'<br><a href="{html.escape(item["url"], quote=True)}" target="_blank" rel="noopener">Open source</a>'
        fields.append(f'''<fieldset><legend>{i}. {html.escape(item['pattern_id'])} — {item['role']}</legend>
<p><strong>{html.escape(item['evidence_id'])}</strong>{timing}{link}<br>{evidence}</p>
<label>Boundary <select required name="item_{i}_boundary"><option value="">Choose</option><option>correct</option><option>needs_revision</option><option>indeterminate</option></select></label>
<label>Pattern decision <select required name="item_{i}_pattern"><option value="">Choose</option><option>supported</option><option>unsupported</option><option>indeterminate</option></select></label>
<label>Audio/visual alignment <select required name="item_{i}_alignment"><option value="">Choose</option><option>supported</option><option>needs_revision</option><option>indeterminate</option></select></label>
<label>Safety <select required name="item_{i}_safety"><option value="">Choose</option><option>safe_as_written</option><option>needs_boundary</option><option>unsafe</option></select></label>
<label>Alternative explanation<textarea required name="item_{i}_alternative" rows="2"></textarea></label>
<label>Reason/disagreement<textarea required name="item_{i}_reason" rows="2"></textarea></label>
<label>New counterexample requested<textarea name="item_{i}_counterexample" rows="2"></textarea></label></fieldset>''')
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vertical slice 02 independent review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style></head><body><h1>Vertical slice 02 independent review</h1><div class="notice"><strong>Independence:</strong> use only if you did not create the draft packets. Indeterminate is valid; this is evidence review, not listener-outcome evidence.</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code <input required name="reviewer_name"></label><label>Role <input required name="reviewer_role"></label><label>Date <input required type="date" name="review_date"></label><label>Modality <input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of draft creation.</label></fieldset>{''.join(fields)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'independent_review',workbook_id:'vertical-slice-02-independent-review-workbook',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='vertical-slice-02-review.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} ({len(items)} items)")
    return workbook


if __name__ == "__main__":
    build()
