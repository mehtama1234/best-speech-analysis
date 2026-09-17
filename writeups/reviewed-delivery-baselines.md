# Reviewed delivery versus same-video baselines

This report compares manually reviewed supported examples with ordinary usable transcript segments from the same video. Each video contributes one mean delta per label, which reduces—but does not remove—speaker, microphone, editing, topic, and segmentation confounds. Results are exploratory and do not establish effectiveness or causation.

Supported reviewed annotations: **35**; feature records: **36**.

| Candidate label | Videos | Examples | RMS Δ dB | Pitch Δ Hz | WPS Δ | Spectral centroid Δ Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 1 | 1 | -4.99899 | 35.55667 | 0.2666 | 546.36948 |
| `conclusion_or_summary` | 2 | 2 | -1.79265 | -27.65331 | -0.3799 | 87.7721 |
| `contrast_or_disagreement` | 3 | 3 | 0.72523 | 39.90607 | 0.23045 | -34.33525 |
| `definition` | 3 | 3 | -4.82014 | 9.04148 | -0.88667 | 148.92435 |
| `example` | 2 | 3 | 1.17035 | -0.00231 | 0.2141 | 39.5351 |
| `pause_event` | 2 | 2 | 2.44813 | 13.52118 | -0.4134 | -124.46775 |
| `question` | 3 | 3 | 1.92635 | -41.38026 | 0.38306 | -118.42462 |
| `story_or_personal_experience` | 3 | 4 | 1.16957 | -1.42866 | 0.24179 | 212.42516 |
| `uncertainty_or_qualification` | 3 | 3 | -3.4406 | -45.40161 | 0.09677 | -117.85101 |

## Reading the deltas

A positive delta means the reviewed segments were higher on that measured quantity than the same video's usable-segment baseline. It does not mean the speaker intentionally changed that feature or that the change improved communication. The small number of reviewed examples and the coarse measurement methods require expansion before generalization.
