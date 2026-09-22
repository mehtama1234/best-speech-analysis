# Autonomous release audit

Status: **release_audit_passed**.

This command verifies repository-local artifact joins, browser behavior, recovery routing and manifest integrity. It does not establish independent review, learner outcomes, listener outcomes or communication effectiveness.

Steps passed: **17/17**.

| Step | Result | Command | Output |
|---|---:|---|---|
| `core release receipt preflight` | `0` | `/usr/bin/python3 scripts/run_autonomous_release_audit.py` | autonomous release audit: release_audit_passed (14/14) |
| `reproducibility manifest preflight build` | `0` | `/usr/bin/python3 scripts/build_reproducibility_manifest.py` | {
  "output": "research/reproducibility-manifest.json",
  "artifact_count": 377,
  "coverage": {
    "unique_inventory_videos": 480,
    "nonempty_transcript_videos": 395,
    "full_context_reviews": 395,
    "inspected_captions": 102816
  }
} |
| `full repository test suite` | `0` | `/usr/bin/python3 -m unittest discover -s tests -v` | wrote delivery inventory (18 jobs; 36 samples)
{
  "output": "writeups/corpus-learning-map.md",
  "jobs": 18,
  "phrases": 10,
  "pairs": 10
}
{
  "output": "research/delivery-proxy-candidate-atlas.json",
  "html_output": "writeups/delivery-proxy-candidate-atlas.html",
  "counts": {
    "candidate_record_count": 1505,
    "candidate_video_count": 188,
    "job_count": 19,
    "exact_alignment_count": 1505,
    "overlap_only_count": 0
  }
}
{
  "output": "research/full-corpus-media-coverage.json",
  "video_count": 395,
  "counts": {
    "derived_features_only": 5,
    "raw_audio_video_present": 354,
    "transcript_only_no_local_media": 35,
    "video_only": 1
  }
}
{
  "output": "research/full-corpus-media-recovery-queue.json",
  "item_count": 41,
  "counts": {
    "by_priority": {
      "feature_backed_next_candidate": 5,
      "fixed_corpus_transcript_only": 36
    },
    "by_media_state": {
      "derived_features_only": 5,
      "transcript_only_no_local_media": 35,
      "video_only": 1
    },
    "by_video_status": {
      "downloaded": 1,
      "failed:1": 40
    }
  }
}
{
  "output": "research/full-delivery-proxy-index.json",
  "counts": {
    "feature_report_count": 364,
    "with_audio_windows": 364,
    "with_sampled_frames": 364,
    "with_aligned_transcript": 357,
    "with_face_detection_counts": 364
  }
}
wrote writeups/learner-field-guide.md (18 jobs)
{
  "output": "writeups/phrase-transfer-guide.md",
  "forms": 50
}
{
  "output": "writeups/unclassified-lesson-leads.md",
  "lead_count": 160
}
wrote research/vertical-slice-01-independent-review-workbook.json, writeups/vertical-slice-01-independent-review-workbook.md and writeups/vertical-slice-01-independent-review-workbook.html (50 items)
wrote writeups/vertical-slice-01-learner-check.html
wrote research/vertical-slice-01-media-audit.json and writeups/vertical-slice-01-media-audit.md
media audit: 15/16 unique IDs have raw media; contradictions=0
wrote research/vertical-slice-01-validation-audit.json and writeups/vertical-slice-01-validation-audit.md
validation audit: 0/5 packets ready; learner=protocol_drafted_not_run
vertical slice valid: five partial packets, linked lessons, source audit, learner protocol
vertical slice 02 drafts valid: 3 packets, not promotion-ready |
| `browser runtime smoke` | `0` | `/usr/bin/python3 scripts/run_autonomous_browser_smoke.py` | autonomous browser smoke: core_browser_smoke_passed (17/17) |
| `compound triad practice browser smoke` | `0` | `/usr/bin/python3 scripts/check_compound_triad_browser.py` | compound triad browser smoke: 24 triads, scaffold, save, reload and JSON export passed |
| `media recovery integrity` | `0` | `/usr/bin/python3 scripts/validate_autonomous_media_recovery.py` | autonomous media recovery valid: 41 routed records, partial media kept out of raw A/V coverage |
| `acceptance matrix build` | `0` | `/usr/bin/python3 scripts/build_end_to_end_acceptance_matrix.py` | {
  "output": "research/end-to-end-acceptance-matrix.json",
  "open_requirement_count": 9
} |
| `shared evidence model build` | `0` | `/usr/bin/python3 scripts/build_shared_evidence_model.py` | {
  "exact_phrase_forms": {
    "source": "research/corpus-phrase-form-inventory.json",
    "form_count": 50,
    "status": "heuristic_exact_phrase_inventory_not_validated"
  },
  "exact_caption_evidence": {
    "source": "research/corpus-evidence-bank.json",
    "function_record_count": 4016,
    "caption_segment_record_count": 102816,
    "status": "transcript_evidence_navigation_not_validated"
  },
  "validated_shared_lesson_cards": {
    "source": "research/shared-lesson-cards.json",
    "card_count": 18,
    "status": "18_draft_cards_not_validated"
  },
  "provisional_job_cards": {
    "source": "research/communication-job-cards.json",
    "card_count": 18,
    "status": "provisional_transcript_cards_not_validated"
  },
  "delivery": {
    "source": "research/delivery-evidence-index.json",
    "internal_observation_count": 21,
    "independent_observation_count": 0,
    "status": "delivery_evidence_reconciled_independent_review_pending"
  },
  "learner": {
    "source": "research/communication-job-learner-check.json",
    "card_count": 18,
    "task_count": 72,
    "completed_records": 0,
    "status": "protocol_drafted_not_run"
  },
  "listener": {
    "source": "research/communication-job-listener-outcome-protocol.json",
    "pattern_count": 18,
    "stimulus_pairs_locked": false,
    "completed_records": 0,
    "status": "design_complete_not_run"
  },
  "counterexamples": {
    "source": "research/communication-job-counterexample-workbook.json",
    "job_count": 18,
    "queued_slot_count": 90,
    "completed_records": 0,
    "status": "template_not_completed"
  },
  "counterexample_candidates": {
    "source": "research/communication-job-counterexample-candidate-queue.json",
    "candidate_count": 90,
    "source_linked_candidate_count": 54,
    "confirmed_counterexample_count": 0,
    "status": "candidate_queue_not_independently_reviewed"
  },
  "mobile_lessons": {
    "source": "research/communication-job-mobile-lessons.json",
    "lesson_count": 18,
    "status": "mobile_payload_provisional_not_validated"
  }
} |
| `native client contract build` | `0` | `/usr/bin/python3 scripts/build_native_client_contracts.py` | native client contracts generated: 5 files, 13 entities |
| `native TypeScript compile` | `0` | `npx --yes -p typescript@5.7.2 tsc --noEmit --target ES2020 --strict clients/generated/shared_evidence_contract.ts clients/examples/practice_record_helpers.ts clients/examples/mobile_lesson_helpers.ts` |  |
| `cross-artifact consistency` | `0` | `/usr/bin/python3 scripts/validate_cross_artifact_consistency.py` | cross-artifact consistency valid: status, acceptance, readiness and gates reconcile |
| `fail-closed promotion readiness` | `0` | `/usr/bin/python3 scripts/check_promotion_readiness.py --allow-blocked` | promotion readiness: promotion_blocked
open requirements: 9; open gates: 10; ready cards: 0/18
next gate: identity (395 items) -> writeups/corpus-identity-review-workbook.html; validate with scripts/validate_corpus_identity_review.py
next gate: function (187 items) -> writeups/corpus-function-independent-review-workbook.html; validate with scripts/validate_corpus_function_review.py
next gate: recurrence (192 items) -> writeups/corpus-recurrence-independent-review-workbook.html; validate with scripts/validate_corpus_recurrence_review.py
next gate: phrase_forms (50 items) -> writeups/corpus-phrase-form-independent-review-workbook.html; validate with scripts/validate_corpus_phrase_form_review.py
next gate: multimodal (21 items) -> writeups/multimodal-independent-review-workbook.html; validate with scripts/validate_multimodal_independent_review.py
next gate: delivery (36 items) -> writeups/communication-job-delivery-sampling.html; validate with scripts/validate_communication_job_delivery_review.py
next gate: counterexamples (90 items) -> writeups/communication-job-counterexample-workbook.html; validate with scripts/validate_communication_job_counterexample_review.py
next gate: learner (72 items) -> writeups/communication-job-learner-check.html; validate with scripts/validate_communication_job_learner_record.py
next gate: listener_stimuli (18 items) -> writeups/communication-job-listener-stimulus-review-workbook.html; validate with scripts/validate_listener_stimulus_review.py
next gate: listener_outcomes (18 items) -> writeups/communication-job-listener-record.html; validate with scripts/validate_communication_job_listener_record.py
A repository checkpoint, protocol, synthetic dry run or passing validator is not human validation or communication effectiveness evidence. |
| `public claim-boundary wording` | `0` | `/usr/bin/python3 scripts/check_public_claim_boundaries.py` | {
  "schema_version": "1.0",
  "audit_id": "public-claim-boundaries",
  "status": "public_claim_boundaries_valid",
  "scanned_document_count": 23,
  "violations": [],
  "missing_disclosures": [],
  "claim_boundary": "This checks selected wording guardrails; it does not validate corpus meaning, human review or communication effectiveness."
} |
| `model-assisted gate readiness` | `0` | `/usr/bin/python3 scripts/run_model_assisted_gate_judge.py` | model-assisted gate judge: model_assisted_readiness_complete_human_evidence_open (10/10 instruments ready) |
| `aggregate end-to-end audit` | `0` | `/usr/bin/python3 scripts/build_autonomous_end_to_end_audit.py` | autonomous end-to-end audit: autonomous_release_candidate_reconciled_not_promotion_validated (27/27) |
| `reproducibility manifest build` | `0` | `/usr/bin/python3 scripts/build_reproducibility_manifest.py` | {
  "output": "research/reproducibility-manifest.json",
  "artifact_count": 377,
  "coverage": {
    "unique_inventory_videos": 480,
    "nonempty_transcript_videos": 395,
    "full_context_reviews": 395,
    "inspected_captions": 102816
  }
} |
| `reproducibility manifest validation` | `0` | `/usr/bin/python3 scripts/validate_reproducibility_manifest.py` | reproducibility manifest valid: artifact hashes and coverage reconcile |
