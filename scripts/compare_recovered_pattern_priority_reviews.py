#!/usr/bin/env python3
"""Compare two independent priority-packet returns without promotion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_recovered_pattern_priority_review_export import validate


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research/recovered-pattern-priority-review.json"
AGREEMENT_FIELDS = ("decision", "primary_function")


def compare(records: list[dict], packet: dict | None = None) -> dict:
    packet = packet or json.loads(PACKET.read_text())
    if len(records) < 2:
        raise ValueError("at least two independent priority reviews are required")
    errors = [error for record in records for error in validate(record)]
    if errors:
        raise ValueError("invalid priority review: " + "; ".join(errors[:8]))
    reviewer_codes = [record["reviewer"]["reviewer_code"] for record in records]
    if len(set(reviewer_codes)) != len(reviewer_codes):
        raise ValueError("reviewer codes must be distinct")
    item_ids = [item["blind_item_id"] for item in packet["items"]]
    field_stats = {
        field: {"items_with_observations": 0, "items_with_two_or_more_observations": 0, "unanimous_items": 0}
        for field in AGREEMENT_FIELDS
    }
    disagreements = []
    missingness_by_reviewer = []
    responses_by_item = []
    packet_by_id = {item["blind_item_id"]: item for item in packet["items"]}
    linked_source_groups = {}
    catalog_source_groups = {}
    for item in packet["items"]:
        linked_source_id = item.get("candidate_video_id") or item["video_id"]
        linked_source_groups.setdefault(linked_source_id, []).append(item["blind_item_id"])
        catalog_source_groups.setdefault(item["video_id"], []).append(item["blind_item_id"])
    for record in records:
        code = record["reviewer"]["reviewer_code"]
        responses = record["responses"]
        missing_decisions = []
        missing_fields_by_item = []
        for item_id in item_ids:
            response = responses.get(item_id, {})
            if not isinstance(response, dict):
                response = {}
            decision = response.get("decision")
            if not isinstance(decision, str) or not decision.strip():
                missing_decisions.append(item_id)
            missing_fields = [
                field for field in sorted(set(AGREEMENT_FIELDS) | {"alternate_explanation", "context_note", "identity_note", "uncertainty_note"})
                if not isinstance(response.get(field), str) or not response[field].strip()
            ]
            if missing_fields:
                missing_fields_by_item.append({"blind_item_id": item_id, "fields": missing_fields})
        missingness_by_reviewer.append({
            "reviewer_code": code,
            "decisions_received": len(item_ids) - len(missing_decisions),
            "missing_decision_count": len(missing_decisions),
            "missing_decision_item_ids": missing_decisions,
            "missing_fields_by_item": missing_fields_by_item,
        })
    for item_id in item_ids:
        responses_by_reviewer = {
            record["reviewer"]["reviewer_code"]: record["responses"].get(item_id)
            for record in records
        }
        responses_by_item.append({
            "blind_item_id": item_id,
            "linked_source_video_id": packet_by_id[item_id].get("candidate_video_id") or packet_by_id[item_id]["video_id"],
            "catalog_video_id": packet_by_id[item_id]["video_id"],
            "evidence_layer": packet_by_id[item_id]["evidence_layer"],
            "responses_by_reviewer": responses_by_reviewer,
        })
        item_disagreements = {}
        for field in AGREEMENT_FIELDS:
            values = {
                code: response.get(field)
                for code, response in responses_by_reviewer.items()
                if isinstance(response, dict)
                and isinstance(response.get(field), str)
                and response[field].strip()
            }
            if values:
                field_stats[field]["items_with_observations"] += 1
            if len(values) >= 2:
                field_stats[field]["items_with_two_or_more_observations"] += 1
                if len(set(values.values())) == 1:
                    field_stats[field]["unanimous_items"] += 1
                else:
                    item_disagreements[field] = values
        if item_disagreements:
            disagreements.append({
                "blind_item_id": item_id,
                "evidence_layer": packet_by_id[item_id]["evidence_layer"],
                "linked_source_video_id": packet_by_id[item_id].get("candidate_video_id") or packet_by_id[item_id]["video_id"],
                "catalog_video_id": packet_by_id[item_id]["video_id"],
                "disagreements": item_disagreements,
                "responses_by_reviewer": responses_by_reviewer,
            })
    agreement = {}
    for field, stats in field_stats.items():
        comparable = stats["items_with_two_or_more_observations"]
        agreement[field] = {
            **stats,
            "packet_items": len(item_ids),
            "unanimous_fraction_among_comparable": round(stats["unanimous_items"] / comparable, 4) if comparable else None,
        }
    any_missing = any(entry["missing_decision_count"] for entry in missingness_by_reviewer)
    missing_decision_item_ids = {
        item_id
        for entry in missingness_by_reviewer
        for item_id in entry["missing_decision_item_ids"]
    }
    return {
        "schema_version": "1.0",
        "record_type": "recovered_pattern_priority_review_agreement_report",
        "review_packet_id": "recovered-pattern-priority-review",
        "status": "priority_review_comparison_not_pattern_or_effectiveness_evidence",
        "decision_coverage_status": "partial" if any_missing else "complete",
        "reviewer_count": len(records),
        "reviewer_codes": reviewer_codes,
        "item_count": packet["item_count"],
        "source_cluster_summary": {
            "linked_source_video_count": len(linked_source_groups),
            "maximum_items_per_linked_source_video": max(map(len, linked_source_groups.values()), default=0),
            "linked_source_clusters": [
                {"source_video_id": source_id, "blind_item_ids": item_ids}
                for source_id, item_ids in sorted(linked_source_groups.items())
            ],
            "catalog_video_count": len(catalog_source_groups),
            "maximum_items_per_catalog_video": max(map(len, catalog_source_groups.values()), default=0),
            "catalog_video_clusters": [
                {"catalog_video_id": source_id, "blind_item_ids": item_ids}
                for source_id, item_ids in sorted(catalog_source_groups.items())
            ],
        },
        "reviewer_coverage": missingness_by_reviewer,
        "responses_by_item": responses_by_item,
        "agreement": agreement,
        "items_with_missing_decisions": len(missing_decision_item_ids),
        "missing_decision_pairs": sum(entry["missing_decision_count"] for entry in missingness_by_reviewer),
        "missing_decision_item_ids": sorted(missing_decision_item_ids),
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "promotion_eligible": False,
        "adjudication_status": "not_started",
        "claim_boundary": "Agreement describes reviewer consistency only on comparable nonblank fields in this bounded priority-packet return; missing values are preserved and excluded from agreement. Source clusters are retained because items from one video are not independent video-level replications. This does not establish semantic truth, recurrence, delivery meaning, learner transfer, listener outcomes or effectiveness.",
        "next_step": "Adjudicate observed disagreements with source context. Resolve or retain missing coverage explicitly; never count missing responses as agreement, disagreement or negative findings.",
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
