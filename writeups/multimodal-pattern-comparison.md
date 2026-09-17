# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **20**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | -23.30056 | 0.87068 | 0.12096 | 660.99065 |
| `conclusion_or_summary` | 2 | 2 | -18.302 | 0.9375 | 0.18206 | 716.264 |
| `contrast_or_disagreement` | 8 | 19 | -22.71172 | 0.92596 | 0.15415 | 903.59116 |
| `definition` | 4 | 5 | -32.02125 | 0.69375 | 0.18157 | 1181.82063 |
| `example` | 6 | 11 | -22.78635 | 0.8565 | 0.12807 | 704.65747 |
| `question` | 16 | 182 | -22.88794 | 0.90767 | 0.13139 | 792.95708 |
| `story_or_personal_experience` | 10 | 30 | -24.84717 | 0.89099 | 0.14905 | 863.63291 |
| `uncertainty_or_qualification` | 14 | 92 | -23.34763 | 0.9314 | 0.14108 | 837.55298 |
| `unclassified` | 18 | 3118 | -23.8647 | 0.91565 | 0.14087 | 816.30013 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `2fWJh-_UG5s` | 139 | 105 | 0.7554 | 0.03017 | 0 |
| `2m_lqGnLtWA` | 17 | 3 | 0.17647 | 0.24514 | 0 |
| `3AIoHLr8nTI` | 102 | 95 | 0.93137 | 0.01637 | 0 |
| `5i0u4jFmE78` | 16 | 9 | 0.5625 | 0.0626 | 0 |
| `9fEurt2OZ0I` | 13 | 10 | 0.76923 | 0.04928 | 0 |
| `JDfP3thQYrM` | 59 | 44 | 0.74576 | 0.04451 | 1 |
| `S43F1BZfQKY` | 47 | 23 | 0.48936 | 0.03699 | 2 |
| `W-mgdUdOjhs` | 28 | 10 | 0.35714 | 0.11947 | 0 |
| `ZwMVMbmQBug` | 23 | 13 | 0.56522 | 0.03118 | 0 |
| `aHXxveJTJoE` | 25 | 4 | 0.16 | 0.03782 | 0 |
| `aXmM0VZv810` | 162 | 107 | 0.66049 | 0.04026 | 0 |
| `fBnAMUkNM2k` | 238 | 139 | 0.58403 | 0.05382 | 0 |
| `hZ0YhrgYejI` | 17 | 5 | 0.29412 | 0.02615 | 0 |
| `jxY2-YgAgm0` | 39 | 34 | 0.87179 | 0.02117 | 0 |
| `lcj1wMZRitI` | 55 | 36 | 0.65455 | 0.04981 | 0 |
| `m92yvNscIAo` | 16 | 6 | 0.375 | 0.03101 | 0 |
| `qOwYULOPuPs` | 93 | 72 | 0.77419 | 0.03875 | 0 |
| `r2kP2Pqdx6w` | 103 | 99 | 0.96117 | 0.00933 | 0 |
| `u1gg_L-syCw` | 18 | 8 | 0.44444 | 0.02543 | 0 |
| `xRiwgtdyjQk` | 59 | 49 | 0.83051 | 0.01611 | 0 |

## Interpretation boundary

A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.
