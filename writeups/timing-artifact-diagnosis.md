# Timing artifact diagnosis: a caption is not a spoken-word interval

17 September 2026. This is a stored-data and code audit, not audio listening,
forced alignment or a new human annotation study.

## Source-to-result trace

The source transcript for AwA0Jnfj3ao ends with an interval from 1,028,260 ms to
1,028,264 ms for “Sachin Tendulkar:Thank you.” The extractor copies that four-
millisecond interval and counts three whitespace tokens, including speaker-label
text. Dividing by the interval yields a stored rate proxy of 750 words/second.
This is a timing/tokenization artifact, not a measurement of how fast the person
spoke. It is already present in the provider transcript, not introduced by the
latest report join. The recording would need inspection to establish true timing.

Among 239 captions in that video, the raw mean caption-rate proxy is 5.632.
Removing that single rate value yields 2.504. This is an equal-caption average,
not total spoken words divided by recording duration.

## What changed

A shared screening helper now returns no rate value for invalid/nonfinite rates
or caption durations below a provisional 0.25-second floor. It does not cap 750
to a convenient number, alter source timestamps or overwrite raw feature files.
Current delivery reports, individual cards, ordinary baselines and disjoint
comparisons use the same rule on both targets and references. Acoustic values
are unchanged and remain coarse window summaries, not validated fine alignment.

The audit covers all 5,059 stored segments across 36 videos. Exactly one caption
rate fails this screen; 3,741 captions overlap their immediate predecessors.
All segments intersect at least one audio window, but that does not validate the
caption words or their timing. Three raw rates exceed eight words/second and
remain review flags; only the four-millisecond case is excluded by this rule.
The 0.25-second floor is an explicit exploratory quality guard, not a biological
rate limit. Valid short speech could exist, so exclusion is not a repair or truth label.

## Correction to the earlier delivery finding

The earlier [summary review](summary-context-review.md) reported a story-rate
sign reversal after removing reviewed context from the reference pool. The tiny
final caption was inside that context/guard-band exclusion. Once its invalid
rate is removed consistently, the like-for-like results are:

| Label | Screened all-usable reference delta | Screened disjoint-reference delta | Videos |
| --- | ---: | ---: | ---: |
| Personal story | +0.168 | +0.200 | 6 |
| Conclusion/summary | -0.184 | -0.190 | 3 |

The historical story sign reversal is therefore superseded, not a current
finding about delivery. These small, selected, caption-derived comparisons still
do not justify advice to speed up stories or slow conclusions. The reference
segments remain unmatched for speech function, scene and topic; speaker identity
and independent observations are not established.

## Evidence and next work

The [timing audit](timing-quality-audit.md) links to raw-preserving exclusions,
per-video means and source hashes. The [current disjoint comparison](disjoint-delivery-comparison.md)
records target/control IDs and per-metric denominators. Reproduce with:

```bash
python3 scripts/audit_timing_quality.py
python3 scripts/build_reviewed_delivery_report.py
python3 scripts/compare_reviewed_delivery_baselines.py
python3 scripts/build_provisional_practice_patterns.py
python3 scripts/build_reviewed_pattern_cards.py
python3 scripts/compare_disjoint_delivery.py
python3 -m unittest discover -s tests -v
```

No raw media or feature files were changed. Next, audit attribution tokens and
caption overlap, inspect localized audio, and establish a reliable segment/word
alignment method before upgrading rate/pause claims. Eighteen contextual reviews
and five admitted language-practice cards remain; this pass adds measurement
quality evidence, not new semantic review coverage.

Verification: all six rebuild commands succeeded; 20 tests passed in 11.266
seconds, including the preserved 750 raw value and its exclusion from the
238-value reference pool. `git diff --check` passed. Git shows no changes to
transcripts, raw feature files or the original annotation ledger. These checks
verify screening consistency and provenance, not actual spoken-word alignment.
