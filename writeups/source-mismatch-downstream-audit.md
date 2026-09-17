# Known mismatch — downstream containment audit

Scope: locally stored uses of `bV5uKHsWQtY`, the Washington-labeled transcript
with conflicting self-identification. This audit does not resolve its origin or
verify the actual video. Raw cache, canonical segments and sampling frame remain
preserved.

## Findings and changes

| Consumer | Finding | Treatment |
|---|---|---|
| Corpus overview | Title association and caption-derived rate of 275.5 words/minute; text fed lexical aggregates | Preserve inventory row, expose restrictions, withhold rate, exclude from lexical aggregates |
| Candidate-pattern inventory | All 465 rows contributed even though no displayed example contained this ID | Exclude restricted rows from counts, distinct sources and examples; report excluded counts |
| Retrieval census | Counts stored heuristic labels, not verified speaker patterns | Preserve as raw census; distinguish its denominator from filtered candidate inventory |
| Blind passage sample | ID appears in sampling frame, not selected passages | Preserve frozen sampling frame and selection |
| Legacy annotation ledger, reviewed cards, provisional practice patterns, passage reviews | No literal source-ID references found | No evidence rows changed; absence is bounded to these inspected artifacts |
| Full-reading ledger and queue | Full text read with explicit restrictions | Retain reading record and open source-resolution action |

The candidate contribution removed comprises 417 unclassified occurrences,
26 questions, 12 story/personal-experience occurrences, six qualifications,
three contrasts and two definitions. Labels overlap, so their sum is not a
distinct-caption count. The exclusion covers 465 distinct captions.

The overview's inventory counts still include the raw source, retaining 395
nonempty caches and 102,816 captions. Its word tokenizer counts 3,921 words for
this source; the segment reading queue reports 3,931 using its different stored
word-count convention. Neither number is a validated spoken-word count.

## Durable safeguards

Both aggregate builders now load explicit restrictions from the full-context
ledger. Restricted sources cannot silently re-enter their lexical/candidate
outputs on regeneration. A missing restriction is not certification of validity.
The overview labels all remaining timing rates as unvalidated caption-duration
proxies; no claim is made that all other timing problems are repaired.

Tests check accumulated restrictions, withheld rate, preserved inventory count,
excluded candidate count, absence from candidate examples, and a full registry
recomputation of filtered label counts.

## Still open

Inspect the actual video and independently establish the correct pairing. Obtain
any corrected transcript as a separately preserved candidate before canonical
repair. Other known timing problems and potential unknown identity mismatches
remain separate audit work. This targeted containment is not a global source
quality certification, nor does it establish any rhetorical best practice.
