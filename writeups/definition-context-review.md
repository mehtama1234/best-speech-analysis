# Definition review: what does “means” actually do?

17 September 2026. Assistant transcript-only review of all nine legacy
definition candidates, using seven adjacent captions per target. These are
contextual judgments, not independent human validation or audio/video findings.

## Category before conclusion

The practice card promised a meaning, translation or paraphrase that clarifies
a term before building on it. A keyword detector for “means” is broader: the word
can introduce a consequence, personal significance or an interpretation of an
event. Counting all those uses as definitions overstates support for that card.

The explicit rubric includes lexical/translation glosses, pragmatic paraphrases
and unpacking the intended content of an abstract phrase. It excludes merely
claiming a consequence or assigning significance. Operational reformulation is
a boundary case: it is not a dictionary definition and must be labeled as such.

## Findings

| Evidence | Decision and specific speech function |
| --- | --- |
| [-6qN3bm2RYo:00068](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=190) | Supported, moderate confidence: operational reformulation of leaving a colonial mindset into a particular governance agenda |
| [3AIoHLr8nTI:00046](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=421) | Supported: imagined pragmatic paraphrase of tolerating someone, contrasted with acceptance |
| [fBnAMUkNM2k:00068](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=440) | Rejected: interpreting an event as a sign of healing, not defining a term |
| [qOwYULOPuPs:00279](https://www.youtube.com/watch?v=qOwYULOPuPs&t=727) | Rejected: persuasive equivalence/consequence connecting energy control with destiny |
| [OfwfTN1mEyM:00055](https://www.youtube.com/watch?v=OfwfTN1mEyM&t=138) | Rejected: inference about solving water problems from a water/land statistic |
| [_Mb1-CN3wZs:00048](https://www.youtube.com/watch?v=_Mb1-CN3wZs&t=136) | Supported: approximate lexical gloss of a code word in dialogue; not evidence of public-speaking effectiveness |
| [fBnAMUkNM2k:00374](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=1581) | Supported: a name followed by a translation; translation accuracy not independently verified |
| [pmAL79dnvu0:00047](https://www.youtube.com/watch?v=pmAL79dnvu0&t=152) | Rejected: personal significance connected to voting |
| [AwA0Jnfj3ao:00174](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=766) | Rejected: significance after a moral-victory account, with an unresolved transcript fragment |

The complete source IDs, context hashes, reasons and subtypes are stored in
[the contextual review ledger](../research/contextual-label-reviews.json).
Original annotations are retained unchanged.

## A boundary error that changes meaning

The legacy observation at fBnAMUkNM2k:00068 discussed crying as a sign of healing.
The preceding caption contains the negation: the completed sentence concerns
recounting a story **without** crying. A target caption alone reversed the sense
of the observation. Neither formulation is validated as a health claim by this
review; the research finding is that context across caption boundaries matters.

Similarly, the odd fragment at AwA0Jnfj3ao:00174 does not justify the old account
of learning a person's name. The nearby captions concern a drawn series and a
moral victory. Audio verification is needed to repair that transcript fragment.

## Consequence for the practice edition

Definition support falls from 7/9 to 4/9 (0.444), below both the five-example
minimum and 0.70 support threshold. The card is withdrawn, not rewritten to keep
it eligible. Five other practice cards remain admitted under the existing rules.
Excluded candidates and reasons now appear explicitly in JSON and Markdown.

This does not prove that defining terms is ineffective. It means this reviewed
sample does not meet the project's evidential threshold for that specific card.
Even the four supported examples mix subtypes and formats; they cannot establish
a universal technique or cross-speaker effect.

## Next work

Verification: five report builders completed; eleven regression tests passed
(13.177 seconds), including the current definition decisions and the excluded-card
record. `git diff --check` passed and the original annotation ledger remains
unchanged. The tests establish report consistency, not independent validation
of these semantic judgments. Use the rebuild commands in
[the preceding review](contextual-label-review.md).

Twelve of the 87 legacy rows now have context-bound assistant reviews; 75 remain.
There are 60 rows with at least one supported label after these corrections.
Continue with other speech-function groups, separate narration from current
audience address, inspect neighboring captions for negation/attribution, and
use audio/video evidence before asserting delivery behavior. No corpus-wide
precision estimate, causal finding or independently validated human review is
claimed.
