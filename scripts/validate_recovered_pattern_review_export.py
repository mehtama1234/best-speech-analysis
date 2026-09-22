#!/usr/bin/env python3
"""Validate a recovered-pattern independent-review browser export."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "research/recovered-pattern-independent-review-workbook.json").read_text())
ITEM_IDS = {item["blind_item_id"] for item in PACKET["items"]}
DECISIONS = {
    "supports_candidate",
    "alternate_function",
    "not_enough_context",
    "indeterminate",
    "identity_mismatch",
    "duplicate_or_compilation",
}
REQUIRED_REVIEW_FIELDS = {
    "decision",
    "primary_function",
    "alternate_explanation",
    "context_note",
    "identity_note",
    "uncertainty_note",
}


def validate(record: dict) -> list[str]:
    errors = []
    if record.get("record_type") != "recovered_pattern_independent_review":
        errors.append("record_type is invalid")
    if record.get("workbook_id") != "recovered-pattern-independent-review":
        errors.append("workbook_id is invalid")
    boundary = str(record.get("claim_boundary", "")).lower()
    if "not effectiveness" not in boundary:
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict):
        return errors + ["reviewer must be an object"]
    for field in ("reviewer_code", "reviewer_role", "review_date", "conflict_statement"):
        if not isinstance(reviewer.get(field), str) or not reviewer[field].strip():
            errors.append(f"missing reviewer field: {field}")
    if reviewer.get("independent_attestation") is not True:
        errors.append("independent_attestation must be true")
    responses = record.get("responses")
    if not isinstance(responses, dict):
        return errors + ["responses must be an object"]
    response_ids = set(responses)
    errors.extend(f"missing response for {item_id}" for item_id in sorted(ITEM_IDS - response_ids))
    errors.extend(f"unknown response item {item_id}" for item_id in sorted(response_ids - ITEM_IDS))
    for item_id in sorted(ITEM_IDS & response_ids):
        response = responses[item_id]
        if not isinstance(response, dict):
            errors.append(f"response {item_id} must be an object")
            continue
        if response.get("decision") not in DECISIONS:
            errors.append(f"response {item_id} has invalid or missing decision")
        for field in sorted(REQUIRED_REVIEW_FIELDS - {"decision"}):
            if not isinstance(response.get(field), str) or not response[field].strip():
                errors.append(f"response {item_id} has missing {field}")
    if "pattern_id" in json.dumps(record) or "candidate_form" in json.dumps(record):
        errors.append("export must not contain internal candidate pattern labels")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_recovered_pattern_review_export.py PATH", file=sys.stderr)
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid recovered pattern review export:\n" + "\n".join(f"- {error}" for error in errors[:30]))
        if len(errors) > 30:
            print(f"- ... {len(errors) - 30} more errors")
        return 1
    print(f"recovered pattern review export valid: {len(ITEM_IDS)} item responses; completeness only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
