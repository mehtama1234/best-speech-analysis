#!/usr/bin/env python3
"""Validate a local expanded-pattern practice export."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = json.loads((ROOT / "research/expanded-pattern-candidate-cards.json").read_text())["cards"]
CARDS_BY_ID = {card["card_id"]: card for card in CARDS}


def validate(record: dict) -> list[str]:
    errors = []
    required = ["record_type", "schema_version", "pattern_ids", "source_evidence_ids", "step_responses", "claim_boundary", "saved_at"]
    for field in required:
        if field not in record:
            errors.append(f"missing field: {field}")
    if record.get("record_type") != "local_expanded_pattern_practice_record":
        errors.append("record_type is invalid")
    if record.get("schema_version") != "1.0":
        errors.append("schema_version is invalid")
    pattern_ids = record.get("pattern_ids")
    if not isinstance(pattern_ids, list) or not pattern_ids:
        errors.append("pattern_ids must be a non-empty list")
        pattern_ids = []
    unknown = sorted(set(pattern_ids) - set(CARDS_BY_ID))
    if unknown:
        errors.append("unknown pattern_ids: " + ", ".join(unknown))
    evidence = record.get("source_evidence_ids")
    if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
        errors.append("source_evidence_ids must be a list of non-empty strings")
        evidence = []
    valid_evidence = {eid for pid in pattern_ids if pid in CARDS_BY_ID for eid in CARDS_BY_ID[pid]["evidence_ids"]}
    invalid_evidence = sorted(set(evidence) - valid_evidence)
    if invalid_evidence:
        errors.append("evidence not linked to selected patterns: " + ", ".join(invalid_evidence))
    responses = record.get("step_responses")
    if not isinstance(responses, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in responses.items()):
        errors.append("step_responses must map text keys to text values")
    boundary = str(record.get("claim_boundary", "")).lower()
    if "not" not in boundary or "effectiveness" not in boundary:
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    try:
        datetime.fromisoformat(str(record.get("saved_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("saved_at must be ISO-8601")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_expanded_pattern_practice_record.py PATH", file=sys.stderr)
        return 2
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid expanded pattern practice record:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("expanded pattern practice record valid: selected patterns, evidence links and claim boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
