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
    evidence_bank = load("research/corpus-evidence-bank.json")
    job_cards = load("research/communication-job-cards.json")
    job_learner = load("research/communication-job-learner-check.json")
    job_listener = load("research/communication-job-listener-outcome-protocol.json")
    stimulus_preflight = load("research/communication-job-stimuli-preflight.json")
    phrase_inventory = load("research/corpus-phrase-form-inventory.json")
    phrase_form_review = load("research/corpus-phrase-form-independent-review-workbook.json")
    delivery_index = load("research/delivery-evidence-index.json")
    evidence_model = load("research/shared-evidence-model.json")
    counterexamples = load("research/communication-job-counterexample-workbook.json")
    counterexample_candidates = load("research/communication-job-counterexample-candidate-queue.json")
    cross_comparison = load("research/communication-job-cross-comparison.json")
    delivery_sampling = load("research/communication-job-delivery-sampling.json")
    delivery_internal = load("research/communication-job-delivery-internal-observations.json")
    identity_review = load("research/corpus-identity-review-workbook.json")
    delivery_measurements = load("research/communication-job-delivery-measurement-preflight.json")
    curriculum_index = load("research/communication-job-curriculum-index.json")
    mobile_lessons = load("research/communication-job-mobile-lessons.json")
    stimulus_review = load("research/communication-job-listener-stimulus-review-workbook.json")
    media = load("research/multimodal-coverage-audit.json")
    media_independent = load("research/multimodal-independent-review-workbook.json")
    recurrence = load("research/corpus-recurrence-independent-review-workbook.json")
    functions = load("research/corpus-function-independent-review-workbook.json")
    cards = load("research/shared-lesson-cards.json")
    learner = load("research/shared-learner-check.json")
    listener = load("research/communication-job-listener-outcome-protocol.json")
    raw_only_visual = load("research/raw-media-only-visual-audit.json")
    full_media = load("research/full-corpus-media-coverage.json")
    media_recovery = load("research/full-corpus-media-recovery-queue.json")
    promotion_readiness = load("research/communication-job-promotion-readiness.json")

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
            "research/corpus-evidence-bank.json",
            "research/communication-job-cards.json",
            "research/communication-job-learner-check.json",
            "research/communication-job-listener-outcome-protocol.json",
            "research/communication-job-stimuli-preflight.json",
            "research/corpus-phrase-form-inventory.json",
            "research/corpus-phrase-form-independent-review-workbook.json",
            "research/delivery-evidence-index.json",
            "research/shared-evidence-model.json",
            "research/communication-job-counterexample-workbook.json",
            "research/communication-job-counterexample-candidate-queue.json",
            "research/communication-job-cross-comparison.json",
            "research/communication-job-delivery-sampling.json",
            "research/communication-job-delivery-internal-observations.json",
            "research/corpus-identity-review-workbook.json",
            "research/communication-job-delivery-measurement-preflight.json",
            "research/communication-job-curriculum-index.json",
            "research/communication-job-mobile-lessons.json",
            "research/communication-job-listener-stimulus-review-workbook.json",
            "research/shared-lesson-cards.json", "research/shared-learner-check.json",
            "research/communication-job-listener-outcome-protocol.json", "research/raw-media-only-visual-audit.json",
            "research/full-corpus-media-coverage.json", "research/full-corpus-media-recovery-queue.json",
            "research/communication-job-promotion-readiness.json",
        ],
        "status": "research_checkpoint_not_complete",
        "claim_boundary": "This dashboard reports artifact and validation status. It does not convert transcript coverage, internal review, generated instruments or passing tests into evidence of communication effectiveness.",
        "stages": {
            "inventory": {"status": "complete_for_fixed_corpus", "video_count": queue["video_count"], "source": "research/full-reading-queue.json"},
            "transcript_context": {"status": "complete_for_fixed_corpus", "video_count": transcript_count, "caption_count": caption_count, "source": "research/full-context-reviews.json"},
            "phrase_retrieval_atlas": {"status": "complete_as_heuristic_transcript_retrieval", "eligible_video_count": atlas["eligible_video_count"], "eligible_segment_count": atlas["eligible_segment_count"], "source": "research/corpus-pattern-atlas.json"},
            "transcript_lesson_inventory": {"status": lesson_index["status"], "review_count": lesson_index["review_count"], "function_inventory_item_count": lesson_index["summary"]["function_inventory_item_count"], "relation_inventory_item_count": lesson_index["summary"]["relation_inventory_item_count"], "source": "research/corpus-lesson-index.json"},
            "canonical_function_taxonomy": {"status": taxonomy["status"], "review_count": taxonomy["summary"]["review_count"], "function_item_count": taxonomy["summary"]["function_item_count"], "canonical_job_count": len(taxonomy["canonical_jobs"]), "unclassified_item_count": taxonomy["summary"]["unclassified_item_count"], "source": "research/corpus-function-taxonomy.json"},
            "exact_caption_evidence_bank": {"status": evidence_bank["status"], "function_record_count": evidence_bank["summary"]["function_record_count"], "caption_segment_record_count": evidence_bank["summary"]["caption_segment_record_count"], "missing_evidence_id_count": evidence_bank["summary"]["missing_evidence_id_count"], "source": "research/corpus-evidence-bank.json"},
            "communication_job_cards": {"status": job_cards["status"], "card_count": job_cards["card_count"], "source": "research/communication-job-cards.json"},
            "communication_job_learner_check": {"status": job_learner["status"], "card_count": job_learner["card_count"], "task_count": job_learner["task_count"], "exact_phrase_form_count": job_learner["exact_phrase_form_count"], "completed_records": 0, "source": "research/communication-job-learner-check.json"},
            "communication_job_listener_outcomes": {"status": job_listener["status"], "pattern_count": len(job_listener["patterns"]), "listener_task_count": len(job_listener["listener_tasks"]), "stimulus_pairs_locked": job_listener["stimulus_pairs_locked"], "completed_records": 0, "source": "research/communication-job-listener-outcome-protocol.json"},
            "listener_stimulus_preflight": {"status": stimulus_preflight["status"], "pair_count": stimulus_preflight["pair_count"], "manual_review_required": stimulus_preflight["summary"]["pairs_requiring_manual_review"], "source": "research/communication-job-stimuli-preflight.json"},
            "exact_phrase_form_inventory": {"status": phrase_inventory["status"], "form_count": phrase_inventory["form_count"], "eligible_caption_segment_count": phrase_inventory["eligible_caption_segment_count"], "source": "research/corpus-phrase-form-inventory.json"},
            "exact_phrase_form_independent_review": {"status": phrase_form_review["status"], "queued_form_count": phrase_form_review["item_count"], "completed_independent_reviews": 0, "source": "research/corpus-phrase-form-independent-review-workbook.json"},
            "delivery_evidence_index": {"status": delivery_index["status"], "selected_video_count": delivery_index["coverage"]["selected_video_count"], "internal_observation_count": delivery_index["coverage"]["internal_manual_observation_count"], "independent_observation_count": delivery_index["coverage"]["independent_review_count"], "source": "research/delivery-evidence-index.json"},
            "shared_evidence_model": {"status": evidence_model["status"], "entity_type_count": len(evidence_model["entity_types"]), "source": "research/shared-evidence-model.json"},
            "counterexample_library": {"status": counterexamples["status"], "job_count": counterexamples["job_count"], "queued_slot_count": counterexamples["item_count"], "completed_independent_reviews": 0, "source": "research/communication-job-counterexample-workbook.json"},
            "counterexample_candidate_queue": {"status": counterexample_candidates["status"], "candidate_count": counterexample_candidates["candidate_count"], "source_linked_candidate_count": counterexample_candidates["source_linked_candidate_count"], "confirmed_counterexample_count": counterexample_candidates["confirmed_counterexample_count"], "source": "research/communication-job-counterexample-candidate-queue.json"},
            "cross_job_comparison": {"status": cross_comparison["status"], "job_count": cross_comparison["job_count"], "pair_count": cross_comparison["pair_count"], "eligible_video_denominator": cross_comparison["video_denominator"], "source": "research/communication-job-cross-comparison.json"},
            "communication_job_delivery_sampling": {"status": delivery_sampling["status"], "job_count": delivery_sampling["job_count"], "queued_sample_count": delivery_sampling["item_count"], "raw_audio_video_sample_count": delivery_sampling["coverage_summary"]["raw_audio_video_items"], "completed_manual_observations": delivery_sampling["coverage_summary"]["manual_observations_completed"], "source": "research/communication-job-delivery-sampling.json"},
            "communication_job_delivery_internal_observations": {"status": delivery_internal["status"], "raw_audio_video_samples": delivery_internal["item_count"], "independence": "not_independent", "manual_vocal_listening": "not_performed", "source": "research/communication-job-delivery-internal-observations.json"},
            "corpus_identity_review": {"status": identity_review["status"], "queued_item_count": identity_review["item_count"], "registry_row_count": identity_review["registry_row_count"], "completed_independent_reviews": 0, "source": "research/corpus-identity-review-workbook.json"},
            "delivery_measurement_preflight": {"status": delivery_measurements["status"], "sample_count": delivery_measurements["item_count"], "matched_sample_count": delivery_measurements["matched_sample_count"], "unmatched_sample_count": delivery_measurements["unmatched_sample_count"], "source": "research/communication-job-delivery-measurement-preflight.json"},
            "communication_job_curriculum": {"status": curriculum_index["status"], "lesson_count": curriculum_index["lesson_count"], "source": "research/communication-job-curriculum-index.json"},
            "communication_job_mobile_lessons": {"status": mobile_lessons["status"], "lesson_count": mobile_lessons["lesson_count"], "completed_records": 0, "source": "research/communication-job-mobile-lessons.json"},
            "listener_stimulus_manual_review": {"status": stimulus_review["status"], "pair_count": stimulus_review["item_count"], "completed_independent_reviews": 0, "locked_pairs": 0, "source": "research/communication-job-listener-stimulus-review-workbook.json"},
            "speech_function_candidate_review": {"status": functions["status"], "queued_item_count": functions["item_count"], "completed_independent_reviews": 0, "source": "research/corpus-function-independent-review-workbook.json"},
            "recurrence_candidate_review": {"status": recurrence["status"], "queued_item_count": recurrence["item_count"], "completed_independent_reviews": 0, "source": "research/corpus-recurrence-independent-review-workbook.json"},
            "delivery_evidence": {"status": media["status"], "selected_video_count": media["selected_video_count"], "raw_audio_video_present": media["raw_audio_video_present_count"], "raw_audio_video_with_transcript": media["raw_audio_video_with_transcript_count"], "raw_audio_video_without_transcript": media["raw_audio_video_without_transcript_count"], "internal_manual_reviews": media["internal_manual_review_count"], "raw_only_visual_audit_items": raw_only_visual["item_count"], "raw_only_visual_audit_status": raw_only_visual["status"], "independent_review_items": media_independent["item_count"], "completed_independent_reviews": 0, "source": "research/multimodal-coverage-audit.json"},
            "full_corpus_media_coverage": {"status": full_media["status"], "video_count": full_media["video_count"], "raw_audio_video_present": full_media["counts"].get("raw_audio_video_present", 0), "derived_features_only": full_media["counts"].get("derived_features_only", 0), "transcript_only_no_local_media": full_media["counts"].get("transcript_only_no_local_media", 0), "source": "research/full-corpus-media-coverage.json"},
            "full_corpus_media_recovery": {"status": media_recovery["status"], "queued_item_count": media_recovery["item_count"], "source": "research/full-corpus-media-recovery-queue.json"},
            "shared_lessons": {"status": cards["status"], "draft_card_count": cards["card_count"], "promotion_ready_card_count": 0, "source": "research/shared-lesson-cards.json"},
            "promotion_readiness": {"status": promotion_readiness["status"], "card_count": promotion_readiness["card_count"], "promotion_ready_count": promotion_readiness["promotion_ready_count"], "blocked_card_count": sum(bool(row["blockers"]) for row in promotion_readiness["cards"]), "source": "research/communication-job-promotion-readiness.json"},
            "learner_check": {"status": learner["status"], "task_count": learner["task_count"], "completed_records": 0, "source": "research/shared-learner-check.json"},
            "listener_outcomes": {"status": listener["status"], "task_count": len(listener["listener_tasks"]), "stimulus_pairs_locked": listener["stimulus_pairs_locked"], "completed_records": 0, "source": "research/communication-job-listener-outcome-protocol.json"},
        },
        "next_required_gates": [
            "obtain independent transcript-function review exports and preserve disagreements",
            "obtain independent recurrence review exports and adjudicate disagreements",
            "obtain independent exact phrase-form review exports and adjudicate form, identity and recurrence disagreements",
            "populate and independently review counterexample, alternate-function, confound and misuse-limit records for all 18 jobs",
            "independently verify speaker/event identity before treating cross-job or holdout comparisons as recurrence evidence",
            "complete manual delivery observations for the 36 two-sample-per-job queue and obtain independent review",
            "complete independent speaker/event identity and duplication review for the 395 reviewed queue items",
            f"manually inspect the {delivery_measurements['matched_sample_count']} aligned delivery measurements and record proxy limits, missingness and nonverbal/setting observations",
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
        f"| Exact caption evidence bank | `{evidence_bank['status']}` | {evidence_bank['summary']['function_record_count']} function records / {evidence_bank['summary']['caption_segment_record_count']} caption segments |",
        f"| Communication-job cards | `{job_cards['status']}` | {job_cards['card_count']} provisional cards / 0 validated |",
        f"| Communication-job learner check | `{job_learner['status']}` | {job_learner['card_count']} cards / {job_learner['task_count']} tasks / {job_learner['exact_phrase_form_count']} exact forms linked / 0 records |",
        f"| Communication-job listener outcomes | `{job_listener['status']}` | {len(job_listener['patterns'])} jobs / {len(job_listener['listener_tasks'])} tasks / stimuli locked: {job_listener['stimulus_pairs_locked']} |",
        f"| Listener stimulus preflight | `{stimulus_preflight['status']}` | {stimulus_preflight['pair_count']} pairs / {stimulus_preflight['summary']['pairs_requiring_manual_review']} manual reviews required |",
        f"| Exact phrase-form inventory | `{phrase_inventory['status']}` | {phrase_inventory['form_count']} forms / {phrase_inventory['eligible_caption_segment_count']} segments |",
        f"| Exact phrase-form independent review | `{phrase_form_review['status']}` | {phrase_form_review['item_count']} forms queued / 0 completed |",
        f"| Delivery evidence index | `{delivery_index['status']}` | {delivery_index['coverage']['internal_manual_observation_count']} internal / {delivery_index['coverage']['independent_review_count']} independent observations |",
        f"| Shared evidence model | `{evidence_model['status']}` | {len(evidence_model['entity_types'])} entity types / web-mobile contract |",
        f"| Counterexample library | `{counterexamples['status']}` | {counterexamples['job_count']} jobs / {counterexamples['item_count']} required slots / 0 completed |",
        f"| Counterexample candidate queue | `{counterexample_candidates['status']}` | {counterexample_candidates['candidate_count']} routed / {counterexample_candidates['source_linked_candidate_count']} source-linked / 0 confirmed |",
        f"| Cross-job comparison | `{cross_comparison['status']}` | {cross_comparison['job_count']} jobs / {cross_comparison['pair_count']} pairs / {cross_comparison['video_denominator']} eligible videos |",
        f"| Communication-job delivery sampling | `{delivery_sampling['status']}` | {delivery_sampling['job_count']} jobs / {delivery_sampling['item_count']} samples / {delivery_sampling['coverage_summary']['raw_audio_video_items']} raw A/V / 0 observations |",
        f"| Internal midpoint-frame delivery observations | `{delivery_internal['status']}` | {delivery_internal['item_count']} raw A/V frames / not independent / manual vocal listening not performed |",
        f"| Corpus identity review | `{identity_review['status']}` | {identity_review['item_count']} queue items / {identity_review['registry_row_count']} registry rows / 0 completed |",
        f"| Delivery measurement preflight | `{delivery_measurements['status']}` | {delivery_measurements['item_count']} samples / {delivery_measurements['matched_sample_count']} aligned / {delivery_measurements['unmatched_sample_count']} unmatched |",
        f"| Communication-job curriculum | `{curriculum_index['status']}` | {curriculum_index['lesson_count']} integrated provisional lessons |",
        f"| Communication-job mobile lessons | `{mobile_lessons['status']}` | {mobile_lessons['lesson_count']} lessons / 0 learner records |",
        f"| Listener stimulus manual review | `{stimulus_review['status']}` | {stimulus_review['item_count']} pairs / 0 completed / 0 locked |",
        f"| Function review | `{functions['status']}` | {functions['item_count']} queued / 0 completed |",
        f"| Recurrence review | `{recurrence['status']}` | {recurrence['item_count']} queued / 0 completed |",
        f"| Delivery evidence | `{media['status']}` | {media['raw_audio_video_present_count']} raw-complete ({media['raw_audio_video_without_transcript_count']} without transcript) / {media['internal_manual_review_count']} internal reviewed |",
        f"| Full-corpus media coverage | `{full_media['status']}` | {full_media['video_count']} videos / {full_media['counts'].get('raw_audio_video_present', 0)} raw A/V / {full_media['counts'].get('derived_features_only', 0)} derived-only / {full_media['counts'].get('transcript_only_no_local_media', 0)} transcript-only |",
        f"| Full-corpus media recovery | `{media_recovery['status']}` | {media_recovery['item_count']} queued missing/derived items |",
        f"| Shared lessons | `{cards['status']}` | {cards['card_count']} drafts / 0 promotion-ready |",
        f"| Promotion readiness | `{promotion_readiness['status']}` | {promotion_readiness['card_count']} cards / {promotion_readiness['promotion_ready_count']} promotion-ready / {sum(bool(row['blockers']) for row in promotion_readiness['cards'])} blocked |",
        f"| Learner check | `{learner['status']}` | {learner['task_count']} tasks / 0 records |",
        f"| Listener outcomes | `{listener['status']}` | {len(listener['listener_tasks'])} tasks / stimuli locked: {listener['stimulus_pairs_locked']} / 0 records |",
        "", "## Required gates", "",
    ]
    lines.extend(f"- {gate}" for gate in report["next_required_gates"])
    (ROOT / "writeups/end-to-end-status.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(out), "transcript_reviews": transcript_count, "caption_count": caption_count, "next_gate_count": len(report["next_required_gates"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
