# External Review Launch Manifest

Status: **operations ready; no human records received**.

Start with operation 1. Give reviewers the form and instructions, never the private pattern key. Preserve each export separately, validate it, compare independent exports where available, and adjudicate disagreements without silently editing decisions.

| Order | Operation | Items | Status | Depends on | Reviewer pack | Validator |
|---:|---|---:|---|---|---|---|
| 1 | `priority_pattern_review` | 162 | `ready_no_human_records` | — | `deliverables/recovered-pattern-priority-reviewer-pack.zip` | `scripts/validate_recovered_pattern_priority_review_export.py` |
| 2 | `vertical_slice_evidence_review` | 50 | `ready_no_human_records` | priority_pattern_review | `—` | `scripts/validate_vertical_slice_review_record.py` |
| 3 | `identity_function_recurrence` | 824 | `ready_no_human_records` | priority_pattern_review | `—` | `scripts/validate_corpus_identity_review.py; scripts/validate_corpus_function_review.py; scripts/validate_corpus_phrase_form_review.py; scripts/validate_corpus_recurrence_review.py` |
| 4 | `delivery_and_multimodal` | 57 | `ready_manual_review_pending` | vertical_slice_evidence_review | `—` | `scripts/validate_communication_job_delivery_review.py; scripts/validate_multimodal_independent_review.py` |
| 5 | `counterexamples` | 90 | `ready_no_human_records` | vertical_slice_evidence_review | `—` | `scripts/validate_communication_job_counterexample_review.py` |
| 6 | `learner_teachability` | 72 | `protocol_ready_no_participant_records` | vertical_slice_evidence_review | `—` | `scripts/validate_communication_job_learner_record.py` |
| 7 | `listener_stimulus_review` | 18 | `ready_no_human_records` | vertical_slice_evidence_review | `—` | `scripts/validate_listener_stimulus_review.py` |
| 8 | `listener_outcomes` | 18 | `blocked_until_stimuli_locked` | listener_stimulus_review | `—` | `scripts/validate_communication_job_listener_record.py` |

Promotion-ready cards remain **0/18**. Synthetic browser smoke and repository validators verify the instruments, not the people or outcomes they are designed to collect.
