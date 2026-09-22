#!/usr/bin/env python3
"""Build a bounded adjudication packet from a recovered-review comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research/recovered-pattern-independent-review-workbook.json"
KEY = ROOT / "research/recovered-pattern-independent-review-key.json"


def build_adjudication(comparison: dict, packet: dict | None = None, key: dict | None = None) -> dict:
    packet = packet or json.loads(PACKET.read_text())
    key = key or json.loads(KEY.read_text())
    if comparison.get("record_type") != "recovered_pattern_review_agreement_report":
        raise ValueError("comparison record_type is invalid")
    if comparison.get("promotion_eligible") is not False:
        raise ValueError("comparison must remain non-promotion eligible")
    packet_by_id = {item["blind_item_id"]: item for item in packet["items"]}
    key_by_id = {item["blind_item_id"]: item for item in key["items"]}
    items = []
    for disagreement in comparison.get("disagreements", []):
        item_id = disagreement["blind_item_id"]
        source = packet_by_id.get(item_id)
        internal = key_by_id.get(item_id)
        if source is None or internal is None:
            raise ValueError(f"comparison item is absent from packet/key: {item_id}")
        items.append({
            "blind_item_id": item_id,
            "card_id": internal["card_id"],
            "pattern_id": internal["pattern_id"],
            "candidate_form": internal["candidate_form"],
            "video_id": source["video_id"],
            "evidence_layer": source["evidence_layer"],
            "source_url": source["source_url"],
            "evidence": source["evidence"],
            "reviewer_disagreements": disagreement["disagreements"],
            "final_decision": None,
            "rationale": None,
            "safety_or_boundary_note": None,
        })
    return {
        "schema_version": "1.0",
        "record_type": "recovered_pattern_adjudication_packet",
        "workbook_id": comparison["workbook_id"],
        "status": "adjudication_required_no_promotion",
        "source_comparison_status": comparison.get("status"),
        "item_count": len(items),
        "decision_vocabulary": ["retain", "revise", "reject", "indeterminate"],
        "items": items,
        "promotion_eligible": False,
        "claim_boundary": (
            "This packet routes reviewer disagreements for adjudication. An "
            "adjudicator decision changes the local candidate record only; it "
            "does not establish recurrence, delivery meaning, learner transfer, "
            "listener outcomes or effectiveness."
        ),
        "next_step": "Complete every final decision, rationale and boundary note, then preserve the adjudication record alongside the comparison report.",
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
