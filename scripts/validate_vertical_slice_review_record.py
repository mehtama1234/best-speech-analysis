#!/usr/bin/env python3
"""Validate an exported independent-review record without judging its content."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/vertical-slice-01-independent-review-workbook.json"

BOUNDARY = {"correct", "needs_revision", "indeterminate"}
PATTERN = {"supported", "unsupported", "indeterminate"}
SPEECH_FUNCTION = {"plausible", "needs_revision", "indeterminate"}
SAFETY = {"safe_as_written", "needs_boundary", "unsafe"}


def validate(record: dict, workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    errors: list[str] = []
    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if record.get("record_type") != "independent_review":
        errors.append("record_type must be independent_review")
    if record.get("workbook_id") != workbook["workbook_id"]:
        errors.append("workbook_id does not match the current workbook")
    if "listener outcomes" in str(record.get("claim_boundary", "")).lower() and "not" not in str(record.get("claim_boundary", "")).lower():
        errors.append("claim_boundary must exclude listener-outcome claims")

    responses = record.get("responses")
    if not isinstance(responses, dict):
        errors.append("responses must be an object")
        responses = {}
    required_reviewer = ["reviewer_name", "reviewer_role", "review_date", "review_modality", "conflict_statement"]
    for key in required_reviewer:
        if not str(responses.get(key, "")).strip():
            errors.append(f"missing reviewer field: {key}")
    if responses.get("independent_attestation") is not True:
        errors.append("independent_attestation must be true")

    items = workbook.get("items", [])
    if len(items) != workbook.get("item_count"):
        errors.append("workbook item_count is inconsistent")
    for index, _item in enumerate(items, 1):
        prefix = f"item_{index}_"
        required = {
            "boundary": BOUNDARY,
            "pattern_decision": PATTERN,
            "speech-function": SPEECH_FUNCTION,
            "safety_decision": SAFETY,
        }
        for suffix, allowed in required.items():
            value = responses.get(prefix + suffix)
            if value not in allowed:
                errors.append(f"{prefix}{suffix} must be one of {sorted(allowed)}")
        for suffix in ("audio_proxy", "alternative", "reason"):
            if not str(responses.get(prefix + suffix, "")).strip():
                errors.append(f"missing {prefix}{suffix}")

    return {
        "schema_version": "1.0",
        "record_type": "independent_review_validation",
        "workbook_id": workbook["workbook_id"],
        "status": "valid" if not errors else "invalid",
        "item_count": len(items),
        "validated_item_count": len(items) if not errors else 0,
        "errors": errors,
        "claim_boundary": "Validation checks completeness and vocabulary only; it does not endorse reviewer judgments or establish outcomes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.input.read_text()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
