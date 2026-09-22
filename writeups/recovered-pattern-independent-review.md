# Recovered pattern independent-review workbook

Status: **operational packet; no human records received**.

This workbook is an independent review instrument for recovered transcript candidates. It does not establish semantic accuracy, source identity, recurrence, delivery meaning, or effectiveness.

- Blinded review items: **2431**
- Candidate pattern labels are withheld from the packet and retained in the internal key.
- Exact excerpts, source layer, timestamps and source URLs remain visible for review.

## Files

- Packet to send: `research/recovered-pattern-independent-review-workbook.json`
- Internal key: `research/recovered-pattern-independent-review-key.json` (do not send)
- Return records must include reviewer identity, independence attestation, decision, context note, identity/duplication note and uncertainty.

## Decision boundary

A completed review can support or reject a candidate retrieval. It cannot by itself prove cross-speaker recurrence, delivery meaning, learner transfer, listener outcomes or effectiveness.

## Reproducibility

```bash
python3 scripts/build_recovered_pattern_review_workbook.py
```
