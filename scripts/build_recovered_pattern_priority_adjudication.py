#!/usr/bin/env python3
"""Build a label-blinded adjudication packet for priority-review disagreements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research/recovered-pattern-priority-review.json"


def build_adjudication(comparison: dict, packet: dict | None = None) -> dict:
    packet = packet or json.loads(PACKET.read_text())
    if comparison.get("record_type") != "recovered_pattern_priority_review_agreement_report":
        raise ValueError("comparison record_type is invalid")
    if comparison.get("promotion_eligible") is not False:
        raise ValueError("comparison must remain non-promotion eligible")
    packet_by_id = {item["blind_item_id"]: item for item in packet["items"]}
    items = []
    for disagreement in comparison.get("disagreements", []):
        item_id = disagreement["blind_item_id"]
        source = packet_by_id.get(item_id)
        if source is None:
            raise ValueError(f"comparison item is absent from packet: {item_id}")
        items.append({
            "blind_item_id": item_id,
            "proposed_move": source.get("proposed_move"),
            "video_id": source["video_id"],
            "candidate_video_id": source.get("candidate_video_id"),
            "linked_source_video_id": source.get("candidate_video_id") or source["video_id"],
            "original_source_url": source.get("original_source_url"),
            "title": source.get("title"),
            "evidence_layer": source["evidence_layer"],
            "source_url": source["source_url"],
            "evidence": source["evidence"],
            "reviewer_disagreements": disagreement["disagreements"],
            "reviewer_responses": disagreement.get("responses_by_reviewer", {}),
            "final_decision": None,
            "rationale": None,
            "safety_or_boundary_note": None,
        })
    missing_item_reviews = []
    for item_review in comparison.get("responses_by_item", []):
        reviewer_responses = item_review.get("responses_by_reviewer", {})
        if any(
            not isinstance(response, dict)
            or not isinstance(response.get("decision"), str)
            or not response["decision"].strip()
            for response in reviewer_responses.values()
        ):
            missing_item_reviews.append(item_review)
    if items:
        adjudication_status = "priority_adjudication_required_no_promotion"
        next_step = "Complete every adjudication decision, rationale and boundary note, then preserve the record alongside the comparison. Keep source missingness explicit."
    elif missing_item_reviews:
        adjudication_status = "no_structured_disagreement_missingness_preserved_no_promotion"
        next_step = "No structured disagreement is queued. Follow up missing coverage where possible or retain it explicitly as unresolved; do not infer a pattern decision."
    else:
        adjudication_status = "no_structured_disagreement_no_promotion"
        next_step = "No structured disagreement is queued. Preserve the comparison and its claim boundary; do not infer recurrence or effectiveness."
    return {
        "schema_version": "1.0",
        "record_type": "recovered_pattern_priority_adjudication_packet",
        "review_packet_id": "recovered-pattern-priority-review",
        "status": adjudication_status,
        "source_comparison_status": comparison.get("status"),
        "source_missingness": {
            "decision_coverage_status": comparison.get("decision_coverage_status", "unknown"),
            "items_with_missing_decisions": comparison.get("items_with_missing_decisions"),
            "missing_decision_pairs": comparison.get("missing_decision_pairs"),
            "missing_decision_item_ids": comparison.get("missing_decision_item_ids", []),
            "reviewer_coverage": comparison.get("reviewer_coverage", []),
            "item_reviews_with_missing_decisions": missing_item_reviews,
        },
        "item_count": len(items),
        "decision_vocabulary": ["retain", "revise", "reject", "indeterminate"],
        "items": items,
        "promotion_eligible": False,
        "claim_boundary": "This packet routes priority-review disagreements for adjudication. An adjudicator decision changes a local candidate record only; it does not establish semantic truth, recurrence, delivery meaning, learner transfer, listener outcomes or effectiveness.",
        "next_step": next_step,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("comparison", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_adjudication(json.loads(args.comparison.read_text()))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "item_count": result["item_count"], "status": result["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
