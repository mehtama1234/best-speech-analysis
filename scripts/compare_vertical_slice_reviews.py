#!/usr/bin/env python3
"""Compare validated independent-review exports without adjudicating them."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_vertical_slice_review_record import validate


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/vertical-slice-01-independent-review-workbook.json"
FIELDS = {
    "boundary": "boundary",
    "pattern_decision": "pattern_decision",
    "speech_function": "speech-function",
    "safety": "safety_decision",
}


def compare(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent review records are required")
    validations = [validate(record, workbook) for record in records]
    errors = [error for result in validations for error in result["errors"]]
    if errors:
        raise ValueError("invalid review record: " + "; ".join(errors[:8]))
    reviewer_codes = [record["responses"]["reviewer_name"] for record in records]
    if len(set(reviewer_codes)) != len(reviewer_codes):
        raise ValueError("reviewer codes must be distinct")

    field_counts = Counter()
    field_agreements = Counter()
    disagreements = []
    for index, item in enumerate(workbook["items"], 1):
        prefix = f"item_{index}_"
        item_values = {}
        for label, suffix in FIELDS.items():
            values = [record["responses"][prefix + suffix] for record in records]
            field_counts[label] += 1
            if len(set(values)) == 1:
                field_agreements[label] += 1
            else:
                item_values[label] = values
        if item_values:
            disagreements.append({
                "review_item_id": item["review_item_id"],
                "evidence_id": item["evidence_id"],
                "pattern_id": item["pattern_id"],
                "disagreements": item_values,
            })

    agreement = {
        label: {
            "items": field_counts[label],
            "unanimous_items": field_agreements[label],
            "unanimous_fraction": round(field_agreements[label] / field_counts[label], 4),
        }
        for label in FIELDS
    }
    return {
        "schema_version": "1.0",
        "record_type": "independent_review_agreement_report",
        "workbook_id": workbook["workbook_id"],
        "status": "agreement_report_not_promotion_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": len(workbook["items"]),
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "claim_boundary": "Agreement describes reviewer consistency only; it does not establish truth, reliability beyond this sample, teachability or listener outcomes.",
        "next_step": "Adjudicate disagreements with evidence and record the adjudicator’s rationale before updating any packet status.",
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
