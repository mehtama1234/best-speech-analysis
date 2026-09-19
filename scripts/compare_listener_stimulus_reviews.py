#!/usr/bin/env python3
"""Compare two or more stimulus reviews while preserving disagreements."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_listener_stimulus_review import validate

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"
FIELDS = ("proposition_equivalence", "readability_match", "target_isolation", "accessibility", "safety", "condition_order_or_blinding", "lock_decision")


def compare(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent stimulus reviews are required")
    errors = [error for record in records for error in validate(record, workbook)]
    if errors:
        raise ValueError("invalid stimulus review: " + "; ".join(errors[:8]))
    reviewer_codes = [record["responses"]["reviewer_name"] for record in records]
    if len(set(reviewer_codes)) != len(reviewer_codes):
        raise ValueError("reviewer codes must be distinct")
    counts = Counter()
    agreements = Counter()
    disagreements = []
    for number, item in enumerate(workbook["items"], 1):
        prefix = f"item_{number}_"
        item_disagreements = {}
        for field in FIELDS:
            values = [record["responses"][prefix + field] for record in records]
            counts[field] += 1
            if len(set(values)) == 1:
                agreements[field] += 1
            else:
                item_disagreements[field] = values
        if item_disagreements:
            disagreements.append({"review_item_id": item["review_item_id"], "stimulus_id": item["stimulus_id"], "canonical_job": item["canonical_job"], "disagreements": item_disagreements})
    agreement = {field: {"items": counts[field], "unanimous_items": agreements[field], "unanimous_fraction": round(agreements[field] / counts[field], 4)} for field in FIELDS}
    return {
        "schema_version": "1.0",
        "record_type": "listener_stimulus_review_agreement_report",
        "workbook_id": workbook["workbook_id"],
        "status": "agreement_report_not_lock_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": len(workbook["items"]),
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "lock_recommendation": "requires_adjudicator_and_accessibility_safety_check",
        "claim_boundary": "Agreement describes reviewer consistency only; it does not establish stimulus equivalence, listener understanding, communication effectiveness or causal outcomes. No pair is locked by this report.",
        "next_step": "An adjudicator must inspect source text, disagreements and accessibility/safety notes, record a rationale, then explicitly decide whether each pair is locked, revised or excluded.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare([json.loads(path.read_text()) for path in args.inputs])
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
