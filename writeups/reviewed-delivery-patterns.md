# Reviewed delivery patterns

Rate-quality screening excludes caption durations below a provisional 0.25-second floor; raw features remain unchanged. This does not validate speech timing. See timing-quality-audit.md.

Review provenance: legacy reviewer identity is unknown. Contextual per-label overrides are assistant transcript-only judgments, not independent human review. See research/contextual-label-reviews.json for rubric, context IDs and hashes.

This report groups only transcript-reviewed, supported transcript functions. It is an evidence index, not a test that any delivery pattern causes comprehension, persuasion, or effectiveness. The pitch field is a coarse spectral proxy; transcript gaps and words/second are alignment proxies.

Reviewed annotations: **87**; supported annotations used in summaries: **60**; feature records available: **36**.

## Summary

| Reviewed function | Examples | Videos | Uploaders | RMS dB | Pitch proxy Hz | Words/second | Gap before s |
|---|---:|---:|---:|---:|---:|---:|---:|
| `audience_or_interlocutor_question` | 1 | 1 | 1 | -37.087 | 291.667 | 0.575 | 0.0 |
| `audience_practice_call` | 1 | 1 | 1 | -21.292 | 101.562 | 0.694 | 0.0 |
| `audience_question_or_rhetorical_question` | 1 | 1 | 1 | -43.174 | 244.792 | 2.174 | 0.0 |
| `childhood_story_setup` | 1 | 1 | 1 | -22.605 | 333.984 | 1.324 | 0.0 |
| `civic_collective_call` | 1 | 1 | 1 | -20.969 | 246.652 | 0.46 | 0.0 |
| `collective_appeal` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `compressed_evaluation` | 1 | 1 | 1 | -20.84 | 177.455 | 1.235 | 0.0 |
| `conceptual_reframing` | 1 | 1 | 1 | -19.159 | 303.267 | 1.667 | 2.64 |
| `concession_and_correction` | 1 | 1 | 1 | -15.293 | 205.357 | 1.006 | 0.0 |
| `conclusion_marker` | 1 | 1 | 1 | -15.764 | 222.656 | 0.615 | 0.0 |
| `conclusion_or_charge` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `definition_or_reformulation` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `dramatic_story_transition` | 1 | 1 | 1 | -32.28 | 290.365 | 1.477 | 0.0 |
| `encouraging_continuation` | 1 | 1 | 1 | -31.259 | 139.509 | 0.949 | 0.0 |
| `epistemic_hedge` | 1 | 1 | 1 | -18.437 | 278.125 | 1.786 | 5.28 |
| `evidence_based_contrast` | 1 | 1 | 1 | -15.454 | 253.348 | 0.88 | 0.0 |
| `example_introduction` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `example_marker` | 1 | 1 | 1 | -15.101 | 260.045 | 0.949 | 0.0 |
| `existential_observation` | 1 | 1 | 1 | -38.193 | 184.896 | 1.667 | 0.0 |
| `explicit_rejection` | 1 | 1 | 1 | -18.776 | 236.979 | 1.695 | 0.0 |
| `explicit_uncertainty` | 1 | 1 | 1 | -27.822 | 268.75 | 1.626 | 0.0 |
| `family_story_dialogue` | 1 | 1 | 1 | -42.935 | 238.281 | 1.429 | 0.0 |
| `hedged_recommendation` | 1 | 1 | 1 | -23.957 | 270.833 | 1.75 | 0.72 |
| `hesitation_and_repair` | 1 | 1 | 1 | -20.801 | 273.437 | 1.359 | 0.239 |
| `historical_example_setup` | 1 | 1 | 1 | -13.916 | 239.063 | 1.524 | 0.0 |
| `hypothetical_visualization` | 1 | 1 | 1 | -15.29 | 263.672 | 2.133 | 0.0 |
| `imagined_future_example` | 1 | 1 | 1 | -18.499 | 247.768 | 1.014 | 0.12 |
| `institutional_call_to_action` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `institutional_example_introduction` | 1 | 1 | 1 | -14.027 | 206.25 | 1.724 | 0.0 |
| `interview_opening_question` | 1 | 1 | 1 | -24.741 | 369.792 | 2.615 | 0.0 |
| `named_example_list` | 1 | 1 | 1 | -23.931 | 225.586 | 0.911 | 0.0 |
| `narrative_correction` | 1 | 1 | 1 | -21.64 | 189.063 | 2.433 | 0.0 |
| `normative_rejection` | 1 | 1 | 1 | -18.045 | 350.447 | 2.239 | 0.0 |
| `opposition_framing` | 1 | 1 | 1 | -33.639 | 234.375 | 9.0 | 0.0 |
| `personal_emotional_story` | 1 | 1 | 1 | -20.469 | 190.104 | 2.787 | 0.0 |
| `personal_rejection_story` | 1 | 1 | 1 | -22.085 | 313.802 | 1.585 | 0.0 |
| `personal_story_dialogue` | 1 | 1 | 1 | -33.165 | 262.5 | 3.598 | 0.0 |
| `personal_story_setup` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `personal_story_transition` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `policy_call_to_action` | 1 | 1 | 1 | -28.763 | 315.104 | 1.471 | 0.0 |
| `qualification_or_contrast` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `qualified_generalization` | 1 | 1 | 1 | -16.421 | 309.896 | 1.339 | 0.0 |
| `qualified_judgment` | 1 | 1 | 1 | -17.383 | 266.741 | 1.755 | 0.0 |
| `qualified_prediction` | 1 | 1 | 1 | -19.983 | 225.447 | 1.332 | 0.0 |
| `qualified_recommendation` | 1 | 1 | 1 | -25.918 | 198.661 | 1.667 | 0.0 |
| `rhetorical_question` | 2 | 2 | 1 | -18.445 | 201.563 | 0.915 | 0.72 |
| `rhetorical_question_with_answer` | 1 | 1 | 1 | -19.441 | 245.739 | 0.869 | 0.0 |
| `self_correction_qualification` | 1 | 1 | 1 | -29.39 | 316.964 | 1.582 | 0.0 |
| `self_question_sequence` | 1 | 1 | 1 | -17.273 | 222.656 | 2.502 | 0.0 |
| `speculative_empathy` | 1 | 1 | 1 | -20.493 | 293.75 | 0.833 | 0.0 |
| `statistical_example_introduction` | 1 | 1 | 1 | -18.201 | 238.281 | 1.679 | 0.0 |
| `story_action` | 1 | 1 | 1 | -20.403 | 179.688 | 0.525 | 0.0 |
| `story_event_with_embedded_advice` | 1 | 1 | 1 | -39.485 | 173.828 | 0.844 | 0.0 |
| `story_recall` | 1 | 1 | 1 | -24.076 | 210.938 | 2.127 | 0.0 |
| `summary_principle` | 1 | 1 | 1 | -18.007 | 229.167 | 2.713 | 0.0 |
| `summary_transition` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |
| `term_definition` | 1 | 1 | 1 | -18.325 | 295.313 | 1.456 | 0.0 |
| `translation_definition` | 1 | 1 | 1 | -33.206 | 296.875 | 2.586 | 0.0 |
| `urgent_collective_call` | 1 | 1 | 1 | n/a | n/a | n/a | n/a |

