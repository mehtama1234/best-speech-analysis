# Draft listener-stimulus automated preflight

Status: **automated screening; not independent review**.

Token overlap, word counts, marker checks and keyword safety flags are screening aids. They cannot establish proposition equivalence, readability, accessibility, causal isolation or listener outcomes.

- Pairs: 18
- Maximum absolute word-count delta: 13
- Minimum non-stopword Jaccard overlap: 0.045
- Marker flags: 0
- Safety flags: 0
- Pairs still requiring manual review: 18

| Job | Word delta | Token overlap | Marker | Safety flags |
|---|---:|---:|---|---|
| `opening` | +2 | 0.500 | `present` | none |
| `closing` | +13 | 0.650 | `present` | none |
| `question` | +13 | 0.400 | `present` | none |
| `answer_or_response` | +13 | 0.588 | `present` | none |
| `story_or_personal_experience` | +7 | 0.139 | `present` | none |
| `example_or_case` | +7 | 0.182 | `present` | none |
| `contrast_or_disagreement` | +4 | 0.333 | `present` | none |
| `correction_or_reframe` | +1 | 0.296 | `present` | none |
| `repair_or_self_correction` | +5 | 0.583 | `present` | none |
| `qualification_or_boundary` | +13 | 0.294 | `present` | none |
| `definition_or_explanation` | +10 | 0.045 | `present` | none |
| `transition_or_structure` | +9 | 0.474 | `present` | none |
| `callback_or_repetition` | +11 | 0.174 | `present` | none |
| `humor_or_rapport` | +8 | 0.647 | `present` | none |
| `credit_or_acknowledgment` | +12 | 0.214 | `present` | none |
| `call_to_action_or_audience_role` | +7 | 0.088 | `present` | none |
| `persuasion_or_advocacy` | +8 | 0.135 | `present` | none |
| `reflection_or_value_frame` | +7 | 0.344 | `present` | none |
