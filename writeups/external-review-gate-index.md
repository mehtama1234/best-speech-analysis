# External review and data-collection gate index

Status: **operations ready; research evidence incomplete**.

This index routes independent review and participant-data collection. The presence of a form, validator or comparator is not evidence that a gate has been completed.

| Gate | Status | Items/tasks | Form | Validator | Comparison/summary |
|---|---|---:|---|---|---|
| `identity` | `metadata_preflight_independent_review_pending` | 395 | `writeups/corpus-identity-review-workbook.html` | `scripts/validate_corpus_identity_review.py` | `scripts/compare_corpus_identity_reviews.py` |
| `function` | `template_not_completed` | 187 | `writeups/corpus-function-independent-review-workbook.html` | `scripts/validate_corpus_function_review.py` | `scripts/compare_corpus_function_reviews.py` |
| `recurrence` | `template_not_completed` | 192 | `writeups/corpus-recurrence-independent-review-workbook.html` | `scripts/validate_corpus_recurrence_review.py` | `scripts/compare_corpus_recurrence_reviews.py` |
| `phrase_forms` | `template_not_completed` | 50 | `writeups/corpus-phrase-form-independent-review-workbook.html` | `scripts/validate_corpus_phrase_form_review.py` | `scripts/compare_corpus_phrase_form_reviews.py` |
| `multimodal` | `template_not_completed` | 21 | `writeups/multimodal-independent-review-workbook.html` | `scripts/validate_multimodal_independent_review.py` | `scripts/compare_multimodal_independent_reviews.py` |
| `delivery` | `queue_built_manual_observation_pending` | 36 | `writeups/communication-job-delivery-sampling.html` | `scripts/validate_communication_job_delivery_review.py` | `scripts/compare_communication_job_delivery_reviews.py` |
| `counterexamples` | `template_not_completed` | 90 | `writeups/communication-job-counterexample-workbook.html` | `scripts/validate_communication_job_counterexample_review.py` | `scripts/summarize_communication_job_counterexamples.py` |
| `learner` | `protocol_drafted_not_run` | 72 | `writeups/communication-job-learner-check.html` | `scripts/validate_communication_job_learner_record.py` | `scripts/summarize_communication_job_learner_records.py` |
| `listener_stimuli` | `manual_equivalence_review_pending` | 18 | `writeups/communication-job-listener-stimulus-review-workbook.html` | `scripts/validate_listener_stimulus_review.py` | `scripts/compare_listener_stimulus_reviews.py` |
| `listener_outcomes` | `design_complete_not_run` | 18 | `writeups/communication-job-listener-record.html` | `scripts/validate_communication_job_listener_record.py` | `scripts/summarize_communication_job_listener_records.py` |

## Operating rule

Use the form only after reading its claim boundary. Validate every export, compare independent exports where a comparator is supplied, preserve disagreements, and adjudicate before changing any research denominator or lesson status.
