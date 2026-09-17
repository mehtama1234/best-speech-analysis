# Review a pause with its surrounding speech

The [audiovisual review browser](pause-review-browser.html) brings all seven
unresolved pause candidates together. It uses local-only clips, nearby provider
captions, three threshold-based quiet-interval lists, and the available visual
reviews and decoded-frame audits. No new pause judgment is made by building or
playing the page.

## Open it locally

From the repository root, run:

```bash
python3 scripts/serve_pause_review.py --port 8891
```

Then visit http://127.0.0.1:8891/. The server binds only to loopback and serves
only the generated page and its seven allowlisted cache clips. It does not
serve credentials, repository directory listings, original media or arbitrary
files. It supports byte-range requests for seeking. Stop with Ctrl-C when done.

The cache is ignored by Git. To rebuild missing clips and the page:

```bash
python3 scripts/build_pause_review_browser.py
```

This requires the original local audio/video files and the existing Python
`imageio_ffmpeg` dependency. It does not download media or call a transcript API.
Each cache key records source hashes, trim range, decoder version and recipe
version. The [packet](../research/pause-review-packet.json) records resulting
clip hashes and input provenance. Do not publish the cached clips as research
artifacts without resolving media rights.

## How to use the evidence

1. Select a case and watch/listen to the surrounding clip before the target.
   The target caption has a border; several overlapping captions may highlight
   at once. Caption timing is approximate, not validated word alignment.
2. Check whether visible speech and audio appear aligned at more than one
   event. Record the anchors, possible offset and uncertainty. These clips
   combine streams at the same requested source time; **that is an assumption,
   not verified synchronization**. Small trim/codec timing effects also remain
   unvalidated. Do not use the player as a millisecond-accurate measurement tool.
3. Distinguish actual quiet audio from a caption gap, music, audience sound,
   breath or another speaker's turn. Energy below a threshold is not a semantic
   pause classification. A threshold run can be censored at its audit window.
4. Inspect cuts, subtitles, camera changes and gestures without inferring an
   internal feeling or intention. The film case already shows different shots
   in sampled frames; continuous viewing is needed to locate the transition.
5. Describe the speech function with surrounding language: idea boundary,
   turn change, story beat, repair, or unresolved. Record alternatives and what
   additional evidence would distinguish them. Compare non-quiet windows before
   interpreting a recurring technique.

Draft notes are per case and stored in this browser origin's local storage.
Changing host or port changes that storage origin. Use Export to retain a JSON
copy. The export remains `unadjudicated_draft`; checkboxes are reviewer assertions,
not automatic proof of viewing/listening. No draft is sent to a server or imported
into the research ledger. Browser storage can be cleared, so it is not a durable
handoff. Independent adjudication and provenance checks must precede promotion.

## Verification boundaries

`python3 scripts/check_pause_review_browser.py` uses an installed Playwright
Chromium to check playback, seeking, draft isolation/persistence/export and
mobile overflow. It plays muted for automation: successful decoding is not
listening, content interpretation, synchronization validation or human review.
The smoke-test report is separate from the semantic review records.
