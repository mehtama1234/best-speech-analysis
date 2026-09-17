# Pilot multimodal pattern comparison

This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.

Pilot videos: **20**

## Acoustic comparison

| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | -23.30056 | 0.87068 | 0.12096 | 660.99065 |
| `conclusion_or_summary` | 3 | 6 | -18.89792 | 0.95833 | 0.16476 | 764.55058 |
| `contrast_or_disagreement` | 17 | 155 | -23.47274 | 0.93275 | 0.14455 | 806.13376 |
| `definition` | 4 | 5 | -32.02125 | 0.69375 | 0.18157 | 1181.82063 |
| `example` | 6 | 11 | -22.78635 | 0.8565 | 0.12807 | 704.65747 |
| `question` | 18 | 471 | -23.549 | 0.92243 | 0.1408 | 806.19485 |
| `story_or_personal_experience` | 10 | 30 | -24.84717 | 0.89099 | 0.14905 | 863.63291 |
| `uncertainty_or_qualification` | 14 | 92 | -23.34763 | 0.9314 | 0.14108 | 837.55298 |
| `unclassified` | 18 | 2756 | -23.93795 | 0.91183 | 0.14138 | 821.90171 |

## Visual coverage

Visual results currently describe face detection and geometry only. They do not identify emotional expression.

| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |
|---|---:|---:|---:|---:|---:|
| `2fWJh-_UG5s` | 47 | 36 | 0.76596 | 0.03069 | 0 |
| `2m_lqGnLtWA` | 6 | 1 | 0.16667 | 0.26694 | 0 |
| `3AIoHLr8nTI` | 34 | 31 | 0.91176 | 0.01573 | 0 |
| `5i0u4jFmE78` | 6 | 3 | 0.5 | 0.06155 | 0 |
| `9fEurt2OZ0I` | 5 | 4 | 0.8 | 0.04101 | 0 |
| `JDfP3thQYrM` | 20 | 16 | 0.8 | 0.04708 | 0 |
| `S43F1BZfQKY` | 16 | 7 | 0.4375 | 0.02271 | 0 |
| `W-mgdUdOjhs` | 10 | 3 | 0.3 | 0.12907 | 0 |
| `ZwMVMbmQBug` | 8 | 3 | 0.375 | 0.0264 | 0 |
| `aHXxveJTJoE` | 9 | 2 | 0.22222 | 0.0173 | 0 |
| `aXmM0VZv810` | 54 | 35 | 0.64815 | 0.03858 | 0 |
| `fBnAMUkNM2k` | 80 | 44 | 0.55 | 0.05591 | 0 |
| `hZ0YhrgYejI` | 6 | 4 | 0.66667 | 0.02713 | 0 |
| `jxY2-YgAgm0` | 13 | 11 | 0.84615 | 0.02118 | 0 |
| `lcj1wMZRitI` | 19 | 10 | 0.52632 | 0.04866 | 0 |
| `m92yvNscIAo` | 6 | 2 | 0.33333 | 0.04125 | 0 |
| `qOwYULOPuPs` | 31 | 26 | 0.83871 | 0.03889 | 0 |
| `r2kP2Pqdx6w` | 35 | 33 | 0.94286 | 0.0093 | 0 |
| `u1gg_L-syCw` | 6 | 3 | 0.5 | 0.038 | 0 |
| `xRiwgtdyjQk` | 20 | 15 | 0.75 | 0.01657 | 0 |

## Interpretation boundary

A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.
