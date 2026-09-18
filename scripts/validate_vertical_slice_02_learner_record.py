#!/usr/bin/env python3
"""Validate an exported slice-02 learner observation without scoring outcomes."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate(path: Path) -> list[str]:
    record = json.loads(path.read_text())
    errors = []
    responses = record.get("responses", {})
    if record.get("record_type") != "learner_observation":
        errors.append("record_type must be learner_observation")
    if record.get("protocol_id") != "vertical-slice-02-learner-check":
        errors.append("protocol_id must identify vertical slice 02")
    if not record.get("claim_boundary"):
        errors.append("claim_boundary is required")
    for key in ("participant_code", "date", "lesson_version"):
        if not str(responses.get(key, "")).strip():
            errors.append(f"responses.{key} is required")
    if responses.get("consent") is not True:
        errors.append("responses.consent must be true")
    task_ids = json.loads((ROOT / "research/vertical-slice-02-learner-task-bank.json").read_text())["tasks"]
    expected = [task["task_id"] for task in task_ids]
    if record.get("task_bank_ids") != expected:
        errors.append("task_bank_ids does not match the fixed task bank")
    for task_number in range(1, 4):
        prefix = f"p{task_number}_"
        for key, value in responses.items():
            if key.startswith(prefix) and key.endswith(("_listener_restatement", "_revision", "_boundary_note")):
                if not str(value).strip():
                    errors.append(f"{key} is required")
    grouped = {}
    for task in task_ids:
        grouped.setdefault(task["pattern_id"], []).append(task["task_id"])
    for number, ids in enumerate(grouped.values(), 1):
        supplied = responses.get(f"p{number}_task_bank_ids", "").split(",")
        if supplied != ids:
            errors.append(f"p{number}_task_bank_ids does not match fixed grouping")
        for task_id in ids:
            if not str(responses.get(f"p{number}_{task_id}", "")).strip():
                errors.append(f"p{number}_{task_id} is required")
    return errors


def main(argv: list[str] | None = None) -> int:
    path = Path((argv or sys.argv[1:])[0])
    errors = validate(path)
    if errors:
        print("invalid learner record:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("vertical slice 02 learner record valid: teachability record only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
