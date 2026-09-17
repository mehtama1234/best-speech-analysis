# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **36**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz | Pitch proxy Hz | Pitch confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 11 | 40 | -24.57549 | 0.90673 | 0.1317 | 783.2814 | 217.97205 | 0.18737 |
| `conclusion_or_summary` | 3 | 3 | -18.20367 | 0.95833 | 0.18258 | 792.802 | 209.75933 | 0.18895 |
| `contrast_or_disagreement` | 14 | 31 | -23.51113 | 0.93856 | 0.14862 | 858.45485 | 252.29909 | 0.16999 |
| `definition` | 8 | 9 | -25.37425 | 0.83125 | 0.16958 | 1097.67169 | 293.99125 | 0.1576 |
| `example` | 8 | 18 | -24.27966 | 0.8495 | 0.12875 | 745.14035 | 231.47074 | 0.15699 |
| `question` | 25 | 251 | -23.89411 | 0.90703 | 0.13625 | 822.18969 | 265.22757 | 0.17814 |
| `story_or_personal_experience` | 15 | 44 | -23.89175 | 0.92494 | 0.15134 | 860.83102 | 273.80487 | 0.15628 |
| `uncertainty_or_qualification` | 20 | 134 | -24.81215 | 0.89983 | 0.13672 | 833.28902 | 265.36704 | 0.16972 |
| `unclassified` | 30 | 4547 | -25.33196 | 0.89578 | 0.13933 | 818.17669 | 256.4432 | 0.17199 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `1crhwQPKr7w` | 17 | 7 | 0.41176 | 0.04548 | 0 |
| `2fWJh-_UG5s` | 139 | 105 | 0.7554 | 0.03017 | 0 |
| `2m_lqGnLtWA` | 17 | 3 | 0.17647 | 0.24514 | 0 |
| `3AIoHLr8nTI` | 102 | 95 | 0.93137 | 0.01637 | 0 |
| `5i0u4jFmE78` | 16 | 9 | 0.5625 | 0.0626 | 0 |
| `9fEurt2OZ0I` | 13 | 10 | 0.76923 | 0.04928 | 0 |
| `AwA0Jnfj3ao` | 107 | 75 | 0.70093 | 0.02339 | 0 |
| `C8-twwwTETE` | 63 | 40 | 0.63492 | 0.00694 | 0 |
| `JDfP3thQYrM` | 59 | 44 | 0.74576 | 0.04451 | 1 |
| `JdUq2opPY-Q` | 12 | 4 | 0.33333 | 0.16961 | 0 |
| `KieuXXue2Ag` | 37 | 26 | 0.7027 | 0.015 | 0 |
| `OfwfTN1mEyM` | 50 | 41 | 0.82 | 0.02261 | 0 |
| `RCxgqHqakXc` | 13 | 4 | 0.30769 | 0.0213 | 0 |
| `S43F1BZfQKY` | 47 | 23 | 0.48936 | 0.03699 | 2 |
| `UtJDpOUIEd8` | 41 | 32 | 0.78049 | 0.02796 | 0 |
| `W-mgdUdOjhs` | 28 | 10 | 0.35714 | 0.11947 | 0 |
| `ZwMVMbmQBug` | 23 | 13 | 0.56522 | 0.03118 | 0 |
| `_Mb1-CN3wZs` | 25 | 9 | 0.36 | 0.07125 | 0 |
| `aHXxveJTJoE` | 25 | 4 | 0.16 | 0.03782 | 0 |
| `aXmM0VZv810` | 162 | 107 | 0.66049 | 0.04026 | 0 |
| `bR4tDSa3O10` | 107 | 101 | 0.94393 | 0.02271 | 0 |
| `dPi40lQetew` | 17 | 12 | 0.70588 | 0.022 | 0 |
| `fBnAMUkNM2k` | 238 | 139 | 0.58403 | 0.05382 | 0 |
| `gDadfh0ZdBM` | 29 | 19 | 0.65517 | 0.06165 | 0 |
| `hZ0YhrgYejI` | 17 | 5 | 0.29412 | 0.02615 | 0 |
| `jxY2-YgAgm0` | 39 | 34 | 0.87179 | 0.02117 | 0 |
| `lcj1wMZRitI` | 55 | 36 | 0.65455 | 0.04981 | 0 |
| `m92yvNscIAo` | 16 | 6 | 0.375 | 0.03101 | 0 |
| `njmzcD4eY94` | 27 | 17 | 0.62963 | 0.03737 | 0 |
| `pmAL79dnvu0` | 51 | 23 | 0.45098 | 0.01753 | 0 |
| `qM-gZintWDc` | 29 | 10 | 0.34483 | 0.085 | 0 |
| `qOwYULOPuPs` | 93 | 72 | 0.77419 | 0.03875 | 0 |
| `r2kP2Pqdx6w` | 103 | 99 | 0.96117 | 0.00933 | 0 |
| `u1gg_L-syCw` | 18 | 8 | 0.44444 | 0.02543 | 0 |
| `xRiwgtdyjQk` | 59 | 49 | 0.83051 | 0.01611 | 0 |
| `zKCjmtxgyNg` | 46 | 40 | 0.86957 | 0.05654 | 0 |

## Interpretation boundary

A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.
