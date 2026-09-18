# Validation handoff

Status: **instruments ready; no human records received**.

These are operational instruments and instructions, not validation results. No reviewer, learner or listener judgment is included.

Before selecting examples, use the [corpus transcript-derived lesson
inventory](corpus-lesson-index.html) to search the communication functions and
structural relations recorded across all 395 completed transcript reviews. It
is a discovery index only; its entries still require the independent review,
delivery, learner and listener gates below.
The [provisional shared function taxonomy](corpus-function-taxonomy.md) is a
comparison aid for those free-text labels; its unclassified queue must not be
treated as evidence of absence.
Use the [exact-caption evidence bank](corpus-evidence-bank.html) to inspect the
retained words and timestamped source before reviewing a function or lesson.

## Independent review gates

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

### learner_teachability — 32 tasks

Test whether learners can recognize, explain, transfer and safely bound all eight current draft communication patterns.

- Protocol: `research/shared-learner-check.json`
- Form: `writeups/shared-learner-check.html`
- Validator: `scripts/validate_shared_learner_record.py`
- Status: `protocol_drafted_not_run`
- Does not establish: original pattern effectiveness, population learning effects

### listener_outcomes — 6 tasks

Test listener comprehension and immediate recall of matched speech versions, separately from learner teachability and from claims about trust, persuasion or behavior.

- Protocol: `research/listener-outcome-protocol.json`
- Form: `writeups/listener-outcome-record.html`
- Validator: `scripts/validate_listener_outcome_record.py`
- Status: `design_complete_not_run`
- Does not establish: universal effectiveness, speaker intent

## Procedure

1. Use a reviewer code and record conflicts; do not use the original analyst for an independent judgment.
2. Inspect full surrounding context and source media where available; use indeterminate when evidence is insufficient.
3. Export the browser form without hand-editing judgment fields.
4. Run the named validator before returning the export.
5. Preserve disagreements; do not silently adjudicate them in the original analysis.
6. Do not send credentials, raw recordings or identifying participant information through these forms.

No gate may be marked complete merely because its workbook or form exists.
