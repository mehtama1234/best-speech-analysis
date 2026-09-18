#!/usr/bin/env python3
"""Validate the consolidated status dashboard against authoritative artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "research/end-to-end-status.json"


def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def validate(report: dict) -> list[str]:
    queue = read("research/full-reading-queue.json")
    reviews = read("research/full-context-reviews.json")
    atlas = read("research/corpus-pattern-atlas.json")
    lesson_index = read("research/corpus-lesson-index.json")
    taxonomy = read("research/corpus-function-taxonomy.json")
    evidence_bank = read("research/corpus-evidence-bank.json")
    job_cards = read("research/communication-job-cards.json")
    media = read("research/multimodal-coverage-audit.json")
    functions = read("research/corpus-function-independent-review-workbook.json")
    recurrence = read("research/corpus-recurrence-independent-review-workbook.json")
    cards = read("research/shared-lesson-cards.json")
    learner = read("research/shared-learner-check.json")
    listener = read("research/listener-outcome-protocol.json")
    raw_visual = read("research/raw-media-only-visual-audit.json")
    errors = []
    if report.get("status") != "research_checkpoint_not_complete": errors.append("dashboard status must remain research_checkpoint_not_complete")
    stages = report.get("stages", {})
    checks = {
        ("inventory", "video_count"): queue["video_count"],
        ("transcript_context", "video_count"): len(reviews["reviews"]),
        ("transcript_context", "caption_count"): queue["caption_count"],
        ("phrase_retrieval_atlas", "eligible_video_count"): atlas["eligible_video_count"],
        ("phrase_retrieval_atlas", "eligible_segment_count"): atlas["eligible_segment_count"],
        ("transcript_lesson_inventory", "review_count"): lesson_index["review_count"],
        ("transcript_lesson_inventory", "function_inventory_item_count"): lesson_index["summary"]["function_inventory_item_count"],
        ("transcript_lesson_inventory", "relation_inventory_item_count"): lesson_index["summary"]["relation_inventory_item_count"],
        ("canonical_function_taxonomy", "review_count"): taxonomy["summary"]["review_count"],
        ("canonical_function_taxonomy", "function_item_count"): taxonomy["summary"]["function_item_count"],
        ("canonical_function_taxonomy", "unclassified_item_count"): taxonomy["summary"]["unclassified_item_count"],
        ("exact_caption_evidence_bank", "function_record_count"): evidence_bank["summary"]["function_record_count"],
        ("exact_caption_evidence_bank", "caption_segment_record_count"): evidence_bank["summary"]["caption_segment_record_count"],
        ("exact_caption_evidence_bank", "missing_evidence_id_count"): evidence_bank["summary"]["missing_evidence_id_count"],
        ("communication_job_cards", "card_count"): job_cards["card_count"],
        ("speech_function_candidate_review", "queued_item_count"): functions["item_count"],
        ("recurrence_candidate_review", "queued_item_count"): recurrence["item_count"],
        ("delivery_evidence", "selected_video_count"): media["selected_video_count"],
        ("delivery_evidence", "raw_audio_video_present"): media["raw_audio_video_present_count"],
        ("delivery_evidence", "raw_only_visual_audit_items"): raw_visual["item_count"],
        ("shared_lessons", "draft_card_count"): cards["card_count"],
        ("learner_check", "task_count"): learner["task_count"],
        ("listener_outcomes", "task_count"): len(listener["listener_tasks"]),
    }
    for (stage, field), expected in checks.items():
        if stages.get(stage, {}).get(field) != expected:
            errors.append(f"{stage}.{field} does not match authoritative value {expected}")
    if stages.get("speech_function_candidate_review", {}).get("completed_independent_reviews") != 0: errors.append("function review completion cannot be nonzero without an imported independent export")
    if stages.get("recurrence_candidate_review", {}).get("completed_independent_reviews") != 0: errors.append("recurrence review completion cannot be nonzero without an imported independent export")
    if stages.get("learner_check", {}).get("completed_records") != 0: errors.append("learner records are not present")
    if stages.get("listener_outcomes", {}).get("completed_records") != 0: errors.append("listener records are not present")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else STATUS
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid end-to-end status:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("end-to-end status valid: counts reconciled; completion remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
