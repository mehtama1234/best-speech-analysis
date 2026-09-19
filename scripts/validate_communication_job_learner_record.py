#!/usr/bin/env python3
"""Validate an exported 18-card communication-job learner record."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/communication-job-learner-check.json"


def validate(record: dict, protocol: dict | None = None) -> list[str]:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    errors = []
    if record.get("record_type") != "communication_job_learner_observation": errors.append("record_type is invalid")
    if record.get("protocol_id") != protocol["protocol_id"]: errors.append("protocol_id does not match")
    if not record.get("claim_boundary"): errors.append("claim_boundary is required")
    responses = record.get("responses", {})
    for key in ("participant_code", "date", "lesson_version", "facilitator_code", "facilitator_role", "scoring_disagreement_or_uncertainty"):
        if not str(responses.get(key, "")).strip(): errors.append(f"responses.{key} is required")
    if responses.get("consent") is not True: errors.append("responses.consent must be true")
    expected = [task["task_id"] for task in protocol["tasks"]]
    if record.get("task_bank_ids") != expected: errors.append("task_bank_ids does not match fixed protocol")
    for card in protocol["cards"]:
        card_id = card["card_id"]
        ids = [task["task_id"] for task in protocol["tasks"] if task["card_id"] == card_id]
        if responses.get(f"{card_id}_task_ids", "").split(",") != ids: errors.append(f"{card_id}_task_ids does not match fixed grouping")
        for task_id in ids:
            if not str(responses.get(task_id, "")).strip(): errors.append(f"{task_id} is required")
        for suffix in ("listener_restatement", "revision", "boundary_note"):
            if not str(responses.get(f"{card_id}_{suffix}", "")).strip(): errors.append(f"{card_id}_{suffix} is required")
        for dimension in card.get("scoring_dimensions", []):
            if responses.get(f"{card_id}_score_{dimension}") not in {"0", "1", "2"}: errors.append(f"{card_id}_score_{dimension} must be 0, 1 or 2")
        if responses.get(f"{card_id}_safety_issue") not in {"yes", "no"}: errors.append(f"{card_id}_safety_issue must be yes or no")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid communication-job learner record:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("communication-job learner record valid: teachability record only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
