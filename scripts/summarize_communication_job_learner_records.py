#!/usr/bin/env python3
"""Summarize validated learner records without promoting teachability to effectiveness."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from scripts.validate_communication_job_learner_record import validate

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/communication-job-learner-check.json"


def summarize(records: list[dict], protocol: dict | None = None) -> dict:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    if not records:
        raise ValueError("at least one learner record is required")
    for record in records:
        errors = validate(record, protocol)
        if errors:
            raise ValueError("invalid learner record: " + "; ".join(errors[:8]))
    by_card = defaultdict(list)
    card_by_id = {card["card_id"]: card for card in protocol["cards"]}
    for record in records:
        responses = record["responses"]
        for card in protocol["cards"]:
            by_card[card["card_id"]].append(responses)
    rows = []
    for card_id, card_records in sorted(by_card.items()):
        card = card_by_id[card_id]
        scores = {}
        for dimension in card["scoring_dimensions"]:
            values = [int(responses[f"{card_id}_score_{dimension}"]) for responses in card_records]
            scores[dimension] = {"count": len(values), "mean": round(sum(values) / len(values), 4), "distribution": {str(score): values.count(score) for score in (0, 1, 2)}}
        rows.append({"card_id": card_id, "canonical_job": card["canonical_job"], "record_count": len(card_records), "scores": scores, "safety_issue_count": sum(responses[f"{card_id}_safety_issue"] == "yes" for responses in card_records)})
    return {
        "schema_version": "1.0",
        "record_type": "communication_job_learner_summary",
        "status": "validated_teachability_summary_non_promotional",
        "protocol_id": protocol["protocol_id"],
        "record_count": len(records),
        "participant_codes": [record["responses"]["participant_code"] for record in records],
        "facilitator_codes": sorted({record["responses"]["facilitator_code"] for record in records}),
        "by_card": rows,
        "claim_boundary": "This summarizes facilitator-entered teachability rubric scores and safety flags. It does not establish that the original speech patterns are effective, recurrent, causal, persuasive or beneficial to listeners.",
        "next_step": "Inspect low scores, disagreements, accessibility needs and safety flags; revise the lesson before describing it as teachable.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = summarize([json.loads(path.read_text()) for path in args.records])
    rendered = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
