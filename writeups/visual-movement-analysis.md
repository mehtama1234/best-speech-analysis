# Pilot visual movement analysis

This report measures changes in detected face geometry and scene luminance between sampled frames. It is not facial-expression recognition and does not infer emotion, confidence, or intent. Speech-function labels are heuristic retrieval aids.

| Candidate label | Videos | Face-center movement | Face-area change | Scene luminance change | Face-presence transitions |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 48 | None | None | 13.49171 | 0.0625 |
| `conclusion_or_summary` | 2 | None | None | 3.0015 | 0.5 |
| `contrast_or_disagreement` | 51 | 0.07244 | 0.0026 | 12.32832 | 0.02614 |
| `definition` | 17 | None | None | 11.24515 | 0.05882 |
| `example` | 14 | 0.24026 | 0.0097 | 4.88367 | 0.02381 |
| `question` | 187 | 0.11334 | 0.00547 | 12.14688 | 0.01772 |
| `story_or_personal_experience` | 59 | 0.17233 | 0.0244 | 15.74848 | 0.0339 |
| `uncertainty_or_qualification` | 119 | 0.19754 | 0.03206 | 11.66879 | 0.02941 |
| `unclassified` | 360 | 0.15925 | 0.02091 | 13.99107 | 0.02594 |

## Limits

A change in detected face position can result from camera movement, cuts, zoom, tracking error, posture, or actual head movement. The current pilot does not measure hands, posture, gaze direction, or facial muscle action units.
