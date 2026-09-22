# Best Speech Analysis: the meaty end-to-end goal

## 1. What we are building

We are building a research and practice system for understanding how people communicate clearly, convincingly, and humanely.

The subject is larger than written words. We will study the words, order, examples, stories, questions, answers, pauses, silence, pace, rhythm, emphasis, loudness, pitch, breath, laughter, fillers, repairs, gaze, facial movement, head movement, hands, posture, walking, stillness, slides, camera framing, cuts, music, objects, audience questions, and room effects.

The final product is not a collection of celebrity tips. It is a searchable, traceable learning library that explains a communication pattern in plain language, shows real examples, states what the evidence does and does not prove, and gives a person a safe way to practise it. It must serve both the web app and native Android/iOS apps through one shared evidence model.

The central question is:

> When a speaker has a communication job to do, what choices help them do that job, how can we see or hear those choices, when do they recur, and how can another person learn the underlying choice without copying the speaker's personality?

## 1.1 The actual end state: a usable speaking curriculum grounded in the corpus

For each important communication job, the finished system must let a learner
start with a real problem and answer all of these questions:

1. **What can I say?** Show the recurring words, phrases, sentence forms,
   transitions, question forms, story structures, contrast structures,
   qualifications, repairs and closing forms in exact context—not isolated
   quotations.
2. **What is the form doing?** Name the speech function and communication job:
   explaining, contrasting, illustrating, telling a bounded story, answering,
   repairing, qualifying, inviting action, creating rapport or closing.
3. **Why might it help?** State a mechanism hypothesis in plain language—for
   example, making a comparison visible, reducing ambiguity, giving a listener
   a concrete handle, or marking the takeaway. Label it as a hypothesis unless
   a separate outcome study supports it.
4. **What else is happening?** Show relevant vocal, temporal, nonverbal and
   setting evidence: pace, silence, turn timing, emphasis, loudness, pitch
   proxy, breath, laughter, gaze, face, head, hands, posture, movement,
   stillness, slides, camera, editing, music, objects, audience and room.
   Keep each modality separate and state missing or unreliable measurements.
5. **Does it recur?** Compare multiple speakers, events, topics, formats and
   communication jobs with denominators and event-level holdouts. Distinguish
   a speaker habit from a cross-speaker pattern.
6. **When does it fail or mislead?** Show absent-but-successful cases,
   present-but-unsuccessful cases, alternate functions, confounds, privacy and
   accessibility risks, and situations where copying the form would be
   manipulative, unsafe, unnatural or inappropriate.
7. **How do I use it?** Provide a repeatable template, a short practice task,
   a self-check, a non-fit test, a listener check and a revision exercise. The
   learner practises the underlying choice, not a celebrity’s accent,
   personality or mannerism.

The finished product is therefore not merely “395 videos analyzed.” It is a
traceable curriculum in which every lesson links **communication problem →
exact language and speech form → delivery evidence → mechanism hypothesis →
cross-talk recurrence → counterexamples and limits → practice → learner check**.
It must say clearly which conclusions are observations, interpretations,
provisional patterns, learning evidence or listener-outcome evidence.

The current [shared provisional curriculum index](research/shared-provisional-curriculum.json)
joins the eight draft lessons across construction slices 01 and 02. Its HTML
view is a discovery surface, while its status fields keep every lesson
provisional until independent review and learner observations exist.

The current five-pattern slice is tracked gate by gate in the
[acceptance matrix](writeups/vertical-slice-01-acceptance-matrix.md). That
matrix is deliberately allowed to say “pending”: a runnable reviewer form or
learner instrument is not evidence that a reviewer or learner has used it.
The wider corpus also contains 87 contextually reviewed pattern annotations,
but those records are legacy/contextual review rather than independent human
validation; they are useful inventory and candidate evidence, not promotion
claims.

## 2. First principles

Do not begin with surface advice such as “use this gesture” or “pause here.” Begin with the problem the speaker is solving.

- A concrete event before a principle helps the audience understand why the principle matters.
- A contrast makes a change visible: what people believed, what happened, and what is now believed.
- A callback gives an earlier idea a new meaning later in the talk.
- A qualification lets a speaker sound clear about the main point while being honest about its limits.
- A pause may give time to process, separate ideas, create expectation, or make room for another person. It is not automatically powerful.
- A gesture may point, show size or direction, mark a list, or simply be a habit. Identify its job before teaching it.
- A smile, laugh, or change in gaze may support rapport, soften disagreement, or reflect the setting. Do not label it as emotion without evidence.

