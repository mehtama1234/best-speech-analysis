#!/usr/bin/env python3
"""Build one operational handoff for the remaining human validation gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def main() -> int:
    function = load("research/corpus-function-independent-review-workbook.json")
    recurrence = load("research/corpus-recurrence-independent-review-workbook.json")
    multimodal = load("research/multimodal-independent-review-workbook.json")
    slice_one = load("research/vertical-slice-01-independent-review-workbook.json")
    learner = load("research/shared-learner-check.json")
    listener = load("research/listener-outcome-protocol.json")
    report = {
        "schema_version": "1.0",
        "report_id": "validation-handoff",
        "status": "instruments_ready_no_human_records_received",
        "claim_boundary": "These are operational instruments and instructions, not validation results. No reviewer, learner or listener judgment is included.",
        "review_gates": [
            {"id": "corpus_function", "purpose": "Check heuristic speech-function labels in surrounding transcript context.", "items": function["item_count"], "workbook": "research/corpus-function-independent-review-workbook.json", "form": "writeups/corpus-function-independent-review-workbook.html", "validator": "scripts/validate_corpus_function_review.py", "summarizer": "scripts/summarize_corpus_function_review.py", "independence": function["independence_requirement"], "does_not_establish": ["delivery effectiveness", "speaker intent", "listener outcomes"]},
            {"id": "phrase_recurrence", "purpose": "Check whether phrase-form hits support the proposed function family in context.", "items": recurrence["item_count"], "workbook": "research/corpus-recurrence-independent-review-workbook.json", "form": "writeups/corpus-recurrence-independent-review-workbook.html", "validator": "scripts/validate_corpus_recurrence_review.py", "summarizer": "scripts/summarize_corpus_recurrence_review.py", "independence": recurrence["independence_requirement"], "does_not_establish": ["effectiveness", "causality", "universal recurrence"]},
            {"id": "multimodal", "purpose": "Check transcript alignment, speaker/setting observations, modality limits and safety boundaries.", "items": multimodal["item_count"], "workbook": "research/multimodal-independent-review-workbook.json", "form": "writeups/multimodal-independent-review-workbook.html", "validator": "scripts/validate_multimodal_independent_review.py", "independence": multimodal["independence_requirement"], "does_not_establish": ["emotion", "intent", "audience response", "effectiveness"]},
            {"id": "vertical_slice", "purpose": "Review the five linked lesson packets and their evidence boundaries.", "items": slice_one["item_count"], "workbook": "research/vertical-slice-01-independent-review-workbook.json", "form": "writeups/vertical-slice-01-independent-review-workbook.html", "validator": "scripts/validate_vertical_slice_review_record.py", "independence": slice_one["independence_requirement"], "does_not_establish": ["listener outcomes", "causal communication effects"]},
        ],
        "learning_gates": [
            {"id": "learner_teachability", "purpose": learner["purpose"], "tasks": learner["task_count"], "protocol": "research/shared-learner-check.json", "form": "writeups/shared-learner-check.html", "validator": "scripts/validate_shared_learner_record.py", "status": learner["status"], "does_not_establish": ["original pattern effectiveness", "population learning effects"]},
            {"id": "listener_outcomes", "purpose": listener["purpose"], "tasks": len(listener["listener_tasks"]), "protocol": "research/listener-outcome-protocol.json", "form": "writeups/listener-outcome-record.html", "validator": "scripts/validate_listener_outcome_record.py", "status": listener["status"], "does_not_establish": ["universal effectiveness", "speaker intent"]},
        ],
        "procedure": [
            "Use a reviewer code and record conflicts; do not use the original analyst for an independent judgment.",
            "Inspect full surrounding context and source media where available; use indeterminate when evidence is insufficient.",
            "Export the browser form without hand-editing judgment fields.",
            "Run the named validator before returning the export.",
            "Preserve disagreements; do not silently adjudicate them in the original analysis.",
            "Do not send credentials, raw recordings or identifying participant information through these forms.",
        ],
    }
    (ROOT / "research/validation-handoff.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Validation handoff", "", "Status: **instruments ready; no human records received**.", "", report["claim_boundary"], "", "## Independent review gates", ""]
    for gate in report["review_gates"]:
        lines += [f"### {gate['id']} — {gate['items']} items", "", gate["purpose"], "", f"- Workbook: `{gate['workbook']}`", f"- Browser form: `{gate['form']}`", f"- Validator: `{gate['validator']}`"]
        if gate.get("summarizer"): lines.append(f"- Summarizer: `{gate['summarizer']}`")
        lines += [f"- Independence: {gate['independence']}", f"- Does not establish: {', '.join(gate['does_not_establish'])}", ""]
    lines += ["## Learning and outcome gates", ""]
    for gate in report["learning_gates"]:
        lines += [f"### {gate['id']} — {gate['tasks']} tasks", "", gate["purpose"], "", f"- Protocol: `{gate['protocol']}`", f"- Form: `{gate['form']}`", f"- Validator: `{gate['validator']}`", f"- Status: `{gate['status']}`", f"- Does not establish: {', '.join(gate['does_not_establish'])}", ""]
    lines += ["## Procedure", ""] + [f"{i}. {step}" for i, step in enumerate(report["procedure"], 1)] + ["", "No gate may be marked complete merely because its workbook or form exists.", ""]
    (ROOT / "writeups/validation-handoff.md").write_text("\n".join(lines))
    print(json.dumps({"output": "research/validation-handoff.json", "review_gates": len(report["review_gates"]), "learning_gates": len(report["learning_gates"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
