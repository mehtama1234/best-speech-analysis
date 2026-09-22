# Recovered pattern lexical-rule audit

The 55 recovered-pattern rules produced a density audit; **1** rows are flagged for broad lexical retrieval density.

Every row remains a contextual-review candidate. Hit counts do not measure semantic correctness or pattern quality.

| Pattern | Total hits | Risk flags |
|---|---:|---|
| `audience_invitation_and_next_turn` | 379 | human_context_review_required, high_candidate_video_coverage |
| `future_hope_and_action` | 545 | human_context_review_required, high_candidate_video_coverage |
| `story_memory_and_scene` | 292 | human_context_review_required, high_candidate_video_coverage |
| `analogy_metaphor_and_callback` | 32 | human_context_review_required |
| `contrast_and_reversal` | 791 | human_context_review_required, broad_lexical_retrieval_density, high_candidate_video_coverage |
| `scale_shift` | 190 | human_context_review_required, high_candidate_video_coverage |
| `qualification_and_boundary` | 48 | human_context_review_required |
| `credit_and_collective_agency` | 270 | human_context_review_required, high_candidate_video_coverage |
| `choice_and_responsibility` | 130 | human_context_review_required |
| `metrics_and_revaluation` | 288 | human_context_review_required, high_candidate_video_coverage |
| `question_and_reframe` | 145 | human_context_review_required |
| `objection_and_response` | 104 | human_context_review_required |
| `orientation_and_roadmap` | 74 | human_context_review_required |
| `identity_status_and_belonging` | 245 | human_context_review_required, high_candidate_video_coverage |
| `value_and_moral_frame` | 205 | human_context_review_required, high_candidate_video_coverage |
| `definition_and_explanation` | 93 | human_context_review_required, high_candidate_video_coverage |
| `risk_safety_and_limit` | 100 | human_context_review_required, high_candidate_video_coverage |
| `cause_and_mechanism` | 1081 | human_context_review_required, high_candidate_video_coverage |
| `institution_system_and_policy` | 183 | human_context_review_required |
| `repair_and_self_correction` | 82 | human_context_review_required |
| `grief_loss_and_continuation` | 86 | human_context_review_required, high_candidate_video_coverage |
| `humor_rapport_and_self_undercut` | 42 | human_context_review_required, high_candidate_video_coverage |
| `premise_correction` | 206 | human_context_review_required |
| `scope_repair` | 44 | human_context_review_required |
| `analogy_transfer` | 89 | human_context_review_required, high_candidate_video_coverage |
| `evidence_gap` | 210 | human_context_review_required, high_candidate_video_coverage |
| `expectation_reversal` | 275 | human_context_review_required, high_candidate_video_coverage |
| `register_shift` | 144 | human_context_review_required, high_candidate_video_coverage |
| `audience_shift` | 832 | human_context_review_required, high_candidate_video_coverage |
| `credit_redirection` | 637 | human_context_review_required, high_candidate_video_coverage |
| `hands_off` | 245 | human_context_review_required, high_candidate_video_coverage |
| `reciprocal_learning` | 292 | human_context_review_required, high_candidate_video_coverage |
| `self_undercut` | 82 | human_context_review_required |
| `despair_to_hope` | 497 | human_context_review_required, high_candidate_video_coverage |
| `metric_revaluation` | 358 | human_context_review_required, high_candidate_video_coverage |
| `moral_to_memorial` | 167 | human_context_review_required, high_candidate_video_coverage |
| `optional_support` | 242 | human_context_review_required, high_candidate_video_coverage |
| `question_redefinition` | 153 | human_context_review_required, high_candidate_video_coverage |
| `sorrow_and_continuation` | 387 | human_context_review_required, high_candidate_video_coverage |
| `story_to_thesis` | 301 | human_context_review_required, high_candidate_video_coverage |
| `purpose_attention_example` | 25 | human_context_review_required |
| `recognition_to_specific_credit` | 24 | human_context_review_required |
| `unfinished_work_to_commitment` | 136 | human_context_review_required |
| `familiarity_to_scope` | 17 | human_context_review_required |
| `unity_across_scale` | 218 | human_context_review_required |
| `authority_to_service` | 76 | human_context_review_required |
| `difficulty_to_capability` | 3 | human_context_review_required |
| `invitation_to_low_barrier_entry` | 37 | human_context_review_required |
| `access_obstacle_to_support` | 137 | human_context_review_required |
| `technical_explanation_and_interruption` | 2 | human_context_review_required |
| `emotion_to_composure` | 75 | human_context_review_required |
| `selection_and_incentive` | 30 | human_context_review_required |
| `failure_to_reframe` | 17 | human_context_review_required |
| `authenticity_vs_performance` | 14 | human_context_review_required, high_candidate_video_coverage |
| `craft_process_over_outcome` | 39 | human_context_review_required, high_candidate_video_coverage |

## Boundary

This audit measures lexical retrieval density only. A hit is not a semantic match, a speech function, a recurrence finding, a source identity decision, or evidence of effectiveness. Every card remains a contextual-review candidate.

```bash
python3 scripts/build_recovered_pattern_rule_audit.py
```
