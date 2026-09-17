# Best Speech Analysis — end-to-end goal and research handoff

Checkpoint: 17 September 2026. Project unfinished. Start here, then read the
[full goal](SPEECH_ANALYSIS_END_TO_END_GOAL.md) and the newest entry in
[PROJECT_STATUS.md](PROJECT_STATUS.md). This handoff consolidates the objective,
provisional learning, evidence boundaries and next actions; it does not replace
the detailed research records.

## 1. What the user wants

Turn entire playlists of speeches, presentations, interviews and related material
into an evidence-backed guide to becoming a better communicator. The three seed
URLs identify playlists, not a three-video assignment. Initial playlist IDs:

- `PLosaC3gb0kGDhmBVm6M47jcU8BbEhTnlP`
- `PLLVLl07BgiJYSCSdl1fd34s4SzILbMxp9`
- `PLosaC3gb0kGDEFRm7OxnWgOmJkEki1LPj`

The meaty end-to-end objective is to enumerate the full corpus, acquire and audit
available transcripts, read speeches in context, explain their argument and story
structure, and progressively align representative examples with verified audio
and video. Discover recurring ways speakers explain, emphasize, qualify, disagree,
answer, tell stories and call for action. Test recurrence across independent
speakers and events, actively seek counterexamples, and distinguish observable
behavior from possible function and demonstrated audience benefit.

The end product must teach someone what to try, why it might help, when not to use
it, and how to assess their own attempt. Every substantial finding needs traceable
examples, source-quality limits and an honest statement of what remains untested.
Famous speakers and popular uploads are not automatically effective examples.

Pipeline: playlist inventory → provenance and acquisition → quality checks →
full-context reading → candidate mechanisms → synchronized delivery evidence →
independent-event comparisons → counterexamples and outcome tests → practical
reader and searchable evidence browser → independent audit.

## 2. What exists at this checkpoint

The saved inventory reports 480 unique videos and 395 nonempty canonical
transcripts; 85 videos lack a canonical transcript. The reading queue contains
102,816 captions. Of these, 48,503 are in inspected contexts (about 47%). It reports
165 videos with all retained captions in one review and 160 full-context records,
including one restricted source-quality inspection. These are different measures:
neither count means 165 independently verified, complete original speeches.

The latest completed record is `full-context-20260917-160`, the Star Trek excerpt
`fHAOWLhrxhQ`, with [its report](writeups/full-context-scene-11.md). Fiction is
analyzed as constructed dialogue, not evidence of real-world speaking success.

The work includes human-readable close readings, machine-readable episode maps,
relations, context hashes, boundary cases, provenance audits, recovery experiments,
delivery-quality diagnostics and tests. Much of the recent effort corrected
overconfident interpretations and restored context rather than adding tips.

The previous checkpoint passed 68 tests. Tests check structure, hashes and safety
restrictions; they do not prove interpretive correctness or communication efficacy.
Audio/video pilots exist, but verified continuous multimodal analysis is unfinished.
Do not present the project as having established optimal pauses, gestures or pitch.

## 3. What a learner can take away now

These are practice hypotheses grounded in the cited readings, NOT validated
cross-corpus best practices. A visible structure supports describing the technique;
it does not establish that the audience understood, remembered or agreed more.

### A. Make the principle concrete before naming it

[Bezos](writeups/full-context-address-72.md), captions 0–51: a remembered childhood
calculation leads to hurt rather than the praise he expected. The grandfather's
response then introduces kindness versus cleverness and the gifts/choices frame.

Practice: describe a specific decision and its consequence, then state the lesson.
Keep an invented example labeled hypothetical. Do not treat one anecdote as proof
of a general rule. Test whether a listener can explain the principle, not merely
remember the anecdote.

### B. Let a later example revise the meaning of an earlier one

[Kaling](writeups/full-context-address-71.md), captions 219–261: a successful
college checklist precedes adult plans that did not unfold on schedule. The second
account changes the first one's meaning. The conclusion permits revised plans
while retaining that structured ambition sometimes helps.

Practice: “I believed X; this experience challenged it; here is the revised view.”
Do not manufacture a reversal or erase useful parts of the original belief. Test
whether the listener remembers both the change and its qualification.

### C. Return to an opening idea with added meaning

[Bezos](writeups/full-context-address-72.md) returns to choices and kindness in
the closing questions. [McRaven](writeups/full-context-address-67.md) connects ten
stories with repeated cues and a closing recap. These are candidate comparisons,
not a measured recurrence or effectiveness result.

Practice: introduce a question, develop the answer, then revisit it. Distinguish
a callback that adds meaning from a slogan repeated without development. Compare
delayed recall with and without the callback before claiming a memory benefit.

### D. Keep confidence and qualification together

