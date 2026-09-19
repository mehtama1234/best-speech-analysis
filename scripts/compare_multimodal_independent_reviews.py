#!/usr/bin/env python3
"""Compare independent multimodal reviews without promoting agreement to evidence."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_multimodal_independent_review import validate

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/multimodal-independent-review-workbook.json"
FIELDS = ("boundary_decision", "candidate_function_decision", "speaker_setting_decision", "audio_visual_decision", "safety_decision")


def compare(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent multimodal reviews are required")
    for record in records:
        result = validate(record, workbook)
        if result["errors"]:
            raise ValueError("invalid multimodal review: " + "; ".join(result["errors"][:8]))
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
            disagreements.append({"review_item_id": item["review_item_id"], "video_id": item["video_id"], "pattern_id": item["pattern_id"], "evidence_id": item["evidence_id"], "disagreements": item_disagreements})
    agreement = {field: {"items": counts[field], "unanimous_items": agreements[field], "unanimous_fraction": round(agreements[field] / counts[field], 4)} for field in FIELDS}
    return {
        "schema_version": "1.0",
        "record_type": "multimodal_review_agreement_report",
        "workbook_id": workbook["workbook_id"],
        "status": "agreement_report_not_delivery_or_outcome_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": workbook["item_count"],
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "adjudication_recommendation": "requires_adjudicator_for_alignment_function_setting_audio_visual_and_safety_disagreements",
        "claim_boundary": "Agreement describes reviewer consistency about multimodal evidence boundaries only. It does not establish delivery effectiveness, emotion, intent, confidence, audience outcomes or causal communication effects.",
        "next_step": "Adjudicate disagreements against source media and preserve missingness before updating any delivery or pattern card status.",
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