Every finding must separate:

1. **Observation:** what can be checked in the recording or transcript.
2. **Speech function:** what the speaker appears to be doing: explaining, contrasting, answering, repairing, persuading, and so on.
3. **Mechanism hypothesis:** why that choice might help with that job.
4. **Outcome evidence:** whether listeners actually understood, remembered, trusted, or acted. Our current corpus does not prove these outcomes without a separate listener study.

## 3. Concrete examples already in the corpus

These are starting examples, not final universal rules.

| Example | What we observe | What it supports now | What still needs testing |
|---|---|---|---|
| Jeff Bezos, `2u2Sd9MeFUc`, `full-context-address-72` / review 157 | Childhood calculation, injury, kindness, and later choices connect into a larger lesson. | A story can move from concrete event to interpretation to a decision principle. | Whether this order improves understanding or recall. |
| Mindy Kaling, `5mXFlne4JB8`, `full-context-address-71` / review 156 | A college checklist is followed by the fact that plans did not happen as expected; its meaning changes. | Plan-versus-reality contrast can revise the audience's first reading. | Whether the contrast works across topics and audiences. |
| Taylor Swift, `l2ojUrbq8EM`, `full-context-interview-27` / review 155 | An answer reframes music and lyrics toward the idea or feeling underneath the words. | A speaker can correct the starting frame before answering the deeper question. | Whether listeners understand the reframing without shared context. |
| Shakira, `full-context-address-65` | A broad concern is narrowed to a specific business role while government responsibility remains visible. | A large issue can be made actionable without pretending one room owns it all. | Whether listeners can state their role afterward. |
| Oprah, `-54zUwySKCg`, contextual review `review-012` | Pressure around Harvard is revised toward drive and purpose. | An answer can address the practical question behind the literal question. | Whether the premise change feels helpful rather than evasive. |
| Bezos and McRaven examples | An earlier image or phrase returns later with changed meaning. | A callback can create structure across a long talk. | How often it is understood and what other effects explain it. |
| Self-including humour or criticism | The speaker includes themselves before criticizing a group, habit, or situation. | This may make a difficult point less one-sided in this setting. | Whether the effect comes from humour, admission, relationship, or audience. |

For every example record exact words, timestamps, surrounding context, delivery notes, and a plain-language explanation. A link without context is not a usable example.

## 4. The end-to-end research journey

```text
question -> complete source inventory -> provenance and transcripts
-> full-context reading -> speech-function labels -> audio/video evidence
-> synchronized measurements -> careful comparisons -> counterexamples
-> pattern card -> practice exercise -> learner check -> web/mobile lesson
```

### Stage 0: define the question and limits

Write the communication job first: make a complex idea concrete; show that a view changed; answer a hostile question without escalating; invite action without overclaiming; or give time to process a difficult point. Record source type, language, event type, sample size, missing modalities, transcript quality, and whether the claim is observation, interpretation, hypothesis, or tested learning result.

### Stage 1: build a complete inventory

Enumerate every eligible video. Keep stable video IDs, playlist position, title, channel, speaker, date, duration, format, availability, language, duplicate status, and provenance. Distinguish “not found,” “not available,” “not transcribed,” and “not reviewed.”

### Stage 2: acquire and audit transcripts

Store timestamped captions and their source type. Check language, gaps, duplicate lines, timing problems, speaker changes, and full-event coverage. A transcript is text evidence and navigation; it is not proof of tone, pause, gesture, or meaning.

### Stage 3: read full context

Read the event end to end, or record why that was impossible. Mark openings, definitions, explanations, examples, stories, contrasts, corrections, questions, answers, repairs, qualifications, transitions, callbacks, humour, persuasion, and closing. Do not turn one sentence into a principle before checking what came before and after it.

The corpus-wide [pattern atlas](research/corpus-pattern-atlas.json) is the
retrieval layer for this stage. It links exact timestamped phrase candidates
and heuristic communication-job labels to every eligible full-transcript video,
while preserving the one explicitly restricted source and the transcript-only
boundary. Phrase hits are discovery aids, not validated findings.

### Stage 4: label speech function

Give each candidate segment one primary function and optional secondary functions: opening, definition, explanation, example, story, contrast, correction, question, answer, repair, qualification, transition, callback, humour/rapport, persuasion, call to action, or closing. The same pause or words can work differently in different functions.

