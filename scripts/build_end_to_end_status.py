#!/usr/bin/env python3
"""Build a consolidated, non-promotional status report for the research goal."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def main() -> int:
    queue = load("research/full-reading-queue.json")
    reviews = load("research/full-context-reviews.json")
    atlas = load("research/corpus-pattern-atlas.json")
    lesson_index = load("research/corpus-lesson-index.json")
    taxonomy = load("research/corpus-function-taxonomy.json")
    media = load("research/multimodal-coverage-audit.json")
    media_independent = load("research/multimodal-independent-review-workbook.json")
    recurrence = load("research/corpus-recurrence-independent-review-workbook.json")
    functions = load("research/corpus-function-independent-review-workbook.json")
    cards = load("research/shared-lesson-cards.json")
    learner = load("research/shared-learner-check.json")
    listener = load("research/listener-outcome-protocol.json")
    raw_only_visual = load("research/raw-media-only-visual-audit.json")

    transcript_count = len(reviews["reviews"])
    caption_count = queue["caption_count"]
    report = {
        "schema_version": "1.0",
        "report_id": "best-speech-analysis-end-to-end-status",
        "generated_from": [
            "research/full-reading-queue.json", "research/full-context-reviews.json",
            "research/corpus-pattern-atlas.json", "research/multimodal-coverage-audit.json",
            "research/corpus-lesson-index.json",
            "research/corpus-function-taxonomy.json",
            "research/shared-lesson-cards.json", "research/shared-learner-check.json",
            "research/listener-outcome-protocol.json", "research/raw-media-only-visual-audit.json",
        ],
        "status": "research_checkpoint_not_complete",
        "claim_boundary": "This dashboard reports artifact and validation status. It does not convert transcript coverage, internal review, generated instruments or passing tests into evidence of communication effectiveness.",
        "stages": {
            "inventory": {"status": "complete_for_fixed_corpus", "video_count": queue["video_count"], "source": "research/full-reading-queue.json"},
            "transcript_context": {"status": "complete_for_fixed_corpus", "video_count": transcript_count, "caption_count": caption_count, "source": "research/full-context-reviews.json"},
            "phrase_retrieval_atlas": {"status": "complete_as_heuristic_transcript_retrieval", "eligible_video_count": atlas["eligible_video_count"], "eligible_segment_count": atlas["eligible_segment_count"], "source": "research/corpus-pattern-atlas.json"},
            "transcript_lesson_inventory": {"status": lesson_index["status"], "review_count": lesson_index["review_count"], "function_inventory_item_count": lesson_index["summary"]["function_inventory_item_count"], "relation_inventory_item_count": lesson_index["summary"]["relation_inventory_item_count"], "source": "research/corpus-lesson-index.json"},
            "canonical_function_taxonomy": {"status": taxonomy["status"], "review_count": taxonomy["summary"]["review_count"], "function_item_count": taxonomy["summary"]["function_item_count"], "canonical_job_count": len(taxonomy["canonical_jobs"]), "unclassified_item_count": taxonomy["summary"]["unclassified_item_count"], "source": "research/corpus-function-taxonomy.json"},
            "speech_function_candidate_review": {"status": functions["status"], "queued_item_count": functions["item_count"], "completed_independent_reviews": 0, "source": "research/corpus-function-independent-review-workbook.json"},
            "recurrence_candidate_review": {"status": recurrence["status"], "queued_item_count": recurrence["item_count"], "completed_independent_reviews": 0, "source": "research/corpus-recurrence-independent-review-workbook.json"},
            "delivery_evidence": {"status": media["status"], "selected_video_count": media["selected_video_count"], "raw_audio_video_present": media["raw_audio_video_present_count"], "raw_audio_video_with_transcript": media["raw_audio_video_with_transcript_count"], "raw_audio_video_without_transcript": media["raw_audio_video_without_transcript_count"], "internal_manual_reviews": media["internal_manual_review_count"], "raw_only_visual_audit_items": raw_only_visual["item_count"], "raw_only_visual_audit_status": raw_only_visual["status"], "independent_review_items": media_independent["item_count"], "completed_independent_reviews": 0, "source": "research/multimodal-coverage-audit.json"},
            "shared_lessons": {"status": cards["status"], "draft_card_count": cards["card_count"], "promotion_ready_card_count": 0, "source": "research/shared-lesson-cards.json"},
            "learner_check": {"status": learner["status"], "task_count": learner["task_count"], "completed_records": 0, "source": "research/shared-learner-check.json"},
            "listener_outcomes": {"status": listener["status"], "task_count": len(listener["listener_tasks"]), "completed_records": 0, "source": "research/listener-outcome-protocol.json"},
        },
        "next_required_gates": [
            "obtain independent transcript-function review exports and preserve disagreements",
            "obtain independent recurrence review exports and adjudicate disagreements",
            "complete independent multimodal alignment/function/safety review",
            "run learner teachability protocol and validate exported records",
            "run blinded listener-outcome protocol before making effectiveness claims",
        ],
    }
    out = ROOT / "research/end-to-end-status.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# End-to-end research status", "",
        "Status: **research checkpoint not complete**.", "",
        report["claim_boundary"], "",
        "| Stage | Status | Key count |", "|---|---|---:|",
        f"| Inventory | `{report['stages']['inventory']['status']}` | {queue['video_count']} videos |",
        f"| Transcript context | `{report['stages']['transcript_context']['status']}` | {transcript_count} videos / {caption_count} captions |",
        f"| Phrase atlas | `{report['stages']['phrase_retrieval_atlas']['status']}` | {atlas['eligible_video_count']} videos / {atlas['eligible_segment_count']} segments |",
        f"| Transcript lesson inventory | `{lesson_index['status']}` | {lesson_index['review_count']} reviews / {lesson_index['summary']['function_inventory_item_count']} functions / {lesson_index['summary']['relation_inventory_item_count']} relations |",
        f"| Canonical function taxonomy | `{taxonomy['status']}` | {taxonomy['summary']['function_item_count']} items / {taxonomy['summary']['unclassified_item_count']} unclassified |",
        f"| Function review | `{functions['status']}` | {functions['item_count']} queued / 0 completed |",
        f"| Recurrence review | `{recurrence['status']}` | {recurrence['item_count']} queued / 0 completed |",
        f"| Delivery evidence | `{media['status']}` | {media['raw_audio_video_present_count']} raw-complete ({media['raw_audio_video_without_transcript_count']} without transcript) / {media['internal_manual_review_count']} internal reviewed |",
        f"| Shared lessons | `{cards['status']}` | {cards['card_count']} drafts / 0 promotion-ready |",
        f"| Learner check | `{learner['status']}` | {learner['task_count']} tasks / 0 records |",
        f"| Listener outcomes | `{listener['status']}` | {len(listener['listener_tasks'])} tasks / 0 records |",
        "", "## Required gates", "",
    ]
    lines.extend(f"- {gate}" for gate in report["next_required_gates"])
    (ROOT / "writeups/end-to-end-status.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(out), "transcript_reviews": transcript_count, "caption_count": caption_count, "next_gate_count": len(report["next_required_gates"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
