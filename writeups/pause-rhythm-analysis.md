# Pilot pause and rhythm analysis

This report measures acoustic low-energy runs around transcript segments. A pause here means one or more consecutive one-second audio windows below the current activity threshold; a caption gap alone is not treated as silence. Labels are heuristic and require review.

| Candidate label | Videos | Segments | Mean pause before (s) | Mean pause after (s) | Caption word-rate proxy | Mean RMS dB |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | 0.0694 | 0.0306 | 1.1005 | -23.3006 |
| `conclusion_or_summary` | 3 | 6 | 0.0 | 0.0 | 1.1964 | -18.8979 |
| `contrast_or_disagreement` | 17 | 155 | 0.1218 | 0.2212 | 1.7318 | -23.4727 |
| `definition` | 4 | 5 | 0.25 | 0.375 | 1.1042 | -32.0212 |
| `example` | 6 | 11 | 0.6667 | 0.1667 | 1.1636 | -22.7863 |
| `question` | 18 | 471 | 0.0864 | 0.1133 | 1.7872 | -23.549 |
| `story_or_personal_experience` | 10 | 30 | 0.3083 | 0.3083 | 1.7304 | -24.8472 |
| `uncertainty_or_qualification` | 14 | 92 | 0.049 | 0.0329 | 1.5137 | -23.3476 |
| `unclassified` | 18 | 2756 | 0.1994 | 0.1526 | 1.5245 | -23.938 |

## Limits

The activity threshold is a loudness proxy and can be affected by music, edits, room noise, compression, and microphone gain. Caption word rate is not a validated speaking-rate measure. These outputs are for locating examples for manual review, not for inferring confidence, hesitation, or emotion.
