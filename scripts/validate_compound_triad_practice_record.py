#!/usr/bin/env python3
"""Validate a local practice record exported by the triad browser."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIADS = json.loads((ROOT / "research/compound-pattern-triads.json").read_text())
KNOWN = {item["triad_id"]: item for item in TRIADS["all_candidate_triads"]}


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("record_type") != "local_compound_triad_practice_record":
        errors.append("record_type must be local_compound_triad_practice_record")
    triad_id = record.get("triad_id")
    if triad_id not in KNOWN:
        errors.append("triad_id is not in the source-linked triad inventory")
    if not isinstance(record.get("source_review_ids"), list) or not record["source_review_ids"]:
        errors.append("source_review_ids must be a non-empty list")
    if not isinstance(record.get("source_evidence_ids"), list) or not record["source_evidence_ids"]:
        errors.append("source_evidence_ids must be a non-empty list")
    if not isinstance(record.get("draft"), str) or not record["draft"].strip():
        errors.append("draft must be non-empty")
    reflections = record.get("reflections")
    required = {"listener", "unclear", "nonfit", "revision"}
    if not isinstance(reflections, dict) or not required.issubset(reflections):
        errors.append("reflections must include listener, unclear, nonfit and revision")
    boundary = str(record.get("claim_boundary", ""))
    if not re.search(r"not .*effectiveness", boundary, re.IGNORECASE):
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    try:
        datetime.fromisoformat(str(record.get("saved_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("saved_at must be an ISO timestamp")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_compound_triad_practice_record.py RECORD.json")
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid compound triad practice record:\n" + "\n".join(f"- {item}" for item in errors))
        return 1
    print("compound triad practice record valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
