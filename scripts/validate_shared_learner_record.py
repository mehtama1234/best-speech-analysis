#!/usr/bin/env python3
"""Validate completeness of a shared learner observation export."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/shared-learner-check.json"


def validate(record: dict, protocol: dict | None = None) -> list[str]:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    errors = []
    if record.get("record_type") != "learner_observation": errors.append("record_type must be learner_observation")
    if record.get("protocol_id") != protocol["protocol_id"]: errors.append("protocol_id does not match shared protocol")
    if not record.get("claim_boundary"): errors.append("claim_boundary is required")
    responses = record.get("responses", {})
    for key in ("participant_code", "date", "lesson_version"):
        if not str(responses.get(key, "")).strip(): errors.append(f"responses.{key} is required")
    if responses.get("consent") is not True: errors.append("responses.consent must be true")
    expected_ids = [task["task_id"] for task in protocol["tasks"]]
    if record.get("task_bank_ids") != expected_ids: errors.append("task_bank_ids does not match shared task bank")
    grouped = {}
    for task in protocol["tasks"]: grouped.setdefault(task["pattern_id"], []).append(task["task_id"])
    for number, ids in enumerate(grouped.values(), 1):
        if responses.get(f"p{number}_task_bank_ids", "").split(",") != ids: errors.append(f"p{number}_task_bank_ids does not match fixed grouping")
        for task_id in ids:
            if not str(responses.get(f"p{number}_{task_id}", "")).strip(): errors.append(f"p{number}_{task_id} is required")
        for suffix in ("listener_restatement", "revision", "boundary_note"):
            if not str(responses.get(f"p{number}_{suffix}", "")).strip(): errors.append(f"p{number}_{suffix} is required")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid shared learner record:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("shared learner record valid: teachability record only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
