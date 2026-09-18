# Vertical slice 01: acceptance matrix

This matrix is the handoff truth for the five-pattern curriculum. A green
entry means the repository has direct evidence for that gate; it does not mean
the patterns are universally effective. A pending entry requires evidence that
cannot be created by the original analyst without compromising independence or
consent.

| Gate | Current evidence | Status | What would change it |
|---|---|---|---|
| Complete transcript corpus | 395 videos, 102,816 captions, 395 full-context reviews; `research/full-context-reviews.json` | Complete for transcript/content scope | Nothing for this fixed queue; audiovisual scope is separate |
| Exact language and speech forms | Five packets with timestamped context, representative examples, counterexamples and linked lessons | Provisional complete | Independent review may revise labels or examples |
| Corpus-wide pattern inventory | `research/reviewed-delivery-patterns.json`: 87 contextually reviewed annotations, 60 supported label decisions and 36 feature-backed records | Legacy/contextual, not independent validation | Reassess labels, expand audiovisual coverage and select additional validated slices |
| Fine-grained label recurrence | The 87 annotations contain 59 legacy reviewed-function labels; only `rhetorical_question` repeats under the exact label across 2 videos, while the other labels are one-video observations | Recurrence not established at fine-label level | Test recurrence using the five higher-level clusters and event-level holdouts |
| Mechanism hypotheses | Each packet states a communication job and bounded practice hypothesis | Provisional complete | Outcome evidence would be needed for causal claims |
| Audio/video acquisition | `research/vertical-slice-01-media-audit.json`: 15/16 raw IDs, 16/16 feature IDs, zero ledger contradictions | Measured partial | Recover or replace unavailable `S43F1BZfQKY` |
| Human-readable audiovisual alignment | `research/vertical-slice-01-manual-multimodal-review.json`: 13 sampled intervals across all five jobs, including counterexamples and cutaways | Internal, not independent | Independent reviewer must inspect the 50-item packet |
| Cross-speaker/event recurrence | [Cluster recurrence report](vertical-slice-01-cluster-recurrence.md): 25 representatives across 13 IDs; all 50 packet roles span 16 IDs, with raw-media denominators and counterexample counts | Provisional | Verify speaker/event independence and preserve holdout analysis |
| Failure, non-fit and safety limits | Packet counterexamples, alternate-function controls, accessibility/privacy warnings and practice boundaries | Provisional complete | Reviewer may add or reject limits |
| Practice lessons | Five linked lesson drafts, shared practice flows, self-checks, non-fit checks and listener checks | Runnable draft | Revise after learner failures |
| Independent review | 50-item browser workbook and review-record validator | Pending; no external record | One or more independent validated exports |
| Learner teachability | Fixed 20-task bank, consent-aware learner instrument and scorer | Pending; protocol not run | Consented learner records and rubric results |
| Browser delivery | Lesson-index and five-section learner-check Playwright smoke test passes with required browser libraries | Verified runnable | Keep passing after UI changes |
| Promotion decision | `research/vertical-slice-01-validation-audit.json` reports `0/5` packets ready | Not promoted | All required review and learner gates must pass |
| Next pattern expansion | [Vertical slice 02 candidate plan](vertical-slice-02-candidate-plan.md) now has draft packets and lessons for questions, definitions/reformulations and calls to action | Drafts only | Independently review and learner-test new packets after slice 01 review |

## Required evidence chain

The intended chain is:

```text
communication problem
  -> exact language / speech form
  -> delivery and setting observations
  -> mechanism hypothesis
  -> recurrence across speakers or events
  -> counterexamples and limits
  -> practice task
  -> learner check
  -> revision or cautious promotion
```

The current repository reaches the practice-task node and has runnable
instruments for the final two nodes. It does not yet contain independent-review
judgments or learner observations, so it must remain provisional.

## Verification commands

```text
python3 scripts/validate_vertical_slice.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_vertical_slice_lesson_browser.py
```

The browser command requires a runnable Chromium and its shared libraries. Its
failure in a base environment missing `libnspr4.so` is an environment issue;
the same smoke test passes when those libraries are supplied in user space.