## Evidence by function

### `audience_or_interlocutor_question`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aHXxveJTJoE:00039](https://www.youtube.com/watch?v=aHXxveJTJoE&t=112): it with?; RMS dB=-37.087, pitch proxy Hz=291.667, words/second proxy=0.575, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `question`: interlocutor_question_spanning_captions; attribution: not separately adjudicated. The target 'it with?' completes a question beginning in captions 37–38 about whom Hopper would share restaurants with; subsequent questions address Doc and friends. This supports a question spanning caption boundaries. Transcript text alone does not settle speaker turns, interruption or whether this is spontaneous conversation.

### `audience_practice_call`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [jxY2-YgAgm0:00125](https://www.youtube.com/watch?v=jxY2-YgAgm0&t=370): Let's speak English; RMS dB=-21.292, pitch proxy Hz=101.562, words/second proxy=0.694, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `call_to_action`: promotional_outro_practice_invitation; attribution: promotional_outro_text_not_featured_speaker_verified. The speech closes with thanks at caption 115; captions 116–126 promote a language-learning community, resources and classes. The target invites English practice in that promotional passage. It supports a call to action in the upload, but must not be attributed to the featured speech's speaker without further evidence.

### `audience_question_or_rhetorical_question`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [m92yvNscIAo:00004](https://www.youtube.com/watch?v=m92yvNscIAo&t=10): hours now how many different ways do you; RMS dB=-43.174, pitch proxy Hz=244.792, words/second proxy=2.174, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `question`: question_form_challenge_to_repetition; attribution: not separately adjudicated. The question begins in the target and continues through captions 5–6, asking how many ways the same story must be told after three and a half hours. This is a challenge about repetition, not simply an audience-orientation prompt. Speaker identity, turn boundaries and vocal affect are not established by this window.

### `childhood_story_setup`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [pmAL79dnvu0:00042](https://www.youtube.com/watch?v=pmAL79dnvu0&t=136): kindness and of hope when I was a little; RMS dB=-22.605, pitch proxy Hz=333.984, words/second proxy=1.324, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: brief_autobiographical_habit_recollection; attribution: not separately adjudicated. The national-story metaphor transitions into the speaker's stated childhood practice of pledging allegiance and its personal significance. This supports a brief autobiographical recollection under the broad personal-experience label, not a complete story arc or evidence of audience effect.

### `civic_collective_call`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [pmAL79dnvu0:00116](https://www.youtube.com/watch?v=pmAL79dnvu0&t=393): bigger we must; RMS dB=-20.969, pitch proxy Hz=246.652, words/second proxy=0.46, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `call_to_action`: civic_participation_appeal_spanning_captions; attribution: current_speech_text. The target ends with 'we must' and the next caption supplies 'vote' and a request for participation. Together they form a collective civic action appeal. The short target is part of the same clause, not labelled merely because a separate request is nearby. No electoral effect or audience compliance is established.

