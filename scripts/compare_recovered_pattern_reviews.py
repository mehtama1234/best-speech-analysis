#!/usr/bin/env python3
"""Compare independent recovered-pattern reviews without promoting them."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_recovered_pattern_review_export import validate


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research/recovered-pattern-independent-review-workbook.json"
KEY = ROOT / "research/recovered-pattern-independent-review-key.json"
AGREEMENT_FIELDS = ("decision", "primary_function")


def compare(records: list[dict], packet: dict | None = None, key: dict | None = None) -> dict:
    packet = packet or json.loads(PACKET.read_text())
    key = key or json.loads(KEY.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent recovered-pattern reviews are required")
    errors = [error for record in records for error in validate(record)]
    if errors:
        raise ValueError("invalid recovered-pattern review: " + "; ".join(errors[:8]))
    reviewer_codes = [record["reviewer"]["reviewer_code"] for record in records]
    if len(set(reviewer_codes)) != len(reviewer_codes):
        raise ValueError("reviewer codes must be distinct")
    item_ids = [item["blind_item_id"] for item in packet["items"]]
    key_by_id = {item["blind_item_id"]: item for item in key["items"]}
    counts = Counter()
    agreements = Counter()
    disagreements = []
    for item_id in item_ids:
        responses = [record["responses"][item_id] for record in records]
        item_disagreements = {}
        for field in AGREEMENT_FIELDS:
            values = [response[field] for response in responses]
            counts[field] += 1
            if len(set(values)) == 1:
                agreements[field] += 1
            else:
                item_disagreements[field] = values
        if item_disagreements:
            internal = key_by_id[item_id]
            disagreements.append({
                "blind_item_id": item_id,
                "card_id": internal["card_id"],
                "pattern_id": internal["pattern_id"],
                "evidence_layer": packet["items"][item_ids.index(item_id)]["evidence_layer"],
                "disagreements": item_disagreements,
            })
    agreement = {
        field: {
            "items": counts[field],
            "unanimous_items": agreements[field],
            "unanimous_fraction": round(agreements[field] / counts[field], 4),
        }
        for field in AGREEMENT_FIELDS
    }
    return {
        "schema_version": "1.0",
        "record_type": "recovered_pattern_review_agreement_report",
        "workbook_id": packet["workbook_id"],
        "status": "agreement_report_not_pattern_or_effectiveness_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": packet["item_count"],
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "adjudication_status": "not_started",
        "claim_boundary": (
            "Agreement describes consistency between reviewers about retrieved "
            "candidate decisions and primary roles only. It does not establish "
            "semantic truth, source identity, recurrence, delivery meaning, "
            "learner transfer, listener outcomes or effectiveness."
        ),
        "next_step": "Adjudicate disagreements with source context before changing any pattern, denominator or lesson status.",
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
