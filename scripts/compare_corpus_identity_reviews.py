#!/usr/bin/env python3
"""Compare independent identity reviews while preserving item-level disagreements."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_corpus_identity_review import validate

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/corpus-identity-review-workbook.json"
FIELDS = ("speaker_identity", "event_identity", "upload_event_match", "duplicate_or_compilation_status", "source_provenance_status")


def compare(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent identity reviews are required")
    errors = [error for record in records for error in validate(record, workbook)]
    if errors:
        raise ValueError("invalid identity review: " + "; ".join(errors[:8]))
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
            disagreements.append({"review_item_id": item["review_item_id"], "video_id": item["video_id"], "title": item["title"], "disagreements": item_disagreements})
    agreement = {field: {"items": counts[field], "unanimous_items": agreements[field], "unanimous_fraction": round(agreements[field] / counts[field], 4)} for field in FIELDS}
    return {
        "schema_version": "1.0",
        "record_type": "corpus_identity_review_agreement_report",
        "workbook_id": workbook["workbook_id"],
        "status": "agreement_report_not_identity_or_recurrence_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": workbook["item_count"],
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "recurrence_eligibility": "not_decided",
        "adjudication_recommendation": "requires_adjudicator_before_using_identity_decisions_for_recurrence",
        "claim_boundary": "Agreement describes reviewer consistency about source identity and duplication only. It does not establish independent recurrence, delivery meaning, communication effectiveness or audience outcomes.",
        "next_step": "An adjudicator must inspect source metadata, media and disagreements, record rationale, and explicitly decide each conflicting item before recurrence denominators are updated.",
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
