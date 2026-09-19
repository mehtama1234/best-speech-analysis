#!/usr/bin/env python3
"""Validate completeness of a browser-exported blinded review response."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads((ROOT / "research/blinded-review-packet.json").read_text())
ITEM_COUNT = sum(gate["item_count"] for gate in PACKET["gates"].values())
REQUIRED_METADATA = {"reviewer_code", "reviewer_role", "review_date", "conflict_statement", "independent_attestation"}
REQUIRED_FIELDS = {"decision", "primary_function", "alternate", "reason", "identity_note"}


def validate(record: dict) -> list[str]:
    errors = []
    if record.get("record_type") != "blinded_transcript_review":
        errors.append("record_type is invalid")
    if record.get("packet_id") != "blinded-corpus-transcript-review":
        errors.append("packet_id is invalid")
    if "not" not in str(record.get("claim_boundary", "")).lower():
        errors.append("claim_boundary is missing")
    responses = record.get("responses")
    if not isinstance(responses, dict):
        return errors + ["responses must be an object"]
    missing_meta = sorted(REQUIRED_METADATA - responses.keys())
    errors.extend(f"missing reviewer field: {field}" for field in missing_meta)
    if responses.get("independent_attestation") is not True:
        errors.append("independent_attestation must be true")
    for number in range(1, ITEM_COUNT + 1):
        prefix = f"item_{number}_"
        missing = sorted(prefix + field for field in REQUIRED_FIELDS if prefix + field not in responses)
        errors.extend(f"missing response field: {field}" for field in missing)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_blinded_review_export.py PATH", file=sys.stderr)
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid blinded review export:\n" + "\n".join(f"- {error}" for error in errors[:30]))
        if len(errors) > 30:
            print(f"- ... {len(errors) - 30} more errors")
        return 1
    print(f"blinded review export valid: {ITEM_COUNT} item responses; completeness only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
