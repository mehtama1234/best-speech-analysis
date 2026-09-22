#!/usr/bin/env python3
"""Validate a communication-job listener record with controlled outcome scores."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/communication-job-listener-outcome-protocol.json"


def validate(record: dict, protocol: dict | None = None, *, allow_unlocked_synthetic: bool = False) -> list[str]:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    errors = []
    if not protocol.get("stimulus_pairs_locked") and not allow_unlocked_synthetic:
        errors.append("listener outcome records are blocked until stimulus pairs are independently locked")
    if record.get("record_type") != "communication_job_listener_outcome_observation": errors.append("record_type is invalid")
    if record.get("protocol_id") != protocol["protocol_id"]: errors.append("protocol_id does not match")
    responses = record.get("responses", {})
    for key in ("participant_code", "date", "protocol_version", "modality", "stimulus_id", "condition", "scorer_id_or_blind_code"):
        if not str(responses.get(key, "")).strip(): errors.append(f"missing required field: {key}")
    if responses.get("consent") is not True: errors.append("consent must be true")
    if responses.get("condition") not in protocol["record_schema"]["condition_values"]: errors.append("condition is invalid")
    task_responses = {key[5:]: value for key, value in responses.items() if key.startswith("task_")}
    for task in protocol["listener_tasks"]:
        if not str(task_responses.get(task["task_id"], "")).strip(): errors.append(f"missing task response: {task['task_id']}")
        score_key = f"score_{task['task_id']}"
        score = responses.get(score_key, "__missing__")
        if score == "__missing__": errors.append(f"missing task score: {task['task_id']}")
        elif score not in protocol["record_schema"]["score_values"]:
            errors.append(f"invalid task score: {task['task_id']}")
    if responses.get("accessibility_issue") not in protocol["record_schema"]["accessibility_issue_values"]:
        errors.append("accessibility_issue must be yes or no")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid communication-job listener record:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("communication-job listener record valid: local outcome schema only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
