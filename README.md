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

The project has completed a 24-video multimodal pilot. Twenty videos have usable local audio/video pairs and derived feature files. The pilot currently measures one-second audio windows, transcript alignment, face-presence and face-geometry proxies, scene change, and visual sampling. It does not infer emotion, intent, confidence, or mental state. Candidate speech-function labels remain retrieval aids until manually reviewed.

Current research outputs include corpus coverage audits, a searchable evidence browser, reviewed annotation queues, pause/rhythm analysis, within-video comparisons, audio/visual pilot comparisons, and counterexample-aware pattern cards. The next scale-up is to expand stratified audio/video measurement and manual review while preserving the distinction between measured observation and interpretation.
