# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **84**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz | Pitch proxy Hz | Pitch confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 39 | 133 | -20.94586 | 0.95764 | 0.12891 | 732.37519 | 219.88913 | 0.19493 |
| `conclusion_or_summary` | 9 | 9 | -17.61044 | 0.98611 | 0.17995 | 885.27756 | 263.40222 | 0.19002 |
| `contrast_or_disagreement` | 44 | 126 | -20.6353 | 0.95454 | 0.14421 | 836.30016 | 260.45328 | 0.17341 |
| `definition` | 28 | 50 | -20.3801 | 0.93998 | 0.14672 | 825.62528 | 261.56011 | 0.16307 |
| `example` | 30 | 61 | -20.30839 | 0.94022 | 0.13182 | 755.75498 | 241.73963 | 0.17713 |
| `question` | 72 | 1019 | -21.76262 | 0.93158 | 0.13926 | 830.64272 | 257.8555 | 0.18305 |
| `story_or_personal_experience` | 51 | 224 | -20.5346 | 0.96103 | 0.14235 | 800.40254 | 259.2452 | 0.1742 |
| `uncertainty_or_qualification` | 58 | 598 | -21.19585 | 0.94573 | 0.13937 | 811.98327 | 259.64863 | 0.17665 |
| `unclassified` | 77 | 16865 | -22.36565 | 0.93021 | 0.14164 | 822.67549 | 255.22687 | 0.18068 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `-54zUwySKCg` | 6 | 0 | 0.0 | None | 0 |
| `-6qN3bm2RYo` | 4 | 0 | 0.0 | None | 0 |
| `-CXBIAH4Kgo` | 4 | 0 | 0.0 | None | 0 |
| `-URn1fARvts` | 2 | 0 | 0.0 | None | 0 |
| `-s-h-eebSgw` | 16 | 0 | 0.0 | None | 0 |
| `0eNEz2lhyk8` | 8 | 0 | 0.0 | None | 0 |
| `19rhQUB_FQc` | 16 | 0 | 0.0 | None | 0 |
| `1crhwQPKr7w` | 17 | 7 | 0.41176 | 0.04548 | 0 |
| `1i9kcBHX2Nw` | 15 | 0 | 0.0 | None | 0 |
| `1qfB9wExiy8` | 10 | 0 | 0.0 | None | 0 |
| `2ZTdqh-a0tU` | 4 | 0 | 0.0 | None | 0 |
| `2fWJh-_UG5s` | 5 | 0 | 0.0 | None | 0 |
| `2m_lqGnLtWA` | 17 | 3 | 0.17647 | 0.24514 | 0 |
| `3AIoHLr8nTI` | 4 | 0 | 0.0 | None | 0 |
| `4u71aIcrxtQ` | 24 | 0 | 0.0 | None | 0 |
| `5i0u4jFmE78` | 16 | 9 | 0.5625 | 0.0626 | 0 |
| `5nN-15CrnGc` | 196 | 0 | 0.0 | None | 0 |
| `6PNDD5Xy5DU` | 15 | 0 | 0.0 | None | 0 |
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
| `N6ROB3Q_iXg` | 26 | 0 | 0.0 | None | 0 |
| `O1VdQQkbUOU` | 26 | 0 | 0.0 | None | 0 |
| `OfwfTN1mEyM` | 50 | 41 | 0.82 | 0.02261 | 0 |
| `PvcLdCo03TM` | 47 | 0 | 0.0 | None | 0 |
| `RCxgqHqakXc` | 13 | 4 | 0.30769 | 0.0213 | 0 |
| `RLklwFPNQ_g` | 14 | 0 | 0.0 | None | 0 |
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
| `_nUDuXRh3zM` | 16 | 0 | 0.0 | None | 0 |
| `a1nvnY2csUw` | 20 | 0 | 0.0 | None | 0 |
| `aHXxveJTJoE` | 25 | 4 | 0.16 | 0.03782 | 0 |
| `aJxynX6kjUE` | 12 | 0 | 0.0 | None | 0 |
| `aXmM0VZv810` | 6 | 0 | 0.0 | None | 0 |
| `bR4tDSa3O10` | 107 | 101 | 0.94393 | 0.02271 | 0 |
| `bV5uKHsWQtY` | 11 | 0 | 0.0 | None | 0 |
| `d4mrO13trBY` | 16 | 0 | 0.0 | None | 0 |
| `dKe3WbGR7Xs` | 49 | 0 | 0.0 | None | 0 |
| `dPi40lQetew` | 17 | 12 | 0.70588 | 0.022 | 0 |
| `dgkxN6RASpg` | 76 | 0 | 0.0 | None | 0 |
| `fBnAMUkNM2k` | 8 | 0 | 0.0 | None | 0 |
| `gDadfh0ZdBM` | 29 | 19 | 0.65517 | 0.06165 | 0 |
| `gQzZkTRhp0U` | 22 | 0 | 0.0 | None | 0 |
| `gWziScXTR_4` | 10 | 0 | 0.0 | None | 0 |
| `h4vlcM-5X1E` | 9 | 0 | 0.0 | None | 0 |
| `hBYoDp-Zh64` | 12 | 0 | 0.0 | None | 0 |
| `hZ0YhrgYejI` | 17 | 5 | 0.29412 | 0.02615 | 0 |
| `jG-4kBIDAzA` | 8 | 0 | 0.0 | None | 0 |
| `jxY2-YgAgm0` | 2 | 0 | 0.0 | None | 0 |
| `kHti_4zsQhc` | 8 | 0 | 0.0 | None | 0 |
| `kM8HJPbFnJg` | 22 | 0 | 0.0 | None | 0 |
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
