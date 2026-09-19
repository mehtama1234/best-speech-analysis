#!/usr/bin/env python3
"""Compare independent delivery observations while preserving disagreements."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from scripts.validate_communication_job_delivery_review import validate

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
FIELDS = ("transcript_alignment", "vocal_timing_observation", "audio_measurement_and_limit", "visual_observation", "setting_editing_music_observation", "speaker_event_identity", "missingness_or_accessibility_note")


def compare(records: list[dict], queue: dict | None = None) -> dict:
    queue = queue or json.loads(QUEUE.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent delivery reviews are required")
    errors = [error for record in records for error in validate(record, queue)]
    if errors:
        raise ValueError("invalid delivery review: " + "; ".join(errors[:8]))
    reviewer_codes = [record["responses"]["reviewer_name"] for record in records]
    if len(set(reviewer_codes)) != len(reviewer_codes):
        raise ValueError("reviewer codes must be distinct")
    counts = Counter()
    agreements = Counter()
    disagreements = []
    for number, item in enumerate(queue["items"], 1):
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
            disagreements.append({"sample_id": item["sample_id"], "canonical_job": item["canonical_job"], "video_id": item["video_id"], "evidence_id": item["evidence_id"], "disagreements": item_disagreements})
    agreement = {field: {"items": counts[field], "unanimous_items": agreements[field], "unanimous_fraction": round(agreements[field] / counts[field], 4)} for field in FIELDS}
    return {
        "schema_version": "1.0",
        "record_type": "communication_job_delivery_review_agreement_report",
        "sampling_id": queue["sampling_id"],
        "status": "agreement_report_not_delivery_or_outcome_evidence",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": queue["item_count"],
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "independent_delivery_status": "not_decided",
        "adjudication_recommendation": "requires_adjudicator_for_alignment_observation_identity_and_accessibility_disagreements",
        "claim_boundary": "Agreement describes reviewer consistency about bounded delivery observations only. It does not establish speaker intent, emotion, confidence, effectiveness, audience outcomes or causal communication effects.",
        "next_step": "Adjudicate disagreements against source media, feature limits and accessibility notes before linking observations to a promoted pattern.",
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
