# LLM panel review — five-job vertical slice

Status: **complete; every job requires revision or more evidence**.

Model-panel judgments assess supplied text, controls and lesson wording. They are not human review, learner evidence, listener evidence, or proof of effectiveness.

Two local models made **40** rubric judgments: **10** support, **6** revise, and **24** indeterminate.

A noncommittal model response is not counted as agreement. Because every packet has disagreement or an indeterminate pass, every decision fails closed.

| Job packet | Result | Why |
|---|---|---|
| `provisional-contrast_or_disagreement` | `model_panel_revision_or_more_evidence_needed` | Model disagreement; one or more judgments lacked an evidence citation. source_context: indeterminate / support, counterexample_scope: indeterminate / revise, lesson_transfer_safety: indeterminate / support, adversarial: indeterminate / indeterminate. |
| `provisional-example` | `model_panel_revision_or_more_evidence_needed` | Model disagreement; one or more judgments lacked an evidence citation. source_context: indeterminate / support, counterexample_scope: indeterminate / revise, lesson_transfer_safety: indeterminate / support, adversarial: indeterminate / revise. |
| `provisional-story_or_personal_experience` | `model_panel_revision_or_more_evidence_needed` | Model disagreement; one or more judgments lacked an evidence citation. source_context: indeterminate / support, counterexample_scope: indeterminate / revise, lesson_transfer_safety: indeterminate / support, adversarial: indeterminate / indeterminate. |
| `provisional-uncertainty_or_qualification` | `model_panel_revision_or_more_evidence_needed` | Model disagreement; one or more judgments lacked an evidence citation. source_context: indeterminate / support, counterexample_scope: indeterminate / revise, lesson_transfer_safety: indeterminate / support, adversarial: indeterminate / indeterminate. |
| `provisional-conclusion_or_summary` | `model_panel_revision_or_more_evidence_needed` | Model disagreement; one or more judgments lacked an evidence citation. source_context: indeterminate / support, counterexample_scope: indeterminate / revise, lesson_transfer_safety: indeterminate / support, adversarial: indeterminate / indeterminate. |

## What this changes

- These five lessons now have a reproducible LLM-panel record instead of an empty human-review queue.
- The panel supports focused revision: strengthen counterexample handling first, then rerun with models that can produce an unambiguous cited decision.
- No result claims learner success, listener comprehension, persuasion, or effectiveness.

## Reuse

The packet protocol is portable: supply five representative excerpts, controls, a bounded lesson, a separate key, and the same four rubrics. Apply it next to the 55 fixed-corpus patterns and 19 expansion candidates; do not merge their evidence counts.
