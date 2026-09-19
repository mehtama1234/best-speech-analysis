#!/usr/bin/env python3
"""Build the shared web/mobile lesson-card model from the current 18-job curriculum."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/communication-job-curriculum-index.json"
OUT = ROOT / "research/shared-lesson-cards.json"


def card_from_lesson(lesson: dict) -> dict:
    examples = lesson.get("exact_examples", [])
    delivery = lesson.get("delivery_samples", [])
    counterexamples = lesson.get("counterexample_slots", [])
    recurrence = lesson.get("recurrence", {})
    validation = lesson.get("validation", {})
    card = {
        "card_id": lesson["pattern_id"],
        "canonical_job": lesson["canonical_job"],
        "slice": "communication-job-curriculum",
        "status": lesson["status"],
        "evidence_level": "provisional_practice_hypothesis",
        "claim_boundary": "This shared card joins transcript evidence, delivery queues and practice scaffolding. It does not establish independent recurrence, delivery meaning, teachability, listener outcomes or causal effectiveness.",
        "communication_problem": lesson["communication_problem"],
        "speech_function_hypothesis": lesson["communication_problem"],
        "speech_function": {
            "candidate_family": lesson["canonical_job"],
            "status": "provisional_transcript_function_label_requires_context_and_independent_review",
        },
        "mechanism_hypothesis": lesson["mechanism_hypothesis"],
        "mechanism_status": "bounded_hypothesis_not_outcome_evidence",
        "repeatable_form": lesson["repeatable_form"],
        "examples": examples,
        "counterexamples": counterexamples,
        "delivery_evidence": {
            "status": "queue_only_manual_observation_pending",
            "observations": delivery,
            "boundary": "Delivery samples and proxies are navigation aids until manual and independent observations are recorded.",
        },
        "recurrence": {
            "phrase_family": lesson["canonical_job"],
            "phrase_forms": lesson.get("phrase_forms", []),
            "function_record_count": recurrence.get("function_record_count"),
            "video_hit_count": recurrence.get("video_count"),
            "segment_hit_count": None,
            "denominator_status": recurrence.get("denominator_status", "inventory_counts_not_effectiveness_denominators"),
            "event_level_holdout": {"status": "not_in_current_job_curriculum_index"},
        },
        "practice": {
            "hypothesis": lesson["practice"],
            "repeatable_form": lesson["repeatable_form"],
            "self_check": lesson["self_check"],
            "non_fit": lesson["non_fit"],
            "task_count": lesson.get("learner", {}).get("task_count", 0),
        },
        "validation": {
            "independent_function_review": validation.get("independent_function_review", "pending"),
            "independent_recurrence_review": validation.get("independent_recurrence_review", "pending"),
            "delivery_review": validation.get("delivery_review", "pending"),
            "learner_status": validation.get("learner_check", "not_run"),
            "listener_outcomes": validation.get("listener_outcome", "not_run"),
            "speaker_event_independence": "pending_independent_identity_review",
        },
        "limits": {
            "counterexample_slot_count": len(counterexamples),
            "next_actions": [
                "complete independent function and phrase-form review",
                "verify speaker/event identity and recurrence",
                "complete delivery observations and counterexamples",
                "run the learner protocol before promotion",
            ],
            "do_not_claim": ["causal effectiveness", "listener outcomes", "speaker intent", "universal best practice"],
        },
    }
    card["evidence_chain"] = {
        "communication_problem": {"value": card["communication_problem"], "status": "lesson_problem_statement"},
        "exact_language_and_function": {
            "phrase_family": lesson["canonical_job"],
            "phrase_forms": lesson.get("phrase_forms", []),
            "example_evidence_ids": [segment["evidence_id"] for example in examples for segment in example.get("exact_segments", []) if segment.get("evidence_id")],
            "function_status": card["speech_function"]["status"],
        },
        "delivery_evidence": {
            "evidence_ids": [item.get("evidence_id") for item in delivery if item.get("evidence_id")],
            "status": card["delivery_evidence"]["status"],
            "boundary": card["delivery_evidence"]["boundary"],
        },
        "mechanism_hypothesis": {"text": card["mechanism_hypothesis"], "status": card["mechanism_status"]},
        "cross_talk_recurrence": {
            "video_hit_count": recurrence.get("video_count"),
            "segment_hit_count": None,
            "event_level_holdout": {"status": "not_in_current_job_curriculum_index"},
            "status": "provisional_inventory_recurrence_pending_independent_review",
        },
        "counterexamples_and_limits": {
            "counterexample_slot_count": len(counterexamples),
            "status": "queued_not_completed",
            "do_not_claim": card["limits"]["do_not_claim"],
        },
        "practice": {"task_count": card["practice"]["task_count"], "status": "draft_practice_hypothesis"},
        "learner_check": {"status": card["validation"]["learner_status"]},
        "listener_outcome_check": {"status": "not_tested"},
    }
    return card


def main() -> int:
    source = json.loads(SOURCE.read_text())
    cards = [card_from_lesson(lesson) for lesson in source["lessons"]]
    output = {
        "schema_version": "1.0",
        "model_id": "shared-lesson-cards",
        "status": "18_draft_cards_not_validated",
        "claim_boundary": "This is the shared web/mobile data model for provisional evidence-linked lessons. It does not promote any pattern or claim learner or listener success.",
        "source_index": "research/communication-job-curriculum-index.json",
        "card_count": len(cards),
        "cards": cards,
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
