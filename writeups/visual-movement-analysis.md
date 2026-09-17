# Pilot visual movement analysis

This report measures changes in detected face geometry and scene luminance between sampled frames. It is not facial-expression recognition and does not infer emotion, confidence, or intent. Speech-function labels are heuristic retrieval aids.

| Candidate label | Videos | Face-center movement | Face-area change | Scene luminance change | Face-presence transitions |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 5 | 0.18225 | 0.00224 | 5.41721 | 0.29524 |
| `contrast_or_disagreement` | 4 | 0.08604 | 0.0021 | 8.68683 | 0.375 |
| `definition` | 2 | 0.04388 | 0.0025 | 61.349 | 0.5 |
| `example` | 4 | 0.167 | 0.01214 | 24.634 | 0.25 |
| `question` | 12 | 0.07432 | 0.00488 | 11.09217 | 0.27969 |
| `story_or_personal_experience` | 5 | 0.1125 | 0.02417 | 10.22305 | 0.2 |
| `uncertainty_or_qualification` | 12 | 0.18263 | 0.01603 | 7.90555 | 0.38353 |
| `unclassified` | 20 | 0.11026 | 0.01612 | 11.81714 | 0.31855 |

## Limits

A change in detected face position can result from camera movement, cuts, zoom, tracking error, posture, or actual head movement. The current pilot does not measure hands, posture, gaze direction, or facial muscle action units.
