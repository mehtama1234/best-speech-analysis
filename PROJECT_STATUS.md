# Best Speech Analysis — Project Goal and Resumption Status

Last verified: 2026-09-16

This file is the practical handoff for resuming the project. The canonical
long-form goal remains in
[`SPEECH_ANALYSIS_END_TO_END_GOAL.md`](SPEECH_ANALYSIS_END_TO_END_GOAL.md).

## The meaty end-to-end goal

Given the three supplied speech and presentation playlists—and additional
relevant playlists added later—build a large, auditable research corpus
covering every discoverable video in those playlists. Use the corpus to
determine how effective speakers repeatedly organize ideas, use language,
control timing, use their voice, move their face and body, interact with
slides, answer questions, disagree, tell stories, and guide an audience's
attention.

The final result should be more than summaries or a list of presentation
tips. It should be a tested explanatory account of recurring communication
patterns. For every proposed pattern, show:

- where it occurs, with video IDs and timestamps;
- what was directly observed or measured;
- what speech function or presentation context was taking place;
- whether it recurs across speakers, videos, formats, and topics;
- what contradicts or qualifies the pattern;
- what alternative explanations may exist; and
- what a person could practice, with the evidence and limits made clear.

The unit of analysis is a timestamped speech segment linked across channels:
transcript words, audio delivery, visible face and body behavior, slides or
scene context, and the surrounding speech function. The project must separate
measurement from interpretation. A pause, pitch change, speaking-rate change,
facial movement, gaze direction, gesture, or posture change can be recorded as
an observation; confidence, emotion, intent, persuasion, or comprehension may
only be discussed as a cautious hypothesis unless independently supported.

The corpus is playlist-scale. The three URLs below are seed playlists, not
three sample videos. The intended inventory is every eligible video in each
playlist, deduplicated across playlists, with unavailable or inaccessible
items explicitly recorded. The project should eventually compare speaker-
specific, situation-specific, and cross-speaker patterns rather than treating
one repeated behavior as a universal best practice.

## Seed playlists

