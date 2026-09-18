# Vertical slice 01: from communication job to teachable practice

## Purpose

The transcript queue is complete, so the next research unit is deliberately
smaller and deeper: turn five existing provisional patterns into evidence-linked
lessons without upgrading them into universal advice.

The slice covers five communication jobs:

| Communication job | Provisional pattern | Practice hypothesis |
| --- | --- | --- |
| Disagree or show a change clearly | `provisional-contrast_or_disagreement` | Make the comparison explicit. |
| Make an abstract point concrete | `provisional-example` | Move from the general claim to a concrete case. |
| Tell a bounded story | `provisional-story_or_personal_experience` | Use bounded personal detail. |
| Admit uncertainty or set a boundary | `provisional-uncertainty_or_qualification` | Qualify predictions and interpretations precisely. |
| Close with a clear takeaway | `provisional-conclusion_or_summary` | Mark the takeaway. |

These are selected because the current practice inventory already has reviewed
examples and transcript/audio proxies for them. They remain `practice hypotheses`:
the existing records do not prove listener trust, memory, action or general
causality.

## Required evidence packet for each pattern

Each pattern must receive one packet containing:

1. the communication problem and primary speech function;
2. at least three exact examples from independent events where independence can
   be verified;
3. surrounding transcript context and synchronized audio/video where available;
4. measured delivery observations with method, reliability and missing-data notes;
5. one case where the pattern is absent but the speech works;
6. one case where it appears but the speech does not work or serves another job;
7. alternative explanations involving topic, editing, audience, microphone,
   speaker, setting or prior context;
8. a misuse warning and accessibility/safety boundary;
9. an independent reviewer decision and disagreement record; and
10. a short practice task, self-check and next listener test.

## Acceptance gates

The slice is not complete when five cards merely exist. It is complete only when
all five cards have evidence packets, counterexamples, independent review, and a
linked practice lesson. A small learner check must then test whether people can
recognize each pattern in a new example, explain it in plain language, use it in
their own words, identify when not to use it and improve a short recording after
feedback.

The learner check tests the teaching system, not whether the original speaker’s
behavior caused better outcomes. Listener trust, memory and action require later
outcome studies.

## Current status

Selected and registered: five patterns. Transcript corpus: complete. Provisional
practice inventory: available. The first partial evidence packet is now recorded
in [vertical-slice-01-contrast-or-disagreement.json](../research/vertical-slice-01-contrast-or-disagreement.json).
It contains five representative reviewed examples, a ten-record annotation
inventory, local transcript context and three existing aligned-audio measurements.
It deliberately remains unvalidated: five job-mismatched controls and one
alternate-function control are recorded, but a failed/ineffective contrast case,
speaker/event independence, manual visual alignment, independent review, lesson
implementation and learner testing are not complete.
An auditable handoff for the independent reviewer is recorded in
[vertical-slice-01-independent-review-request.md](vertical-slice-01-independent-review-request.md);
it is pending an external reviewer and is not itself validation.

The next implementation step is to freeze the five example sets, verify source
and event identity, and complete the first two partial packets:
`provisional-contrast_or_disagreement` and `provisional-example`. The second
packet is recorded in [vertical-slice-01-example.json](../research/vertical-slice-01-example.json)
with its draft lesson in
[vertical-slice-01-lesson-example.md](vertical-slice-01-lesson-example.md).
The story packet is also now registered in
[vertical-slice-01-story.json](../research/vertical-slice-01-story.json), with
privacy-aware practice guidance in
[vertical-slice-01-lesson-story.md](vertical-slice-01-lesson-story.md).
The fourth packet covers qualification and uncertainty in
[vertical-slice-01-uncertainty.json](../research/vertical-slice-01-uncertainty.json),
with its draft lesson in
[vertical-slice-01-lesson-uncertainty.md](vertical-slice-01-lesson-uncertainty.md).
The fifth and final packet covers conclusion and summary in
[vertical-slice-01-conclusion.json](../research/vertical-slice-01-conclusion.json),
with its draft lesson in
[vertical-slice-01-lesson-conclusion.md](vertical-slice-01-lesson-conclusion.md).

## Source and event audit

The five packets are audited in
[vertical-slice-01-source-event-independence.json](../research/vertical-slice-01-source-event-independence.json).
The audit verifies canonical video IDs, URLs, titles, channels and playlist
metadata for the 50 packet item occurrences. It finds 16 unique canonical video
IDs and records repeated reuse across packets. This verifies source-record
distinctness where IDs differ, but it does not independently verify speaker
identity or event independence beyond the video IDs; all five packets remain
unvalidated on that dimension.

## Learner-check protocol

The five lessons share a learner-check protocol in
[vertical-slice-01-learner-check.md](vertical-slice-01-learner-check.md) and
[vertical-slice-01-learner-check.json](../research/vertical-slice-01-learner-check.json).
It tests recognition in new examples, plain-language explanation, transfer,
non-fit detection, safety boundaries and second-listener restatement. It has not
yet been run with learners, so no pattern is promoted to learning evidence.

The repository gate is [validate_vertical_slice.py](../scripts/validate_vertical_slice.py);
it checks all five packet anchors against canonical transcripts, lesson links,
source-audit linkage and the not-yet-run learner protocol.

The shared product-facing lesson index is available as
[JSON](vertical-slice-01-lesson-index.json) and a self-contained
[HTML browser](vertical-slice-01-lesson-index.html). Both preserve the
provisional evidence label and link each lesson back to its packet, shared
practice flow and learner-check instrument.

The UI-agnostic practice model is recorded in
[vertical-slice-01-practice-flows.json](../research/vertical-slice-01-practice-flows.json).
It gives web and native clients the same five flows, input modes, prompts,
self-check/listener-check hooks, accessibility options and safety boundaries.

The protocol also has a backend-free [learner-check instrument](vertical-slice-01-learner-check.html)
that records pseudonymous session metadata, baseline and transfer responses,
non-fit judgments, listener restatements, revisions and rubric scores as a
downloadable JSON record. It is an instrument for a future consented run, not
evidence that learners have completed the check.

Downloaded records can be checked and summarized with
`score_vertical_slice_learner_records.py`. Invalid or non-consented records
are rejected, boundary-score failures remain explicit, and the output is
restricted to teachability observations.

The [media audit](vertical-slice-01-media-audit.md) reconciles all 50 packet
item occurrences across 16 unique video IDs. Fifteen IDs currently have
verified raw audio/video locally and one remains without raw media because the
source is unavailable; the media-status ledger currently agrees with local file
presence. All 16 IDs have derived features. These files and measurements do not establish synchronization,
delivery meaning or audience effect.

An [internal manual multimodal review](vertical-slice-01-manual-multimodal-review.md)
now records bounded sampled-frame observations for thirteen evidence intervals,
covering all five communication jobs plus counterexample and cutaway cases.
The review records caption overlap and setting only; it is explicitly not
independent validation and does not infer emotion, intent or audience effect.

The [independent-review workbook](vertical-slice-01-independent-review-workbook.md)
now enumerates all 50 packet item occurrences with blank decisions and required
disagreement fields. It is ready for an external reviewer but contains no
reviewer judgments yet.
