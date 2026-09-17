# Within-video event comparison

For each candidate label, this compares the mean measurement of matching transcript segments with the mean measurement of all usable segments in the same video. The contrast reduces—but does not eliminate—speaker, microphone, editing, and topic confounds. Labels are heuristic retrieval aids.

| Candidate label | Videos | Segments | RMS delta dB | Activity delta | ZCR delta | Spectral centroid delta Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | -3.83359 | -0.08268 | -0.01559 | -43.21248 |
| `conclusion_or_summary` | 2 | 2 | -1.79265 | -0.05092 | 0.02792 | 87.7721 |
| `contrast_or_disagreement` | 8 | 19 | -0.55492 | -0.02461 | 0.00532 | 47.78407 |
| `definition` | 4 | 5 | -4.30882 | -0.14655 | 0.02204 | 246.82767 |
| `example` | 6 | 11 | -2.10535 | -0.08723 | -0.00407 | 0.83092 |
| `question` | 16 | 182 | -0.24371 | -0.01407 | -0.0053 | -7.64871 |
| `story_or_personal_experience` | 10 | 30 | -0.87667 | -0.0191 | 0.00519 | 15.8084 |
| `uncertainty_or_qualification` | 14 | 92 | -0.66022 | 0.01753 | -9e-05 | 15.50033 |
| `unclassified` | 18 | 3118 | 0.075 | 0.00196 | -0.0001 | -3.86791 |

## Reading the table

A positive RMS delta means the labeled segments were louder than that video's overall usable segments on average. It does not mean the speaker was more confident or that the delivery was more effective. A label should only become a research finding after manual review, counterexamples, and replication on a larger stratified sample.