Kaling's self-belief is accompanied by support from others. Bezos preserves
uncertainty, spousal support and an admired boss's reasonable caution.
[Jack Ma](writeups/full-context-interview-25.md) pairs persistence with adaptation.
None justifies the simple instruction to ignore everyone and never change course.

Practice: give advice and its operating boundary: keep working toward the goal,
but revise the approach when evidence changes. Include conditions for stopping.
Success stories have survivorship bias and do not establish what would work for
someone with different resources, risks or responsibilities.

### E. Make humor include the speaker

Kaling, captions 27–48 and 98–118, undercuts her own distinction and turns jokes
about literal names onto her own show titles. The observable feature is a joke
whose teller is also a target. Increased rapport has not been measured.

Practice: include yourself honestly in a humorous criticism. Keep the point clear
and avoid a joke that makes others feel diminished. Evaluate reception in the
actual audience; do not assume self-deprecation always improves credibility.

### F. Correct a premise before explaining the mechanism

[Taylor Swift](writeups/full-context-interview-27.md) reframes music-versus-lyrics
as sometimes beginning with an idea or feeling. The interview also preserves
uncertainty and disclosure boundaries. Jack Ma's interview demonstrates a related
caution: the interviewer supplies the concrete escrow explanation, so the guest
must not receive sole credit for it.

Practice: “That assumes X; in this case the process starts with Y; here is an
example.” Then return to the actual question. A premise correction should not be
used to evade a difficult question. Attribute a co-produced explanation correctly.

### G. Give this audience a specific role

[Shakira](writeups/full-context-address-65.md), captions 45–62, connects a broad
social concern to business capabilities while retaining government responsibility
and partnership. The request is more specific than asking everyone to care.

Practice: specify what these listeners can decide, contribute or do next. An
executive, engineer and controller may need different actions from the same
explanation. Specificity is observable; actual uptake requires separate evidence.

### An immediate practice exercise

Give a three-minute explanation of why a finance agent may propose a payment but
may not authorize money movement. This is a learner exercise connecting to the
user's separate finance project, not a change in this repository's research scope.

1. Introduce a clearly hypothetical invoice incident.
2. Explain why agent confidence does not resolve the financial-control risk.
3. Separate proposal from authorization.
4. Describe deterministic checks and policy-controlled escalation.
5. Return to the incident and show how the design handles it.

Record the explanation. Ask a listener to restate the mechanism, its boundary and
the next action. Assess clarity before imitating a celebrity's voice or gestures.

## 4. Evidence rules the next researcher must preserve

- Read the entire retained transcript before claiming a full-context reading.
  Truncated command output is not read evidence. Read long sources in visible,
  consecutive chunks. Retained-upload completeness is not original-event completeness.
- Preserve raw captions, provenance and uncertainty. Do not silently repair corrupt
  wording from memory, subtitles from another version, or a familiar film script.
- Attribute biographical, political, scientific and outcome claims to the speaker
  unless independently checked. A compelling story does not verify its facts.
- Preserve objections, qualifications, unanswered questions, interviewer contributions
  and contradictions. Do not extract a slogan that reverses the larger argument.
- A caption gap is not a measured pause. Reported silence in an anecdote is not
  the presenter's delivery. RMS is not listening or validated speech detection.
  Sparse pose frames are not gesture trajectories. Verify synchronization first.
- Deduplicate events and reused text, not just video IDs. Compilation previews,
  reuploads and overlapping excerpts are not independent replications.
- Do not infer honesty, intelligence, personality or internal emotional state as
  fact from text, voice or appearance. Describe observable behavior instead.
- Do not promote a technique to an established practice card merely because a
  famous speaker uses it. Recurrence and benefit are separate questions.

Critical restricted source: `bV5uKHsWQtY` is labeled Denzel Washington, but the
retained transcript names Muniba Mazari and has suspect timestamp spacing.
Record 050 is a source-quality inspection, not a completed Washington analysis.
Keep `speaker_attribution_unverified`, `video_transcript_pairing_unverified` and
`timestamp_alignment_unreliable` active. Read the
[mismatch report](writeups/source-mismatch-washington-labeled.md) and
[downstream audit](writeups/source-mismatch-downstream-audit.md).
`scripts/source_restrictions.py` propagates exclusions; missing restrictions are
not permission to use the source as validated evidence.

The Vivekananda-labeled upload is a text composite of portions of two historical
addresses. Text correspondence does not authenticate the voice or original delivery.
See [historical-source report](writeups/full-context-historical-01.md).

## 5. Exact place to resume

The next fixed-queue source is P. V. Sindhu, `uIs3o2eEtUg`: 392 captions / 2,564
stored words. Captions 0–195 were read in the interrupted session; 196–391 were
NOT read. No completed review or report was added. The next researcher should
reread 0–195 to restore context, then read the remainder before making conclusions.

