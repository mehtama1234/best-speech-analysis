# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **48**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz | Pitch proxy Hz | Pitch confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 18 | 68 | -22.33927 | 0.9375 | 0.12047 | 716.80092 | 210.59425 | 0.20185 |
| `conclusion_or_summary` | 5 | 5 | -18.6502 | 0.975 | 0.1652 | 752.2958 | 239.0196 | 0.18767 |
| `contrast_or_disagreement` | 22 | 65 | -22.08016 | 0.95045 | 0.14246 | 842.83395 | 250.50277 | 0.17186 |
| `definition` | 14 | 22 | -21.60116 | 0.89846 | 0.14894 | 889.84486 | 271.28604 | 0.16624 |
| `example` | 13 | 24 | -21.9866 | 0.88785 | 0.12935 | 779.74032 | 235.46734 | 0.16705 |
| `question` | 36 | 462 | -22.70814 | 0.92114 | 0.13465 | 804.98508 | 260.42418 | 0.18318 |
| `story_or_personal_experience` | 25 | 86 | -22.08828 | 0.93804 | 0.14299 | 808.29165 | 263.44741 | 0.17086 |
| `uncertainty_or_qualification` | 28 | 233 | -23.61572 | 0.91405 | 0.13675 | 835.60385 | 263.84223 | 0.17119 |
| `unclassified` | 41 | 8719 | -23.84527 | 0.91339 | 0.13679 | 798.40128 | 254.30628 | 0.17511 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `-54zUwySKCg` | 6 | 0 | 0.0 | None | 0 |
| `-6qN3bm2RYo` | 4 | 0 | 0.0 | None | 0 |
| `-URn1fARvts` | 2 | 0 | 0.0 | None | 0 |
| `1crhwQPKr7w` | 17 | 7 | 0.41176 | 0.04548 | 0 |
| `2fWJh-_UG5s` | 5 | 0 | 0.0 | None | 0 |
| `2m_lqGnLtWA` | 17 | 3 | 0.17647 | 0.24514 | 0 |
| `3AIoHLr8nTI` | 4 | 0 | 0.0 | None | 0 |
| `5i0u4jFmE78` | 16 | 9 | 0.5625 | 0.0626 | 0 |
| `5nN-15CrnGc` | 196 | 0 | 0.0 | None | 0 |
| `6dKimoybmEo` | 24 | 0 | 0.0 | None | 0 |
| `9fEurt2OZ0I` | 1 | 0 | 0.0 | None | 0 |
| `AwA0Jnfj3ao` | 107 | 75 | 0.70093 | 0.02339 | 0 |
| `C8-twwwTETE` | 63 | 40 | 0.63492 | 0.00694 | 0 |
| `DY2s25yRa3M` | 19 | 0 | 0.0 | None | 0 |
| `JDfP3thQYrM` | 20 | 0 | 0.0 | None | 0 |
| `JdUq2opPY-Q` | 12 | 4 | 0.33333 | 0.16961 | 0 |
| `KieuXXue2Ag` | 37 | 26 | 0.7027 | 0.015 | 0 |
| `Mo1YPGySiko` | 146 | 0 | 0.0 | None | 0 |
| `OfwfTN1mEyM` | 50 | 41 | 0.82 | 0.02261 | 0 |
| `PvcLdCo03TM` | 47 | 0 | 0.0 | None | 0 |
| `RCxgqHqakXc` | 13 | 4 | 0.30769 | 0.0213 | 0 |
| `S43F1BZfQKY` | 47 | 23 | 0.48936 | 0.03699 | 2 |
| `UtJDpOUIEd8` | 41 | 32 | 0.78049 | 0.02796 | 0 |
| `W-mgdUdOjhs` | 28 | 10 | 0.35714 | 0.11947 | 0 |
| `Y0B32z3WwwA` | 50 | 0 | 0.0 | None | 0 |
| `ZwMVMbmQBug` | 23 | 13 | 0.56522 | 0.03118 | 0 |
| `_Mb1-CN3wZs` | 25 | 9 | 0.36 | 0.07125 | 0 |
| `a1nvnY2csUw` | 20 | 0 | 0.0 | None | 0 |
| `aHXxveJTJoE` | 25 | 4 | 0.16 | 0.03782 | 0 |
| `aXmM0VZv810` | 6 | 0 | 0.0 | None | 0 |
| `bR4tDSa3O10` | 107 | 101 | 0.94393 | 0.02271 | 0 |
| `dKe3WbGR7Xs` | 49 | 0 | 0.0 | None | 0 |
| `dPi40lQetew` | 17 | 12 | 0.70588 | 0.022 | 0 |
| `dgkxN6RASpg` | 76 | 0 | 0.0 | None | 0 |
| `fBnAMUkNM2k` | 8 | 0 | 0.0 | None | 0 |
| `gDadfh0ZdBM` | 29 | 19 | 0.65517 | 0.06165 | 0 |
| `hZ0YhrgYejI` | 17 | 5 | 0.29412 | 0.02615 | 0 |
| `jxY2-YgAgm0` | 2 | 0 | 0.0 | None | 0 |
| `lcj1wMZRitI` | 55 | 36 | 0.65455 | 0.04981 | 0 |
| `m92yvNscIAo` | 16 | 6 | 0.375 | 0.03101 | 0 |
| `njmzcD4eY94` | 27 | 17 | 0.62963 | 0.03737 | 0 |
| `pmAL79dnvu0` | 51 | 23 | 0.45098 | 0.01753 | 0 |
| `qM-gZintWDc` | 29 | 10 | 0.34483 | 0.085 | 0 |
| `qOwYULOPuPs` | 4 | 0 | 0.0 | None | 0 |
| `r2kP2Pqdx6w` | 4 | 0 | 0.0 | None | 0 |
| `u1gg_L-syCw` | 18 | 8 | 0.44444 | 0.02543 | 0 |
| `xRiwgtdyjQk` | 59 | 49 | 0.83051 | 0.01611 | 0 |
| `zKCjmtxgyNg` | 46 | 40 | 0.86957 | 0.05654 | 0 |

## Interpretation boundary

A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.
