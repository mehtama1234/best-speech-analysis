# Model-assisted gate judge

Status: **model_assisted_readiness_complete_human_evidence_open**.

This model-assisted judgment evaluates instrument readiness and current status metadata. It is not an independent human review, learner observation, listener outcome, causal result or promotion decision.

Instrument-ready gates: **10/10**; human gates closed: **0/10**; open requirements: **9**.

| Gate | Instrument | Human gate | Judgment | Next action |
|---|---|---|---|---|
| `identity` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review all 395 queue items; do not treat title matches as proof of distinct events. |
| `function` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 187 candidate function items in full context. |
| `recurrence` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 192 train/holdout phrase candidates; preserve indeterminate decisions. |
| `phrase_forms` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review all 50 retrieved forms before changing the inventory. |
| `multimodal` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 21 bounded internal media observations; proxies are not meaning or outcomes. |
| `delivery` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 36 queued samples; record missingness and identity limits. |
| `counterexamples` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 90 slots; no candidate is preferable to a forced example. |
| `learner` | `True` | `False` | `instrument_ready_human_evidence_missing` | Run the consented 18-job learner protocol; do not call it effectiveness evidence. |
| `listener_stimuli` | `True` | `False` | `instrument_ready_human_evidence_missing` | Review 18 matched pairs for equivalence, accessibility, safety and blinding before locking. |
| `listener_outcomes` | `True` | `False` | `instrument_ready_human_evidence_missing` | Run only after stimuli are independently reviewed and locked. |
