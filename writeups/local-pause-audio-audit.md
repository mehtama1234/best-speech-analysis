# Local acoustic screening of pause candidates

Threshold-sensitivity screen of decoded local audio; no listening or semantic pause adjudication. Quiet energy is not speech absence, intentional silence, or an audience effect. No legacy decisions overwritten.

20 ms mono energy frames; runs at least 200 ms at three exploratory fixed thresholds. These are sensitivity settings, not calibrated speech/non-speech thresholds. Frames and run boundaries are in the JSON artifact.

| Evidence | Local audio | Runs below -50 / -40 / -30 dBFS |
| --- | --- | --- |
| `2fWJh-_UG5s:00035` | decoded | 6 / 5 / 4 |
| `C8-twwwTETE:00019` | decoded | 3 / 3 / 5 |
| `aXmM0VZv810:00269` | decoded | 0 / 0 / 4 |
| `aXmM0VZv810:00227` | decoded | 0 / 1 / 6 |
| `fBnAMUkNM2k:00021` | decoded | 4 / 4 / 6 |
| `gDadfh0ZdBM:00036` | decoded | 6 / 8 / 5 |
| `qM-gZintWDc:00055` | decoded | 0 / 0 / 7 |

Runs are measured over the entire caption plus three seconds either side, not necessarily immediately before speech. Distance to each caption boundary and window-censoring flags are recorded. Overlapping captions are not independent trials. Music, room noise, gain, edits and speaker changes remain confounds. Mono downmixing may also change energy. No absence of a quiet run proves continuous speech; no detected run proves a rhetorical pause.
