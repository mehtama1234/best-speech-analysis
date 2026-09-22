#!/usr/bin/env python3
"""Validate a priority review export while preserving omitted and partial responses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "research/recovered-pattern-priority-review.json").read_text())
ITEM_IDS = {item["blind_item_id"] for item in PACKET["items"]}
DECISIONS = {"supports_candidate", "alternate_function", "not_enough_context", "indeterminate", "identity_mismatch", "duplicate_or_compilation"}
FIELDS = {"decision", "primary_function", "alternate_explanation", "context_note", "identity_note", "uncertainty_note"}


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = []
    if record.get("record_type") != "recovered_pattern_priority_review":
        errors.append("record_type is invalid")
    if record.get("review_packet_id") != "recovered-pattern-priority-review":
        errors.append("review_packet_id is invalid")
    if "not effectiveness" not in str(record.get("claim_boundary", "")).lower():
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
    errors.extend(f"unknown response item {item_id}" for item_id in sorted(response_ids - ITEM_IDS, key=str))
    decision_count = 0
    for item_id in sorted(ITEM_IDS & response_ids):
        response = responses[item_id]
        if not isinstance(response, dict):
            errors.append(f"response {item_id} must be an object")
            continue
        decision = response.get("decision")
        valid_decision = isinstance(decision, str) and decision in DECISIONS
        if decision not in (None, ""):
            if not valid_decision:
                errors.append(f"response {item_id} has invalid decision")
            else:
                decision_count += 1
        for field in sorted(FIELDS - {"decision"}):
            if field in response and not isinstance(response[field], str):
                errors.append(f"response {item_id} has non-text {field}")
            elif valid_decision and not str(response.get(field, "")).strip():
                errors.append(f"response {item_id} has a decision but is missing {field}")
    if decision_count == 0:
        errors.append("at least one item decision is required")
    serialized = json.dumps(record, ensure_ascii=False)
    if "pattern_id" in serialized or "candidate_form" in serialized:
        errors.append("export must not contain internal candidate pattern labels")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a recovered-pattern priority review export. Partial exports are "
            "allowed; omitted item decisions remain missing and are never imputed."
        )
    )
    parser.add_argument("path", type=Path, help="reviewer export JSON file")
    args = parser.parse_args()
    try:
        record = json.loads(args.path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"cannot read review export {args.path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"invalid JSON in review export {args.path}: {exc}", file=sys.stderr)
        return 2

    errors = validate(record)
    if errors:
        print("invalid recovered pattern priority review export:\n" + "\n".join(f"- {error}" for error in errors[:30]))
        if len(errors) > 30:
            print(f"- ... {len(errors) - 30} more errors")
        return 1
    decision_count = sum(
        isinstance(response, dict)
        and isinstance(response.get("decision"), str)
        and response.get("decision") in DECISIONS
        for response in record.get("responses", {}).values()
    )
    missing_count = len(ITEM_IDS) - decision_count
    coverage = "complete" if missing_count == 0 else "partial; missingness preserved"
    print(f"recovered pattern priority review export valid: {decision_count}/{len(ITEM_IDS)} decisions; {coverage}; schema only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
