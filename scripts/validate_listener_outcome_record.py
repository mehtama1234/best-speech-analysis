#!/usr/bin/env python3
"""Validate a listener-outcome record without scoring or endorsing results."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/listener-outcome-protocol.json"


def validate(record: dict, protocol: dict | None = None) -> list[str]:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    errors = []
    if record.get("record_type") != "listener_outcome_observation": errors.append("record_type must be listener_outcome_observation")
    if record.get("protocol_id") != protocol["protocol_id"]: errors.append("protocol_id does not match")
    responses = record.get("responses", {})
    for key in ("participant_code", "date", "protocol_version", "modality", "stimulus_id", "condition", "scorer_id_or_blind_code"):
        if not str(responses.get(key, "")).strip(): errors.append(f"missing required field: {key}")
    if responses.get("consent") is not True: errors.append("consent must be true")
    if responses.get("condition") not in protocol["record_schema"]["condition_values"]: errors.append("condition is invalid")
    if not isinstance(responses.get("task_responses"), dict): errors.append("task_responses must be an object")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid listener outcome record:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("listener outcome record valid: schema only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
