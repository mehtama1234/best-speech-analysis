# Pose movement analysis

This report measures frame-to-frame displacement of detected body keypoints. It does not identify gestures or infer emotion, emphasis, confidence, intent, or audience effect. Transcript joins are nearest-time retrieval aids and require manual review.

Videos: **36**; movement pairs: **68**; transcript/motion joins: **352**.

## Video-level movement

| Video | Pairs | Mean keypoint displacement | Mean wrist displacement | Mean shoulder displacement |
|---|---:|---:|---:|---:|
| `1crhwQPKr7w` | 2 | 0.29802 | 0.24375 | 0.32253 |
| `2fWJh-_UG5s` | 2 | 0.06104 | 0.0875 | 0.03 |
| `2m_lqGnLtWA` | 2 | 0.21322 | 0.08908 | 0.20464 |
| `3AIoHLr8nTI` | 1 | 0.10865 | 0.25383 | 0.06279 |
| `5i0u4jFmE78` | 3 | 0.43523 | 0.5172 | 0.42417 |
| `9fEurt2OZ0I` | 2 | 0.4281 | 0.50805 | 0.33841 |
| `AwA0Jnfj3ao` | 1 | 0.05838 | 0.04954 | 0.00864 |
| `C8-twwwTETE` | 2 | 0.20821 | 0.1662 | 0.20906 |
| `JDfP3thQYrM` | 2 | 0.25042 | 0.2665 | 0.21369 |
| `JdUq2opPY-Q` | 2 | 0.27513 | 0.34109 | 0.19021 |
| `KieuXXue2Ag` | 2 | 0.17873 | 0.10963 | 0.12412 |
| `OfwfTN1mEyM` | 2 | 0.12243 | 0.1776 | 0.16274 |
| `RCxgqHqakXc` | 1 | 0.18276 | 0.15237 | 0.16639 |
| `S43F1BZfQKY` | 1 | 0.29538 | 0.48787 | 0.19977 |
| `UtJDpOUIEd8` | 2 | 0.23038 | 0.24618 | 0.19873 |
| `W-mgdUdOjhs` | 2 | 0.35156 | 0.45961 | 0.31159 |
| `ZwMVMbmQBug` | 2 | 0.40574 | 0.48168 | 0.45047 |
| `_Mb1-CN3wZs` | 2 | 0.39363 | 0.44883 | 0.3271 |
| `aHXxveJTJoE` | 1 | 0.64415 | 0.96075 | 0.58193 |
| `aXmM0VZv810` | 2 | 0.20761 | 0.28836 | 0.10227 |
| `bR4tDSa3O10` | 2 | 0.08077 | 0.11557 | 0.03773 |
| `dPi40lQetew` | 2 | 0.40138 | 0.48732 | 0.35338 |
| `fBnAMUkNM2k` | 1 | 0.3032 | 0.43409 | 0.27846 |
| `gDadfh0ZdBM` | 2 | 0.28629 | 0.23123 | 0.31636 |
| `hZ0YhrgYejI` | 1 | 0.17538 | 0.23087 | 0.27011 |
| `jxY2-YgAgm0` | 2 | 0.12204 | 0.13256 | 0.10039 |
| `lcj1wMZRitI` | 2 | 0.27849 | 0.43907 | 0.42251 |
| `m92yvNscIAo` | 2 | 0.27147 | 0.29363 | 0.3854 |
| `njmzcD4eY94` | 3 | 0.23298 | 0.24911 | 0.24006 |
| `pmAL79dnvu0` | 2 | 0.34537 | 0.34718 | 0.34079 |
| `qM-gZintWDc` | 3 | 0.36612 | 0.38579 | 0.34777 |
| `qOwYULOPuPs` | 2 | 0.24095 | 0.26868 | 0.19858 |
| `r2kP2Pqdx6w` | 2 | 0.03848 | 0.03643 | 0.02561 |
| `u1gg_L-syCw` | 2 | 0.38204 | 0.44503 | 0.38688 |
| `xRiwgtdyjQk` | 2 | 0.04905 | 0.03177 | 0.03229 |
| `zKCjmtxgyNg` | 2 | 0.18738 | 0.17467 | 0.13934 |

## Heuristic speech-function joins

| Candidate label | Joins | Videos | Mean keypoint movement | Mean wrist movement | Mean shoulder movement |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 1 | 1 | 0.5194 | 0.52137 | 0.50127 |
| `contrast_or_disagreement` | 3 | 3 | 0.3161 | 0.29424 | 0.33106 |
| `question` | 20 | 13 | 0.34521 | 0.43225 | 0.31986 |
| `story_or_personal_experience` | 1 | 1 | 0.5194 | 0.52137 | 0.50127 |
| `uncertainty_or_qualification` | 10 | 6 | 0.17545 | 0.21455 | 0.14802 |
| `unclassified` | 318 | 30 | 0.26374 | 0.30568 | 0.25175 |

Movement can come from a speaker, camera motion, cuts, zooms, tracking errors, or scene changes. The measurements therefore require frame inspection and scene controls before they can support a communication principle.