### Stage 5: collect multimodal evidence

Use a stratified sample rather than pretending every recording has equal quality. Record transcript structure; speech rate; silence length; turn timing; loudness; pitch estimates; breath; laughter; fillers; restarts; gaze; face; head; hands; posture; movement; stillness; slides; camera changes; edits; objects; music; audience turns; and room conditions.

The [multimodal coverage audit](research/multimodal-coverage-audit.json)
reconciles the current 41-video deterministic expansion against files that
actually exist locally and keeps `raw_audio_video_present` separate from
`derived_features_only`. Its manual-review queue is a sampling frame, not a
claim that the selected recordings have already been human-reviewed.

The bounded internal review report
([JSON](research/multimodal-expansion-manual-review.json)) records one sampled
interval for each of the 11 currently raw-complete, transcribed queue items.
It preserves exact caption alignment, edit/title-card contamination and
multi-speaker boundaries; independent review is still a separate gate.
The blank [multimodal independent-review workbook](research/multimodal-independent-review-workbook.json)
and [browser form](writeups/multimodal-independent-review-workbook.html)
make that gate runnable without treating an uncompleted form as evidence.

Every measure must name its reliability and failure cases. A pitch estimate is not confidence. A detected hand movement is not engagement. Sparse visual samples cannot establish facial or gesture meaning.

### Stage 6: ask the mechanism question

What problem might the repeated choice solve? What would be harder without it? What other choice could solve the same problem? When might it fail, distract, or sound false? This moves the project from a feature list to reusable principles.

### Stage 7: compare carefully

Compare the same speaker across functions, independent speakers doing the same function, prepared and spontaneous settings, short and long formats, and sections with and without the candidate pattern. Use event-level holdouts. Check duplicate uploads, speaker/channel identity, topic, audience, microphone, editing, slides, and baseline rates. One famous speech is an example, not a general finding.

### Stage 8: write a pattern card

```text
Pattern name:
Plain-language idea:
Communication problem it may solve:
Speech function:
Concrete examples and source links:
Exact timestamps and surrounding context:
Transcript evidence:
Audio evidence:
Visual or setting evidence:
Direct measurements and method:
Recurrence and denominators:
Independent speakers and events:
Counterexamples:
Alternative explanations and confounds:
What the evidence does not show:
Confidence level:
Practice exercise:
Self-check:
When not to use it:
Next listener test:
```

### Stage 9: turn patterns into practice

Teach the choice, not a fake accent or borrowed personality. Each exercise has a purpose, a short task, a boundary, and a self-check.

- **Concrete before principle:** explain a hard idea once with the rule and once with a small real event. Ask which made it easier to picture and why.
- **Contrast:** say “I used to think X; then Y happened; now I think Z.” Remove the contrast and compare whether the change is still clear.
- **Pause:** record a sentence with no pause, a natural pause, and an exaggerated pause. Keep the version that gives processing time without breaking the thought.
- **Qualification:** state the main claim and one limit. Check whether the limit makes the claim more exact rather than cancelling it.
- **Callback:** introduce an image early, return to it later with new meaning, and ask a listener what changed.
- **Repair:** answer a difficult question, notice a wrong frame, say “The more useful question is…,” and answer that.

### Stage 10: make evidence learnable

The browser and apps should let a person move through:

```text
communication problem -> plain-language pattern -> real example
-> transcript/audio/video evidence -> limits and counterexamples
-> practice -> self-recording and notes -> listener check
```

Users must filter by function, modality, setting, difficulty, source quality, and confidence. Missing evidence and disagreement must remain visible.

The current presenter-facing implementation is indexed in the [presentation
pattern atlas](writeups/presentation-pattern-atlas.html). It links the
395-review exhaustive pattern inventory, 33 source-linked candidate cards, 136
recurring compound pairings, six sequence architectures, and the local
expanded-pattern and compound-bundle practice surfaces. These remain
transcript-derived practice hypotheses until the independent evidence gates
below are completed.

### Stage 11: test learning separately

Test whether learners can identify a pattern, explain it, use it in a new situation, recognize when it does not fit, and improve a recording after feedback. A listener can restate the intended point. This tests whether teaching is usable; it does not prove that the pattern increases trust, memory, or action. Those need later outcome studies.

## 5. Parallel work we must do during the analysis

The research cannot be only a long queue of videos. While the corpus grows, we must also turn the evidence into a usable and testable system.

### 5.1 Build a shared pattern language

