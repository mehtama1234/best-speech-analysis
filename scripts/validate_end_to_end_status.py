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
    job_learner = read("research/communication-job-learner-check.json")
    job_listener = read("research/communication-job-listener-outcome-protocol.json")
    stimulus_preflight = read("research/communication-job-stimuli-preflight.json")
    phrase_inventory = read("research/corpus-phrase-form-inventory.json")
    phrase_form_review = read("research/corpus-phrase-form-independent-review-workbook.json")
    delivery_index = read("research/delivery-evidence-index.json")
    evidence_model = read("research/shared-evidence-model.json")
    counterexamples = read("research/communication-job-counterexample-workbook.json")
    cross_comparison = read("research/communication-job-cross-comparison.json")
    delivery_sampling = read("research/communication-job-delivery-sampling.json")
    identity_review = read("research/corpus-identity-review-workbook.json")
    delivery_measurements = read("research/communication-job-delivery-measurement-preflight.json")
    curriculum_index = read("research/communication-job-curriculum-index.json")
    mobile_lessons = read("research/communication-job-mobile-lessons.json")
    stimulus_review = read("research/communication-job-listener-stimulus-review-workbook.json")
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
        ("communication_job_learner_check", "card_count"): job_learner["card_count"],
        ("communication_job_learner_check", "task_count"): job_learner["task_count"],
        ("communication_job_learner_check", "exact_phrase_form_count"): job_learner["exact_phrase_form_count"],
        ("communication_job_listener_outcomes", "pattern_count"): len(job_listener["patterns"]),
        ("communication_job_listener_outcomes", "listener_task_count"): len(job_listener["listener_tasks"]),
        ("listener_stimulus_preflight", "pair_count"): stimulus_preflight["pair_count"],
        ("listener_stimulus_preflight", "manual_review_required"): stimulus_preflight["summary"]["pairs_requiring_manual_review"],
        ("exact_phrase_form_inventory", "form_count"): phrase_inventory["form_count"],
        ("exact_phrase_form_inventory", "eligible_caption_segment_count"): phrase_inventory["eligible_caption_segment_count"],
        ("exact_phrase_form_independent_review", "queued_form_count"): phrase_form_review["item_count"],
        ("delivery_evidence_index", "selected_video_count"): delivery_index["coverage"]["selected_video_count"],
        ("delivery_evidence_index", "internal_observation_count"): delivery_index["coverage"]["internal_manual_observation_count"],
        ("delivery_evidence_index", "independent_observation_count"): delivery_index["coverage"]["independent_review_count"],
        ("shared_evidence_model", "entity_type_count"): len(evidence_model["entity_types"]),
        ("counterexample_library", "job_count"): counterexamples["job_count"],
        ("counterexample_library", "queued_slot_count"): counterexamples["item_count"],
        ("cross_job_comparison", "job_count"): cross_comparison["job_count"],
        ("cross_job_comparison", "pair_count"): cross_comparison["pair_count"],
        ("cross_job_comparison", "eligible_video_denominator"): cross_comparison["video_denominator"],
        ("communication_job_delivery_sampling", "job_count"): delivery_sampling["job_count"],
        ("communication_job_delivery_sampling", "queued_sample_count"): delivery_sampling["item_count"],
        ("communication_job_delivery_sampling", "raw_audio_video_sample_count"): delivery_sampling["coverage_summary"]["raw_audio_video_items"],
        ("corpus_identity_review", "queued_item_count"): identity_review["item_count"],
        ("corpus_identity_review", "registry_row_count"): identity_review["registry_row_count"],
        ("delivery_measurement_preflight", "sample_count"): delivery_measurements["item_count"],
        ("delivery_measurement_preflight", "matched_sample_count"): delivery_measurements["matched_sample_count"],
        ("delivery_measurement_preflight", "unmatched_sample_count"): delivery_measurements["unmatched_sample_count"],
        ("communication_job_curriculum", "lesson_count"): curriculum_index["lesson_count"],
        ("communication_job_mobile_lessons", "lesson_count"): mobile_lessons["lesson_count"],
        ("listener_stimulus_manual_review", "pair_count"): stimulus_review["item_count"],
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
    if stages.get("exact_phrase_form_independent_review", {}).get("completed_independent_reviews") != 0: errors.append("exact phrase-form review completion cannot be nonzero without an imported independent export")
    if stages.get("counterexample_library", {}).get("completed_independent_reviews") != 0: errors.append("counterexample completion cannot be nonzero without an imported independent export")
    if stages.get("communication_job_delivery_sampling", {}).get("completed_manual_observations") != 0: errors.append("delivery sampling observations cannot be nonzero without completed observation records")
    if stages.get("corpus_identity_review", {}).get("completed_independent_reviews") != 0: errors.append("identity review completion cannot be nonzero without an imported independent export")
    if stages.get("communication_job_mobile_lessons", {}).get("completed_records") != 0: errors.append("mobile lesson records are not present")
    if stages.get("listener_stimulus_manual_review", {}).get("completed_independent_reviews") != 0: errors.append("stimulus review completion cannot be nonzero without an imported independent export")
    if stages.get("listener_stimulus_manual_review", {}).get("locked_pairs") != 0: errors.append("stimulus pairs cannot be locked without an adjudicated review")
    if stages.get("learner_check", {}).get("completed_records") != 0: errors.append("learner records are not present")
    if stages.get("listener_outcomes", {}).get("completed_records") != 0: errors.append("listener records are not present")
    if stages.get("communication_job_learner_check", {}).get("completed_records") != 0: errors.append("communication-job learner records are not present")
    if stages.get("communication_job_listener_outcomes", {}).get("completed_records") != 0: errors.append("communication-job listener records are not present")
    if stages.get("communication_job_listener_outcomes", {}).get("stimulus_pairs_locked") is not False: errors.append("communication-job listener stimuli are not locked")
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
