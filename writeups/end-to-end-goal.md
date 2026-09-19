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
