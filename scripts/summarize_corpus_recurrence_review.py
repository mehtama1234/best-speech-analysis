#!/usr/bin/env python3
"""Summarize a validated recurrence review without promoting its findings."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from .validate_corpus_recurrence_review import validate
except ImportError:
    from validate_corpus_recurrence_review import validate


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/corpus-recurrence-independent-review-workbook.json"


def summarize(record: dict, workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    errors = validate(record, workbook)
    if errors:
        raise ValueError("record is not valid: " + "; ".join(errors[:5]))
    responses = record["responses"]
    grouped = defaultdict(lambda: {"item_count": 0, "event_splits": Counter(), "context": Counter(), "phrase_role": Counter(), "primary_function": Counter(), "recurrence": Counter()})
    for number, item in enumerate(workbook["items"], 1):
        group = grouped[item["phrase_family"]]
        group["item_count"] += 1
        group["event_splits"][item["event_split"]] += 1
        group["context"][responses[f"item_{number}_context_decision"]] += 1
        group["phrase_role"][responses[f"item_{number}_phrase_role_decision"]] += 1
        group["primary_function"][responses[f"item_{number}_primary_function"]] += 1
        group["recurrence"][responses[f"item_{number}_recurrence_include_decision"]] += 1
    def serialize(group: dict) -> dict:
        return {key: (dict(value) if isinstance(value, Counter) else value) for key, value in group.items()}
    return {
        "schema_version": "1.0",
        "record_type": "corpus_recurrence_review_summary",
        "status": "validated_summary_non_promotional",
        "workbook_id": workbook["workbook_id"],
        "reviewer": {key: record["responses"].get(key) for key in ("reviewer_name", "reviewer_role", "review_date", "review_modality")},
        "item_count": len(workbook["items"]),
        "by_phrase_family": {key: serialize(value) for key, value in sorted(grouped.items())},
        "claim_boundary": "This summarizes one independent transcript-function review. It does not establish phrase effectiveness, speaker intent, delivery effects, audience outcomes or universal recurrence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    workbook = json.loads(WORKBOOK.read_text())
    summary = summarize(json.loads(args.record.read_text()), workbook)
    output = args.output or ROOT / "research/corpus-recurrence-review-summary.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {output} ({summary['item_count']} items; non-promotional summary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
