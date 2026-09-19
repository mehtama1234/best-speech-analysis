#!/usr/bin/env python3
"""Validate one completed listener-stimulus review export."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"


def validate(record: dict, workbook: dict | None = None) -> list[str]:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    errors = []
    if record.get("record_type") != "listener_stimulus_independent_review": errors.append("record_type is invalid")
    if record.get("workbook_id") != workbook["workbook_id"]: errors.append("workbook_id does not match")
    responses = record.get("responses", {})
    for key in ("reviewer_name", "reviewer_role", "review_date", "review_modality", "conflict_statement"):
        if not str(responses.get(key, "")).strip(): errors.append(f"missing reviewer field: {key}")
    if responses.get("independent_attestation") is not True: errors.append("independent_attestation must be true")
    for n, _item in enumerate(workbook["items"], 1):
        for key, allowed in workbook["decision_vocabulary"].items():
            if responses.get(f"item_{n}_{key}") not in allowed: errors.append(f"item_{n}_{key} has invalid value")
        for key in ("reviewer_code", "rationale_and_revision"):
            if not str(responses.get(f"item_{n}_{key}", "")).strip(): errors.append(f"missing item_{n}_{key}")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid listener stimulus review:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("listener stimulus review valid: completeness only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