Create a fixed set of communication jobs so examples can be compared: explain a complex idea; tell a story; show that a view changed; disagree safely; answer a difficult question; admit uncertainty or set a boundary; ask for action; create connection or ease tension; give the listener time to think; and close with a clear takeaway.

The labels describe the job, not the speaker's personality. A segment may have one main job and a secondary job, but labels must not force every example into a favourite theory.

### 5.2 Build a counterexample library

For every proposed pattern, deliberately collect a case where the pattern is absent but the speech still works; a case where it appears but the speech does not work; a case where the same behavior serves another purpose; a case where editing, topic, microphone, audience, or setting may explain it; and a case where copying it would sound unnatural or inappropriate.

Counterexamples are required evidence, not later cleanup. They prevent the product from becoming shallow speaking advice.

### 5.3 Compare communication jobs, not only famous speakers

Compare how the same speaker explains versus persuades, how a pause works in a story versus disagreement, and how a prepared answer differs from a spontaneous answer. Compare unrelated speakers solving the same job in talks, interviews, debates, classrooms, meetings, and other settings.

“What does this speaker do?” is useful for discovery. “How do different speakers solve this job?” is needed for a general pattern.

### 5.4 Create a reusable example bank

Every approved example must have the speaker, event, source, timestamp, transcript excerpt, surrounding context, audio/video segment where available, communication problem, speech function, observed pattern in plain language, alternative explanation, misuse warning, practice exercise, and self-check.

This bank is the foundation for the web browser, mobile lessons, research reports, and later listener studies.

### 5.5 Add independent review

At least a meaningful sample of examples must be reviewed by someone who did not create the original interpretation. The second reviewer checks the segment, communication job, explanation, evidence limits, and possible alternative readings.

Store reviewer identity, date, modality, disagreements, and resolution. “Reviewed” without this record is not strong validation.

### 5.6 Test whether people can learn the pattern

Before calling a pattern teachable, test whether learners can recognize it in a new speech, explain it simply, use it in their own words, know when not to use it, improve a recording after feedback, and make their point clearer to another listener.

This measures whether our explanation and exercise work. It does not prove that the original speaker's behavior caused better audience outcomes.

### 5.7 Measure listener outcomes separately

Later studies should test whether listeners can repeat the main point, explain a change in the speaker's thinking, remember the example, identify the requested action, or report confusion, rushing, or overload.

Until such a study exists, use “observed pattern,” “practice hypothesis,” and “may help.” Do not claim that a pattern improves trust, recall, or engagement from the corpus alone.

### 5.8 Design the product while researching

The first useful product flow should let a person choose a communication problem, see two or three real examples, inspect words and delivery together, read limits and counterexamples, practise the underlying choice, record themselves, compare versions, receive listener response, and save what worked and what did not.

Research records must be usable in this flow without being rewritten by hand. Every lesson links back to its source evidence.

### 5.9 Use a staged order of work

The working order is: finish interrupted reviews; clean and verify labels; verify speaker and event independence; select a synchronized audio/video sample; complete five strong pattern cards; find counterexamples for each; create five practice lessons; test those lessons with learners; then expand the corpus using what the tests reveal.

Do not spend all effort collecting more speeches before proving that current evidence can become a useful lesson.

## 6. Evidence levels and safe language

1. **Source observation:** visible or audible in a named recording.
2. **Contextual interpretation:** a reasonable reading supported by the surrounding segment.
3. **Candidate mechanism:** a proposed explanation for why the choice may help.
4. **Provisional pattern:** repeated in the reviewed sample with denominators, independent events, and counterexamples.
5. **Practice hypothesis:** a teachable exercise derived from the pattern.
6. **Learning evidence:** people can recognize and use the exercise in a separate test.
7. **Outcome evidence:** a separate listener or audience study measures understanding, memory, trust, or action.

Use “we observed,” “in this sample,” “may help,” and “needs testing.” Avoid “this always works,” “this proves confidence,” or claims about emotion, honesty, intelligence, personality, or audience outcome without suitable evidence.

## 7. Product to build: Communication Patterns Lab

The product should be a **Communication Patterns Lab** with one shared evidence model and two experiences.

The web app is the research and teaching workspace: source inventory, transcript reader, synchronized evidence clips, pattern cards, comparisons, citations, review status, and authoring tools.

The mobile apps are the practice and capture workspace: short lessons, examples, rehearsal prompts, audio/video recording, pause and pace review, self-checks, listener feedback, saved patterns, and progress. Mobile results link to exact evidence records instead of presenting unsupported scores.

