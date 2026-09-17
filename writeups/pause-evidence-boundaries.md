# What a pause measurement can and cannot establish

17 September 2026. This pass separates caption timing, acoustic energy and
speech-function interpretation for the seven legacy pause candidates.
It does not promote any candidate to a verified rhetorical-pause example.

## Three different observations

1. A **caption gap** is time not covered by adjacent provider caption intervals.
   Speech can occur during it; overlapping captions can also span actual silence.
2. A **low-energy interval** is a run of audio samples whose frame RMS falls
   below a chosen threshold. It can contain quiet speech, or reflect editing,
   gain changes or a break in background sound. Music can mask speech pauses.
3. A **rhetorical pause** is an interpretation of a localized break in a speaker's
   delivery in context. Energy and text alone do not establish its intention,
   function or effect on an audience.

The existing one-second audio analysis measured a coarse low-energy proxy.
Some legacy annotation prose calls it a gap without keeping those definitions
separate. Legacy reviewer identity and listening modality are not established.

## A contradicted legacy statement

`review-060` (`gDadfh0ZdBM:00036`) says a ten-second transcript gap follows the
target. The saved feature row records zero before and zero after. The registry
also contradicts a gap at this location: the target is 133.12–136.72 seconds;
caption 37 begins at 134.48 and caption 38 at 136.72. These intervals overlap
or touch. This is not evidence of a ten-second pause or an edit here.

The legacy record is preserved for traceability. Its explanation must not be
used as a measured fact. Contradicting that explanation does not establish
continuous speech or settle whether a shorter acoustic pause occurred.

## New local-audio screen

Run `python3 scripts/audit_local_pause_audio.py` to generate the
[acoustic audit](local-pause-audio-audit.md) and
[machine-readable evidence](../research/local-pause-audio-audit.json).
The script decodes existing local audio; it makes no download or API request.

It measures 20 ms mono RMS frames and locates runs of at least 200 ms below
-50, -40 and -30 dBFS. These are exploratory sensitivity settings, not validated
voice-activity thresholds or recommended speaking pauses. Each target window
includes the caption and three seconds either side. The report keeps:

- all local energy frames;
- absolute run boundaries and durations for each threshold;
- distances from each run to the caption start and end;
- flags for runs cut off by the inspection window;
- source-caption timing and the older feature-file caption gaps;
- input hashes for audio, features, registry, annotations and analysis script;
- explicit missing/decode-error status without zero-filling measurements.

A run anywhere in that window is not necessarily a pause immediately before
the target words. Caption timing is not validated word timing. Threshold
agreement alone does not resolve these alignment and interpretation problems.
Synthetic tests check measurement mechanics, not speech recognition accuracy.

## Next evidentiary step

The first run decoded local audio for all seven targets. At -40 dBFS:

| Target | Nearby low-energy interval | Relation to provider caption start |
| --- | --- | --- |
| `2fWJh-_UG5s:00035` | 93.12–94.62 s (1.50 s) | Spans the 94.479 s caption start |
| `fBnAMUkNM2k:00021` | 196.94–197.88 s (0.94 s) | Ends 0.229 s before the 198.109 s caption start |
| `gDadfh0ZdBM:00036` | 132.24–133.50 s (1.26 s) | Spans the 133.12 s caption start despite zero caption gap |

These directly measured energy intervals offer localized examples to inspect;
they do not repair the legacy semantic judgments automatically. In particular,
the third example illustrates why zero caption gap does not imply no quiet
audio. Two other targets (`aXmM0VZv810:00269` and `qM-gZintWDc:00055`) have
no qualifying runs at -40 or -50 dBFS but have runs at -30 dBFS. Threshold
sensitivity therefore matters. Run counts need not increase with a more
permissive threshold because adjacent quiet intervals can merge.

Verification: 31 tests passed in 14.249 seconds, including four new synthetic
acoustic-measurement tests. Whitespace checks passed; source transcripts,
original annotations and raw feature files have no diff. No human listening
or visual validation occurred. The implementation currently decodes whole
audio files before selecting local frames, so reruns can be memory-intensive;
a bounded/streaming implementation is a useful efficiency follow-up.

Inspect localized listening/video evidence for each candidate and identify
speaker turns, edits, music and word boundaries. Record actual review modality
and leave unavailable judgments unresolved. Then compare like-for-like speech
functions with non-target examples, separating speaker, format and recording
conditions. Do not infer emotion or causal communication benefit from silence.

The semantic review checkpoint remains 77/87. Seven pause candidates and three
unclassified cases still need appropriate adjudication; a new numeric screen
does not count as completion of their semantic review or of the project.
