# Are the quiet audio and inspected frames on the same timeline?

**Decoded frame times are now verified; audiovisual content synchronization is
not.** Re-decoding all nine requested seeks with original timestamps preserved
produced PNG bytes identical to the inspected cache. This binds the timestamp
of each newly decoded frame to the exact image previously reviewed.

The [machine-readable audit](../research/pause-media-timeline-audit.json) retains
integer presentation timestamps (PTS), stream time bases, displayed times,
PNG hashes, source-file hashes, script hash and decoder version.

| Probe | Requested seek seconds | Verified decoded frame seconds |
| --- | --- | --- |
| `2fWJh-_UG5s:00035` | 92.8 / 93.8 / 94.9 | 92.827 / 93.828 / 94.928 |
| `fBnAMUkNM2k:00021` | 196.6 / 197.4 / 198.2 | 196.629767 / 197.430567 / 198.231367 |
| `gDadfh0ZdBM:00036` | 131.9 / 132.8 / 133.7 | 131.9 / 132.8 / 133.7 |

A requested seek is not necessarily a frame boundary. The first six reviewed
frames are approximately 27–31 milliseconds after their requested seeks;
the film probe's seeks coincide with decoded frame times. These are frame
selection differences, **not measured audio/video synchronization errors**.

## What the containers establish

The three video files contain only video; the separate M4A files contain only
audio. All six containers display a start time of zero. Displayed audio/video
durations are respectively 1388.41/1388.35, 2370.46/2370.40 and 287.67/287.53
seconds. These metadata values are rounded and do not establish packet-level
alignment. Duration differences cannot be used as local offset corrections.

The downloader selected separate video-only and audio streams for the same
video ID. That is provenance consistent with a common upload, not proof of
local lip synchronization, absence of drift, matching edits, or transcript
alignment. There is no audio track inside these video files to cross-correlate
against the M4A waveform. No offset has been estimated or silently applied.

## Consequence for interpretation

The prior [visual observations](pause-visual-review.md) remain valid. The film
shot changes somewhere between decoded frames at 131.9 and 132.8 seconds;
the exact cut has not been located. Its relationship to the audio quiet
interval at 132.24–133.50 remains conditional on synchronization. This audit
does not turn that overlap into a deliberate rhetorical pause.

For the next review, use continuous local audiovisual playback with explicit
alignment checks at multiple observable speech events, recording offset and
uncertainty. If playback merely overlays both streams at zero, label it an
assumed alignment rather than a validated measurement. Content-level checking
and listening have not been performed here. All seven legacy pause judgments
remain unresolved, and no practice finding has been promoted.

Rebuild: `python3 scripts/audit_pause_media_timeline.py`. Original media and
the historical visual-review manifest are not modified by this audit.
