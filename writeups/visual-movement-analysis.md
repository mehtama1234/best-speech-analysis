# Full local visual movement analysis

This report measures changes in detected face geometry and scene luminance between sampled frames in locally available feature reports. It is not facial-expression recognition and does not infer emotion, confidence, or intent. Speech-function labels are heuristic retrieval aids.

| Candidate label | Videos | Face-center movement | Face-area change | Scene luminance change | Face-presence transitions |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 48 | 0.07682 | 0.00664 | 13.49171 | 0.40625 |
| `conclusion_or_summary` | 2 | None | None | 3.0015 | 0.5 |
| `contrast_or_disagreement` | 51 | 0.04087 | 0.00777 | 12.32832 | 0.27124 |
| `definition` | 17 | 0.10731 | 0.03731 | 11.24515 | 0.11765 |
| `example` | 14 | 0.10082 | 0.00875 | 4.88367 | 0.16667 |
| `question` | 187 | 0.07195 | 0.011 | 12.14688 | 0.29455 |
| `story_or_personal_experience` | 59 | 0.08135 | 0.01012 | 15.73062 | 0.35085 |
| `uncertainty_or_qualification` | 119 | 0.09901 | 0.02018 | 11.66879 | 0.35308 |
| `unclassified` | 360 | 0.09237 | 0.01406 | 13.98456 | 0.33853 |

## Limits

A change in detected face position can result from camera movement, cuts, zoom, tracking error, posture, or actual head movement. The current proxy does not measure hands, posture, gaze direction, or facial muscle action units. A null face count means the detector was unavailable for that frame, not that no face was present.
