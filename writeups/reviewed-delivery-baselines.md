# Reviewed delivery versus same-video baselines

This report compares manually reviewed supported examples with ordinary usable transcript segments from the same video. Each video contributes one mean delta per label, which reduces—but does not remove—speaker, microphone, editing, topic, and segmentation confounds. Results are exploratory and do not establish effectiveness or causation.

Supported reviewed annotations: **62**; feature records: **36**.

| Candidate label | Videos | Examples | RMS Δ dB | Pitch Δ Hz | WPS Δ | Spectral centroid Δ Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 4 | 4 | -6.11893 | -46.16644 | -0.15588 | 95.84392 |
| `conclusion_or_summary` | 3 | 3 | 0.36422 | -12.44097 | -1.22622 | 92.19269 |
| `contrast_or_disagreement` | 7 | 7 | 1.42165 | 12.21817 | 0.61405 | 42.06158 |
| `definition` | 5 | 6 | -1.75799 | 30.963 | -0.36778 | 58.09262 |
| `example` | 4 | 7 | -0.42955 | -3.53387 | 0.18469 | 5.89654 |
| `pause_event` | 2 | 2 | 2.44813 | 13.52118 | -0.4134 | -124.46775 |
| `question` | 6 | 6 | 0.17618 | 9.00494 | -0.71285 | 58.53343 |
| `story_or_personal_experience` | 6 | 8 | -0.11226 | -0.5027 | -0.32649 | 98.39248 |
| `uncertainty_or_qualification` | 7 | 8 | -2.00437 | 1.97689 | 0.01203 | -43.55161 |

## Reading the deltas

A positive delta means the reviewed segments were higher on that measured quantity than the same video's usable-segment baseline. It does not mean the speaker intentionally changed that feature or that the change improved communication. The small number of reviewed examples and the coarse measurement methods require expansion before generalization.
