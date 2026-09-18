#!/usr/bin/env python3
"""Summarize a validated independent review without promoting any pattern."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.validate_vertical_slice_review_record import validate


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/vertical-slice-01-independent-review-workbook.json"


def summarize(record: dict, workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    validation = validate(record, workbook)
    if validation["status"] != "valid":
        raise ValueError(json.dumps(validation, ensure_ascii=False))
    responses = record["responses"]
    by_pattern = defaultdict(lambda: {"item_count": 0, "boundary": Counter(), "pattern_decision": Counter(), "speech_function": Counter(), "safety": Counter()})
    by_role = defaultdict(Counter)
    for index, item in enumerate(workbook["items"], 1):
        prefix = f"item_{index}_"
        summary = by_pattern[item["pattern_id"]]
        summary["item_count"] += 1
        summary["boundary"][responses[prefix + "boundary"]] += 1
        summary["pattern_decision"][responses[prefix + "pattern_decision"]] += 1
        summary["speech_function"][responses[prefix + "speech-function"]] += 1
        summary["safety"][responses[prefix + "safety_decision"]] += 1
        by_role[item["role"]][responses[prefix + "pattern_decision"]] += 1

    def plain(value):
        if isinstance(value, Counter):
            return dict(sorted(value.items()))
        if isinstance(value, dict):
            return {key: plain(val) for key, val in value.items()}
        return value

    return {
        "schema_version": "1.0",
        "record_type": "independent_review_summary",
        "workbook_id": workbook["workbook_id"],
        "status": "review_received_not_promotion_evidence",
        "reviewer_code": responses["reviewer_name"],
        "review_date": responses["review_date"],
        "item_count": len(workbook["items"]),
        "by_pattern": plain(dict(by_pattern)),
        "by_role": plain(dict(by_role)),
        "promotion_eligible": False,
        "claim_boundary": "This is a descriptive review summary. It does not resolve truth, establish inter-rater reliability, prove teachability, or establish listener outcomes.",
        "next_step": "Adjudicate disagreements, verify speaker/event identity and visual alignment, then combine with the learner protocol before any promotion decision.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(json.loads(args.input.read_text()))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
