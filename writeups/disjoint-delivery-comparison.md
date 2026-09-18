# Delivery compared with disjoint same-video segments

Exploratory sensitivity analysis, not matched controls or evidence of effectiveness.
Rate screening excludes caption durations below a provisional 0.25-second floor; it is not validated alignment. See timing-quality-audit.md.
Every legacy annotation target and every context caption inspected in contextual review
is excluded from the reference pool, with a five-second guard band. At least five
finite-valued reference segments are required per metric. Each video contributes
one delta; missing comparisons remain missing, not zero.

| Label | RMS delta / videos | Pitch proxy delta / videos | WPS proxy delta / videos |
| --- | --- | --- | --- |
| call_to_action | -4.634 / 5 | -40.689 / 5 | -0.054 / 5 |
| conclusion_or_summary | 0.916 / 5 | 3.742 / 5 | -0.035 / 5 |
| contrast_or_disagreement | 1.740 / 9 | 9.528 / 9 | 0.946 / 9 |
| definition | 1.717 / 4 | 14.193 / 4 | -0.091 / 4 |
| example | -0.103 / 5 | -7.091 / 5 | 0.147 / 5 |
| pause_event | 2.482 / 2 | 14.327 / 2 | -0.363 / 2 |
| question | -0.264 / 7 | 7.451 / 7 | 0.011 / 7 |
| story_or_personal_experience | -1.014 / 6 | -2.872 / 6 | 0.206 / 6 |
| uncertainty_or_qualification | -1.565 / 7 | 1.349 / 7 | 0.081 / 7 |

RMS deltas are in dB; pitch-proxy deltas in Hz; WPS in words/second.
Full target/reference IDs, per-metric denominators, per-video signs and source hashes
are in [the comparison record](../research/disjoint-delivery-comparison.json).

## Like-for-like WPS sensitivity

Both columns use identical eligible target segments and videos. Only the reference pool changes.
These are transcript timing proxies, not validated articulation rates.

| Label | All usable reference | Disjoint reference |
| --- | --- | --- |
| call_to_action | -0.051 | -0.054 |
| conclusion_or_summary | -0.043 | -0.035 |
| contrast_or_disagreement | 0.925 | 0.946 |
| definition | -0.134 | -0.091 |
| example | 0.148 | 0.147 |
| pause_event | -0.413 | -0.363 |
| question | -0.002 | 0.011 |
| story_or_personal_experience | 0.079 | 0.206 |
| uncertainty_or_qualification | 0.012 | 0.081 |

## Limits

- Reference segments may contain unreviewed instances of the same function.
- Not matched for function, duration, scene, music or camera conditions.
- Targets may contain overlapping captions; counts are not independent observations.
- Both targets and controls require overlapping audio windows; this differs from older reports that retained some transcript-only target metrics.
- No causal, speaker-independent or audience-outcome inference.
- Audio pitch and transcript timing remain unvalidated screening proxies.

The older all-usable-segment baseline is retained separately. This comparison
removes direct target/context contamination; it does not remove selection bias
or validate the underlying measurements. Review coverage changes the exclusion
pool, so rebuild this report after contextual reviews change.
