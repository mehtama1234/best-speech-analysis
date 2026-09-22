# Next validation runbook

Status: **ready for external execution; no human validation records received**.

This is the next end-to-end operating sequence for promoting a five-job
vertical slice. It is intentionally operational: a workbook, protocol or
passing validator is not counted as completed evidence until a distinct person
has completed the record and the export has been validated and compared.

## Promotion target

Start with these five provisional jobs, which already have linked examples,
practice tasks and delivery samples:

Use the [reviewer start-here handoff](vertical-slice-01-reviewer-start-here.md)
as the single entry point for the packet files, source/media audits, workbook,
export commands and current status.

1. `contrast_or_disagreement` — packet `provisional-contrast_or_disagreement`
2. `example_or_case` — packet `provisional-example`
3. `story_or_personal_experience` — packet `provisional-story_or_personal_experience`
4. `uncertainty_or_qualification` — packet `provisional-uncertainty_or_qualification`
5. `conclusion_or_summary` — packet `provisional-conclusion_or_summary`

These names intentionally match the five entries in
`research/vertical-slice-01.json`. The broader curriculum uses the canonical
communication-job names `admit_uncertainty_or_set_a_boundary` and
`close_with_a_clear_takeaway`; those are the jobs being tested by the fourth
and fifth slice packets, respectively.

All five correspond to the existing vertical-slice packet. Keep the remaining
13 jobs provisional while this slice is tested.

## Dependency order

| Order | Operation | Current input | Completion evidence | Promotion effect |
|---:|---|---|---|---|
| 1 | Identity and event review | 395-item identity workbook; slice sources | Independent reviewer export, validator pass, disagreement report and adjudication | Allows recurrence denominators to be used |
| 2 | Function review | 187-item candidate-function workbook | Independent function decisions, validator pass and adjudication | Confirms the communication-job labels |
| 3 | Phrase and recurrence review | 50 phrase forms; 192 recurrence items | Independent exports, validators, comparator reports and adjudication | Confirms exact forms and cross-event recurrence |
| 4 | Delivery observation | 36 aligned samples, prioritizing the 10 slice samples | Manual observations with modality-specific missingness and validator pass | Adds vocal, temporal, visual and setting evidence |
| 5 | Counterexample review | 90 slots, five per job | Completed absence/failure/alternate/confound/misuse checks with sources | Prevents universal or unsafe teaching claims |
| 6 | Multimodal independent review | 21 internal observations | Independent review export, comparator and adjudication | Separates observation from internal interpretation |
| 7 | Lesson review | Five linked vertical-slice packets | Independent review of evidence, interpretation, limits and safety | Permits a packet to be considered promotion-ready |
| 8 | Learner check | 72-task protocol; use the five slice jobs first | Consented records, facilitator scores, safety flags, validator and summary | Tests teachability, not original effectiveness |
| 9 | Stimulus review | 18 draft listener pairs; use five slice jobs first | Independent equivalence/readability/accessibility/safety review and lock decision | Permits listener study stimuli |
| 10 | Listener outcome study | Locked matched pairs and six-task protocol | Blinded listener records, missingness/accessibility fields, validator and summary | Adds bounded comprehension/recall evidence only |

## Export discipline

For every independent operation:

1. Use a reviewer or facilitator code that is not the original analyst.
2. Read the form's claim boundary before reviewing.
3. Inspect the full surrounding transcript and available source media.
4. Use `indeterminate` or `not_available` when evidence is insufficient; never
   infer a missing observation.
5. Export without hand-editing judgment fields.
6. Run the named validator.
7. Compare independent exports when a comparator exists.
8. Preserve disagreements and record adjudication separately.

Do not send credentials, raw recordings or identifying participant information
through repository forms. Store only the minimum pseudonymous learner/listener
fields needed for the protocol.

## First presentation-pattern review pass

Use the [162-item priority browser](recovered-pattern-priority-review.html),
which covers all 55 proposed moves. Each item states the move to check in plain
words, while hiding the internal pattern name, category and card ID. The batch uses all 83 linked source videos in the
candidate pool, with no more than three items per linked source or original
catalog video. A source may still appear under multiple candidate patterns, so
162 items are not 162 independent video-level replications. The source layers
are also not sampled in their original proportions: all 26 external-transcript
candidates come from one video and the capped batch includes only one of them.
Keep the internal key private.

For a portable handoff, build and send
`deliverables/recovered-pattern-priority-reviewer-pack.zip`. It contains only
the reviewer instructions, blinded packet and browser; the packager verifies
that the private key and internal label fields are absent and checks the
archive checksums. Rebuild it with
`python3 scripts/package_recovered_pattern_priority_review.py` after changing
the packet or browser.

Each export must contain valid reviewer metadata and at least one item decision.
Every decided item must also include the requested function, alternate
explanation, context, identity/accessibility and uncertainty notes. Undecided
items may remain missing rather than being forced into “indeterminate.” The
validator checks record shape and coverage; it does not validate reviewer
independence or any pattern claim. Validate each return:

```text
python3 scripts/validate_recovered_pattern_priority_review_export.py <reviewer-a.json>
```

Obtain a second independent return and compare them:

```text
python3 scripts/compare_recovered_pattern_priority_reviews.py reviewer-a.json reviewer-b.json --output priority-comparison.json
```

If disagreements exist, route the comparison to adjudication:

```text
python3 scripts/build_recovered_pattern_priority_adjudication.py priority-comparison.json --output priority-adjudication.json
```