The first useful release should not judge personality or give a single “good speaker” score. It should help a person choose a communication problem, study two or three grounded examples, practise one underlying choice, compare recordings, and explain what changed.

## 8. Definition of done

- The corpus has an auditable inventory, provenance, transcript status, and review status.
- Every published pattern has examples, full context, timestamps, direct evidence, denominators, recurrence, counterexamples, limits, and confidence.
- The pattern language covers the main communication jobs and is used consistently across the corpus.
- A counterexample is recorded for every major pattern, including cases where the pattern fails or has another explanation.
- Verbal, vocal, pause, non-verbal, visual, and setting evidence remain distinct and are synchronized where possible.
- The system distinguishes speaker habit from a cross-speaker pattern.
- The example bank records source, context, modality, interpretation, limits, and practice use.
- A second reviewer has checked a meaningful sample of important examples, with disagreements recorded.
- Practice tasks teach an underlying communication job and state when not to use them.
- Web supports research; mobile supports repeated practice.
- A separate learner check shows whether people can identify, explain, use, and reject patterns appropriately.
- Listener outcome studies are kept separate from corpus observations and learner usability tests.
- No report turns a measurement proxy into a claim about emotion, confidence, intelligence, honesty, or audience outcome.
- Unresolved questions and missing evidence remain visible.

## 9. Current position and immediate next work

The fixed transcript queue is now complete: 480 unique videos, 395 non-empty
canonical transcripts, 85 videos without a canonical transcript, 102,816
captions, 102,816 captions in inspected contexts, and 395 full-context analytic
records. This is a transcript milestone, not a claim that the corpus proves
delivery effects, listener outcomes or universal communication rules. Audio,
video, recurrence, independent-speaker validation and learner testing remain
unfinished.

The next goal is the first internally reconciled evidence-to-practice vertical
slice. No external reviewer or learner study is available in this project, so
the autonomous path must complete every repository-checkable gate and label the
remaining human-outcome questions explicitly instead of leaving the work
blocked on an absent participant. Do not expand the transcript queue before
proving that current evidence can become a useful lesson. The slice should:

1. select five communication jobs and five candidate patterns from the completed
   reviews;
2. re-audit their speech-function labels, source provenance and speaker/event
   independence;
3. select a synchronized audio/video sample and record pauses, turn timing,
   pace, vocal emphasis, gaze, gesture, posture, editing, music and room context
   with reliability and failure notes;
4. add denominators, counterexamples and alternative explanations to each
   pattern card;
5. run autonomous adversarial checks over the evidence, interpretation, limits
   and safety boundary, while recording independent-review status as unavailable;
6. create five linked web lessons and mobile practice flows; and
7. provide a runnable learner check for recognition, explanation, transfer and
   misuse detection, while recording improvement and listener outcomes as
   unmeasured until participants exist.

The autonomous end-to-end audit (writeups/autonomous-end-to-end-audit.md) now
joins the autonomous curriculum, vertical-slice packet, delivery
reconciliation, full-media reconciliation, language reconciliation,
counterexample screening, learner/listener instrument dry runs, full curriculum
surface, identity metadata preflight, recurrence split validation, review-gate readiness, recovered-pattern priority review readiness, evidence-to-practice, multimodal traceability, web-surface integrity, browser runtime smoke, accessibility/privacy checks, claim-boundary integrity, media recovery integrity, practice-record integrity, local practice ingestion and metadata summarization into one twenty-seven-check release-candidate
audit. These
artifacts cover the repository-checkable portion of this slice. The
[autonomous curriculum audit](writeups/autonomous-curriculum-audit.md) is the
current corpus-level control document, and the [vertical-slice packet audit](writeups/autonomous-vertical-slice-01.md) is the five-packet control document.
The older
[validation audit](writeups/vertical-slice-01-validation-audit.md) remains a
record of unavailable external and participant evidence; its 0/5 promotion
count must not be mistaken for a failure of the autonomous reconciliation.

The project may use the internally reconciled materials as provisional lessons
and practice prompts, with their claim boundaries visible. It must not call a
pattern universally effective or claim learner improvement, listener trust,
memory or action without a separate outcome study.

The end state is a living evidence system: a person can start with a real communication problem, find a clearly explained pattern, inspect exact examples and limits, practise the underlying choice, and return new observations to the research corpus.