Context hash at interruption:
`28b9172612155b78c5d2e17f01a04ba1006caa271bfd79983838af80ca423fd3`.

Working observations, not admitted conclusions: a four-lesson roadmap; early
effort and showing-up stories; failure and doubt; Rio silver contrasted with the
speaker's disappointment; Tokyo bronze; an internally inconsistent later phrase
about two bronze medals; a Commonwealth Games injury story beginning near the
end of the read portion. Do not silently fix the medal inconsistency. Read the
injury story's remainder before judging whether persistence includes safety,
support or recovery. Do not turn it into advice to play through injury.

If no intervening changes exist, use review `full-context-20260917-161` and report
`writeups/full-context-address-74.md`. Confirm IDs and filenames are still free.
Next sources: `rOSqiOyy1tc` (Priyanka Chopra, 685 captions / 5,054 words), then
`zgDnvVaoV98` (Cory Booker, 392 / 4,242). Preserve the fixed order; do not skip long
sources to inflate completion counts.

## 6. Repeatable work procedure

1. Inspect current Git status and the newest checkpoint; preserve unrelated changes.
2. Use `research/full-reading-queue.json` to identify the next source. Read relevant
   prior context records; some identify videos through evidence IDs, not `video_id`.
3. Read all retained captions from `research/segment-registry.jsonl`. Compute the
   context digest with `scripts/review_evidence.py`; never invent a hash.
4. Write a report separating source boundary, episode sequence, mechanisms,
   qualifications, counterexamples, limits and a concrete next comparison.
5. Add a record to `research/full-context-reviews.json`: reviewer/date/modality,
   ordered context evidence IDs and hash, coverage/selection, format evidence,
   episode map partitioning the source, relations, boundary cases, limits,
   next test and report path. Match the actual schema of existing records.
6. Rebuild the queue and run the checks below. Inspect changed artifacts. Update
   README and prepend a status checkpoint without deleting history.
7. Report what changed and what is still unsupported. Structural validation is
   not independent substantive review.

Run from the repository root:

```bash
python3 scripts/build_full_reading_queue.py
python3 -m unittest discover -s tests -q
git diff --check
git diff --numstat -- data/transcripts data/features research/speech-annotations.jsonl
```

The last command detects unintended changes to existing source/feature/legacy
annotation files; it is not itself a test that their contents are correct.

## 7. Remaining work beyond transcript reading

Continue full reading while separately accounting for unavailable sources and
quarantined recovery candidates. Reconcile acquisition manifests before spending
more API calls. The user identified ScrapeCreators credentials in the parent
directory's `.env`; load secrets only when needed, never print or commit them.
Do not mistake successful API responses or cache-file counts for usable transcripts.

Build an event-level duplicate map before estimating recurrence. Define comparison
units and denominators, stratify by speech function and format, retain negative
cases, and hold out independent speakers/events for confirmation. Candidate
techniques above are a starting comparison agenda, not a completed synthesis.

For delivery work, begin with a small, continuously reviewed and synchronized
audio/video sample. Verify transcript/audio pairing and time offsets. Annotate
edits, music, slides, speaker turns and recording conditions. Compare pauses,
emphasis and gesture within context; normalize or qualify measurements affected
by microphones and editing. Earlier coarse pilots and unsuccessful OCR tests do
not justify automatically scaling those methods.

Test comprehension, recall or action with an appropriate learner/listener task
before claiming effectiveness. Add an independent reviewer for interpretation
and annotation agreement; resolve disagreements visibly rather than silently.

Publish a navigable reader and evidence browser linking each explanation to its
source, supporting and contrary examples, permitted playback references, modality,
confidence and limitations. An old local server address is not evidence it is
currently running; verify before advertising a live link.

## 8. Completion criteria

- Every discoverable playlist item is accounted for, including unavailable items.
- Every available canonical transcript has a context-complete review or an explicit
  unresolved quality restriction; recovered sources have documented admission checks.
- Major pattern claims have independent-event comparisons, denominators,
  counterexamples, confounds and limits. Habit, recurrence and effectiveness are
  clearly different labels.
- Every delivery claim has verified relevant audio/video evidence and alignment.
  Unsupported modalities remain explicitly unknown.
- The reader teaches usable exercises with evidence and boundaries, not just
  biographies, summaries, motivational slogans or a wall of audit records.
- Provenance, reproducibility, restriction propagation and independent substantive
  review have been checked. No claim of full completion while major evidence or
  validation work remains.

## 9. Repository handoff and commit scope

The user requested committing all current project work together with this handoff.
Include the existing research, scripts, tests, reports, metadata and quarantined
recovery artifacts, preserving their restricted status. This is a research
checkpoint, not a finished-results release. Keep credentials, caches, raw media
and other ignored runtime assets out of Git. Do not touch the separate finance,
ml-youtube or other repositories. A local commit is not a remote push.
