#!/usr/bin/env python3
"""Build a blank independent-review workbook for both bounded media reviews."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "research/multimodal-expansion-manual-review.json",
    ROOT / "research/multimodal-expansion-manual-review-02.json",
]
OUT_JSON = ROOT / "research/multimodal-independent-review-workbook.json"
OUT_MD = ROOT / "writeups/multimodal-independent-review-workbook.md"
OUT_HTML = ROOT / "writeups/multimodal-independent-review-workbook.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    items = []
    for source_path in SOURCES:
        source = json.loads(source_path.read_text())
        for item in source["items"]:
            items.append({
                "review_item_id": f"{item['video_id']}:{item['evidence_id']}:{item['pattern_id']}",
                "video_id": item["video_id"],
                "title": item["title"],
                "pattern_id": item["pattern_id"],
                "evidence_id": item["evidence_id"],
                "transcript_text": item["transcript_text"],
                "sampled_time_seconds": item["sampled_time_seconds"],
                "video_source": item["video_source"],
                "audio_source": item["audio_source"],
                "source_url": f"https://www.youtube.com/watch?v={item['video_id']}",
                "internal_alignment": item["alignment_decision"],
                "internal_review_source": source_path.relative_to(ROOT).as_posix(),
                "review": {
                    "boundary_decision": None,
                    "candidate_function_decision": None,
                    "speaker_setting_decision": None,
                    "audio_visual_decision": None,
                    "safety_decision": None,
                    "alternative_explanation": None,
                    "reason": None,
                    "disagreement": None,
                    "new_counterexample": None,
                },
            })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "multimodal-independent-review-workbook",
        "status": "template_not_completed",
        "source_reviews": [path.relative_to(ROOT).as_posix() for path in SOURCES],
        "independence_requirement": "Reviewer must not be the internal review author or packet creator.",
        "claim_boundary": "A completed review evaluates alignment and interpretation boundaries; it does not establish delivery effectiveness, audience outcomes or learner outcomes.",
        "reviewer": {"name": None, "role": None, "date": None, "modality": None, "conflict_statement": None},
        "decision_vocabulary": {
            "boundary_decision": ["aligned", "partial", "not_aligned", "indeterminate"],
            "candidate_function_decision": ["supported", "unsupported", "indeterminate"],
            "speaker_setting_decision": ["supported", "needs_revision", "indeterminate"],
            "audio_visual_decision": ["supports", "contradicts", "not_assessed", "indeterminate"],
            "safety_decision": ["safe_as_written", "needs_boundary", "unsafe"],
        },
        "item_count": len(items),
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Multimodal independent-review workbook",
        "",
        "Status: **template not completed**. This contains no independent reviewer judgments.",
        "",
        "The reviewer must inspect the local source files or source URL, retain uncertainty, and state when a frame or feature record cannot support the claim. The internal review is shown only as provenance; it is not an answer key.",
        "",
        f"Items: **{len(items)}**.",
        "",
        "| # | Video | Candidate | Evidence | Internal alignment | Independent decision | Reason |",
        "|---:|---|---|---|---|---|---|",
    ]
    for number, item in enumerate(items, 1):
        text = " ".join((item.get("transcript_text") or "").split()).replace("|", "\\|")
        lines.append(f"| {number} | `{item['video_id']}` | `{item['pattern_id']}` | `{item['evidence_id']}` | `{item['internal_alignment']}` |  | {text[:100]} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fields = []
    for number, item in enumerate(items, 1):
        fields.append(f'''<fieldset><legend>{number}. {esc(item['video_id'])} — {esc(item['pattern_id'])}</legend>
<p><strong>{esc(item['evidence_id'])}</strong> · {esc(item['sampled_time_seconds'])}s<br>{esc(item['transcript_text'])}<br><small>Internal alignment: {esc(item['internal_alignment'])}<br>Local video: {esc(item['video_source'])}<br>Local audio: {esc(item['audio_source'])}<br><a href="{esc(item['source_url'])}" target="_blank" rel="noopener">Open source URL</a></small></p>
<label>Caption/frame boundary <select required name="item_{number}_boundary_decision"><option value="">Choose</option><option>aligned</option><option>partial</option><option>not_aligned</option><option>indeterminate</option></select></label>
<label>Candidate function <select required name="item_{number}_candidate_function_decision"><option value="">Choose</option><option>supported</option><option>unsupported</option><option>indeterminate</option></select></label>
<label>Speaker/setting observation <select required name="item_{number}_speaker_setting_decision"><option value="">Choose</option><option>supported</option><option>needs_revision</option><option>indeterminate</option></select></label>
<label>Audio/visual evidence <select required name="item_{number}_audio_visual_decision"><option value="">Choose</option><option>supports</option><option>contradicts</option><option>not_assessed</option><option>indeterminate</option></select></label>
<label>Safety <select required name="item_{number}_safety_decision"><option value="">Choose</option><option>safe_as_written</option><option>needs_boundary</option><option>unsafe</option></select></label>
<label>Alternative explanation<textarea required name="item_{number}_alternative_explanation" rows="2"></textarea></label>
<label>Reason<textarea required name="item_{number}_reason" rows="2"></textarea></label>
<label>Disagreement with internal review<textarea name="item_{number}_disagreement" rows="2"></textarea></label>
<label>New counterexample requested<textarea name="item_{number}_new_counterexample" rows="2"></textarea></label></fieldset>''')
    html_doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Multimodal independent review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}button{{padding:.6rem 1rem}}</style></head><body><h1>Multimodal independent review</h1><div class="notice"><strong>Independence:</strong> use only if you did not create the internal review. Indeterminate and not_assessed are valid. This evaluates evidence boundaries, not communication effectiveness.</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code <input required name="reviewer_name"></label><label>Role <input required name="reviewer_role"></label><label>Date <input required type="date" name="review_date"></label><label>Modality <input required name="review_modality"></label><label>Conflict statement<textarea required name="conflict_statement"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of the internal review and draft interpretation.</label></fieldset>{''.join(fields)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'independent_review',workbook_id:'multimodal-independent-review-workbook',claim_boundary:'Validation of evidence boundaries only; not delivery effectiveness or audience outcomes.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='multimodal-independent-review.json';a.click();URL.revokeObjectURL(u)}};</script></body></html>'''
    OUT_HTML.write_text(html_doc)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
