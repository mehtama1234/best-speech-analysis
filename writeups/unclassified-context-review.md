# Unclassified does not mean uninformative

17 September 2026. The three legacy unclassified candidates received assistant
transcript-only review using five captions before and after each target. Exact
context IDs and hashes are retained in the contextual review ledger. No audio,
video, independent semantic adjudication or source-claim verification is implied.

| Target | Contextual interpretation |
| --- | --- |
| [2fWJh-_UG5s:00165](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=373) | A transition into describing a particular drawing, following reported wishes about sharing a child's art |
| [S43F1BZfQKY:00010](https://www.youtube.com/watch?v=S43F1BZfQKY&t=59) | A condition detail inside an autobiographical sequence about hair loss and a subsequent wig-shop visit |
| [fBnAMUkNM2k:00391](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=1648) | A habitual action followed by reported questions from others and a recurring reply |

Links use provider caption start times rounded down, not verified word onsets.
The drawing was not visually inspected, health details are attributed rather
than independently verified, and saying one smiles does not establish visible
smiling at that moment in the recording.

## Why the retrieval rules missed them

`candidate_functions` in `scripts/build_segment_registry.py` searches narrow
phrase patterns. It returns `unclassified` when none match. A story's condition
detail or habitual action need not repeat phrases such as remembering something
or describing what happened one day. That is a retrieval limitation, not proof
that the sentence lacks a speech function.

The saved false support decisions remain false because unclassified is not a
substantive pattern to promote. Current contextual subtypes now explain the
passages. No new candidate label or supported example is silently inserted into
the pattern counts. In particular, 0/3 support for this fallback is not a
detector-quality score. These selected cases cannot estimate recall.

## The larger coverage issue

The new [full-registry census](retrieval-coverage-audit.md) finds 90,397 of
102,816 stored segments (87.9%) have only the unclassified fallback. The registry
covers 395 videos. Eighty distinct targets now have contextual assistant reviews;
692 distinct captions occur in their inspected context windows. Membership in
a context window is not complete semantic adjudication of that caption, and
these numbers do not mean 395 transcripts have been read end-to-end.

This is why repairing the 87-row legacy queue cannot finish the research goal.
The next discovery sample must include contiguous passages outside keyword hits,
not simply harvest more of the same marked phrases. Sampling and speaker/format
boundaries must be recorded before making corpus-wide recurrence estimates.
The census records per-video denominators and preserves overlapping label counts.

## Checkpoint

Contextual semantic review is now 80/87 legacy rows. The seven remaining rows
are pause candidates with a separate acoustic screen but no new semantic
adjudication. Sixty rows retain at least one supported label, and five
provisional practice cards remain. Raw transcripts, features and the original
annotation ledger are preserved. Full-corpus interpretation, independent
validation and multimodal pattern testing remain unfinished.

Verification: six dependent report/audit builders and the new corpus census
succeeded. All 33 tests passed in 14.902 seconds; whitespace checks passed and
original source/annotation files have no diff. Tests check consistency and
counting behavior, not independent semantic agreement or corpus recall.
