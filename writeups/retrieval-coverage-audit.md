# Corpus retrieval coverage

Census of stored heuristic retrieval labels. Unclassified is not meaningless. Context-window membership is not complete reading or semantic review of every caption. Counts do not estimate precision, recall or real-world effectiveness.

The stored registry has 102,816 segments in 395 videos. 90,397 segments (87.9%) have only the unclassified fallback.

80 distinct segments are targets of contextual assistant reviews; 692 distinct segments appear in their inspected context windows. Overlapping windows are deduplicated. Neither number proves full-transcript reading.

| Stored candidate | Segment occurrences |
| --- | ---: |
| `call_to_action` | 827 |
| `conclusion_or_summary` | 39 |
| `contrast_or_disagreement` | 854 |
| `definition` | 374 |
| `example` | 260 |
| `question` | 6,207 |
| `story_or_personal_experience` | 1,075 |
| `uncertainty_or_qualification` | 3,349 |
| `unclassified` | 90,397 |

Labels can overlap, so the occurrence column is not additive. The JSON includes per-video denominators. The existing rules use narrow phrase patterns, so unclassified passages can contain stories, claims, transitions or other substantive functions. The three contextually inspected fallback cases demonstrate this possibility but do not estimate its frequency.

Next sampling should include independently selected contiguous passages from both labelled and unclassified strata, balanced across videos and formats. Use complete speech episodes, establish speaker/promotion boundaries, and retain selection probabilities before estimating corpus rates. Do not use these hand-selected reviews as a held-out quality score.
