# Multimodal expansion coverage audit

Status: **raw media reconciled; manual review pending**.

The deterministic expansion contains **41** selected videos, of which **30** have both local raw video and audio, **0** have partial raw media, **7** have derived features but no local raw files, and **4** have neither local raw media nor derived features. Derived feature files are present for **37** selected videos.

This is coverage evidence, not a claim that the selected videos have been manually reviewed or that the full corpus has audiovisual coverage. Raw-complete items without retained transcripts are accounted for separately and cannot support transcript-linked speech-function review.

## Manual-review queue

The JSON queue is limited to selected videos with both raw streams and nonempty transcripts. Each item keeps its duration stratum, candidate-function counts, and source selection reason so reviewers can sample across settings rather than choosing only famous examples.

## Limits

- Raw files prove local availability, not that a human inspected the delivery.
- Derived features are measurements/proxies and do not establish speech function or audience effect.
- The expansion is stratified but not a complete audiovisual census of the 395 transcript-reviewed videos.
- Candidate function counts come from heuristic transcript retrieval and remain unvalidated.
