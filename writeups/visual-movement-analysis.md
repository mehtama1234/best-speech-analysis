# Pilot visual movement analysis

This report measures changes in detected face geometry and scene luminance between sampled frames. It is not facial-expression recognition and does not infer emotion, confidence, or intent. Speech-function labels are heuristic retrieval aids.

| Candidate label | Videos | Face-center movement | Face-area change | Scene luminance change | Face-presence transitions |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 8 | 0.18225 | 0.00224 | 9.82982 | 0.43452 |
| `conclusion_or_summary` | 1 | None | None | 2.193 | 1 |
| `contrast_or_disagreement` | 5 | 0.08264 | 0.00223 | 7.37347 | 0.36667 |
| `definition` | 3 | 0.04388 | 0.0025 | 50.41233 | 0.66667 |
| `example` | 5 | 0.167 | 0.01214 | 20.22107 | 0.26667 |
| `question` | 18 | 0.0987 | 0.00538 | 10.61028 | 0.26146 |
| `story_or_personal_experience` | 9 | 0.14301 | 0.02108 | 10.56075 | 0.22222 |
| `uncertainty_or_qualification` | 18 | 0.17824 | 0.02434 | 7.50527 | 0.28347 |
| `unclassified` | 36 | 0.13829 | 0.01733 | 12.88509 | 0.31029 |

## Limits

A change in detected face position can result from camera movement, cuts, zoom, tracking error, posture, or actual head movement. The current pilot does not measure hands, posture, gaze direction, or facial muscle action units.
