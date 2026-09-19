#!/usr/bin/env python3
"""Validate an exported delivery-observation record without promoting it to evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"


def validate(record: dict, queue: dict | None = None) -> list[str]:
    queue = queue or json.loads(QUEUE.read_text())
    errors = []
    schema = queue["review_schema"]
    if record.get("record_type") != schema["record_type"]:
        errors.append("record_type is invalid")
    if record.get("sampling_id") != queue["sampling_id"]:
        errors.append("sampling_id does not match queue")
    if "manual delivery observation" not in str(record.get("claim_boundary", "")).lower():
        errors.append("claim_boundary must preserve the manual-observation boundary")
    responses = record.get("responses", {})
    for field in schema["required_session_fields"]:
        if not str(responses.get(field, "")).strip():
            errors.append(f"missing required session field: {field}")
    for number in range(1, queue["item_count"] + 1):
        for field in schema["required_item_fields"]:
            key = f"item_{number}_{field}"
            if not str(responses.get(key, "")).strip():
                errors.append(f"missing required item field: {key}")
        alignment = responses.get(f"item_{number}_transcript_alignment")
        if alignment not in schema["transcript_alignment_values"]:
            errors.append(f"invalid transcript alignment: item_{number}")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid communication-job delivery review:\n" + "\n".join(f"- {error}" for error in errors[:40]))
        return 1
    print("communication-job delivery review valid: bounded observation record only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
