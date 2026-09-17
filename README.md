# Best Speech Analysis

An auditable research system for studying effective speech and presentation across four synchronized channels:

1. **Words** — claims, explanations, stories, structure, qualification, and disagreement.
2. **Voice** — rate, pauses, pitch movement, loudness, rhythm, emphasis, breath, and disfluency.
3. **Visible behavior** — facial movement, gaze, gesture, posture, and interaction with slides.
4. **Context** — opening, explanation, question-answer, story, conclusion, persuasion, or disagreement.

The project identifies recurring patterns only when they are supported by timestamped examples. It separates directly measured observations from interpretations and records counterexamples and limitations.

## Initial corpus

The first corpus contains three YouTube playlists focused on speech and presentation. They are registered in `config/playlists.json`. More playlists can be added as separate sources.

The three supplied video links are retained as seed examples:

- `fBnAMUkNM2k`
- `5i0u4jFmE78`
- `qOwYULOPuPs`

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

The project is at corpus-definition and pipeline-design stage. Network access was unavailable during the initial playlist probe, so playlist metadata and transcripts have not yet been downloaded.

