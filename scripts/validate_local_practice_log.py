#!/usr/bin/env python3
"""Validate a browser-exported local learner practice log."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "research/local-practice-log-contract.json").read_text())


def validate(record: dict) -> list[str]:
    errors = []
    for field in CONTRACT["required_log_fields"]:
        if field not in record:
            errors.append(f"missing log field: {field}")
    if record.get("record_type") != CONTRACT["record_type"]:
        errors.append("record_type is invalid")
    if not isinstance(record.get("records"), list) or not record.get("records"):
        errors.append("records must be a non-empty list")
        return errors
    boundary = str(record.get("claim_boundary", "")).lower()
    if "not" not in boundary or "effect" not in boundary:
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    for number, item in enumerate(record["records"], 1):
        for field in CONTRACT["required_record_fields"]:
            if field not in item:
                errors.append(f"record {number} missing field: {field}")
        if item.get("record_type") != "local_learner_practice":
            errors.append(f"record {number} has invalid record_type")
        if item.get("delivery_mode") not in CONTRACT["delivery_modes"]:
            errors.append(f"record {number} has invalid delivery_mode")
        if not isinstance(item.get("source_evidence_ids"), list):
            errors.append(f"record {number} source_evidence_ids must be a list")
        for field in ("card_id", "video_id", "title", "adapted_wording", "listener_restatement", "non_fit_or_safety_note", "revision"):
            if not isinstance(item.get(field), str):
                errors.append(f"record {number} field {field} must be text")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_local_practice_log.py PATH", file=sys.stderr)
        return 2
    record = json.loads(Path(sys.argv[1]).read_text())
    errors = validate(record)
    if errors:
        print("invalid local practice log:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print(f"local practice log valid: {len(record['records'])} records; format only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
