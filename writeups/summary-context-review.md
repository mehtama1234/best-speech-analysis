# Summary review and delivery sensitivity

17 September 2026. Assistant transcript-only review; no independent human,
audio-listening or visual validation is claimed.

## Six contextual decisions

All six conclusion/summary candidates were inspected with up to five preceding
and three following captions. Five remain supported, one remains rejected.
The decision requires a takeaway tied to identifiable preceding material,
not merely a keyword. Local conclusions need not end a whole speech.

| Target | Observed function and decision |
| --- | --- |
| [-54zUwySKCg:00196](https://www.youtube.com/watch?v=-54zUwySKCg&t=989) | Supported: several ways to make a difference lead into a broad generational charge |
| [-URn1fARvts:00119](https://www.youtube.com/watch?v=-URn1fARvts&t=254) | Supported: school/sport experience compressed into a statement about critical curiosity |
| [3AIoHLr8nTI:00003](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=40) | Rejected: opening inference from potential to responsibility and announcement of the topic |
| [aXmM0VZv810:00483](https://www.youtube.com/watch?v=aXmM0VZv810&t=1175) | Supported: local prioritizing conclusion from an energy-use criterion; not speech closure |
| [qOwYULOPuPs:00124](https://www.youtube.com/watch?v=qOwYULOPuPs&t=312) | Supported: a two-part evaluation compresses the preceding account of proposed terms |
| [AwA0Jnfj3ao:00234](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=1016) | Supported: an anticipation story becomes a general lesson, followed by interviewer thanks |

The exact contexts, hashes, subtypes and reasons are in
[the review ledger](../research/contextual-label-reviews.json). The result verifies
the local textual function under this rubric, not truth, effectiveness or intent.
Eighteen of 87 legacy rows now have explicit contextual assistant review; 69 remain.
There are still 60 rows with at least one supported label and five admitted cards.

## Do the delivery comparisons withstand a changed reference pool?

**Historical pre-screening result, superseded by [the timing diagnosis](timing-artifact-diagnosis.md):**
the direction reversal described below was driven by a four-millisecond caption
artifact. After rate-quality screening, the story delta is positive under both
references (+0.168 and +0.200), and the summary deltas are -0.184 and -0.190.
The old numbers are retained as the investigation trail, not current findings.

The old baseline averaged all usable captions, including the reviewed examples.
The new [disjoint comparison](disjoint-delivery-comparison.md) excludes all legacy
annotation targets, inspected contextual captions and a five-second guard band.
It retains exact target/reference IDs, per-metric sample counts, per-video results
and source hashes. At least five usable reference values per video/metric are
required. The five-second guard and five-value minimum are exploratory settings,
not validated best-practice thresholds.

A paired comparison holds eligible targets and videos constant while changing
only the reference pool. For summary examples, the mean words/second-proxy delta
changes from -1.226 to -0.190 across just three videos. For personal-story examples,
it changes from -0.353 to +0.200 across six videos. Thus the direction of the
story-rate difference is not robust to this reference choice.

This does **not** show that stories should be delivered faster. It shows why
the present data do not justify a general slower-story prescription. These are
caption-derived timing proxies, not validated articulation rates; overlapping
captions and within-video variation remain important. Reference segments are
unreviewed and may contain the same speech function. The comparison is disjoint,
not matched for topic, scene, duration, music or function, and is not causal.

## Verification and next step

Four affected existing reports and the new comparison builder ran successfully.
Sixteen tests passed (10.893 seconds), including fixture guard-band exclusions,
missing/nonfinite measurements, duplicate-ID rejection, real-corpus reference
disjointness, saved input hashes and published label decisions. Whitespace checks
passed. These tests establish computation and provenance, not semantic truth.

Rebuild the existing reports using the commands in the handoff, then run:

```bash
python3 scripts/compare_disjoint_delivery.py
python3 -m unittest discover -s tests -v
```

Continue contextual review, then inspect localized audio and timing quality before
making stronger delivery claims. Updating contextual review changes exclusion
regions, so regenerate this sensitivity report after each review batch.
