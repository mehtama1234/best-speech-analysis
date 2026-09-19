#!/usr/bin/env python3
"""Validate the explicit adjudication step for listener stimulus locking."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"

DECISIONS = {"lock_for_pilot", "hold_for_revision", "exclude_pair"}
SAFETY = {"pass", "revise", "exclude"}


def validate(record: dict, workbook: dict | None = None) -> list[str]:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    errors = []
    if record.get("record_type") != "listener_stimulus_adjudication": errors.append("record_type is invalid")
    if record.get("workbook_id") != workbook["workbook_id"]: errors.append("workbook_id does not match")
    boundary = str(record.get("claim_boundary", "")).lower()
    if "lock" not in boundary or "outcome" not in boundary: errors.append("claim_boundary must preserve the lock and non-outcome boundary")
    for key in ("adjudicator_code", "adjudication_date", "review_a_code", "review_b_code", "source_review_a", "source_review_b"):
        if not str(record.get(key, "")).strip(): errors.append(f"missing adjudication field: {key}")
    if record.get("review_a_code") == record.get("review_b_code"):
        errors.append("review_a_code and review_b_code must be distinct")
    responses = record.get("responses", {})
    for number, _item in enumerate(workbook["items"], 1):
        decision = responses.get(f"item_{number}_final_decision")
        safety = responses.get(f"item_{number}_accessibility_safety")
        if decision not in DECISIONS: errors.append(f"item_{number}_final_decision is invalid")
        if safety not in SAFETY: errors.append(f"item_{number}_accessibility_safety is invalid")
        if not str(responses.get(f"item_{number}_rationale", "")).strip(): errors.append(f"item_{number}_rationale is required")
        if decision == "lock_for_pilot" and safety != "pass": errors.append(f"item_{number} cannot lock without accessibility_safety=pass")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid listener stimulus adjudication:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("listener stimulus adjudication valid: lock decision schema only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
