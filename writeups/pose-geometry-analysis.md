# Pose geometry analysis

This report measures visible person/keypoint geometry only. It does not identify gestures, emotional expressions, confidence, intent, or meaning. Transcript-to-frame joins are nearest-time retrieval aids and require manual review.

Pose records: **36** videos and **144** sampled frames; person detections: **104**; transcript/frame joins: **220**.

## Video coverage

| Video | Frames | Person frames | Detection fraction | Mean visible keypoints | Mean visible wrists | Mean shoulder width |
|---|---:|---:|---:|---:|---:|---:|
| `1crhwQPKr7w` | 4 | 3 | 0.75 | 17 | 2 | 0.36068 |
| `2fWJh-_UG5s` | 4 | 3 | 0.75 | 17 | 2 | 0.27738 |
| `2m_lqGnLtWA` | 4 | 3 | 0.75 | 17 | 2 | 0.43704 |
| `3AIoHLr8nTI` | 4 | 2 | 0.5 | 17 | 2 | 0.21785 |
| `5i0u4jFmE78` | 4 | 4 | 1.0 | 17 | 2 | 0.19194 |
| `9fEurt2OZ0I` | 4 | 3 | 0.75 | 17 | 2 | 0.28384 |
| `AwA0Jnfj3ao` | 4 | 2 | 0.5 | 17 | 2 | 0.24849 |
| `C8-twwwTETE` | 4 | 3 | 0.75 | 17 | 2 | 0.15393 |
| `JDfP3thQYrM` | 4 | 3 | 0.75 | 17 | 2 | 0.29688 |
| `JdUq2opPY-Q` | 4 | 3 | 0.75 | 17 | 2 | 0.42964 |
| `KieuXXue2Ag` | 4 | 3 | 0.75 | 17 | 2 | 0.15861 |
| `OfwfTN1mEyM` | 4 | 3 | 0.75 | 17 | 2 | 0.24148 |
| `RCxgqHqakXc` | 4 | 2 | 0.5 | 17 | 2 | 0.08152 |
| `S43F1BZfQKY` | 4 | 2 | 0.5 | 17 | 2 | 0.16162 |
| `UtJDpOUIEd8` | 4 | 3 | 0.75 | 17 | 2 | 0.18787 |
| `W-mgdUdOjhs` | 4 | 3 | 0.75 | 17 | 2 | 0.32735 |
| `ZwMVMbmQBug` | 4 | 3 | 0.75 | 17 | 2 | 0.22614 |
| `_Mb1-CN3wZs` | 4 | 3 | 0.75 | 17 | 2 | 0.25199 |
| `aHXxveJTJoE` | 4 | 2 | 0.5 | 17 | 2 | 0.35631 |
| `aXmM0VZv810` | 4 | 3 | 0.75 | 17 | 2 | 0.1211 |
| `bR4tDSa3O10` | 4 | 3 | 0.75 | 17 | 2 | 0.29953 |
| `dPi40lQetew` | 4 | 3 | 0.75 | 17 | 2 | 0.21772 |
| `fBnAMUkNM2k` | 4 | 2 | 0.5 | 17 | 2 | 0.35786 |
| `gDadfh0ZdBM` | 4 | 3 | 0.75 | 17 | 2 | 0.39399 |
| `hZ0YhrgYejI` | 4 | 2 | 0.5 | 17 | 2 | 0.15118 |
| `jxY2-YgAgm0` | 4 | 3 | 0.75 | 17 | 2 | 0.17828 |
| `lcj1wMZRitI` | 4 | 3 | 0.75 | 17 | 2 | 0.44342 |
| `m92yvNscIAo` | 4 | 3 | 0.75 | 17 | 2 | 0.21762 |
| `njmzcD4eY94` | 4 | 4 | 1.0 | 17 | 2 | 0.24232 |
| `pmAL79dnvu0` | 4 | 3 | 0.75 | 17 | 2 | 0.15864 |
| `qM-gZintWDc` | 4 | 4 | 1.0 | 17 | 2 | 0.36856 |
| `qOwYULOPuPs` | 4 | 3 | 0.75 | 17 | 2 | 0.17729 |
| `r2kP2Pqdx6w` | 4 | 3 | 0.75 | 17 | 2 | 0.12476 |
| `u1gg_L-syCw` | 4 | 3 | 0.75 | 17 | 2 | 0.1797 |
| `xRiwgtdyjQk` | 4 | 3 | 0.75 | 17 | 2 | 0.24181 |
| `zKCjmtxgyNg` | 4 | 3 | 0.75 | 17 | 2 | 0.35043 |

## Heuristic speech-function joins

| Candidate label | Joined examples | Videos | Mean visible keypoints | Mean visible wrists | Mean shoulder width |
|---|---:|---:|---:|---:|---:|
| `call_to_action` | 1 | 1 | 17 | 2 | 0.12657 |
| `definition` | 1 | 1 | 17 | 2 | 0.37424 |
| `question` | 10 | 7 | 17 | 2 | 0.27309 |
| `story_or_personal_experience` | 1 | 1 | 17 | 2 | 0.24282 |
| `uncertainty_or_qualification` | 5 | 5 | 17 | 2 | 0.22427 |
| `unclassified` | 202 | 30 | 17 | 2 | 0.24159 |

A difference in keypoint visibility, wrist visibility, or shoulder geometry is an observable difference in sampled frames. It is not evidence of a gesture, emotion, emphasis, persuasion, or audience effect. The next step is manual review of matched frames and expansion beyond four sampled frames per video.
