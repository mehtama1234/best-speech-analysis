# Communication-job delivery — three-frame interval audit

Status: **internal visual navigation audit; independent review pending**.

Three-frame visual sequences distinguish speaker visibility and production/cutaway risk for navigation. They do not establish continuous delivery, gesture meaning, emotion, intent, identity, alignment, effectiveness or listener response.

Intervals: **36** · frames per interval: **3**.

| Sample | Job | Sequence | Speaker visibility | Navigation status |
|---|---|---|---|---|
| `delivery:opening:01` | `opening` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:opening:02` | `opening` | `multi_shot` | `speaker_visible_but_changes` | `limited` |
| `delivery:closing:01` | `closing` | `graphic_or_cutaway` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:closing:02` | `closing` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:question:01` | `question` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:question:02` | `question` | `interview_multi_shot` | `speaker_and_listener_visible` | `limited` |
| `delivery:answer_or_response:01` | `answer_or_response` | `multi_shot` | `speakers_change` | `not_usable_for_continuous_speaker_delivery` |
| `delivery:answer_or_response:02` | `answer_or_response` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:story_or_personal_experience:01` | `story_or_personal_experience` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:story_or_personal_experience:02` | `story_or_personal_experience` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:example_or_case:01` | `example_or_case` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:example_or_case:02` | `example_or_case` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:contrast_or_disagreement:01` | `contrast_or_disagreement` | `stable_scene_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:contrast_or_disagreement:02` | `contrast_or_disagreement` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:correction_or_reframe:01` | `correction_or_reframe` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:correction_or_reframe:02` | `correction_or_reframe` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:repair_or_self_correction:01` | `repair_or_self_correction` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:repair_or_self_correction:02` | `repair_or_self_correction` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:qualification_or_boundary:01` | `qualification_or_boundary` | `graphic_or_cutaway` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:qualification_or_boundary:02` | `qualification_or_boundary` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:definition_or_explanation:01` | `definition_or_explanation` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:definition_or_explanation:02` | `definition_or_explanation` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:transition_or_structure:01` | `transition_or_structure` | `graphic_or_cutaway` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:transition_or_structure:02` | `transition_or_structure` | `scripted_scene_change` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:callback_or_repetition:01` | `callback_or_repetition` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:callback_or_repetition:02` | `callback_or_repetition` | `insert_to_room_cut` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:humor_or_rapport:01` | `humor_or_rapport` | `graphic_or_cutaway` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:humor_or_rapport:02` | `humor_or_rapport` | `stable_speaker_frame` | `speakers_visible_all_three` | `limited` |
| `delivery:credit_or_acknowledgment:01` | `credit_or_acknowledgment` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:credit_or_acknowledgment:02` | `credit_or_acknowledgment` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:call_to_action_or_audience_role:01` | `call_to_action_or_audience_role` | `stable_speaker_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:call_to_action_or_audience_role:02` | `call_to_action_or_audience_role` | `stable_scene_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:persuasion_or_advocacy:01` | `persuasion_or_advocacy` | `audience_to_stage_cut` | `speaker_visibility_changes` | `not_usable_for_continuous_speaker_delivery` |
| `delivery:persuasion_or_advocacy:02` | `persuasion_or_advocacy` | `graphic_or_cutaway` | `speaker_not_visible` | `not_usable_for_speaker_delivery` |
| `delivery:reflection_or_value_frame:01` | `reflection_or_value_frame` | `stable_scene_frame` | `speaker_visible_all_three` | `limited` |
| `delivery:reflection_or_value_frame:02` | `reflection_or_value_frame` | `multi_shot` | `speaker_visibility_changes` | `not_usable_for_continuous_speaker_delivery` |

## What this changes

Stable-speaker rows can be opened for bounded delivery inspection. Graphic, insert, scripted-scene and multi-shot rows must not be used as evidence for a continuous speaker gesture, gaze, pause or vocal pattern. The three-frame audit is internal and non-independent.
