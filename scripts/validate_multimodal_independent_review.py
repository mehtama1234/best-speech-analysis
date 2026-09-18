#!/usr/bin/env python3
"""Validate completeness/vocabulary of a multimodal independent review export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/multimodal-independent-review-workbook.json"
VOCAB = {
    "boundary_decision": {"aligned", "partial", "not_aligned", "indeterminate"},
    "candidate_function_decision": {"supported", "unsupported", "indeterminate"},
    "speaker_setting_decision": {"supported", "needs_revision", "indeterminate"},
    "audio_visual_decision": {"supports", "contradicts", "not_assessed", "indeterminate"},
    "safety_decision": {"safe_as_written", "needs_boundary", "unsafe"},
}


def validate(record: dict, workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    errors = []
    if record.get("schema_version") != "1.0": errors.append("schema_version must be 1.0")
    if record.get("record_type") != "independent_review": errors.append("record_type must be independent_review")
    if record.get("workbook_id") != workbook["workbook_id"]: errors.append("workbook_id does not match workbook")
    if not record.get("claim_boundary"): errors.append("claim_boundary is required")
    responses = record.get("responses", {})
    for key in ("reviewer_name", "reviewer_role", "review_date", "review_modality", "conflict_statement"):
        if not str(responses.get(key, "")).strip(): errors.append(f"missing reviewer field: {key}")
    if responses.get("independent_attestation") is not True: errors.append("independent_attestation must be true")
    for number, _item in enumerate(workbook["items"], 1):
        for suffix, allowed in VOCAB.items():
            value = responses.get(f"item_{number}_{suffix}")
            if value not in allowed: errors.append(f"item_{number}_{suffix} has invalid value")
        for suffix in ("alternative_explanation", "reason"):
            if not str(responses.get(f"item_{number}_{suffix}", "")).strip(): errors.append(f"missing item_{number}_{suffix}")
    return {"schema_version": "1.0", "record_type": "independent_review_validation", "workbook_id": workbook["workbook_id"], "status": "valid" if not errors else "invalid", "item_count": len(workbook["items"]), "errors": errors, "claim_boundary": "Completeness/vocabulary validation only; does not endorse reviewer judgments."}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.input.read_text()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
