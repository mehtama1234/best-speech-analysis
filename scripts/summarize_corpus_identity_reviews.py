#!/usr/bin/env python3
"""Summarize validated identity reviews without promoting metadata to recurrence evidence."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_corpus_identity_review import validate

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/corpus-identity-review-workbook.json"


def summarize(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if not records:
        raise ValueError("at least one identity review export is required")
    for record in records:
        errors = validate(record, workbook)
        if errors:
            raise ValueError("invalid identity review: " + "; ".join(errors[:8]))
    distributions = {}
    for key, allowed in workbook["decision_vocabulary"].items():
        distributions[key] = {value: 0 for value in allowed}
        for record in records:
            responses = record["responses"]
            for number in range(1, workbook["item_count"] + 1):
                distributions[key][responses[f"item_{number}_{key}"]] += 1
    return {
        "schema_version": "1.0",
        "record_type": "corpus_identity_review_summary",
        "status": "validated_identity_summary_non_promotional",
        "workbook_id": workbook["workbook_id"],
        "record_count": len(records),
        "reviewed_item_count_per_export": workbook["item_count"],
        "decision_distributions": distributions,
        "promotion_eligible": False,
        "claim_boundary": "This summarizes independent identity, event, upload correspondence, duplication and provenance decisions. It does not by itself establish independent recurrence, delivery meaning, effectiveness or audience outcomes.",
        "next_step": "Preserve disagreements and adjudicate identity/event conflicts before using cross-talk comparisons as recurrence evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize([json.loads(path.read_text()) for path in args.records])
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
