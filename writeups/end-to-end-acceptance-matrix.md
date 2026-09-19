# End-to-end acceptance matrix

Status: **research checkpoint not complete**.

This matrix audits requirements and evidence status; it is not proof that pending human reviews or outcome studies have occurred.

| Requirement | Status | Evidence | Remaining |
|---|---|---|---|
| `inventory_and_provenance` | `complete_for_fixed_corpus` | `research/full-reading-queue.json`, `research/corpus-identity-review-workbook.json` | Complete independent identity/duplication decisions before promotion. |
| `full_context_transcript` | `complete_for_fixed_corpus` | `research/full-context-reviews.json`, `research/corpus-evidence-bank.json` | Transcript evidence does not establish delivery or outcomes. |
| `exact_language_and_forms` | `provisional_transcript_evidence` | `research/communication-job-cards.json`, `research/corpus-phrase-form-inventory.json`, `writeups/communication-job-curriculum.html`, `writeups/repeatable-communication-patterns.md` | Complete independent phrase-form review and adjudication. |
| `function_and_mechanism` | `provisional_transcript_interpretation` | `research/communication-job-cards.json`, `scripts/validate_communication_job_cards.py` | Independently review 187 candidate function items. |
| `verbal_vocal_nonverbal_setting` | `partial_internal_coverage` | `research/multimodal-coverage-audit.json`, `research/communication-job-delivery-sampling.json`, `research/communication-job-delivery-measurement-preflight.json`, `research/corpus-learning-coverage-audit.json`, `research/full-corpus-media-coverage.json`, `research/full-delivery-proxy-index.json`, `research/full-corpus-delivery-inspection.json`, `writeups/full-corpus-delivery-inspection.html`, `research/full-corpus-delivery-review-workbook.json`, `writeups/full-corpus-delivery-review-workbook.html` | Complete manual observation and independent multimodal review; missing media remains explicit. |
| `cross_talk_recurrence` | `provisional_transcript_comparison` | `research/communication-job-cross-comparison.json`, `research/corpus-recurrence-independent-review-workbook.json` | Independently review 192 recurrence candidates and identity splits. |
| `counterexamples_and_limits` | `queued_not_completed` | `research/communication-job-counterexample-workbook.json`, `writeups/communication-job-counterexample-workbook.html` | Populate, independently review and adjudicate the slots; do not force candidates. |
| `practice_and_shared_curriculum` | `provisional_constructed` | `research/communication-job-curriculum-index.json`, `research/communication-job-mobile-lessons.json`, `writeups/repeatable-communication-patterns.md`, `scripts/validate_communication_job_curriculum.py` | Promotion depends on independent evidence and learner observations. |
| `independent_review` | `not_started` | `research/corpus-function-independent-review-workbook.json`, `research/corpus-recurrence-independent-review-workbook.json`, `research/multimodal-independent-review-workbook.json` | Obtain and adjudicate independent exports. |
| `learner_validation` | `protocol_ready_not_run` | `research/communication-job-learner-check.json`, `scripts/summarize_communication_job_learner_records.py` | Run the consented learner protocol and validate exports. |
| `listener_outcome_separation` | `protocol_ready_not_run` | `research/communication-job-listener-outcome-protocol.json`, `scripts/summarize_communication_job_listener_records.py` | Complete independent stimulus review, lock pairs, then run the blinded study. |
| `claim_boundary_and_missingness` | `contract_and_validators_ready` | `research/shared-evidence-model.json`, `research/end-to-end-status.json`, `scripts/validate_end_to_end_status.py` | Recheck these boundaries whenever evidence is promoted. |

Open requirements: **9**. A protocol, workbook or passing validator is not counted as completed human evidence.
