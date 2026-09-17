# Pilot pause and rhythm analysis

This report measures acoustic low-energy runs around transcript segments. A pause here means one or more consecutive one-second audio windows below the current activity threshold; a caption gap alone is not treated as silence. Labels are heuristic and require review.

| Candidate label | Videos | Segments | Mean pause before (s) | Mean pause after (s) | Caption word-rate proxy | Mean RMS dB |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | 0.0694 | 0.0306 | 1.1005 | -23.3006 |
| `conclusion_or_summary` | 2 | 2 | 0.0 | 0.0 | 0.9248 | -18.302 |
| `contrast_or_disagreement` | 8 | 19 | 0.0417 | 0.125 | 1.7922 | -22.7117 |
| `definition` | 4 | 5 | 0.25 | 0.375 | 1.1042 | -32.0212 |
| `example` | 6 | 11 | 0.6667 | 0.1667 | 1.1636 | -22.7863 |
| `question` | 16 | 182 | 0.0971 | 0.0743 | 1.3854 | -22.8879 |
| `story_or_personal_experience` | 10 | 30 | 0.3083 | 0.3083 | 1.7304 | -24.8472 |
| `uncertainty_or_qualification` | 14 | 92 | 0.049 | 0.0329 | 1.5137 | -23.3476 |
| `unclassified` | 18 | 3118 | 0.1872 | 0.1436 | 1.5591 | -23.8647 |

## Limits

The activity threshold is a loudness proxy and can be affected by music, edits, room noise, compression, and microphone gain. Caption word rate is not a validated speaking-rate measure. These outputs are for locating examples for manual review, not for inferring confidence, hesitation, or emotion.
