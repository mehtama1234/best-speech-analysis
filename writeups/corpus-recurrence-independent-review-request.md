# Request: independent review of corpus phrase recurrence

## Purpose

Please independently review the 192 transcript intervals in
`research/corpus-recurrence-independent-review-workbook.json`. The goal is to
test whether a phrase-form hit supports the proposed speech-function family in
its surrounding context. This is a label and evidence-boundary review, not a
test of delivery effectiveness, speaker intent, persuasion, trust or audience
outcomes.

## Independence and safety

- Do not participate if you created the atlas, queue, candidate labels or
  internal packet interpretations.
- Use a reviewer code, role, date, modality and conflict statement.
- Inspect the surrounding transcript before deciding. Use `indeterminate` when
  the retained context is insufficient.
- Do not infer speaker psychology, truth of claims, audience response or causal
  effects from the caption interval.
- Flag privacy, sensitive-content, language-quality or speaker-attribution
  concerns in the reason field.

## Review fields

For each interval, record:

1. **Context decision:** supports, alternate function, not enough context, or
   not relevant.
2. **Phrase role:** central, incidental, quoted/repeated, or unclear.
3. **Primary function:** choose the function actually performed in context, not
   the queue’s proposed family.
4. **Recurrence inclusion:** include, exclude or indeterminate.
5. **Alternative function/explanation:** state what else the words may be doing.
6. **Reason:** cite surrounding wording and preserve uncertainty.
7. **Identity/duplicate note:** record possible re-upload, mixed speaker,
   quotation, translation or event-identity concerns.

The 12 train and 12 holdout intervals per phrase family are a deterministic
sampling frame. They are not a claim that the families are balanced in the
underlying corpus.

## Procedure

1. Open the browser form at
   `writeups/corpus-recurrence-independent-review-workbook.html`.
2. Review the source URL and retained context for every item.
3. Complete every required field; use `indeterminate` rather than guessing.
4. Download the JSON export without editing judgments by hand.
5. Run:

   ```text
   python3 scripts/validate_corpus_recurrence_review.py path/to/export.json
   ```

6. Return the validated export and any separate methodological notes. Do not
   send raw recordings or identifying participant information through this
   workbook.

## Interpretation boundary

Agreement would support more reliable transcript-function labels and recurrence
candidate selection. Disagreement should be preserved and summarized, not
silently adjudicated by the original analyst. Even a fully completed review
would not establish that a phrase improves communication or that copying it
works for every speaker, topic or setting; those claims require separate
delivery review and listener studies.
