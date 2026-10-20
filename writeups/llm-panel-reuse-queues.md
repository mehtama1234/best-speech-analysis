# Reusable LLM-panel queues

These are evidence packets prepared for the same two-model, four-rubric review used in the five-job vertical slice. Source identity and internal labels are held in separate keys. A panel result reviews supplied evidence; it does not prove audience response, learning, transfer, or effectiveness.

| Queue | Packets | Ready to run | Held before model review | What blocks promotion |
|---|---:|---:|---:|---|
| Fieldbook | 55 | 55 | 0 | Evidence-linked counterexamples are absent. |
| Humor/TED expansion | 19 | 17 | 2 | Two items need five distinct contextual excerpts; all items still need counterexamples. |

## What is ready now

- All 55 fieldbook cards have five retained-caption excerpts, a bounded lesson, a media caveat, and a private packet key. They may be run to identify wording and evidence problems, but lack controls and therefore cannot be promoted.
- Seventeen of 19 humor/TED candidates have five bounded transcript excerpts and can enter the panel. Two are explicitly held until more distinct source context is retrieved.
- The runner accepts any blinded packet set: `python3 scripts/run_llm_panel.py --packets research/<packet-set>.json --output research/<results>.json`.

## Decision rule

Each packet receives source/context, counterexample/scope, lesson-transfer/safety, and adversarial reviews from two local models. Any disagreement, indeterminate answer, absent citation, malformed output, or explicit evidence gap produces `model_panel_revision_or_more_evidence_needed`. No automated result is treated as an effectiveness claim.
