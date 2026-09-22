# Recovered pattern candidate cards

This is the per-video evidence layer for recovered transcripts. Each card
connects one candidate pattern to exact transcript segments while preserving
source, quality and human-review boundaries.

- Source transcript rows: **83**
- Candidate cards: **2431**
- Patterns represented: **55/55**
- Cards by evidence layer: **{'alternate_source': 182, 'direct_audio': 2223, 'external_transcript': 26}**

## How to use

Use a card to open the exact excerpt, read its surrounding context, and
decide whether the words actually perform the candidate function. Treat the
candidate form as a drafting hypothesis, not a rule. Keep the quality flags
and source-review status attached when exporting a card into a lesson.

## Claim boundary

Cards are regex-assisted retrieval candidates from direct machine, alternate-source machine, and one external transcript layer. They do not establish semantic accuracy, source identity, recurrence, speaker intent, delivery meaning, or effectiveness. Exact excerpts require human context review before promotion.

## Reproducibility

```bash
python3 scripts/build_recovered_pattern_candidate_cards.py
```
