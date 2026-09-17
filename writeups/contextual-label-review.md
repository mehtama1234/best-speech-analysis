# Contextual review: one label is not another

Date: 17 September 2026. Reviewer: Codex assistant. Modality: transcript only.
This is not independent human review, audio listening, video inspection or a
claim that the transcript accurately captures every word spoken.

## What was inspected

All three legacy annotations with multiple candidate labels were re-read using
nine adjacent caption segments each. The original annotation ledger is unchanged.
The [new review ledger](../research/contextual-label-reviews.json) contains the
rubric, per-label reasons, exact context IDs and hashes binding text and timing.
Report generation stops if those source contexts no longer match.

| Target | Context inspected | Separate decisions | Why the distinction matters |
| --- | --- | --- | --- |
| [-54zUwySKCg:00059](https://www.youtube.com/watch?v=-54zUwySKCg&t=305) | 280.550–335.729 seconds | Contrast: supported; personal story: supported | Comfort with success is contrasted with changing direction; no interpersonal disagreement is established |
| [-54zUwySKCg:00122](https://www.youtube.com/watch?v=-54zUwySKCg&t=613) | 599.000–639.090 seconds | Question: supported; claim qualification: unsupported | Narrated wondering about possible action differs from hedging an assertion or prediction |
| [S43F1BZfQKY:00011](https://www.youtube.com/watch?v=S43F1BZfQKY&t=65) | 47.500–106.630 seconds | Call to action: unsupported; personal story: supported | Advice attributed to a character is part of a story, not an instruction to the present audience |

The uncertainty category depends on its definition. Here it means qualification
of a claim, prediction or interpretation, consistent with the practice card.
A broader taxonomy of narrated wondering could legitimately include the second
example, but would need a separate label and could not inherit advice about
qualifying claims. No judgment concerns the speaker's internal mental state.

## Consequences for current summaries

There are still 87 legacy annotation rows. After the separate decisions, 63 have
at least one supported label (previously 62). Personal-story support becomes
11/13 instead of 10/13; qualification support becomes 8/9 instead of 9/9.
The total number of supported label assignments is unchanged: one was added and
one removed. Six practice cards still meet the existing admission thresholds.
Counts are not precision estimates for the full corpus or evidence of efficacy.

The story's audio values now contribute to its label-specific report and
baseline. The rejected qualification no longer contributes to that label's
examples. Legacy function names and observations remain visible for provenance;
current per-label support is shown separately on individual cards.

## What remains

Verification: all five affected report builders completed successfully; nine
regression tests passed (11.531 seconds), including real-corpus source joins and
published per-label eligibility checks. `git diff --check` passed. The original
annotation ledger has no diff. Reproduce with:

```bash
python3 scripts/build_reviewed_delivery_report.py
python3 scripts/compare_reviewed_delivery_baselines.py
python3 scripts/build_provisional_practice_patterns.py
python3 scripts/build_reviewed_pattern_cards.py
python3 scripts/audit_annotation_ledger.py
python3 -m unittest discover -s tests -v
```

Tests verify provenance and computation, not independent correctness of the
assistant's semantic judgments. Context hashing detects changed inspected text
and timing; it does not certify the original transcript against audio.

The other 84 legacy rows still have unknown reviewer provenance. These three
assistant reviews are not replacements for independent review, full-transcript
reading or multimodal validation. Next, expand context-aware review beyond the
multi-label cases and maintain explicit candidate-label definitions. Sample
negative cases as well as positive ones; do not tune judgments to preserve a
desired number of practice cards. Disjoint matched controls and reliable speaker
metadata remain prerequisites for stronger cross-speech delivery findings.
