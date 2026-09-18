# Independent review request: vertical slice 01

Status: pending independent reviewer; this document is not a review result.

The blank [review workbook](vertical-slice-01-independent-review-workbook.md)
contains all 50 item occurrences across the five provisional packets with
decision fields. It is a template, not evidence that a reviewer has completed
the task.

The same workbook is available as a [browser review form](vertical-slice-01-independent-review-workbook.html)
that exports a structured JSON record. It does not fill or submit judgments on
behalf of a reviewer.

## Reviewer task

Review all five evidence packets without assuming that an existing label or
practice hypothesis is correct. The workbook identifies each item’s packet,
role, evidence ID, timestamp and source link. Some source records have only
partial official corroboration; exact upload/event correspondence remains
unverified.

For every representative example and control, record:

1. whether the evidence boundary is correctly located;
2. whether the primary communication job is plausible from the supplied context;
3. whether “contrast/disagreement” is supported, unsupported or indeterminate;
4. whether the interpretation distinguishes textual contrast from interpersonal
   disagreement;
5. whether the audio proxy is being described as observation rather than effect;
6. what alternative explanation or missing evidence matters; and
7. whether the practice task could mislead, exclude or escalate conflict.

## Required review record

The completed export must name the reviewer, date, modality, evidence IDs
checked, decision for each item, reasons for disagreement, resolution status
and any new counterexample requested. A reviewer may mark an item
indeterminate; uncertainty is a valid result and must not be silently converted
into support.

Before using the record, run:

```text
python3 scripts/validate_vertical_slice_review_record.py REVIEW.json
```

With two or more independent exports, preserve disagreements with:

```text
python3 scripts/compare_vertical_slice_reviews.py REVIEW_A.json REVIEW_B.json
```

These tools check completeness and describe agreement; neither endorses a
judgment or promotes a pattern.

## Independence rule

The reviewer must not be the person who created the packet or original
interpretation. Identity and role should be recorded in the resulting JSON. This
request itself is only a handoff artifact and does not satisfy independent review.
