# Within-video event comparison

For each candidate label, this compares the mean measurement of matching transcript segments with the mean measurement of all usable segments in the same video. The contrast reduces—but does not eliminate—speaker, microphone, editing, and topic confounds. Labels are heuristic retrieval aids.

| Candidate label | Videos | Segments | RMS delta dB | Activity delta | ZCR delta | Spectral centroid delta Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 6 | 33 | -3.83359 | -0.08268 | -0.01559 | -43.21248 |
| `conclusion_or_summary` | 3 | 6 | -1.36769 | -0.03148 | 0.02089 | 114.90092 |
| `contrast_or_disagreement` | 17 | 155 | 0.34655 | 0.02275 | 0.00065 | -28.3633 |
| `definition` | 4 | 5 | -4.30882 | -0.14655 | 0.02204 | 246.82767 |
| `example` | 6 | 11 | -2.10535 | -0.08723 | -0.00407 | 0.83092 |
| `question` | 18 | 471 | 0.3907 | 0.00873 | -0.00017 | -13.97319 |
| `story_or_personal_experience` | 10 | 30 | -0.87667 | -0.0191 | 0.00519 | 15.8084 |
| `uncertainty_or_qualification` | 14 | 92 | -0.66022 | 0.01753 | -9e-05 | 15.50033 |
| `unclassified` | 18 | 2756 | 0.00174 | -0.00186 | 0.00041 | 1.73366 |

## Reading the table

A positive RMS delta means the labeled segments were louder than that video's overall usable segments on average. It does not mean the speaker was more confident or that the delivery was more effective. A label should only become a research finding after manual review, counterexamples, and replication on a larger stratified sample.
