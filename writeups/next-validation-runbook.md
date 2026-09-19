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

1. `contrast_or_disagreement`
2. `example_or_case`
3. `story_or_personal_experience`
4. `qualification_or_boundary`
5. `closing`

The first four correspond to the existing vertical-slice packet; `closing` is
the fifth job in the shared 18-job curriculum. Keep the remaining 13 jobs
provisional while this slice is tested.

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
