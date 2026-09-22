#!/usr/bin/env python3
"""Build the single operational manifest for the next external review run."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "research/external-review-gate-index.json"
OUT_JSON = ROOT / "research/external-review-launch-manifest.json"
OUT_MD = ROOT / "writeups/external-review-launch-manifest.md"

def main() -> int:
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    by_id = {gate["gate_id"]: gate for gate in gates["gates"]}
    operations = [
        {"order": 1, "id": "priority_pattern_review", "purpose": "Label-blinded first review across all 55 recovered presentation-pattern candidates.", "items": 162, "form": "writeups/recovered-pattern-priority-review.html", "reviewer_pack": "deliverables/recovered-pattern-priority-reviewer-pack.zip", "validator": "scripts/validate_recovered_pattern_priority_review_export.py", "comparison": "scripts/compare_recovered_pattern_priority_reviews.py", "adjudication": "scripts/build_recovered_pattern_priority_adjudication.py", "status": "ready_no_human_records", "depends_on": []},
        {"order": 2, "id": "vertical_slice_evidence_review", "purpose": "Review the five lesson-facing jobs and their evidence, limits, safety and function claims.", "items": 50, "form": "writeups/vertical-slice-01-independent-review-workbook.html", "validator": "scripts/validate_vertical_slice_review_record.py", "comparison": "scripts/compare_vertical_slice_reviews.py", "adjudication": None, "status": "ready_no_human_records", "depends_on": ["priority_pattern_review"]},
        {"order": 3, "id": "identity_function_recurrence", "purpose": "Verify source identity, speech-function labels, exact forms and event-level recurrence.", "items": by_id.get("identity", {}).get("item_count", 395) + by_id.get("function", {}).get("item_count", 187) + by_id.get("phrase_forms", {}).get("item_count", 50) + by_id.get("recurrence", {}).get("item_count", 192), "form": "writeups/corpus-identity-review-workbook.html; writeups/corpus-function-independent-review-workbook.html; writeups/corpus-phrase-form-independent-review-workbook.html; writeups/corpus-recurrence-independent-review-workbook.html", "validator": "scripts/validate_corpus_identity_review.py; scripts/validate_corpus_function_review.py; scripts/validate_corpus_phrase_form_review.py; scripts/validate_corpus_recurrence_review.py", "comparison": "scripts/compare_corpus_identity_reviews.py; scripts/compare_corpus_function_reviews.py; scripts/compare_corpus_phrase_form_reviews.py; scripts/compare_corpus_recurrence_reviews.py", "adjudication": None, "status": "ready_no_human_records", "depends_on": ["priority_pattern_review"]},
        {"order": 4, "id": "delivery_and_multimodal", "purpose": "Record manual vocal, visual, setting, editing and accessibility observations, preserving missingness.", "items": by_id.get("delivery", {}).get("item_count", 36) + by_id.get("multimodal", {}).get("item_count", 21), "form": "writeups/communication-job-delivery-sampling.html; writeups/multimodal-independent-review-workbook.html", "validator": "scripts/validate_communication_job_delivery_review.py; scripts/validate_multimodal_independent_review.py", "comparison": "scripts/compare_communication_job_delivery_reviews.py; scripts/compare_multimodal_independent_reviews.py", "adjudication": None, "status": "ready_manual_review_pending", "depends_on": ["vertical_slice_evidence_review"]},
        {"order": 5, "id": "counterexamples", "purpose": "Complete absence, alternate-function, confound, misuse and safety checks for the 18 jobs.", "items": by_id.get("counterexamples", {}).get("item_count", 90), "form": "writeups/communication-job-counterexample-workbook.html", "validator": "scripts/validate_communication_job_counterexample_review.py", "comparison": None, "adjudication": None, "status": "ready_no_human_records", "depends_on": ["vertical_slice_evidence_review"]},
        {"order": 6, "id": "learner_teachability", "purpose": "Run consented recognition, explanation, transfer and misuse-detection tasks.", "items": by_id.get("learner", {}).get("item_count", 72), "form": "writeups/communication-job-learner-check.html", "validator": "scripts/validate_communication_job_learner_record.py", "comparison": None, "adjudication": None, "status": "protocol_ready_no_participant_records", "depends_on": ["vertical_slice_evidence_review"]},
        {"order": 7, "id": "listener_stimulus_review", "purpose": "Review and lock matched listener stimuli before any outcome study.", "items": by_id.get("listener_stimuli", {}).get("item_count", 18), "form": "writeups/communication-job-listener-stimulus-review-workbook.html", "validator": "scripts/validate_listener_stimulus_review.py", "comparison": "scripts/compare_listener_stimulus_reviews.py", "adjudication": "scripts/validate_listener_stimulus_adjudication.py", "status": "ready_no_human_records", "depends_on": ["vertical_slice_evidence_review"]},
        {"order": 8, "id": "listener_outcomes", "purpose": "Run a blinded listener protocol only after stimuli are locked.", "items": by_id.get("listener_outcomes", {}).get("item_count", 18), "form": "writeups/communication-job-listener-record.html", "validator": "scripts/validate_communication_job_listener_record.py", "comparison": None, "adjudication": None, "status": "blocked_until_stimuli_locked", "depends_on": ["listener_stimulus_review"]},
    ]
    manifest = {"schema_version": "1.0", "manifest_id": "external-review-launch-manifest", "status": "operations_ready_no_human_records_received", "first_action": "priority_pattern_review", "operations": operations, "promotion_ready_cards": 0, "claim_boundary": "This manifest routes external review and participant operations. It contains no reviewer, learner, listener or effectiveness records and cannot promote a pattern by itself."}
    OUT_JSON.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    lines = ["# External Review Launch Manifest", "", "Status: **operations ready; no human records received**.", "", "Start with operation 1. Give reviewers the form and instructions, never the private pattern key. Preserve each export separately, validate it, compare independent exports where available, and adjudicate disagreements without silently editing decisions.", "", "| Order | Operation | Items | Status | Depends on | Reviewer pack | Validator |", "|---:|---|---:|---|---|---|---|"]
    for op in operations:
        lines.append(f"| {op['order']} | `{op['id']}` | {op['items']} | `{op['status']}` | {', '.join(op['depends_on']) or '—'} | `{op.get('reviewer_pack', '—')}` | `{op['validator']}` |")
    lines += ["", "Promotion-ready cards remain **0/18**. Synthetic browser smoke and repository validators verify the instruments, not the people or outcomes they are designed to collect.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": str(OUT_MD.relative_to(ROOT)), "operation_count": len(operations), "status": manifest["status"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