The comparison preserves every reviewer response, missing decision, blank note
and reviewer explanation. Agreement is calculated only where at least two
reviewers supplied a nonblank value; missing values are never counted as
agreement, disagreement or negative findings. Adjudication receives all
reviewer responses for disputed items, while missing coverage stays explicit
and unresolved. These steps do not promote a pattern, establish recurrence, or
measure learner/listener outcomes.

## First bounded human session

The first session is a two-reviewer, label-blinded review of the 162-item
presentation-pattern packet. It gives every one of the 55 candidate patterns
one to three reviewed examples. Because source videos recur across patterns,
do not interpret those items as 162 independent replications or use this pass
to estimate corpus prevalence or recurrence.

### Before the session

1. Give each reviewer a different reviewer code. Neither reviewer may have
   created the recovered cards, candidate labels or private key.
2. Give each reviewer the [browser form](recovered-pattern-priority-review.html)
   and [packet instructions](recovered-pattern-priority-review.md), or the
   [portable reviewer ZIP](../deliverables/recovered-pattern-priority-reviewer-pack.zip).
   Do **not** distribute `research/recovered-pattern-priority-review-key.json`.
3. Ask each reviewer to save a separate JSON export, for example
   `reviewer-a.json` and `reviewer-b.json`. Do not merge or edit the judgment
   fields by hand.

### After the session

Run these commands from the repository root:

```text
python3 scripts/validate_recovered_pattern_priority_review_export.py reviewer-a.json
python3 scripts/validate_recovered_pattern_priority_review_export.py reviewer-b.json
python3 scripts/compare_recovered_pattern_priority_reviews.py reviewer-a.json reviewer-b.json --output priority-comparison.json
python3 scripts/build_recovered_pattern_priority_adjudication.py priority-comparison.json --output priority-adjudication.json
```

Preserve all reviewer exports, the comparison, and the adjudication packet as
separate records. A disagreement is a result, not a validator failure. The
adjudicator may retain, revise, reject or mark a candidate indeterminate, but
may not promote a pattern on recurrence or effectiveness grounds that were not
reviewed.

The review-processing pass is complete when both exports validate and a
comparison record preserves their coverage. Full item-level agreement review
is **not complete** while either reviewer has missing decisions; follow up or
keep those items explicitly unresolved. The comparison/adjudication files do
not close the broader
identity, function, delivery, counterexample, learner or listener gates.

## Nineteen newer crosswalk candidates

Keep the 19 newer candidates separate from the 55-pattern review. There are
seven Ali Siddiq candidates, six Dry Bar Comedy candidates and six TED
candidates. They are still unconfirmed. Read the [review request](https://github.com/mehtama1234/speaking-humor-and-communication-concepts-research/blob/main/analysis/wave-2-context-review-request.md)
and use the [focused 19-item review page](https://github.com/mehtama1234/speaking-humor-and-communication-concepts-research/blob/main/site/pattern-review-wave-2.html)
or [portable review pack](https://github.com/mehtama1234/speaking-humor-and-communication-concepts-research/blob/main/deliverables/wave-2-full-context-reviewer-pack.zip).
The focused page links to 56 source passages, 43 full transcripts and cue
files, and the original videos. Review the full transcript and video, not only
the short excerpts.

The focused page can export only completed items. A return containing the 19 target
decisions is a valid partial 19/107 queue export; the other 88 IDs are listed
as unreviewed, not imputed or silently dropped. Validate it with
`python3 scripts/validate_source_pattern_review_export.py <reviewer.json>`;
the report must show wave-2 coverage 19/19 before the contextual pass is
considered covered. The browser’s local runtime smoke test passed, including
this partial-export path, but it used disposable synthetic decisions and is
not human evidence. Preserve actual reviewer exports separately. A contextual
pass does not itself establish recurrence, transfer, learner benefit, listener
outcomes or effectiveness; do not merge the 19 candidates into the 55-pattern
fieldbook or validated release before the remaining gates.

## Slice completion rule

A slice packet is promotion-ready only when its identity, function, exact-form
and recurrence evidence are independently reviewed; its delivery evidence is
manually observed and independently checked; its five counterexample checks
are completed; its lesson review is adjudicated; and its learner protocol has
at least one validated record per required task. Listener data remain a
separate outcome gate and must not be substituted with learner feedback.

Current state: **0/5 packets promotion-ready, 0 learner records, 0 locked
listener pairs, and 0 listener records**.

## Commands

Run from the repository root after each export:

```text
python3 scripts/validate_corpus_identity_review.py <export.json>
python3 scripts/validate_corpus_function_review.py <export.json>
python3 scripts/validate_corpus_phrase_form_review.py <export.json>
python3 scripts/validate_corpus_recurrence_review.py <export.json>
python3 scripts/validate_communication_job_delivery_review.py <export.json>
python3 scripts/validate_communication_job_counterexample_review.py <export.json>
python3 scripts/validate_multimodal_independent_review.py <export.json>
python3 scripts/validate_communication_job_learner_record.py <export.json>
python3 scripts/validate_listener_stimulus_review.py <export.json>
python3 scripts/validate_communication_job_listener_record.py <export.json>
python3 scripts/validate_end_to_end_status.py
python3 scripts/build_communication_job_promotion_readiness.py
```

The final two checks report repository state; they do not manufacture missing
human records. The promotion-readiness builder is intentionally a report
generator rather than a pass/fail validator.