### `collective_appeal`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-6qN3bm2RYo:00343](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=988): let let us strive to return to the; no aligned feature values.
  Contextual `call_to_action`: closing_collective_aspiration; attribution: current_speech_text. The target begins a collective appeal continued by peace, progress and prosperity in the following captions, then thanks the audience. It supports a broad closing aspiration, not a detailed executable instruction or measured audience response.

### `compressed_evaluation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [qOwYULOPuPs:00124](https://www.youtube.com/watch?v=qOwYULOPuPs&t=312): In short, they were asking far too much; RMS dB=-20.84, pitch proxy Hz=177.455, words/second proxy=1.235, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `conclusion_or_summary`: compressed_evaluation; attribution: not separately adjudicated. The preceding account lists proposed terms and effects on industries; a two-part evaluation compresses that account before the narrative resumes. The political evaluation's truth is not assessed.

### `conceptual_reframing`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [3AIoHLr8nTI:00046](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=421): Think about it: Saying “I tolerate you” actually means something like, “Ok, I grudgingly admit that; RMS dB=-19.159, pitch proxy Hz=303.267, words/second proxy=1.667, gap before seconds=2.64, gap after seconds=0.0.
  Contextual `definition`: pragmatic_paraphrase; attribution: not separately adjudicated. The speaker supplies an imagined paraphrase of 'I tolerate you' and contrasts tolerance with acceptance. It explains the intended pragmatic meaning, not a universally valid lexical definition.

### `concession_and_correction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [OfwfTN1mEyM:00139](https://www.youtube.com/watch?v=OfwfTN1mEyM&t=368): often not quite understood but but the; RMS dB=-15.293, pitch proxy Hz=205.357, words/second proxy=1.006, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: public_perception_versus_claimed_analysis; attribution: current_turn_argument. The speaker contrasts limited public understanding of available solar power with a claim that its mathematics is clear, followed by a recommendation. The textual opposition is present; neither the mathematics nor public understanding is independently evaluated.

### `conclusion_marker`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aXmM0VZv810:00483](https://www.youtube.com/watch?v=aXmM0VZv810&t=1175): overwhelmingly what matters; RMS dB=-15.764, pitch proxy Hz=222.656, words/second proxy=0.615, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `conclusion_or_summary`: local_argumentative_conclusion; attribution: not separately adjudicated. The preceding energy-use criterion leads to a prioritizing conclusion that space matters. It is a local argumentative takeaway, not a speech-ending summary. Additional support follows; garbled scientific wording is not repaired or fact-checked here.

### `conclusion_or_charge`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-54zUwySKCg:00196](https://www.youtube.com/watch?v=-54zUwySKCg&t=989): The point is your generation is charged withthis task of breaking through what the body; no aligned feature values.
  Contextual `conclusion_or_summary`: broad_takeaway_and_charge; attribution: not separately adjudicated. Several possible ways to make a difference precede a general charge to the generation to change political conditions. This is a broad takeaway tied to those examples, not merely an isolated 'point' marker. Full speech closure is not established.

### `definition_or_reformulation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-6qN3bm2RYo:00068](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=190): mindset externally this means reformed; no aligned feature values.
  Contextual `definition`: operational_reformulation; attribution: not separately adjudicated. The surrounding phrase is liberation from a colonial mindset; the next captions unpack its external content as reformed multilateralism and contemporary global governance. This supports operational reformulation, not a dictionary definition. The boundary with policy implication is interpretive; confidence is moderate.

### `dramatic_story_transition`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [fBnAMUkNM2k:00021](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=198): And those incidents are so strong that theychange your DNA.; RMS dB=-32.28, pitch proxy Hz=290.365, words/second proxy=1.477, gap before seconds=0.0, gap after seconds=0.0.

### `encouraging_continuation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [qOwYULOPuPs:00348](https://www.youtube.com/watch?v=qOwYULOPuPs&t=902): just getting started. Let's keep going.; RMS dB=-31.259, pitch proxy Hz=139.509, words/second proxy=0.949, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `call_to_action`: closing_continuation_encouragement; attribution: current_speech_text. The target links an assertion of progress to encouragement to continue, then thanks the audience before a resource promotion begins. It is a broad continuation appeal with no operationally specified task; garbled earlier wording is not repaired or used to identify the speaker.

### `epistemic_hedge`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [3AIoHLr8nTI:00008](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=91): This group is truly diverse in every possible way. And I think that is an extraordinarily; RMS dB=-18.437, pitch proxy Hz=278.125, words/second proxy=1.786, gap before seconds=5.28, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: opinion_framed_evaluation; attribution: current_turn_text. After describing the group's diversity, 'I think' introduces an evaluation of its value. This marks the evaluation as a view; it does not establish weak conviction or internal uncertainty.

### `evidence_based_contrast`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [qOwYULOPuPs:00075](https://www.youtube.com/watch?v=qOwYULOPuPs&t=185): Canada grew stronger. Instead of; RMS dB=-15.454, pitch proxy Hz=253.348, words/second proxy=0.88, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: expected_versus_asserted_outcome; attribution: current_turn_argument. The passage contrasts the claimed intention to create dependence with an asserted opposite outcome, then contrasts dependence with diversified relationships. It is an asserted policy-outcome contrast, not verified causal evidence.

