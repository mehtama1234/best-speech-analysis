# End-to-end goal: a trustworthy speech-learning system

## Objective

For the single consolidated version of the project goal, see the [master
speech-learning system](master-speech-learning-system.md).

Turn the fixed speech corpus into a usable, evidence-bounded learning system
that helps a learner choose a communication job, understand the words and
speech structure that may serve it, inspect relevant vocal and nonverbal
delivery, rehearse an adapted version, receive a listener-based check, and
revise without copying a speaker's identity or treating popularity as proof.

The system must preserve the difference between:

1. what a transcript contains;
2. what recurs across independently identified sources;
3. what delivery looks or sounds like in available media;
4. what is a plausible mechanism or teaching hypothesis; and
5. what learners and listeners actually do or understand.

No later layer may silently promote an earlier layer. Missing, ambiguous,
edited, inaccessible or unverifiable evidence must remain visible.

## Required end state

For every promoted communication job, the repository must contain a linked
evidence chain:

1. **Source and identity** — speaker, event, upload correspondence,
   duplication risk and source restrictions independently reviewed.
2. **Full-context language** — retained captions reread in order, exact
   timestamped examples, neighboring context and recognition-error boundary.
3. **Function and structure** — an independently checked description of what
   the words are doing, including alternate functions and indeterminate cases.
4. **Phrase and recurrence evidence** — exact word forms, event-level and
   holdout recurrence, with compilation/duplicate risks adjudicated.
5. **Delivery evidence** — manually reviewed vocal timing/prosody proxies,
   visible action, setting, editing, music, speaker visibility and accessibility
   limits; independent multimodal review must agree or preserve disagreement.
6. **Mechanism hypothesis** — a falsifiable explanation of why the pattern
   might help, separated from the transcript observation.
7. **Counterexamples and limits** — absence, failure, alternate-function,
   confound and misuse checks, including a safe `no_candidate_found` outcome.
8. **Practice lesson** — a problem statement, adaptable form, exact examples,
   non-fit warning, self-check, accessibility options and anti-imitation guard.
9. **Learner evidence** — consented, pseudonymous records showing whether a
   learner can recognize, explain, transfer, reject a non-fit use and revise;
   facilitator scoring and uncertainty must be retained.
10. **Listener evidence** — independently reviewed, locked matched stimuli and
    blinded listener tasks for comprehension/recall; listener outcomes remain
    separate from learner satisfaction and original speech effectiveness.
11. **Promotion decision** — explicit status, unresolved disagreements,
    missingness, safety review and claim boundary; no card becomes a “best
    practice” merely because its files or tests exist.
12. **Reproducibility** — source IDs, evidence IDs, generated artifacts,
    validators, manifests and the exact commands needed to regenerate them.

## Operational sequence

```text
395-source transcript corpus
        ↓
context evidence → function/phrase candidates → identity + recurrence review
        ↓
delivery sampling → manual multimodal review → independent adjudication
        ↓
counterexamples + mechanism hypothesis → provisional lesson
        ↓
learner teachability run → locked listener stimuli → blinded listener run
        ↓
promotion audit → published lesson with claims, limits and provenance
```

The first execution target is a five-job vertical slice. Only after its gates
are met should the workflow expand to the remaining 13 jobs and then be
repeated across the full corpus.

## Definition of done

The overall project is complete only when the acceptance matrix has no open
requirements, every promoted job has the evidence chain above, all exports pass
their validators, disagreements have adjudication records, and the final
dashboard distinguishes:

- transcript coverage from audiovisual coverage;
- internal observations from independent observations;
- practice logs from learner-validation evidence; and
- listener comprehension outcomes from claims about real-world speaking
  effectiveness.

Passing tests and generated workbooks are necessary infrastructure, not human
evidence. If the required independent reviewers, learners or listeners have
not completed their records, the project remains incomplete.

## Current checkpoint

## Latest implementation update — exhaustive pattern-to-presentation path

