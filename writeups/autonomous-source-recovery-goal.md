# Next autonomous goal: close the fixed-inventory recovery boundary

This is the next workstream that can proceed without independent reviewers or
participants. It improves corpus completeness and provenance; it does **not**
promote recovered material into canonical semantic evidence.

## Objective

Give every one of the 480 inventory videos an explicit, auditable recovery
disposition:

1. canonical full-context review;
2. direct recovered media/transcript candidate;
3. alternate-source candidate with identity and alignment status;
4. externally hosted transcript or source lead; or
5. unresolved, with the search attempts and reason recorded.

The target is not to force 480 positive matches. The target is zero silent
gaps and a reproducible explanation for every unresolved item.

## Current checkpoint

- Inventory: **480** videos.
- Canonical full-context reviews: **395**.
- Unresolved after media recovery: **14**.
- Alternate-source machine-transcript candidates: **11**.
- External transcript candidates: **1**.
- External source leads without a canonical transcript: **2**.
- Latest unresolved-source search: **58 leads**, all still unverified.

The 11 alternate-source transcripts and the external transcript remain
separate evidence layers. Their text can support retrieval triage, but not
identity, recurrence, rhetorical interpretation or effectiveness claims.

## Execution sequence

1. Re-run `scripts/search_unresolved_source_candidates.py` and preserve the
   dated result.
2. Download only selected alternate candidates with
   `scripts/download_alternate_source_candidates.py`.
3. Transcribe them with `scripts/transcribe_alternate_source_candidates.py`.
4. Build the identity queue with
   `scripts/build_alternate_source_identity_review.py`.
5. Run transcript-quality and pattern-candidate builders while preserving the
   `alternate_source` and `external_transcript` layer labels.
6. Rebuild `research/corpus-coverage-audit.json` and
   `writeups/corpus-coverage-audit.md`.
7. Leave unresolved rows unresolved when provenance or content cannot be
   established. Do not infer identity from title similarity alone.

## Definition of done

- Every inventory ID appears in exactly one disposition layer or an explicit
  unresolved queue.
- No alternate or external row is counted as canonical review evidence.
- Each recovered row has source URL, provenance, transcript status and
  missingness fields.
- Every unresolved row has a recorded search result or a documented reason
  search cannot establish a source.
- Coverage and full-inventory pattern reports reconcile to the same 480 IDs.
- Existing public-claim, reproducibility and release audits still pass.

## Boundary

This goal closes source accounting and retrieval coverage. It does not replace
the independent identity/function/review gates, and it cannot make the five-job
curriculum promotion-ready without human evidence.
