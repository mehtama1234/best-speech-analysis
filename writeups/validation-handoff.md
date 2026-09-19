# Validation handoff

Status: **instruments ready; no human records received**.

These are operational instruments and instructions, not validation results. No reviewer, learner or listener judgment is included.

Before selecting examples, use the [corpus lesson inventory](corpus-lesson-index.html), [exact phrase-form inventory](corpus-phrase-form-inventory.html), [evidence bank](corpus-evidence-bank.html), [provisional cards](communication-job-cards.html), [delivery inventory](communication-job-delivery-inventory.md) and [shared evidence model](shared-evidence-model.md). These are discovery and routing surfaces; none is proof that a pattern works.

## Independent review gates

### corpus_identity — 395 items

Verify speaker, event, upload correspondence, source provenance and duplication status before recurrence denominators are used.

- Workbook: `research/corpus-identity-review-workbook.json`
- Browser form: `writeups/corpus-identity-review-workbook.html`
- Validator: `scripts/validate_corpus_identity_review.py`
- Summarizer: `scripts/summarize_corpus_identity_reviews.py`
- Independence: Reviewer must not be the person who created the transcript corpus, labels or identity candidate groups.
- Does not establish: function, delivery effectiveness, listener outcomes

### corpus_function — 187 items

Check heuristic speech-function labels in surrounding transcript context.

- Workbook: `research/corpus-function-independent-review-workbook.json`
- Browser form: `writeups/corpus-function-independent-review-workbook.html`
- Validator: `scripts/validate_corpus_function_review.py`
- Summarizer: `scripts/summarize_corpus_function_review.py`
- Independence: Reviewer must not have created the atlas, candidate labels or review queue.
- Does not establish: delivery effectiveness, speaker intent, listener outcomes

### phrase_recurrence — 192 items

Check whether phrase-form hits support the proposed function family in context.

- Workbook: `research/corpus-recurrence-independent-review-workbook.json`
- Browser form: `writeups/corpus-recurrence-independent-review-workbook.html`
- Validator: `scripts/validate_corpus_recurrence_review.py`
- Summarizer: `scripts/summarize_corpus_recurrence_review.py`
- Independence: Reviewer must not have created the atlas, phrase queue or candidate labels.
- Does not establish: effectiveness, causality, universal recurrence

### exact_phrase_form — 50 items

Check retrieved word forms in sampled train/holdout contexts before using exact wording or recurrence counts.

- Workbook: `research/corpus-phrase-form-independent-review-workbook.json`
- Browser form: `writeups/corpus-phrase-form-independent-review-workbook.html`
- Validator: `scripts/validate_corpus_phrase_form_review.py`
- Summarizer: `scripts/summarize_corpus_phrase_form_reviews.py`
- Independence: Reviewer must not have created the phrase inventory, regex families, candidate mechanisms or workbook.
- Does not establish: delivery effectiveness, speaker intent, listener outcomes, causality

### delivery — 36 items

Complete manual observations for transcript alignment, vocal timing, visual action, setting, editing, identity and accessibility across the two-sample-per-job queue.

- Workbook: `research/communication-job-delivery-sampling.json`
- Browser form: `writeups/communication-job-delivery-sampling.html`
- Validator: `scripts/validate_communication_job_delivery_review.py`
- Independence: A reviewer code and conflict statement are required; an export is not independent merely because those fields are present.
- Does not establish: emotion, intent, audience response, effectiveness

### counterexamples — 90 items

Check absence, failure, alternate function, confound/setting and misuse limits for every provisional job.

- Workbook: `research/communication-job-counterexample-workbook.json`
- Browser form: `writeups/communication-job-counterexample-workbook.html`
- Validator: `scripts/validate_communication_job_counterexample_review.py`
- Independence: Reviewer must not be the person who created the original card interpretation or candidate counterexample selection.
- Does not establish: effectiveness, causality, universal failure

### multimodal — 21 items

Check transcript alignment, speaker/setting observations, modality limits and safety boundaries.

- Workbook: `research/multimodal-independent-review-workbook.json`
- Browser form: `writeups/multimodal-independent-review-workbook.html`
- Validator: `scripts/validate_multimodal_independent_review.py`
- Independence: Reviewer must not be the internal review author or packet creator.
- Does not establish: emotion, intent, audience response, effectiveness

### vertical_slice — 50 items

Review the five linked lesson packets and their evidence boundaries.

- Workbook: `research/vertical-slice-01-independent-review-workbook.json`
- Browser form: `writeups/vertical-slice-01-independent-review-workbook.html`
- Validator: `scripts/validate_vertical_slice_review_record.py`
- Independence: Reviewer must not be the packet creator or original interpreter.
- Does not establish: listener outcomes, causal communication effects

## Learning and outcome gates

### listener_stimulus_review — 18 tasks

Review proposition equivalence, readability, accessibility, safety and blinding before locking listener pairs; then preserve an explicit adjudicator decision.

- Protocol: `research/communication-job-listener-stimuli-draft.json`
- Form: `writeups/communication-job-listener-stimulus-review-workbook.html`
- Validator: `scripts/validate_listener_stimulus_review.py`
- Adjudication form: `writeups/communication-job-listener-stimulus-adjudication.html`
- Adjudication validator: `scripts/validate_listener_stimulus_adjudication.py`
- Status: `manual_equivalence_review_pending`
- Does not establish: listener comprehension, real-world effectiveness

### learner_teachability — 72 tasks

Test whether learners can recognize, explain, transfer and safely bound all 18 provisional communication-job cards.

- Protocol: `research/communication-job-learner-check.json`
- Form: `writeups/communication-job-learner-check.html`
- Validator: `scripts/validate_communication_job_learner_record.py`
- Status: `protocol_drafted_not_run`
- Does not establish: original pattern effectiveness, population learning effects

### listener_outcomes — 6 tasks

Test comprehension, recall and reported cognitive load for matched control versus pattern-informed versions of the 18 provisional communication-job cards.

- Protocol: `research/communication-job-listener-outcome-protocol.json`
- Form: `writeups/communication-job-listener-record.html`
- Validator: `scripts/validate_communication_job_listener_record.py`
- Status: `design_complete_not_run`
- Does not establish: universal effectiveness, speaker intent

## Procedure

1. Use a reviewer code and record conflicts; do not use the original analyst for an independent judgment.
2. Inspect full surrounding context and source media where available; use indeterminate when evidence is insufficient.
3. Export the browser form without hand-editing judgment fields.
4. Run the named validator before returning the export.
5. Preserve disagreements; do not silently adjudicate them in the original analysis.
6. Do not send credentials, raw recordings or identifying participant information through these forms.

No gate may be marked complete merely because its workbook or form exists. Independent review records must come from a distinct reviewer; learner and listener records must be consented, pseudonymous and validated.
