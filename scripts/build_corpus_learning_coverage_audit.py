#!/usr/bin/env python3
"""Audit learner-surface coverage for every fixed-corpus video."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/corpus-learner-card-inventory.json"
ITINERARY = ROOT / "research/corpus-video-learning-itinerary.json"
OUT = ROOT / "research/corpus-learning-coverage-audit.json"
MD = ROOT / "writeups/corpus-learning-coverage-audit.md"


def build() -> dict:
    cards = json.loads(CARDS.read_text())
    itinerary = json.loads(ITINERARY.read_text())
    functions = defaultdict(list)
    sequences = defaultdict(list)
    for card in cards["cards"]:
        functions[card["video_id"]].append(card)
    for card in cards["structural_cards"]:
        sequences[card["video_id"]].append(card)
    rows = []
    for route in itinerary["entries"]:
        video_id = route["video_id"]
        function_cards = functions[video_id]
        sequence_cards = sequences[video_id]
        all_cards = function_cards + sequence_cards
        row = {
            "video_id": video_id,
            "title": route["title"],
            "writeup": route.get("writeup"),
            "function_card_count": len(function_cards),
            "sequence_card_count": len(sequence_cards),
            "total_card_count": len(all_cards),
            "cards_with_exact_evidence": sum(bool(card.get("exact_evidence")) for card in all_cards),
            "cards_with_phrase_handles": sum(bool(card.get("phrase_handles")) for card in all_cards),
            "phrase_handle_count": sum(len(card.get("phrase_handles", [])) for card in all_cards),
            "cards_with_local_delivery_proxy": sum(card.get("delivery_proxy", {}).get("status", "").startswith("local") for card in all_cards),
            "cards_with_delivery_candidates": sum(bool(card.get("delivery_candidates")) for card in all_cards),
            "delivery_candidate_count": sum(len(card.get("delivery_candidates", [])) for card in all_cards),
            "cards_with_movement_candidates": sum(bool(card.get("movement_candidates")) for card in all_cards),
            "movement_candidate_count": sum(len(card.get("movement_candidates", [])) for card in all_cards),
            "selected_lesson_has_exact_evidence": bool(route.get("exact_evidence")),
            "selected_lesson_phrase_handle_count": len(route.get("phrase_handles", [])),
            "selected_lesson_delivery_status": route.get("delivery_proxy", {}).get("status"),
            "coverage_status": "covered_with_transcript_lesson" if all_cards and route.get("exact_evidence") else "review_required",
        }
        rows.append(row)
    report = {
        "schema_version": "1.0",
        "audit_id": "corpus-learning-coverage-audit",
        "status": "coverage_reconciled_transcript_derived_not_validation",
        "claim_boundary": "This audit proves that local learner artifacts are linked and counts reconcile for the fixed corpus. It is not validation evidence and does not prove source identity, function correctness, delivery meaning, teachability, listener comprehension or effectiveness.",
        "source_artifacts": ["research/corpus-learner-card-inventory.json", "research/corpus-video-learning-itinerary.json"],
        "video_count": len(rows),
        "videos_with_transcript_lesson": sum(row["coverage_status"] == "covered_with_transcript_lesson" for row in rows),
        "videos_requiring_review": sum(row["coverage_status"] != "covered_with_transcript_lesson" for row in rows),
        "summary": {
            "function_cards": sum(row["function_card_count"] for row in rows),
            "sequence_cards": sum(row["sequence_card_count"] for row in rows),
            "cards_with_exact_evidence": sum(row["cards_with_exact_evidence"] for row in rows),
            "cards_with_phrase_handles": sum(row["cards_with_phrase_handles"] for row in rows),
            "phrase_handle_count": sum(row["phrase_handle_count"] for row in rows),
            "cards_with_local_delivery_proxy": sum(row["cards_with_local_delivery_proxy"] for row in rows),
            "cards_with_delivery_candidates": sum(row["cards_with_delivery_candidates"] for row in rows),
            "delivery_candidate_count": sum(row["delivery_candidate_count"] for row in rows),
            "cards_with_movement_candidates": sum(row["cards_with_movement_candidates"] for row in rows),
            "movement_candidate_count": sum(row["movement_candidate_count"] for row in rows),
        },
        "videos": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Corpus learning coverage audit", "", "Status: **coverage reconciled; transcript-derived and not validation evidence**.", "", report["claim_boundary"], "", f"Fixed-corpus videos: **{report['video_count']}** · videos with a transcript lesson and exact selected evidence: **{report['videos_with_transcript_lesson']}** · requiring review: **{report['videos_requiring_review']}**.", "", f"Cards: **{report['summary']['function_cards']}** function + **{report['summary']['sequence_cards']}** sequence · cards with exact evidence: **{report['summary']['cards_with_exact_evidence']}** · cards with phrase handles: **{report['summary']['cards_with_phrase_handles']}** (**{report['summary']['phrase_handle_count']}** handles) · local delivery proxies: **{report['summary']['cards_with_local_delivery_proxy']}** · cards with delivery candidates: **{report['summary']['cards_with_delivery_candidates']}** (**{report['summary']['delivery_candidate_count']}** windows) · cards with movement candidates: **{report['summary']['cards_with_movement_candidates']}** (**{report['summary']['movement_candidate_count']}** records).", "", "| Video | Function cards | Sequence cards | Exact evidence | Phrase-handle cards | Delivery proxy cards | Movement cards | Status |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in rows:
        lines.append(f"| `{row['video_id']}` {row['title'].replace('|', '\\|')} | {row['function_card_count']} | {row['sequence_card_count']} | {row['cards_with_exact_evidence']} | {row['cards_with_phrase_handles']} | {row['cards_with_local_delivery_proxy']} | {row['cards_with_movement_candidates']} | `{row['coverage_status']}` |")
    lines += ["", "Use the [full learner-card browser](corpus-learner-card-inventory.html) for card-level evidence and the [video itinerary](corpus-video-learning-itinerary.html) for one starting lesson per video. Coverage is not validation.", ""]
    MD.write_text("\n".join(lines))
    return report


if __name__ == "__main__":
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": build()["video_count"]}, indent=2))
