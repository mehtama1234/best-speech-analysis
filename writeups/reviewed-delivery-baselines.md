# Reviewed delivery versus same-video baselines

Caption-rate screening excludes durations below a provisional 0.25-second floor; original features are preserved. See timing-quality-audit.md before interpreting deltas.

Review provenance: legacy reviewer identity is unknown; contextual per-label overrides are assistant transcript-only judgments. Baselines include target segments and are not disjoint matched controls.

This report compares transcript-reviewed supported examples with all usable transcript segments (including target examples) from the same video. Each video contributes one mean delta per label, which reduces—but does not remove—speaker, microphone, editing, topic, and segmentation confounds. Results are exploratory and do not establish effectiveness or causation.

Supported reviewed annotations: **60**; feature records: **36**.

| Candidate label | Videos | Examples | RMS Δ dB | Pitch Δ Hz | WPS Δ | Spectral centroid Δ Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 4 | 4 | -6.11893 | -46.16644 | -0.15588 | 95.84392 |
| `conclusion_or_summary` | 3 | 3 | 0.36422 | -12.44097 | -0.18368 | 92.19269 |
| `contrast_or_disagreement` | 8 | 8 | 1.88977 | 8.38618 | 0.99482 | 36.69241 |
| `definition` | 3 | 3 | 1.95341 | 27.07056 | -0.11302 | 42.63691 |
| `example` | 4 | 7 | -0.42955 | -3.53387 | 0.18469 | 5.89654 |
| `pause_event` | 2 | 2 | 2.44813 | 13.52118 | -0.4134 | -124.46775 |
| `question` | 6 | 6 | 0.17618 | 9.00494 | -0.19159 | 58.53343 |
| `story_or_personal_experience` | 5 | 8 | -1.66985 | 2.35248 | 0.02171 | 120.69756 |
| `uncertainty_or_qualification` | 7 | 8 | -2.00437 | 1.97689 | 0.01203 | -43.55161 |

## Reading the deltas

A positive delta means the reviewed segments were higher on that measured quantity than the same video's usable-segment baseline. It does not mean the speaker intentionally changed that feature or that the change improved communication. The small number of reviewed examples and the coarse measurement methods require expansion before generalization.