### `example_introduction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-6qN3bm2RYo:00079](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=221): together on global issues such as; no aligned feature values.
  Contextual `example`: category_enumeration; attribution: not separately adjudicated. Global issues are unpacked into terrorism, pandemics and the environment after a statement about unity. These are category members, not detailed empirical cases or evidence that the policy succeeds.

### `example_marker`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aXmM0VZv810:00274](https://www.youtube.com/watch?v=aXmM0VZv810&t=673): this earlier radiology for example has; RMS dB=-15.101, pitch proxy Hz=260.045, words/second proxy=0.949, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: asserted_domain_case_with_explanation; attribution: not separately adjudicated. The speaker introduces radiology as a case for a claim about technology and work, contrasts a forecast with an asserted employment trend, then explains a goal-versus-task distinction. The extended context establishes the illustration; the medical/employment assertions are not independently validated.

### `existential_observation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [gDadfh0ZdBM:00036](https://www.youtube.com/watch?v=gDadfh0ZdBM&t=133): that there's something wrong with the; RMS dB=-38.193, pitch proxy Hz=184.896, words/second proxy=1.667, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: explanation_versus_felt_presence_in_dialogue; attribution: scene_dialogue_text. The captions oppose inability to explain/identify something with feeling or sensing its presence. This supports contextual contrast under the broad label, though not interpersonal disagreement. Adjacent stored intervals overlap and do not support the legacy ten-second-gap rationale; audio silence is not inferred from captions.

### `explicit_rejection`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [jxY2-YgAgm0:00008](https://www.youtube.com/watch?v=jxY2-YgAgm0&t=24): I do not object to their ignorance, but; RMS dB=-18.776, pitch proxy Hz=236.979, words/second proxy=1.695, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: contrastive_reformulation_of_rejection; attribution: current_turn_argument. The construction contrasts not objecting to one alleged quality with rejecting alleged attempts to damage reputation. The alternative objects of rejection establish contrast. The allegations are not verified or endorsed.

### `explicit_uncertainty`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [r2kP2Pqdx6w:00014](https://www.youtube.com/watch?v=r2kP2Pqdx6w&t=47): yeah might might end up being true you; RMS dB=-27.822, pitch proxy Hz=268.75, words/second proxy=1.626, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: qualified_possibility_in_exchange; attribution: turn_attribution_unresolved. The exchange about an alternative expansion of AI is followed by 'might end up being true' and 'you never know'. Possibility is textually qualified, but captions do not reliably assign this response to a speaker or establish whether it is humorous.

### `family_story_dialogue`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [fBnAMUkNM2k:00104](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=574): My mother said to me that this two sell-pass.; RMS dB=-42.935, pitch proxy Hz=238.281, words/second proxy=1.429, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: family_dialogue_in_personal_recollection; attribution: not separately adjudicated. The narrator introduces the mother's words during a recalled difficult period and describes their significance in that account. The garbled phrase 'this two sell-pass' is preserved, not silently reconstructed. Reported spiritual/health implications are not independently endorsed.

### `hedged_recommendation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [3AIoHLr8nTI:00074](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=665): from their leaders today and tomorrow? Now, I think you need to be brave.; RMS dB=-23.957, pitch proxy Hz=270.833, words/second proxy=1.75, gap before seconds=0.72, gap after seconds=1.04.
  Contextual `uncertainty_or_qualification`: opinion_framed_advice_with_reinforcement; attribution: current_turn_text. A question about leadership is answered with 'I think you need to be brave', followed by 'Really brave'. The viewpoint marker coexists with textually reinforced advice; it does not prove hesitation.

### `hesitation_and_repair`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [2fWJh-_UG5s:00035](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=94): my uh wife and i; RMS dB=-20.801, pitch proxy Hz=273.437, words/second proxy=1.359, gap before seconds=0.239, gap after seconds=0.0.

### `historical_example_setup`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [qOwYULOPuPs:00040](https://www.youtube.com/watch?v=qOwYULOPuPs&t=97): knew that agreements such as; RMS dB=-13.916, pitch proxy Hz=239.063, words/second proxy=1.524, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: historical_case_in_limitation_argument; attribution: not separately adjudicated. Confederation is presented as one agreement in an argument that agreements alone could do only so much, followed by the claimed need for a corridor. This identifies rhetorical case use, not validation of historical or causal claims.

### `hypothetical_visualization`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aXmM0VZv810:00529](https://www.youtube.com/watch?v=aXmM0VZv810&t=1274): >> Just imagine how tiny that little; RMS dB=-15.29, pitch proxy Hz=263.672, words/second proxy=2.133, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: scale_visualization_of_existing_object; attribution: not separately adjudicated. A discussion of rack weight and cooling is followed by an invitation to imagine the small computational object. This is concrete scale illustration of an existing referent, not necessarily a new hypothetical event. Speaker turns are not reliably attributed by captions.

### `imagined_future_example`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [pmAL79dnvu0:00083](https://www.youtube.com/watch?v=pmAL79dnvu0&t=281): here imagine our daughters growing up; RMS dB=-18.499, pitch proxy Hz=247.768, words/second proxy=1.014, gap before seconds=0.12, gap after seconds=0.0.
  Contextual `example`: imagined_future_scenario; attribution: not separately adjudicated. A broad vision about a world without limitations is made concrete through daughters growing up with possibilities and then grandmothers' imagined responses. It is an aspirational scenario, not an observed event or measured audience effect.