- [Learn English with Speeches](https://www.youtube.com/playlist?list=PLosaC3gb0kGDhmBVm6M47jcU8BbEhTnlP)
- [Greatest Movie Speeches](https://www.youtube.com/playlist?list=PLLVLl07BgiJYSCSdl1fd34s4SzILbMxp9)
- [The Best Speeches Ever](https://www.youtube.com/playlist?list=PLosaC3gb0kGDEFRm7OxnWgOmJkEki1LPj)

## Verified current status

### Corpus and transcript layer

- 958 playlist memberships were inventoried.
- 480 unique videos remain after deduplication.
- 478 duplicate memberships were recorded in the inventory.
- One unavailable playlist item was hidden during enumeration.
- 477 transcript responses were attempted through ScrapeCreators.
- 474 responses succeeded; 3 returned provider 404s:
  `BS8I9H07wKw`, `E7Sr-cpFwUc`, and `nWRxPDhd3d0`.
- 395 videos have non-empty transcripts; 82 successful responses have zero
  transcript segments.
- The corpus contains 102,816 timestamped transcript segments and 770,424
  words.
- Transcript acquisition uses the root `/home/mehtama1/git-repo/.env`.
  Credentials must never be printed, committed, or copied into this repo.

### Multimodal media and feature layer

- The phase-two multimodal sample contains 41 videos: 24 pilot videos and 17
  additional videos selected across duration buckets.
- 36 videos have complete audio/video pairs; 5 have media failures.
- Audio features contain 19,233 one-second windows and 5,059 transcript-aligned
  segments across those 36 videos.
- Current audio measurements include RMS/loudness, a speech-activity proxy,
  zero-crossing rate, spectral centroid, coarse spectral pitch and pitch
  confidence proxies, transcript word counts, words-per-second proxies, and
  transcript gaps before and after segments.
- Visual features currently record sampled frames, face presence and geometry
  through OpenCV Haar detection, and scene-pixel measures. They do not infer
  emotion.
- Raw audio and video are intentionally ignored by Git. Manifests, derived
  features, status records, and evidence are tracked instead.

### Body and movement layer

- Pose features cover the same 36 multimodal videos with four evenly spaced
  frames per video: 144 sampled frames total.
- A person was detected in 104 of those frames.
- The current layer records observable person/keypoint geometry only.
- Frame-to-frame movement analysis produced 68 movement pairs and 352
  transcript/motion retrieval joins.
- Current movement metrics include overall keypoint, wrist, and shoulder
  displacement. Cuts, zooms, camera movement, tracking errors, and framing
  can create apparent movement, so these are exploratory measurements.
- MediaPipe was not retained because of dependency incompatibilities. The
  current pose implementation uses the pinned torchvision approach documented
  in `requirements-vision.txt`.

### Human-reviewed evidence layer

- `research/annotation-ledger.jsonl` contains 87 reviewed annotations.
- The latest audit identifies 62 supported annotation rows; some rows carry
  more than one candidate label.
- Current reviewed support rates are:

  | Candidate pattern | Supported / reviewed | Support rate |
  | --- | ---: | ---: |
  | call to action | 7 / 11 | 0.636 |
  | conclusion or summary | 5 / 6 | 0.833 |
  | contrast or disagreement | 9 / 10 | 0.900 |
  | definition | 7 / 9 | 0.778 |
  | example | 8 / 10 | 0.800 |
  | pause event | 2 / 7 | 0.286 |
  | question | 7 / 12 | 0.583 |
  | story or personal experience | 10 / 13 | 0.769 |
  | uncertainty or qualification | 9 / 9 | 1.000 |

- Six provisional practice cards currently pass the admission rule of at
  least five supported examples, four distinct videos, and a support rate of
  at least 0.70: contrast/disagreement, definition, example,
  story/personal-experience, uncertainty/qualification, and
  conclusion/summary.
- Question and pause cards are deliberately excluded from the provisional
  practice edition because their current support rates are too low.
- The cards include direct measurements, timestamped examples, counterexamples,
  limits, visual-evidence status, and a required next test. They are not claims
  that any behavior is universally effective.

## What is complete and what is not

The inventory and transcript acquisition foundation is in place, and the
repository has a working auditable pipeline from playlist membership through
transcripts, derived audio/visual/pose measurements, reviewed annotations,
counterexamples, and provisional reader-facing pattern cards.

The research is not finished. In particular:

- The multimodal media sample covers 36 complete videos, not all 480 unique
  videos.
- Manual review is still a small, structured sample, not full reading and
  annotation of every transcript.
- Speech-function labels and transcript/audio joins are partly heuristic and
  need broader review.
- Pose coverage is four sampled frames per video; it is not continuous gesture
  tracking.
- Facial expression, gaze, gesture semantics, audience response, speaker
  identity, and slide understanding are not yet reliable measured layers.
- There is no causal evidence that any observed behavior improves persuasion,
  comprehension, or presentation outcomes.
- The project must not state that a speaker is confident, deceptive, nervous,
  intelligent, honest, emotional, or persuasive as a directly observed fact.
- Provider failures, empty transcripts, media failures, editing, microphones,
  compression, music, topic, and camera framing remain important limitations.

## Resumption point

Start from the repository root:

```bash
cd /home/mehtama1/git-repo/best-speech-analysis
git status --short --branch
git pull --ff-only origin master
```

Useful validation and report rebuild commands:

```bash
python3 scripts/audit_transcript_coverage.py
python3 scripts/audit_annotation_ledger.py
python3 scripts/build_reviewed_delivery_report.py
python3 scripts/compare_reviewed_delivery_baselines.py
python3 scripts/build_provisional_practice_patterns.py
python3 scripts/analyze_pose_geometry.py
python3 scripts/analyze_pose_movement.py
```

Do not rerun the expensive pose extractor or redownload the corpus unless the
next task specifically requires it. The ScrapeCreators credential is available
from the parent `.env` through the existing scripts; keep it outside tracked
files and do not expose it in logs.

## Recommended next work

1. Continue human review from the remaining annotation queue, deliberately
   balancing speakers, uploaders, speech functions, formats, and video lengths.
2. Expand the multimodal sample and media recovery, recording every failure and
   selection rule in manifests.
3. Inspect pose and visual evidence against timestamped transcript functions,
   while keeping camera/framing confounds explicit.
4. Improve metadata for speaker, format, prepared versus interview speech,
   audience setting, editing, and slide presence.
5. Add a robust facial-landmark or expression measurement path only after its
   dependencies and validation plan are compatible with this environment.
6. Rebuild pattern cards only when cross-video support, counterexamples, and
   direct evidence justify them; then produce the reader/practice edition.

## Research rules

- Preserve source IDs, timestamps, provenance, and retrieval status for every
  claim and example.
- Distinguish measured observation, interpretation, and practical suggestion.
- Prefer counterexamples and uncertainty over inflated generalizations.
- Do not infer protected or private traits, mental states, honesty, or intent.
- Do not commit raw media, credentials, or unrestricted copied source material.
- Treat automated transcripts, audio proxies, visual detectors, and model
  outputs as fallible evidence requiring quality checks.

## Latest checkpoint

The repository is connected to
`https://github.com/mehtama1234/best-speech-analysis.git` on `master`.
The latest committed checkpoint before this handoff is
`89605d3 Build provisional speech practice patterns`, preceded by
`c55a48c Analyze observable pose movement` and
`c5b08a3 Add observable body keypoint analysis`.

