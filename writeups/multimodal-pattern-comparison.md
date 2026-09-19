# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **68**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz | Pitch proxy Hz | Pitch confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 29 | 114 | -21.18938 | 0.96006 | 0.12523 | 706.5825 | 215.79605 | 0.19582 |
| `conclusion_or_summary` | 8 | 8 | -17.65038 | 0.98438 | 0.16855 | 798.29287 | 257.46025 | 0.18691 |
| `contrast_or_disagreement` | 33 | 91 | -21.29954 | 0.94798 | 0.14259 | 806.50562 | 256.88093 | 0.17262 |
| `definition` | 19 | 35 | -20.55683 | 0.92411 | 0.14705 | 826.47139 | 265.92513 | 0.15987 |
| `example` | 23 | 51 | -21.00832 | 0.92202 | 0.13355 | 758.20985 | 247.26378 | 0.16892 |
| `question` | 56 | 786 | -22.57904 | 0.91856 | 0.13662 | 799.43154 | 258.54048 | 0.17989 |
| `story_or_personal_experience` | 37 | 141 | -21.16136 | 0.95034 | 0.14134 | 784.30392 | 260.88226 | 0.17264 |
| `uncertainty_or_qualification` | 42 | 455 | -22.11659 | 0.93462 | 0.13736 | 786.26966 | 260.63874 | 0.17202 |
| `unclassified` | 61 | 13069 | -23.24509 | 0.91637 | 0.13973 | 796.56984 | 255.21298 | 0.17715 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `-54zUwySKCg` | 6 | 0 | 0.0 | None | 0 |
| `-6qN3bm2RYo` | 4 | 0 | 0.0 | None | 0 |
| `-CXBIAH4Kgo` | 4 | 0 | 0.0 | None | 0 |
| `-URn1fARvts` | 2 | 0 | 0.0 | None | 0 |
| `1crhwQPKr7w` | 17 | 7 | 0.41176 | 0.04548 | 0 |
| `1qfB9wExiy8` | 10 | 0 | 0.0 | None | 0 |
| `2fWJh-_UG5s` | 5 | 0 | 0.0 | None | 0 |
| `2m_lqGnLtWA` | 17 | 3 | 0.17647 | 0.24514 | 0 |
| `3AIoHLr8nTI` | 4 | 0 | 0.0 | None | 0 |
| `4u71aIcrxtQ` | 24 | 0 | 0.0 | None | 0 |
| `5i0u4jFmE78` | 16 | 9 | 0.5625 | 0.0626 | 0 |
| `5nN-15CrnGc` | 196 | 0 | 0.0 | None | 0 |
| `6dKimoybmEo` | 24 | 0 | 0.0 | None | 0 |
| `9fEurt2OZ0I` | 1 | 0 | 0.0 | None | 0 |
| `AjxbqKcPX_4` | 21 | 0 | 0.0 | None | 0 |
| `AwA0Jnfj3ao` | 107 | 75 | 0.70093 | 0.02339 | 0 |
| `C8-twwwTETE` | 63 | 40 | 0.63492 | 0.00694 | 0 |
| `DY2s25yRa3M` | 19 | 0 | 0.0 | None | 0 |
| `EC5L1MSlqtg` | 9 | 0 | 0.0 | None | 0 |
| `Elv-c3ZTkYg` | 6 | 0 | 0.0 | None | 0 |
| `GRiDVoMFxcU` | 10 | 0 | 0.0 | None | 0 |
| `H5bSGdZk8pQ` | 11 | 0 | 0.0 | None | 0 |
| `JDfP3thQYrM` | 20 | 0 | 0.0 | None | 0 |
| `JFd8bnupsQY` | 9 | 0 | 0.0 | None | 0 |
| `JdUq2opPY-Q` | 12 | 4 | 0.33333 | 0.16961 | 0 |
| `KieuXXue2Ag` | 37 | 26 | 0.7027 | 0.015 | 0 |
| `LJRs2TnP9H8` | 4 | 0 | 0.0 | None | 0 |
| `Mo1YPGySiko` | 146 | 0 | 0.0 | None | 0 |
| `O1VdQQkbUOU` | 26 | 0 | 0.0 | None | 0 |
| `OfwfTN1mEyM` | 50 | 41 | 0.82 | 0.02261 | 0 |
| `PvcLdCo03TM` | 47 | 0 | 0.0 | None | 0 |
| `RCxgqHqakXc` | 13 | 4 | 0.30769 | 0.0213 | 0 |
| `RnIqGFqPwkQ` | 23 | 0 | 0.0 | None | 0 |
| `S43F1BZfQKY` | 47 | 23 | 0.48936 | 0.03699 | 2 |
| `UtJDpOUIEd8` | 41 | 32 | 0.78049 | 0.02796 | 0 |
| `W-mgdUdOjhs` | 28 | 10 | 0.35714 | 0.11947 | 0 |
| `XR8aTbvRhxQ` | 28 | 0 | 0.0 | None | 0 |
| `Y0B32z3WwwA` | 50 | 0 | 0.0 | None | 0 |
| `ZHpyfTC_Ovo` | 21 | 0 | 0.0 | None | 0 |
| `ZaX_8iKSBsQ` | 4 | 0 | 0.0 | None | 0 |
| `ZwMVMbmQBug` | 23 | 13 | 0.56522 | 0.03118 | 0 |
| `_Mb1-CN3wZs` | 25 | 9 | 0.36 | 0.07125 | 0 |
| `_S955fkSZd8` | 16 | 0 | 0.0 | None | 0 |
| `a1nvnY2csUw` | 20 | 0 | 0.0 | None | 0 |
| `aHXxveJTJoE` | 25 | 4 | 0.16 | 0.03782 | 0 |
| `aJxynX6kjUE` | 12 | 0 | 0.0 | None | 0 |
| `aXmM0VZv810` | 6 | 0 | 0.0 | None | 0 |
| `bR4tDSa3O10` | 107 | 101 | 0.94393 | 0.02271 | 0 |
| `dKe3WbGR7Xs` | 49 | 0 | 0.0 | None | 0 |
| `dPi40lQetew` | 17 | 12 | 0.70588 | 0.022 | 0 |
| `dgkxN6RASpg` | 76 | 0 | 0.0 | None | 0 |
| `fBnAMUkNM2k` | 8 | 0 | 0.0 | None | 0 |
| `gDadfh0ZdBM` | 29 | 19 | 0.65517 | 0.06165 | 0 |
| `gWziScXTR_4` | 10 | 0 | 0.0 | None | 0 |
| `hZ0YhrgYejI` | 17 | 5 | 0.29412 | 0.02615 | 0 |
| `jxY2-YgAgm0` | 2 | 0 | 0.0 | None | 0 |
| `kHti_4zsQhc` | 8 | 0 | 0.0 | None | 0 |
| `lcj1wMZRitI` | 55 | 36 | 0.65455 | 0.04981 | 0 |
| `m92yvNscIAo` | 16 | 6 | 0.375 | 0.03101 | 0 |
| `njmzcD4eY94` | 27 | 17 | 0.62963 | 0.03737 | 0 |
| `pmAL79dnvu0` | 51 | 23 | 0.45098 | 0.01753 | 0 |
| `qM-gZintWDc` | 29 | 10 | 0.34483 | 0.085 | 0 |
| `qOwYULOPuPs` | 4 | 0 | 0.0 | None | 0 |
| `r2kP2Pqdx6w` | 4 | 0 | 0.0 | None | 0 |
| `stxIHzmQw6w` | 17 | 0 | 0.0 | None | 0 |
| `u1gg_L-syCw` | 18 | 8 | 0.44444 | 0.02543 | 0 |
| `xRiwgtdyjQk` | 59 | 49 | 0.83051 | 0.01611 | 0 |
| `zKCjmtxgyNg` | 46 | 40 | 0.86957 | 0.05654 | 0 |

## Interpretation boundary

A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.