### `institutional_call_to_action`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-6qN3bm2RYo:00276](https://www.youtube.com/watch?v=-6qN3bm2RYo&t=792): we need to create a global architecture; no aligned feature values.
  Contextual `call_to_action`: institutional_collective_proposal; attribution: current_speech_text. A present invitation to member states precedes the target proposal for a global architecture, which continues through captions 277–280. This is a collective policy appeal, not a completed institutional action or independently endorsed policy.

### `institutional_example_introduction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [qOwYULOPuPs:00221](https://www.youtube.com/watch?v=qOwYULOPuPs&t=576): the many. For example, in July of this; RMS dB=-14.027, pitch proxy Hz=206.25, words/second proxy=1.724, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: named_institutional_case; attribution: not separately adjudicated. A general contrast between deals and agreements is illustrated by an announced company contract; the passage returns to a claim about why companies can reach agreements. The case's occurrence, name spelling and claimed benefits are not independently verified.

### `interview_opening_question`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [AwA0Jnfj3ao:00003](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=23): Why don't we start right at the beginning?; RMS dB=-24.741, pitch proxy Hz=369.792, words/second proxy=2.615, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `question`: interviewer_narrative_prompt; attribution: not separately adjudicated. The transcript explicitly labels an interviewer who proposes starting at the beginning, followed by a Sachin Tendulkar-labeled answer recalling school cricket. The question prompts a narrative answer; it is not a monologue technique used by the interviewee.

### `named_example_list`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [jxY2-YgAgm0:00087](https://www.youtube.com/watch?v=jxY2-YgAgm0&t=258): such as Daily Beast, James Carville, and; RMS dB=-23.931, pitch proxy Hz=225.586, words/second proxy=0.911, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: named_instances_of_asserted_category; attribution: not separately adjudicated. The speaker names entities after asserting a category of people/companies that retracted statements. The local list instantiates that asserted category. This review does not endorse allegations, legal characterizations or claims about the named parties.

### `narrative_correction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [AwA0Jnfj3ao:00125](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=580): But and I said, oh, this is a wrong place.; RMS dB=-21.64, pitch proxy Hz=189.063, words/second proxy=2.433, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: observed_versus_expected_position_in_story; attribution: current_turn_narrative. The surrounding narrative contrasts seeing the ball with reacting too late and where it was versus where it should be. The wording is somewhat garbled; the target's 'wrong place' belongs to that narrative contrast, not a live dispute.

### `normative_rejection`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [3AIoHLr8nTI:00097](https://www.youtube.com/watch?v=3AIoHLr8nTI&t=845): genital mutilation is wrong, no matter how many generations have practiced it.; RMS dB=-18.045, pitch proxy Hz=350.447, words/second proxy=2.239, gap before seconds=0.0, gap after seconds=2.08.
  Contextual `contrast_or_disagreement`: normative_rejection_of_justification; attribution: current_turn_argument. The passage rejects a practice despite its historical prevalence after distinguishing understanding from moral relativism. It opposes a possible justification; no actual exchange with a disputant is observed in these captions.

### `opposition_framing`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [fBnAMUkNM2k:00278](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=1328): and there will be you to proving them wrong.; RMS dB=-33.639, pitch proxy Hz=234.375, words/second proxy=9.0, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: opposition_and_response_in_reported_advice; attribution: reported_mother_text. The surrounding clauses explicitly attribute the contrast between critics and proving them wrong to the narrator's mother. It is reported motivational advice, not an observed argument with those critics or proof of the narrator's own current stance.

### `personal_emotional_story`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [AwA0Jnfj3ao:00130](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=598): I went to the bathroom and I cried.; RMS dB=-20.469, pitch proxy Hz=190.104, words/second proxy=2.787, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: setback_action_and_self_address; attribution: not separately adjudicated. Following a cricket setback, the narrator describes going to a bathroom, crying and speaking to himself in a mirror, before later seeking advice. Those are narrated actions, not acoustic or visual evidence of emotion during the current speech.

### `personal_rejection_story`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [9fEurt2OZ0I:00008](https://www.youtube.com/watch?v=9fEurt2OZ0I&t=31): I went for a police they said no you're; RMS dB=-22.085, pitch proxy Hz=313.802, words/second proxy=1.585, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: sequence_of_personal_rejection_accounts; attribution: not separately adjudicated. The narrator links job applications, a reported rejection and another application example. Despite garbled wording, personal actions and responses form a sequence. Counts, job names and outcomes are not independently fact-checked.

### `personal_story_dialogue`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [fBnAMUkNM2k:00072](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=462): One day the doctor came to me, and he said,well I heard that you want to be an artist,; RMS dB=-33.165, pitch proxy Hz=262.5, words/second proxy=3.598, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: personal_event_with_attributed_dialogue; attribution: not separately adjudicated. The account places a doctor's visit within a hospital period and quotes what the doctor reportedly said. It is an event with attributed dialogue; the quoted prognosis is not validated medical guidance or an observation of present health.

