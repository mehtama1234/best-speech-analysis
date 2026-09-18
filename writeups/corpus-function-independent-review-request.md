# Request: independent review of corpus speech-function candidates

Please independently review the 187 transcript intervals in
`research/corpus-function-independent-review-workbook.json`. The purpose is to
test whether heuristic labels such as `question`, `story_or_personal_experience`
or `call_to_action` match the segment’s surrounding communication job. This is
not a test of delivery effectiveness, speaker intent, persuasion, trust or
listener outcomes.

## Independence and procedure

- Do not participate if you created the atlas, queue, candidate labels or
  internal interpretations.
- Inspect surrounding transcript context and the source where available.
- Use `indeterminate` when the retained context is insufficient.
- Record alternative functions and duplicate, quotation, translation or
  speaker-attribution concerns rather than silently resolving them.
- Do not infer internal emotion, honesty, intelligence or audience response.

The queue contains up to 12 train and 12 holdout videos for each of eight
non-`unclassified` candidate labels. It is a review sample, not a balanced
estimate of the underlying corpus.

## Export and validation

1. Open `writeups/corpus-function-independent-review-workbook.html`.
2. Complete the reviewer identity and every required item field.
3. Download the JSON export without editing judgments by hand.
4. Run:

   ```text
   python3 scripts/validate_corpus_function_review.py path/to/export.json
   ```

5. To produce a non-promotional label summary after validation, run:

   ```text
   python3 scripts/summarize_corpus_function_review.py path/to/export.json
   ```

Agreement or disagreement describes transcript-label consistency only. It does
not promote a lesson, establish recurrence outside this sample, or show that a
communication form improves understanding or action. Those claims require
separate delivery, learner and listener studies.
