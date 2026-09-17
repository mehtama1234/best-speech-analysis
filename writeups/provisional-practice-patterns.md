# Provisional practice patterns

Review provenance: legacy reviewer identity is unknown; contextual per-label overrides are assistant transcript-only judgments. See research/contextual-label-reviews.json. These are not independently human-validated findings.

Delivery robustness is evaluated separately in [the disjoint-reference sensitivity report](disjoint-delivery-comparison.md). A historical rate-direction reversal was traced to a four-millisecond caption artifact; current rate summaries exclude durations below a provisional 0.25-second floor. See [timing diagnosis](timing-artifact-diagnosis.md). Screening does not validate speech timing; do not convert pooled means into instructions to speak faster, slower, louder or at a particular pitch.

These are practice hypotheses, not universal speech rules. A card is admitted only when at least five reviewed examples support the candidate label, those examples span at least four videos, and the reviewed support rate is at least 0.70. The delivery values are measured summaries and same-video exploratory deltas; they do not establish causation, persuasion, comprehension, or internal state.

Eligible provisional patterns: **5** of **7** candidate labels.

## Make the comparison explicit

Candidate label: `contrast_or_disagreement`  
Evidence: 10 supported examples across 9 videos and 3 uploaders; reviewed support rate 1.0.

Practice hypothesis: When correcting or distinguishing ideas, state the contrast directly (for example, expected outcome versus observed outcome) and then supply the replacement claim or evidence.

Direct measurement summary: RMS mean -22.30288; pitch proxy mean 240.15075; words/second proxy mean 2.58438; transcript gap-before mean 0.0 seconds.
Same-video exploratory deltas: RMS 1.88977 dB; pitch proxy 8.38618 Hz; words/second 0.99482.
Measurement denominators (not the full supported-example count): {'mean_rms_db': 8, 'mean_pitch_hz_proxy': 8, 'words_per_second_proxy': 8, 'transcript_gap_before_seconds': 8, 'transcript_gap_after_seconds': 8}. Baseline comparison uses 8 examples across 8 videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.
Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.

Timestamped examples:

- [-54zUwySKCg:00028](https://www.youtube.com/watch?v=-54zUwySKCg&t=173): But then I realized that you don’t haveto necessarily go to Harvard to have a driven.
  Context: personal_reconsideration; attribution: current_turn_narrative. The speaker first describes pressure about addressing Harvard graduates, then revises the premise that attendance is necessary for a particular disposition. This is a personal reconsideration. The self-description is reported wording, not a personality assessment by this project.
- [-54zUwySKCg:00059](https://www.youtube.com/watch?v=-54zUwySKCg&t=305): But a few years ago I decided, as you willat some point, that it was time to recalculate,.
  Context: see review reason; attribution: not separately adjudicated. The preceding captions describe sustained success and comfort; 'But' introduces a decision to change direction. This supports contrast, not interpersonal disagreement.
- [3AIoHLr8nTI:00097](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=845): genital mutilation is wrong, no matter how many generations have practiced it..
  Context: normative_rejection_of_justification; attribution: current_turn_argument. The passage rejects a practice despite its historical prevalence after distinguishing understanding from moral relativism. It opposes a possible justification; no actual exchange with a disputant is observed in these captions.
- [AwA0Jnfj3ao:00125](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=580): But and I said, oh, this is a wrong place..
  Context: observed_versus_expected_position_in_story; attribution: current_turn_narrative. The surrounding narrative contrasts seeing the ball with reacting too late and where it was versus where it should be. The wording is somewhat garbled; the target's 'wrong place' belongs to that narrative contrast, not a live dispute.
- [OfwfTN1mEyM:00139](https://www.youtube.com/watch?v=OfwfTN1mEyM&t=368): often not quite understood but but the.
  Context: public_perception_versus_claimed_analysis; attribution: current_turn_argument. The speaker contrasts limited public understanding of available solar power with a claim that its mathematics is clear, followed by a recommendation. The textual opposition is present; neither the mathematics nor public understanding is independently evaluated.

Counterexamples retained:

No rejected cases in the current reviewed sample; this is not evidence that counterexamples do not exist.

Limit: This sample combines personal reconsideration, asserted outcomes, reported advice and scene dialogue. Textual contrast does not establish a real interpersonal dispute, successful disagreement handling or truth of the contrasted claims. The selected reviewed sample is not a population precision estimate.

Visual evidence status: Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.

Required next test: Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.

## Move from the general claim to a concrete case

Candidate label: `example`  
Evidence: 8 supported examples across 5 videos and 1 uploaders; reviewed support rate 0.8.

Practice hypothesis: After an abstract claim, announce or signal a specific case, statistic, named example, or imagined scene, and connect it back to the claim.

Direct measurement summary: RMS mean -16.995; pitch proxy mean 240.095; words/second proxy mean 1.41914; transcript gap-before mean 0.01714 seconds.
Same-video exploratory deltas: RMS -0.42955 dB; pitch proxy -3.53387 Hz; words/second 0.18469.
Measurement denominators (not the full supported-example count): {'mean_rms_db': 7, 'mean_pitch_hz_proxy': 7, 'words_per_second_proxy': 7, 'transcript_gap_before_seconds': 7, 'transcript_gap_after_seconds': 7}. Baseline comparison uses 7 examples across 4 videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.
Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.

Timestamped examples:

- [-6qN3bm2RYo:00079](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=221): together on global issues such as.
  Context: category_enumeration; attribution: not separately adjudicated. Global issues are unpacked into terrorism, pandemics and the environment after a statement about unity. These are category members, not detailed empirical cases or evidence that the policy succeeds.
- [aXmM0VZv810:00274](https://www.youtube.com/watch?v=aXmM0VZv810&t=673): this earlier radiology for example has.
  Context: asserted_domain_case_with_explanation; attribution: not separately adjudicated. The speaker introduces radiology as a case for a claim about technology and work, contrasts a forecast with an asserted employment trend, then explains a goal-versus-task distinction. The extended context establishes the illustration; the medical/employment assertions are not independently validated.
- [aXmM0VZv810:00529](https://www.youtube.com/watch?v=aXmM0VZv810&t=1274): >> Just imagine how tiny that little.
  Context: scale_visualization_of_existing_object; attribution: not separately adjudicated. A discussion of rack weight and cooling is followed by an invitation to imagine the small computational object. This is concrete scale illustration of an existing referent, not necessarily a new hypothetical event. Speaker turns are not reliably attributed by captions.
- [aXmM0VZv810:00596](https://www.youtube.com/watch?v=aXmM0VZv810&t=1418): some over 20 years. Let me give you one.
  Context: quantitative_before_after_case; attribution: not separately adjudicated. A claim about movement toward accelerated computing is followed by a top-500-supercomputer percentage comparison and a return to the transition claim. The transcript gives both 'less than 15%' and '10%' for the later CPU share; these must not be silently reconciled. The numerical claim is not fact-checked.
- [jxY2-YgAgm0:00087](https://www.youtube.com/watch?v=jxY2-YgAgm0&t=258): such as Daily Beast, James Carville, and.
  Context: named_instances_of_asserted_category; attribution: not separately adjudicated. The speaker names entities after asserting a category of people/companies that retracted statements. The local list instantiates that asserted category. This review does not endorse allegations, legal characterizations or claims about the named parties.

Counterexamples retained:

- `S43F1BZfQKY:00018`: The shop visit continues with a wig being shown and bought, followed by the narrator's reported reaction. 'Imagine' intensifies description of that object rather than introducing a case for general reasoning. The source explicitly says wig shop owner; the legacy record's doctor attribution is unsupported.
- `gDadfh0ZdBM:00001`: The speaker offers advice to be honest, not an event or case illustrating a broader proposition. Later unrelated dialogue in the inspected window does not establish an example relation.

Limit: This sample mixes category lists, asserted cases, numerical comparisons and imagined scenarios. A vivid detail is not automatically an example; an illustration is not factual verification or causal proof. Source allegations and numerical claims are not endorsed.

Visual evidence status: Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.

Required next test: Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.

## Use bounded personal detail

Candidate label: `story_or_personal_experience`  
Evidence: 10 supported examples across 6 videos and 1 uploaders; reviewed support rate 0.769.

Practice hypothesis: A short first-person event, setting, action, or quoted line can make an abstract point concrete; mark the transition back to the broader point.

Direct measurement summary: RMS mean -28.15288; pitch proxy mean 237.89062; words/second proxy mean 1.77737; transcript gap-before mean 0.0 seconds.
Same-video exploratory deltas: RMS -1.66985 dB; pitch proxy 2.35248 Hz; words/second 0.02171.
Measurement denominators (not the full supported-example count): {'mean_rms_db': 8, 'mean_pitch_hz_proxy': 8, 'words_per_second_proxy': 8, 'transcript_gap_before_seconds': 8, 'transcript_gap_after_seconds': 8}. Baseline comparison uses 8 examples across 5 videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.
Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.

Timestamped examples:

- [-54zUwySKCg:00035](https://www.youtube.com/watch?v=-54zUwySKCg&t=201): That was when I was 16 years old in Nashville,Tennessee, and you had the requirement of.
  Context: autobiographical_scene_setup; attribution: not separately adjudicated. The narrator names a career origin, a contest, an age and a place, then introduces its question-and-answer sequence. The target sets up a personal event; this short window does not contain the full story or verify its historical truth.
- [-54zUwySKCg:00059](https://www.youtube.com/watch?v=-54zUwySKCg&t=305): But a few years ago I decided, as you willat some point, that it was time to recalculate,.
  Context: see review reason; attribution: not separately adjudicated. A first-person decision anchored a few years earlier is followed by ending the show and launching a network. The inspected sequence supports a personal-story transition.
- [9fEurt2OZ0I:00008](https://www.youtube.com/watch?v=9fEurt2OZ0I&t=31): I went for a police they said no you're.
  Context: sequence_of_personal_rejection_accounts; attribution: not separately adjudicated. The narrator links job applications, a reported rejection and another application example. Despite garbled wording, personal actions and responses form a sequence. Counts, job names and outcomes are not independently fact-checked.
- [AwA0Jnfj3ao:00130](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=598): I went to the bathroom and I cried..
  Context: setback_action_and_self_address; attribution: not separately adjudicated. Following a cricket setback, the narrator describes going to a bathroom, crying and speaking to himself in a mirror, before later seeking advice. Those are narrated actions, not acoustic or visual evidence of emotion during the current speech.
- [S43F1BZfQKY:00002](https://www.youtube.com/watch?v=S43F1BZfQKY&t=29): I remember that day..
  Context: dated_recollection_with_trigger_event; attribution: not separately adjudicated. The remembered date is followed by a first-person shower episode and discovery of hair in the hand. Context supplies an actual narrated event rather than merely the marker 'I remember'. The report does not independently verify the medical history.

Counterexamples retained:

- `3AIoHLr8nTI:00069`: The passage describes what leaders in every generation supposedly realize and urges the graduates to lead. It is a generalized scenario, not an identified personally experienced event.
- `bR4tDSa3O10:00051`: A childhood location anchors an imagined reaction: if acquaintances had been told about the later opportunity, they would have laughed. The target does not report that such an exchange occurred or narrate a sequence of experienced events. This can still be a useful counterfactual device, but is not support for the narrower experienced-event rubric.
- `OfwfTN1mEyM:00152`: The speaker compares earlier and current solar/battery costs. Time references alone do not make this a personally experienced narrative. The price claims are not verified here.

Limit: This sample mixes scene setups, actions, reported dialogue and brief autobiographical memories, not complete story arcs. Isolated counterfactual reactions and historical comparisons are excluded under the experienced-event rubric. Narrated events, quoted claims and emotional descriptions are not independently verified facts or current delivery measurements.

Visual evidence status: Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.

Required next test: Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.

## Qualify predictions and interpretations precisely

Candidate label: `uncertainty_or_qualification`  
Evidence: 8 supported examples across 7 videos and 1 uploaders; reviewed support rate 0.889.

Practice hypothesis: Use explicit qualifiers such as 'I think', 'might', or 'probably' when a claim is a view, prediction, or interpretation rather than an established fact.

Direct measurement summary: RMS mean -22.80262; pitch proxy mean 270.30325; words/second proxy mean 1.48937; transcript gap-before mean 0.75 seconds.
Same-video exploratory deltas: RMS -2.00437 dB; pitch proxy 1.97689 Hz; words/second 0.01203.
Measurement denominators (not the full supported-example count): {'mean_rms_db': 8, 'mean_pitch_hz_proxy': 8, 'words_per_second_proxy': 8, 'transcript_gap_before_seconds': 8, 'transcript_gap_after_seconds': 8}. Baseline comparison uses 8 examples across 7 videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.
Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.

Timestamped examples:

- [2fWJh-_UG5s:00160](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=362): maybe that would make.
  Context: reported_hypothetical_consequence; attribution: reported_other_people_text. The surrounding clauses say Ryan and Jessica said sharing the art might have a hoped-for consequence. The qualification is in reported speech, not evidence of the narrator's own belief strength. No afterlife or emotional-response claim is validated.
- [3AIoHLr8nTI:00008](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=91): This group is truly diverse in every possible way. And I think that is an extraordinarily.
  Context: opinion_framed_evaluation; attribution: current_turn_text. After describing the group's diversity, 'I think' introduces an evaluation of its value. This marks the evaluation as a view; it does not establish weak conviction or internal uncertainty.
- [3AIoHLr8nTI:00074](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=665): from their leaders today and tomorrow? Now, I think you need to be brave..
  Context: opinion_framed_advice_with_reinforcement; attribution: current_turn_text. A question about leadership is answered with 'I think you need to be brave', followed by 'Really brave'. The viewpoint marker coexists with textually reinforced advice; it does not prove hesitation.
- [9fEurt2OZ0I:00020](https://www.youtube.com/watch?v=9fEurt2OZ0I&t=66): sorry now I think we have to get used to.
  Context: opinion_framed_recommendation; attribution: current_turn_text. Following repeated rejection in the account, 'I think' frames the recommendation to get used to rejection. 'Have to' still expresses necessity. No softness of vocal delivery is inferred.
- [C8-twwwTETE:00045](https://www.youtube.com/watch?v=C8-twwwTETE&t=98): how into him I was right but I think I.
  Context: qualified_retrospective_self_evaluation; attribution: current_turn_text. The narrator describes talking at length to someone, then uses 'I think' and 'might have probably' to evaluate whether it was excessive. The continuation is needed to complete the clause; this is not an acoustic uncertainty judgment.

Counterexamples retained:

- `-54zUwySKCg:00122`: Under the claim-qualification definition, 'could' describes hypothetical capacity inside a narrated question. No factual assertion or prediction is explicitly hedged in this context. A broader wondering category could differ; no internal uncertainty is inferred.

Limit: Verbal qualification does not prove internal uncertainty. This sample mixes current-turn views, reported other people's words and unresolved turn attribution; recommendations may remain strong. Voice has not been adjudicated against the wording.

Visual evidence status: Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.

Required next test: Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.

## Mark the takeaway

Candidate label: `conclusion_or_summary`  
Evidence: 5 supported examples across 5 videos and 1 uploaders; reviewed support rate 0.833.

Practice hypothesis: Use a clear summary or conclusion marker when compressing a preceding explanation, story, or comparison into the point the audience should retain.

Direct measurement summary: RMS mean -18.20367; pitch proxy mean 209.75933; words/second proxy mean 1.521; transcript gap-before mean 0.0 seconds.
Same-video exploratory deltas: RMS 0.36422 dB; pitch proxy -12.44097 Hz; words/second -0.18368.
Measurement denominators (not the full supported-example count): {'mean_rms_db': 3, 'mean_pitch_hz_proxy': 3, 'words_per_second_proxy': 3, 'transcript_gap_before_seconds': 3, 'transcript_gap_after_seconds': 3}. Baseline comparison uses 3 examples across 3 videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.
Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.

Timestamped examples:

- [-54zUwySKCg:00196](https://www.youtube.com/watch?v=-54zUwySKCg&t=989): The point is your generation is charged withthis task of breaking through what the body.
  Context: broad_takeaway_and_charge; attribution: not separately adjudicated. Several possible ways to make a difference precede a general charge to the generation to change political conditions. This is a broad takeaway tied to those examples, not merely an isolated 'point' marker. Full speech closure is not established.
- [-URn1fARvts:00119](https://www.youtube.com/watch?v=-URn1fARvts&t=254): In short, being a young person balancing.
  Context: autobiographical_summary; attribution: not separately adjudicated. The earlier captions describe combining skills, asking hard questions and willingness to learn; the following complete sentence compresses school and sport into critical curiosity and learning about the world. Some transcript phrasing remains uncertain.
- [AwA0Jnfj3ao:00234](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=1016): So, it's just, in short, it's just being astep ahead of your opposition..
  Context: story_to_principle; attribution: not separately adjudicated. The preceding cricket sequence describes anticipating an opponent and warning a teammate. The target states the general lesson of being a step ahead, followed by interviewer thanks. This supports a story-to-principle summary, not proof the strategy is universally useful.
- [aXmM0VZv810:00483](https://www.youtube.com/watch?v=aXmM0VZv810&t=1175): overwhelmingly what matters.
  Context: local_argumentative_conclusion; attribution: not separately adjudicated. The preceding energy-use criterion leads to a prioritizing conclusion that space matters. It is a local argumentative takeaway, not a speech-ending summary. Additional support follows; garbled scientific wording is not repaired or fact-checked here.
- [qOwYULOPuPs:00124](https://www.youtube.com/watch?v=qOwYULOPuPs&t=312): In short, they were asking far too much.
  Context: compressed_evaluation; attribution: not separately adjudicated. The preceding account lists proposed terms and effects on industries; a two-part evaluation compresses that account before the narrative resumes. The political evaluation's truth is not assessed.

Counterexamples retained:

- `3AIoHLr8nTI:00003`: The speaker moves from graduates' potential to responsibility and then announces today's topic. This is an opening inference/agenda, not a summary of a developed account. 'Therefore' alone does not support the label.

Limit: A transition word such as 'therefore' can introduce a consequence without closing the speech.

Visual evidence status: Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.

Required next test: Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.

## Candidates not admitted

Exclusion is retained rather than silently dropping a failed candidate. Existing reviewed examples remain in the delivery report and annotation ledger.

- `definition`: fewer than five supported examples; support rate below 0.70; supported/reviewed = 4/9.
- `question`: support rate below 0.70; supported/reviewed = 7/12.

This edition evaluates the seven practice-guidance candidates listed by the builder, not every speech-function label in the corpus.
