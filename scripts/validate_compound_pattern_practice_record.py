#!/usr/bin/env python3
"""Validate a local compound-pattern practice export."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = json.loads((ROOT / "research/compound-pattern-bundles.json").read_text())["bundles"]
BY_ID = {bundle["bundle_id"]: bundle for bundle in BUNDLES}


def validate(record: dict) -> list[str]:
    errors = []
    required = ["record_type", "schema_version", "bundle_id", "source_review_ids", "source_evidence_ids", "draft", "reflections", "claim_boundary", "saved_at"]
    errors.extend(f"missing field: {field}" for field in required if field not in record)
    if record.get("record_type") != "local_compound_pattern_practice_record":
        errors.append("record_type is invalid")
    if record.get("schema_version") != "1.0":
        errors.append("schema_version is invalid")
    bundle = BY_ID.get(record.get("bundle_id"))
    if bundle is None:
        errors.append("bundle_id is unknown")
    reviews = record.get("source_review_ids")
    if not isinstance(reviews, list) or not reviews or any(not isinstance(item, str) or not item for item in reviews):
        errors.append("source_review_ids must be a non-empty list of strings")
    evidence = record.get("source_evidence_ids")
    if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) or not item for item in evidence):
        errors.append("source_evidence_ids must be a non-empty list of strings")
    if bundle:
        valid_reviews = {example["review_id"] for example in bundle["examples"]}
        valid_evidence = {evidence_id for example in bundle["examples"] for evidence_id in example["left_evidence_ids"] + example["right_evidence_ids"]}
        if set(reviews or []) - valid_reviews:
            errors.append("source_review_ids contain IDs not linked to the selected bundle")
        if set(evidence or []) - valid_evidence:
            errors.append("source_evidence_ids contain IDs not linked to the selected bundle")
    if not isinstance(record.get("draft"), str) or not record["draft"].strip():
        errors.append("draft must be non-empty text")
    reflections = record.get("reflections")
    required_reflections = {"listener-restatement", "still-unclear", "non-fit", "next-revision"}
    if not isinstance(reflections, dict) or not required_reflections.issubset(reflections) or any(not isinstance(reflections.get(key), str) for key in required_reflections):
        errors.append("reflections must contain four text fields")
    boundary = str(record.get("claim_boundary", "")).lower()
    if "not" not in boundary or "effectiveness" not in boundary:
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    try:
        datetime.fromisoformat(str(record.get("saved_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("saved_at must be ISO-8601")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_compound_pattern_practice_record.py PATH", file=sys.stderr)
        raise SystemExit(2)
    problems = validate(json.loads(Path(sys.argv[1]).read_text()))
    if problems:
        print("invalid compound pattern practice record:\n" + "\n".join(f"- {problem}" for problem in problems))
        raise SystemExit(1)
    print("compound pattern practice record valid: bundle, evidence, reflections and boundary")
