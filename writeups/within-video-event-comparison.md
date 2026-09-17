# Within-video event comparison

For each candidate label, this compares the mean measurement of matching transcript segments with the mean measurement of all usable segments in the same video. The contrast reduces—but does not eliminate—speaker, microphone, editing, and topic confounds. Labels are heuristic retrieval aids.

| Candidate label | Videos | Segments | RMS delta dB | Activity delta | ZCR delta | Spectral centroid delta Hz |
|---|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 11 | 40 | -3.10058 | -0.05223 | -0.01438 | -39.71444 |
| `conclusion_or_summary` | 3 | 3 | 0.36422 | -0.02843 | 0.03182 | 92.19269 |
| `contrast_or_disagreement` | 14 | 31 | 0.57181 | 0.02697 | 0.00289 | 19.52533 |
| `definition` | 8 | 9 | -1.40504 | -0.08243 | 0.01172 | 175.81785 |
| `example` | 8 | 18 | -0.95339 | -0.02682 | -0.00344 | -15.52082 |
| `question` | 25 | 251 | -0.09818 | -0.00398 | -0.00198 | 3.68196 |
| `story_or_personal_experience` | 15 | 44 | -0.76047 | -0.00936 | 0.00285 | -11.07625 |
| `uncertainty_or_qualification` | 20 | 134 | -0.65669 | 0.00162 | 0.00069 | 41.91664 |
| `unclassified` | 30 | 4547 | 0.04099 | 0.0008 | -0.00013 | -2.77926 |

## Reading the table

A positive RMS delta means the labeled segments were louder than that video's overall usable segments on average. It does not mean the speaker was more confident or that the delivery was more effective. A label should only become a research finding after manual review, counterexamples, and replication on a larger stratified sample.
