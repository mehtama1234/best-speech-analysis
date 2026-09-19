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
The [exact phrase-form inventory](corpus-phrase-form-inventory.html) exposes
the actual matched wording behind the phrase families; every form still needs
full-context and independent recurrence review.
The [delivery evidence index](delivery-evidence-index.md) is the accounting
surface for raw media, derived proxies and internal multimodal notes; the
independent workbook remains the authoritative review gate.
The [shared evidence model](shared-evidence-model.md) is the client-facing
contract; it must not be interpreted as proof that any pending entity has been
validated.
Use the [exact-caption evidence bank](corpus-evidence-bank.html) to inspect the
retained words and timestamped source before reviewing a function or lesson.
The [communication-job cards](communication-job-cards.html) are a provisional
practice surface; reviewers should check their mechanism language, examples,
limits and non-fit warnings rather than treating the cards as findings.
Their delivery sections contain only bounded internal observations; the blank
multimodal workbook remains the independent gate.
The expanded [18-card learner check](communication-job-learner-check.html) is
also unrun; exported records must pass its validator before any teachability
summary is written.
Its tasks now expose exact phrase forms for eight indexed job families and
preserve an explicit no-direct-match status for the other ten; this is a
curriculum link, not evidence that any phrase works.
The [18-job listener protocol](communication-job-listener-outcome-protocol.md)
remains a separate outcome gate; it cannot start until matched stimuli are
independently reviewed, pretested and locked. The current [draft stimulus
bank](communication-job-listener-stimuli-draft.md) is not yet that locked set.
The [stimulus preflight](communication-job-stimuli-preflight.md) is only an
automated screen; its 18 pairs still need independent content-equivalence,
readability, accessibility and safety review.

The [communication-job counterexample workbook](communication-job-counterexample-workbook.html)
requires five explicit checks for every provisional job: absence with speech
still working, presence with an observable failure or limit, alternate
function, confound/setting, and misuse or copying risk. It is blank and must
not be treated as evidence until independently completed.
The [cross-job comparison](communication-job-cross-comparison.html) is the
current denominator surface for comparing jobs; verify speaker and event
identity before promoting its video-level comparisons to recurrence claims.
The [18-job delivery sampling queue](communication-job-delivery-sampling.html)
is the next manual multimodal collection surface: 36 samples with transcript
alignment, media state and fields for vocal timing, audio limits, visual
observations, editing, setting and accessibility. It contains no observations
yet.
The [delivery measurement preflight](communication-job-delivery-measurement-preflight.md)
contains 32 aligned proxy-measurement records and four unmatched samples. Treat
these as reproducible navigation/measurement aids only; manual observation and
independent review remain required.
The [corpus identity workbook](corpus-identity-review-workbook.html) separately
requires independent verification for all 395 reviewed queue items, including
speaker, event, upload correspondence and duplicate/compilation status. Do not
promote cross-video comparisons until this gate is addressed.

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

### exact_phrase_form — 50 items

Check the actual retrieved word forms in sampled train/holdout contexts before
using exact wording or recurrence counts in a lesson.

- Workbook: `research/corpus-phrase-form-independent-review-workbook.json`
- Browser form: `writeups/corpus-phrase-form-independent-review-workbook.html`
- Validator: `scripts/validate_corpus_phrase_form_review.py`
- Independence: Reviewer must not have created the phrase inventory, regex families, candidate mechanisms or workbook.
- Does not establish: delivery effectiveness, speaker intent, listener outcomes, causality or universal best practice

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
