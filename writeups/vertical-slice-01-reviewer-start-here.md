# Vertical slice 01 — reviewer start here

This page is the execution handoff for an independent reviewer. It is not a
research result. The slice is selected but unvalidated, and the reviewer must
not be the person who created the packets or original interpretations.

## Scope

Review five provisional communication jobs:

| Job | Packet | Lesson | Representative items |
|---|---|---|---:|
| Contrast or disagreement | [`vertical-slice-01-contrast-or-disagreement.json`](../research/vertical-slice-01-contrast-or-disagreement.json) | [`vertical-slice-01-lesson-contrast.md`](vertical-slice-01-lesson-contrast.md) | 5 |
| Example or case | [`vertical-slice-01-example.json`](../research/vertical-slice-01-example.json) | [`vertical-slice-01-lesson-example.md`](vertical-slice-01-lesson-example.md) | 5 |
| Story or personal experience | [`vertical-slice-01-story.json`](../research/vertical-slice-01-story.json) | [`vertical-slice-01-lesson-story.md`](vertical-slice-01-lesson-story.md) | 5 |
| Uncertainty or qualification | [`vertical-slice-01-uncertainty.json`](../research/vertical-slice-01-uncertainty.json) | [`vertical-slice-01-lesson-uncertainty.md`](vertical-slice-01-lesson-uncertainty.md) | 5 |
| Conclusion or summary | [`vertical-slice-01-conclusion.json`](../research/vertical-slice-01-conclusion.json) | [`vertical-slice-01-lesson-conclusion.md`](vertical-slice-01-lesson-conclusion.md) | 5 |

The 25 representative examples are part of a 50-item review workbook. Review
all workbook items, not just the representatives; the representatives are the
minimum lesson-facing subset.

## Read in this order

1. [Slice manifest](../research/vertical-slice-01.json) — scope, status and
   completion rule.
2. [Independent review request](vertical-slice-01-independent-review-request.md)
   — independence, decisions and claim boundary.
3. [Source/event independence audit](../research/vertical-slice-01-source-event-independence.json)
   — metadata-only audit; it does not prove speaker identity or event identity.
4. [Media audit](../research/vertical-slice-01-media-audit.json) — which
   canonical items have locally available raw media.
5. [Manual multimodal notes](../research/vertical-slice-01-manual-multimodal-review.json)
   — internal notes only; do not treat them as independent observations.
6. [Independent review workbook](vertical-slice-01-independent-review-workbook.html)
   — complete the 50 item-level records and reviewer metadata.

## Required decisions

For every item, inspect the surrounding transcript and source media where
available, then record:

- evidence-boundary decision: `correct`, `needs_revision` or `indeterminate`;
- pattern decision: `supported`, `unsupported` or `indeterminate`;
- safety decision: `safe_as_written`, `needs_boundary` or `unsafe`;
- speech-function label and whether the proposed mechanism is actually
  supported by the excerpt;
- counterexample adequacy, alternative explanations and accessibility risks;
- media availability/alignment and any modality-specific missingness.

Do not infer tone, intent, emotion, confidence, audience response or
effectiveness from captions, proxies or a missing recording.

## Export and verification

Record reviewer code, role, date, modality and conflict statement. Export the
completed workbook without silently resolving disagreement fields. Then run:

```text
python3 scripts/validate_vertical_slice_review_record.py <completed-export.json>
python3 scripts/compare_vertical_slice_reviews.py <reviewer-a.json> <reviewer-b.json>
python3 scripts/summarize_vertical_slice_review.py <validated-export.json>
```

If only one reviewer is available, preserve the single-review status; do not
call it agreement or adjudication. The comparator is required when multiple
independent exports exist.

## Separate learner step

After the evidence review, use the [learner protocol](vertical-slice-01-learner-check.html)
with consented participants. Learner records test recognition, explanation,
transfer, non-fit judgment and revision; they do not prove that the original
speech pattern causes better audience outcomes. Validate learner exports with
the protocol's named validator and retain missingness, safety and accessibility
fields.

## Current status

- Packets ready for promotion: **0/5**
- Independent review records: **0**
- Learner records: **0**
- Listener outcome records: **0**
- Listener stimuli: separate gate; not required to complete this evidence
  review, and not yet locked

Promotion requires independent evidence review, speaker/event verification,
manual delivery alignment, counterexamples, lesson adjudication and the learner
gate. This page does not change any of those statuses.