### `personal_story_setup`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-54zUwySKCg:00035](https://www.youtube.com/watch?v=-54zUwySKCg&t=201): That was when I was 16 years old in Nashville,Tennessee, and you had the requirement of; no aligned feature values.
  Contextual `story_or_personal_experience`: autobiographical_scene_setup; attribution: not separately adjudicated. The narrator names a career origin, a contest, an age and a place, then introduces its question-and-answer sequence. The target sets up a personal event; this short window does not contain the full story or verify its historical truth.

### `personal_story_transition`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-54zUwySKCg:00059](https://www.youtube.com/watch?v=-54zUwySKCg&t=305): But a few years ago I decided, as you willat some point, that it was time to recalculate,; no aligned feature values.
  Contextual `contrast_or_disagreement`: see review reason; attribution: not separately adjudicated. The preceding captions describe sustained success and comfort; 'But' introduces a decision to change direction. This supports contrast, not interpersonal disagreement.
  Contextual `story_or_personal_experience`: see review reason; attribution: not separately adjudicated. A first-person decision anchored a few years earlier is followed by ending the show and launching a network. The inspected sequence supports a personal-story transition.

### `policy_call_to_action`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [2fWJh-_UG5s:00401](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=954): we need to save for schools; RMS dB=-28.763, pitch proxy Hz=315.104, words/second proxy=1.471, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `call_to_action`: policy_necessity_sequence_with_transcript_uncertainty; attribution: current_speech_text. Repeated 'we need to' constructions list proposed public actions. The target's 'save for schools' wording is unclear and remains unrepaired; the surrounding sequence supports the action-appeal function but not a precise reconstruction of that proposal.

### `qualification_or_contrast`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-54zUwySKCg:00028](https://www.youtube.com/watch?v=-54zUwySKCg&t=173): But then I realized that you don’t haveto necessarily go to Harvard to have a driven; no aligned feature values.
  Contextual `contrast_or_disagreement`: personal_reconsideration; attribution: current_turn_narrative. The speaker first describes pressure about addressing Harvard graduates, then revises the premise that attendance is necessary for a particular disposition. This is a personal reconsideration. The self-description is reported wording, not a personality assessment by this project.

### `qualified_generalization`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aXmM0VZv810:00350](https://www.youtube.com/watch?v=aXmM0VZv810&t=858): pools. So I think with every; RMS dB=-16.421, pitch proxy Hz=309.896, words/second proxy=1.339, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: opinion_framed_generalization; attribution: current_turn_text. After discussing research and AI, 'I think' introduces a broad claim that humanity will always shift to new value pools. The view marker coexists with 'always'; the generalization's truth and the speaker's certainty are not assessed.

### `qualified_judgment`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [lcj1wMZRitI:00095](https://www.youtube.com/watch?v=lcj1wMZRitI&t=337): not a judge or jury but I can tell you; RMS dB=-17.383, pitch proxy Hz=266.741, words/second proxy=1.755, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `contrast_or_disagreement`: authority_disclaimer_versus_committed_statement; attribution: scene_or_speech_turn_text. The speaker disclaims being a judge or jury, then asserts a character's refusal to betray others and labels it integrity. That contrast in authority and commitment is textual; it does not establish the actor's traits or a verified real-world assessment.

### `qualified_prediction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [OfwfTN1mEyM:00041](https://www.youtube.com/watch?v=OfwfTN1mEyM&t=98): be great for the world and I think we're; RMS dB=-19.983, pitch proxy Hz=225.447, words/second proxy=1.332, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: conditional_and_opinion_framed_prediction; attribution: current_turn_text. The preceding conditional excludes complacency or entitlement, and 'I think' introduces an optimistic forecast. It qualifies the prediction as a viewpoint under a stated condition, not as an objectively validated forecast.

### `qualified_recommendation`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [9fEurt2OZ0I:00020](https://www.youtube.com/watch?v=9fEurt2OZ0I&t=66): sorry now I think we have to get used to; RMS dB=-25.918, pitch proxy Hz=198.661, words/second proxy=1.667, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: opinion_framed_recommendation; attribution: current_turn_text. Following repeated rejection in the account, 'I think' frames the recommendation to get used to rejection. 'Have to' still expresses necessity. No softness of vocal delivery is inferred.

### `rhetorical_question`

