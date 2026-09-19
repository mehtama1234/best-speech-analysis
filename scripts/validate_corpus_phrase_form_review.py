#!/usr/bin/env python3
"""Validate one completed exact phrase-form independent review export."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/corpus-phrase-form-independent-review-workbook.json"


def validate(record: dict, workbook: dict | None = None) -> list[str]:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    vocab = workbook["decision_vocabulary"]
    errors = []
    if record.get("record_type") != "corpus_phrase_form_independent_review": errors.append("record_type is invalid")
    if record.get("workbook_id") != workbook["workbook_id"]: errors.append("workbook_id does not match")
    if "phrase" not in str(record.get("claim_boundary", "")).lower() or "outcome" not in str(record.get("claim_boundary", "")).lower(): errors.append("claim_boundary must preserve the phrase-form-only and non-outcome boundary")
    responses = record.get("responses", {})
    for key in ("reviewer_name", "reviewer_role", "review_date", "review_modality", "conflict_statement"):
        if not str(responses.get(key, "")).strip(): errors.append(f"missing reviewer field: {key}")
    if responses.get("independent_attestation") is not True: errors.append("independent_attestation must be true")
    for number, _item in enumerate(workbook["items"], 1):
        for key, allowed in vocab.items():
            if responses.get(f"item_{number}_{key}") not in allowed: errors.append(f"item_{number}_{key} has invalid value")
        for key in ("alternate_function", "reason"):
            if not str(responses.get(f"item_{number}_{key}", "")).strip(): errors.append(f"missing item_{number}_{key}")
    return errors


def main() -> int:
    errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    if errors:
        print("invalid phrase-form review:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("phrase-form review valid: completeness only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
