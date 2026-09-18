# Vertical slice 02 candidate plan

The slice is registered in [research/vertical-slice-02.json](../research/vertical-slice-02.json)
with an explicit candidate-only status and source hashes.

The first slice turns five higher-level jobs into runnable provisional lessons.
The next candidate slice should test three additional jobs already represented
in the context-reviewed corpus: questions, definitions/reformulations and calls
to action.

| Candidate | Candidate evidence | Current media status | What must be distinguished |
|---|---|---|---|
| Question | `-54zUwySKCg:00122`, `2fWJh-_UG5s:00005`, `AwA0Jnfj3ao:00003` | 3/3 raw audio/video | Inquiry, rhetorical question, interview transition and pressure |
| Definition/reformulation | `_Mb1-CN3wZs:00048`, `-6qN3bm2RYo:00068`, `fBnAMUkNM2k:00374` | 2/3 raw audio/video | Dictionary definition, translation, reformulation and example |
| Call to action | `2fWJh-_UG5s:00401`, `-6qN3bm2RYo:00276`, `-6qN3bm2RYo:00343` | 3/3 raw audio/video | Feasible action, institutional aspiration, coercion and promotion |

These are candidate packets, not additional validated best practices. Each
needs surrounding context, source/event verification, delivery observations,
counterexamples, accessibility and safety boundaries, independent review and a
learner check before promotion.

The question candidate now has a [draft packet](../research/vertical-slice-02-question-draft.json)
and [draft lesson](vertical-slice-02-lesson-question-draft.md). The definition
candidate has a [draft packet](../research/vertical-slice-02-definition-draft.json)
and [draft lesson](vertical-slice-02-lesson-definition-draft.md). The call-to-action
candidate has a [draft packet](../research/vertical-slice-02-call-to-action-draft.json)
and [draft lesson](vertical-slice-02-lesson-call-to-action-draft.md). None are
part of the five-pattern promotion gate.

The draft integrity check is:

```text
python3 scripts/validate_vertical_slice_02_drafts.py
```