The fixed transcript corpus has now been mined into an additional source-linked
pattern layer: 22 broad candidate themes, 18 structural relation architectures,
15 unmatched-label clusters, and 33 expanded candidate cards. The
[exhaustive pattern inventory](exhaustive-pattern-inventory.md) preserves the
395-review scope, 50,380 episode records, 33,330 relation records, exact
evidence IDs and linked writeups. A local Qwen model screened the 33 candidates
using retained caption excerpts; its shortlist prioritizes scope repair and
analogy transfer while forcing promotion to remain false.

The [compound pattern bundle report](compound-pattern-bundles.md) retains 136
recurring pairings among those candidate leads and foregrounds the top 24 for
practice. Each pairing appears in at least three distinct full-context reviews
and retains source evidence for practice design; co-occurrence is kept separate
from an ordered or effective recipe claim. The [compound-pattern browser](compound-pattern-bundles.html)
turns each pairing into a local two-move draft with retained source excerpts,
source-linked JSON export and Markdown rehearsal output. The exported compound
record has a validator for bundle lineage, evidence IDs, reflections, timestamp
and the non-effectiveness boundary.
The triad layer retains 160 recurring three-move candidates under the same
boundary, with 24 foregrounded for practice. The [triad practice browser](compound-pattern-triads.html)
creates a three-move scaffold, stores listener/uncertainty/non-fit/revision
reflections, and exports records checked by
`scripts/validate_compound_triad_practice_record.py`.

The [expanded practice browser](expanded-pattern-candidate-cards.html) turns
those cards into a local drafting workflow. It supports six sequence presets,
outline generation, listener restatement and non-fit reflection, local
save/reload, Markdown export, and a separate expanded-pattern JSON practice
record. The record validator checks selected pattern IDs, source evidence links,
timestamps and the non-effectiveness boundary. These records are local practice
artifacts, not learner-validation or listener-outcome evidence.

The [presentation sequence library](presentation-sequence-library.md) combines
the candidate cards into complete architectures for explanation, proposals,
incident reports, room leadership, hard questions and story-led talks. Each
architecture now also carries sentence-level drafting stems, listener checks
and boundary checks; the browser inserts those scaffolds into a draft when a
sequence preset is selected and creates a separate response field for every
move. Those per-step responses persist through local save/reload and enter the
practice JSON alongside the outline. The local draft judge can screen a
completed worksheet for visible sequence moves, boundary checks and
listener-checkability while retaining a non-effectiveness boundary. The
authoritative release receipt currently reports 14/14 core release steps,
17/17 full-test release steps, 27/27 aggregate checks and 15/15 browser paths.
The current reproducibility manifest contains 361 artifacts. The latest full
test release receipt and focused checks pass; the audit records the exact test
and browser receipts. A manifest-freshness coupling remains an explicit
maintenance concern because tests regenerate authoritative artifacts; rebuilding
the manifest and rerunning the targeted check is part of the release path. The
independent identity, function, recurrence, delivery, counterexample, learner
and listener gates remain open as required by the definition of done.

The fixed transcript layer is complete: 395 reviews and 102,816 inspected
captions. The repository has 18 provisional communication-job cards, 4,016
function cards, 2,800 structural cards, 50 exact phrase-form hypotheses and
learner surfaces for all 395 videos. The video itinerary separates 207
canonical-job lessons, 31 structural-bridge lessons and 157
transcript-exploration leads; every “what to notice” note records whether it
comes from a canonical card, structural card or corpus relation. The
per-video media audit reports 354 raw A/V learner-route videos, 357 linked
feature reports and 364 total proxy reports, including 7 proxy records without
a retained itinerary entry. The [all-video delivery inspection queue](full-corpus-delivery-inspection.html)
routes 354 raw-media cases, 5 proxy-only cases and 36 locally unavailable
cases for a manual pass. The [395-item delivery review workbook](full-corpus-delivery-review-workbook.html)
provides the observation fields and JSON export; it is blank until a reviewer
completes it. These are availability and measurement records, not manual
nonverbal findings.

The remaining work is human evidence: independent source/function/recurrence/
delivery/counterexample review, learner records, stimulus locking and blinded
listener records. No job is promotion-ready yet.

The operational next step is the [next validation runbook](next-validation-runbook.md),
starting with the five-job vertical slice and its reviewer handoff.
