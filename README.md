# Best Speech Analysis

An auditable research system for studying effective speech and presentation across four synchronized channels:

1. **Words** — claims, explanations, stories, structure, qualification, and disagreement.
2. **Voice** — rate, pauses, pitch movement, loudness, rhythm, emphasis, breath, and disfluency.
3. **Visible behavior** — facial movement, gaze, gesture, posture, and interaction with slides.
4. **Context** — opening, explanation, question-answer, story, conclusion, persuasion, or disagreement.

The project identifies recurring patterns only when they are supported by timestamped examples. It separates directly measured observations from interpretations and records counterexamples and limitations.

## Initial corpus

The first corpus contains three YouTube playlists focused on speech and presentation. They are registered in `config/playlists.json` and currently resolve to 958 playlist memberships covering 480 unique videos after deduplication.

The three supplied video links were used as seed examples for testing ingestion:

- `fBnAMUkNM2k`
- `5i0u4jFmE78`
- `qOwYULOPuPs`

The complete playlist registry is in `data/metadata/video-registry.jsonl`. Transcript acquisition is resumable through `scripts/download_corpus_transcripts.py` and is tracked in `data/metadata/transcript-status.jsonl`.

## Research rule

The system may say:

> In these observed segments, speaking rate decreased before the conclusion and a pause occurred before the final clause.

It must not silently upgrade that into:

> The speaker felt confident.

Internal emotion, honesty, intelligence, personality, and mental state are outside the initial scope. Any interpretation beyond observable behavior must be explicitly tentative.

## Planned pipeline

```text
playlists
  -> video registry
  -> permitted metadata/transcripts/media
  -> timestamp normalization
  -> speech-function annotation
  -> audio and visual feature extraction
  -> word/voice/visual alignment
  -> cross-speech pattern analysis
  -> examples, counterexamples, and limitations
  -> reader-facing reports
```

Raw media stays outside Git. The repository stores manifests, derived features, annotations, provenance, and small evidence excerpts.

## Status

The playlist inventory is complete: 958 playlist memberships resolve to 480 unique videos, with duplicate memberships retained as provenance. The first transcript pass returned 477 responses: 474 successful responses and 3 provider 404 failures. The returned files contain 102,816 timestamped segments and 770,424 words; 395 videos have non-empty transcripts and 82 responses contain zero segments.

The project has completed a 24-video pilot and a 41-video phase-two manifest. Thirty-six phase-two videos currently have usable local audio/video pairs and derived feature files; five are explicitly recorded as media failures. The measurement layer currently produces one-second audio windows, transcript alignment, transcript-derived words-per-second and inter-caption gaps, RMS/loudness, zero-crossing rate, spectral centroid, a coarse spectral pitch proxy, face-presence and face-geometry proxies, scene change, visual sampling, and an optional torchvision body-keypoint pass. Pitch and transcript timing are explicitly proxies rather than validated speech or pitch tracking. The body-keypoint pass measures person boxes, keypoint visibility, wrist visibility, and shoulder geometry; it does not infer gestures, emotion, intent, confidence, or mental state. Candidate speech-function labels remain retrieval aids until manually reviewed.

Current research outputs include corpus coverage audits, a searchable evidence browser, reviewed annotation queues, pause/rhythm analysis, within-video comparisons, audio/visual comparisons, pose-geometry coverage, pose-movement summaries, reviewed delivery summaries, same-video baseline deltas, and counterexample-aware pattern cards. The manual ledger now contains 87 reviewed annotations, including 62 supported examples. `research/reviewed-delivery-patterns.json` and `writeups/reviewed-delivery-patterns.md` aggregate only manually reviewed supported examples; `research/reviewed-delivery-baselines.json` and its writeup compare those examples against ordinary segments from the same video; `research/pose-geometry-analysis.json` summarizes 144 sampled keypoint frames across 36 videos, and `research/pose-movement-analysis.json` summarizes 68 observable frame-to-frame movement pairs. Unsupported cases remain in the counterexample audit—for example, the current pause-event candidates support only 2 of 7 reviewed cases. The phase-two manifest is generated reproducibly with `scripts/build_multimodal_sample.py --per-bucket 8`; raw media remains ignored, while `data/media-status.jsonl`, `data/metadata/multimodal-expansion.json`, `data/features/`, and `data/pose-features/` preserve the auditable state. The next scale-up is more densely sampled body/face review and manual alignment while preserving the distinction between measured observation and interpretation.
