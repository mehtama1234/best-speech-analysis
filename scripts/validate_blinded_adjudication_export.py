#!/usr/bin/env python3
"""Validate completeness of an adjudicator's blinded-review export."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "research/blinded-review-packet.json").read_text())
ITEM_COUNT = sum(gate["item_count"] for gate in PACKET["gates"].values())
DECISIONS = {"retain", "revise", "reject", "indeterminate"}


def validate(record: dict) -> list[str]:
    errors = []
    if record.get("record_type") != "blinded_review_adjudication":
        errors.append("record_type is invalid")
    if "not" not in str(record.get("claim_boundary", "")).lower() or "effect" not in str(record.get("claim_boundary", "")).lower():
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    responses = record.get("responses")
    if not isinstance(responses, dict):
        return errors + ["responses must be an object"]
    for field in ("adjudicator_code", "adjudicator_role", "adjudication_date", "conflict_statement"):
        if not isinstance(responses.get(field), str) or not responses[field].strip():
            errors.append(f"missing adjudicator field: {field}")
    for number in range(1, ITEM_COUNT + 1):
        decision = responses.get(f"item_{number}_final_decision")
        if decision not in DECISIONS:
            errors.append(f"item {number} has invalid or missing final decision")
        for field in ("rationale", "safety_note"):
            if not isinstance(responses.get(f"item_{number}_{field}"), str) or not responses[f"item_{number}_{field}"].strip():
                errors.append(f"item {number} has missing {field}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_blinded_adjudication_export.py PATH", file=sys.stderr)
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid adjudication export:\n" + "\n".join(f"- {error}" for error in errors[:30]))
        if len(errors) > 30:
            print(f"- ... {len(errors) - 30} more errors")
        return 1
    print(f"adjudication export valid: {ITEM_COUNT} decisions; format only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
