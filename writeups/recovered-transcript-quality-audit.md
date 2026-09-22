# Recovered transcript quality audit

This report audits structural properties of recovered transcript candidates.
It is not a semantic or effectiveness validation report.

- Candidate rows: **83**
- Evidence layers: **{'alternate_source': 11, 'direct_audio': 71, 'external_transcript': 1}**
- Dispositions: **{'external_candidate_not_timestamped': 1, 'machine_candidate_structurally_consistent': 10, 'machine_candidate_with_quality_flags': 72}**

## What this establishes

The report checks timestamp shape, ordering, overlaps, duplicate segments, empty text and obvious publisher boilerplate. Direct and alternate rows remain machine-transcript candidates; alternate-source identity is not promoted by structural cleanliness.

## Boundary

This audit checks transcript structure and obvious contamination only. It does not establish semantic accuracy, source identity, speaker identity, human review, recurrence, delivery meaning, or effectiveness.

## Reproducibility

```bash
python3 scripts/build_recovered_transcript_quality_audit.py
```