Reviewed supported examples: **2** across **2** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-54zUwySKCg:00122](https://www.youtube.com/watch?v=-54zUwySKCg&t=613): girl with a bucket and big heart could dothat, I wonder what I could do?; no aligned feature values.
  Contextual `question`: see review reason; attribution: not separately adjudicated. The narrator reports asking what she could do, then describes asking viewers to collect change. This is a narrated self-question, not an observed audience exchange.
  Contextual `uncertainty_or_qualification`: see review reason; attribution: not separately adjudicated. Under the claim-qualification definition, 'could' describes hypothetical capacity inside a narrated question. No factual assertion or prediction is explicitly hedged in this context. A broader wondering category could differ; no internal uncertainty is inferred.
- [2fWJh-_UG5s:00005](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=12): how about that; RMS dB=-18.445, pitch proxy Hz=201.563, words/second proxy=0.915, gap before seconds=0.72, gap after seconds=0.0.
  Contextual `question`: interrogative_form_reaction; attribution: not separately adjudicated. The short 'how about that' follows a reference to children being killed and precedes a greeting. It supports a question-form reaction, not an information request or evidence of audience participation; neither tone nor the reported event is independently verified.

### `rhetorical_question_with_answer`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [hZ0YhrgYejI:00001](https://www.youtube.com/watch?v=hZ0YhrgYejI&t=16): So, what do you do when you fall down?; RMS dB=-19.441, pitch proxy Hz=245.739, words/second proxy=0.869, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `question`: question_followed_by_transcribed_answer; attribution: not separately adjudicated. The target asks what to do after falling; the next caption supplies 'Get back up', then the passage qualifies that advice by describing difficulty doing so. The transcript supports question-answer structure, but lacks turn labels proving who supplied the answer or whether an audience answered.

### `self_correction_qualification`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [C8-twwwTETE:00045](https://www.youtube.com/watch?v=C8-twwwTETE&t=98): how into him I was right but I think I; RMS dB=-29.39, pitch proxy Hz=316.964, words/second proxy=1.582, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: qualified_retrospective_self_evaluation; attribution: current_turn_text. The narrator describes talking at length to someone, then uses 'I think' and 'might have probably' to evaluate whether it was excessive. The continuation is needed to complete the clause; this is not an acoustic uncertainty judgment.

### `self_question_sequence`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [S43F1BZfQKY:00049](https://www.youtube.com/watch?v=S43F1BZfQKY&t=262): Am I Indian?; RMS dB=-17.273, pitch proxy Hz=222.656, words/second proxy=2.502, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `question`: narrated_identity_self_question_sequence; attribution: not separately adjudicated. The target is an explicit first-person question among questions about appearance, identity and fitting in. The narrator presents self-questioning as part of a personal account. This does not establish current internal state or an audience question.

### `speculative_empathy`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [2fWJh-_UG5s:00160](https://www.youtube.com/watch?v=2fWJh-_UG5s&t=362): maybe that would make; RMS dB=-20.493, pitch proxy Hz=293.75, words/second proxy=0.833, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `uncertainty_or_qualification`: reported_hypothetical_consequence; attribution: reported_other_people_text. The surrounding clauses say Ryan and Jessica said sharing the art might have a hoped-for consequence. The qualification is in reported speech, not evidence of the narrator's own belief strength. No afterlife or emotional-response claim is validated.

### `statistical_example_introduction`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [aXmM0VZv810:00596](https://www.youtube.com/watch?v=aXmM0VZv810&t=1418): some over 20 years. Let me give you one; RMS dB=-18.201, pitch proxy Hz=238.281, words/second proxy=1.679, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `example`: quantitative_before_after_case; attribution: not separately adjudicated. A claim about movement toward accelerated computing is followed by a top-500-supercomputer percentage comparison and a return to the transition claim. The transcript gives both 'less than 15%' and '10%' for the later CPU share; these must not be silently reconciled. The numerical claim is not fact-checked.

### `story_action`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [S43F1BZfQKY:00036](https://www.youtube.com/watch?v=S43F1BZfQKY&t=197): So, I went for it and f*cking shaved my head.; RMS dB=-20.403, pitch proxy Hz=179.688, words/second proxy=0.525, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: decision_and_action_with_reported_aftermath; attribution: not separately adjudicated. The preceding self-question leads to the narrator's stated action of shaving the head, followed by reported messages and encounters. This is a narrative event/aftermath sequence; other people's attributed descriptions are not this project's trait judgments.

### `story_event_with_embedded_advice`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [S43F1BZfQKY:00011](https://www.youtube.com/watch?v=S43F1BZfQKY&t=65): Then one day, my boyfriend turns to me andsays maybe you should get a wig.; RMS dB=-39.485, pitch proxy Hz=173.828, words/second proxy=0.844, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `call_to_action`: see review reason; attribution: not separately adjudicated. The recommendation is attributed to the boyfriend within a past event. It is not a request for the current audience to act.
  Contextual `story_or_personal_experience`: see review reason; attribution: not separately adjudicated. The narrator describes a sequence of hair loss, a boyfriend's suggestion, crying that night and visiting a shop two weeks later. The target is an event within that personal story.

### `story_recall`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [S43F1BZfQKY:00002](https://www.youtube.com/watch?v=S43F1BZfQKY&t=29): I remember that day.; RMS dB=-24.076, pitch proxy Hz=210.938, words/second proxy=2.127, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `story_or_personal_experience`: dated_recollection_with_trigger_event; attribution: not separately adjudicated. The remembered date is followed by a first-person shower episode and discovery of hair in the hand. Context supplies an actual narrated event rather than merely the marker 'I remember'. The report does not independently verify the medical history.

### `summary_principle`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [AwA0Jnfj3ao:00234](https://www.youtube.com/watch?v=AwA0Jnfj3ao&t=1016): So, it's just, in short, it's just being astep ahead of your opposition.; RMS dB=-18.007, pitch proxy Hz=229.167, words/second proxy=2.713, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `conclusion_or_summary`: story_to_principle; attribution: not separately adjudicated. The preceding cricket sequence describes anticipating an opponent and warning a teammate. The target states the general lesson of being a step ahead, followed by interviewer thanks. This supports a story-to-principle summary, not proof the strategy is universally useful.

### `summary_transition`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-URn1fARvts:00119](https://www.youtube.com/watch?v=-URn1fARvts&t=254): In short, being a young person balancing; no aligned feature values.
  Contextual `conclusion_or_summary`: autobiographical_summary; attribution: not separately adjudicated. The earlier captions describe combining skills, asking hard questions and willingness to learn; the following complete sentence compresses school and sport into critical curiosity and learning about the world. Some transcript phrasing remains uncertain.

### `term_definition`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [_Mb1-CN3wZs:00048](https://www.youtube.com/watch?v=_Mb1-CN3wZs&t=136): Pitchfork means an assassin or something; RMS dB=-18.325, pitch proxy Hz=295.313, words/second proxy=1.456, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `definition`: lexical_gloss_in_dialogue; attribution: not separately adjudicated. The transcript explicitly offers a meaning for a code word, with an approximation marker. This supports a lexical-gloss act within dialogue, not factual correctness of the gloss or its suitability as a public-speaking technique.

### `translation_definition`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [fBnAMUkNM2k:00374](https://www.youtube.com/watch?v=fBnAMUkNM2k&t=1581): Bijli means electricity.; RMS dB=-33.206, pitch proxy Hz=296.875, words/second proxy=2.586, gap before seconds=0.0, gap after seconds=0.0.
  Contextual `definition`: translation_gloss; attribution: not separately adjudicated. The name Bijli is followed by an explicit translation as electricity, then dialogue about the name. The translation act is present in the text; linguistic accuracy is not independently checked.

### `urgent_collective_call`

Reviewed supported examples: **1** across **1** videos and **1** uploaders. Uploader identity is not treated as speaker identity.

- [-HA8kSdsf_M:00079](https://www.youtube.com/watch?v=-HA8kSdsf_M&t=217): enslave the people now let us fight to; no aligned feature values.
  Contextual `call_to_action`: repeated_collective_appeal; attribution: performed_address_text_identity_unverified. The target pivots from a description of dictators to repeated appeals to fulfill a promise, free the world and unite. The expanded window completes the appeal. This identifies rhetorical structure in the transcript, not literal combat instructions, historical truth, spontaneous delivery or audience effect.

## Aggregate by candidate label

These aggregates combine supported reviewed examples that share a retrieval label, even when their more specific reviewed functions differ.

| Candidate label | Examples | Videos | Uploaders | RMS dB | Pitch proxy Hz | Words/second | Gap before s |
|---|---:|---:|---:|---:|---:|---:|---:|
| `call_to_action` | 7 | 6 | 2 | -25.57075 | 200.70675 | 0.8935 | 0.0 |
| `conclusion_or_summary` | 5 | 5 | 1 | -18.20367 | 209.75933 | 1.521 | 0.0 |
| `contrast_or_disagreement` | 10 | 9 | 3 | -22.30288 | 240.15075 | 2.58438 | 0.0 |
| `definition` | 4 | 4 | 2 | -23.56333 | 298.485 | 1.903 | 0.88 |
| `example` | 8 | 5 | 1 | -16.995 | 240.095 | 1.41914 | 0.01714 |
| `pause_event` | 2 | 2 | 1 | -26.5405 | 281.901 | 1.418 | 0.1195 |
| `question` | 7 | 7 | 3 | -26.6935 | 262.7015 | 1.60833 | 0.12 |
| `story_or_personal_experience` | 10 | 6 | 1 | -28.15288 | 237.89062 | 1.77737 | 0.0 |
| `uncertainty_or_qualification` | 8 | 7 | 1 | -22.80262 | 270.30325 | 1.48937 | 0.75 |
## Counterexample audit

The candidate labels remain imperfect retrieval aids. Unsupported reviewed examples are retained rather than discarded:

| Candidate label | Reviewed | Supported | Unsupported | Support rate |
|---|---:|---:|---:|---:|
| `call_to_action` | 11 | 7 | 4 | 0.636 |
| `conclusion_or_summary` | 6 | 5 | 1 | 0.833 |
| `contrast_or_disagreement` | 10 | 10 | 0 | 1.0 |
| `definition` | 9 | 4 | 5 | 0.444 |
| `example` | 10 | 8 | 2 | 0.8 |
| `pause_event` | 7 | 2 | 5 | 0.286 |
| `question` | 12 | 7 | 5 | 0.583 |
| `story_or_personal_experience` | 13 | 10 | 3 | 0.769 |
| `uncertainty_or_qualification` | 9 | 8 | 1 | 0.889 |
| `unclassified` | 3 | 0 | 3 | 0.0 |

A repeated measurement in this report is evidence that the reviewed examples share an observable property. It is not evidence that the property is universal, speaker-independent, intentional, or effective. General claims require more reviewed examples, explicit counterexamples, and comparisons against same-video baselines and speech-function controls.
