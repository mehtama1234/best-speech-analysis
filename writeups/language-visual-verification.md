# Three different witnesses to the same speech

The recovered candidate for `05RW7gx-gG4` remains outside the canonical corpus.
We now have stronger evidence for treating its language label cautiously:
**all three directly inspected upload frames display English subtitles**,
while the candidate uses Devanagari phonetic renderings of recognizable English
expressions. This does not establish the exact spoken wording; no audio was
downloaded or listened to in this pass.

## What was actually checked

The local video-only download succeeded (format 396, approximately 10.89 MiB).
Three frames were decoded with original presentation timestamps preserved:

| Requested time | Decoded frame time | Direct visual observation |
| ---: | ---: | --- |
| 60 s | 60.026633 s | Wide hall scene; English subtitle describes a health-document example. |
| 100 s | 100.033267 s | Seated attendees; an English subtitle continues the drawing example. |
| 378 s | 378.010967 s | Close view of the podium speaker; English subtitle discusses data quality. |

Frame hashes, video hash, candidate hash, decoder version and acquisition
details are in the [extraction manifest](../research/language-verification-frames.json).
The [assistant observation record](../research/language-visual-verification.json)
binds each observation to those exact images. They are purposive stills, not a
representative sample or continuous audiovisual review.

An [official English address text](https://www.pmindia.gov.in/en/news_updates/opening-address-by-pm-at-the-ai-action-summit-paris/)
also corresponds to the sampled opening example, governance discussion and
closing responsibility theme. It supports document identification, not precise
delivery or upload timing. It is a separate untimed witness, not replacement
captions. Its factual claims remain attributed and unverified here.

## Why these distinctions matter

Caption availability, text language, written script, spoken language, faithful
transcription and translation status are different properties. A nonempty ASR
response can pass timestamp-shape checks while still being inappropriate for
word choice, syntax or rhetorical-pattern statistics. Recovering content is
not the same as recovering reliable language evidence.

The audience frame also exposes a visual attribution trap. A speaker-name
overlay and the speech's subtitles can persist while the camera shows other
people. Measuring visible faces at that moment would not measure the speaker's
facial delivery. No attendee identity, emotion, attention or intention is inferred.

Only candidate ordinals 17–41 and 235–248 were additionally inspected in this
pass; comparisons also use earlier inspected ordinals 120–127. The first batch
overlaps the earlier spot check at ordinal 17. Do not count overlapping reviews
as independent evidence or claim a full read of all 259 records.

Next: independently checked original-language transcription or aligned captions,
then explicit source/translation lineage before corpus integration. Visible
subtitles are editorial evidence; an official text is a documentary witness;
neither alone proves exact spoken-word timing. The main registry still has 395
nonempty transcripts, with two unpromoted language-recovery candidates separate.
