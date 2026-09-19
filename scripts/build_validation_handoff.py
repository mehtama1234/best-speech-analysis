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
    slice_one = load("research/vertical-slice-01-independent-review-workbook.json")
    identity = load("research/corpus-identity-review-workbook.json")
    phrase_forms = load("research/corpus-phrase-form-independent-review-workbook.json")
    delivery = load("research/communication-job-delivery-sampling.json")
    counterexamples = load("research/communication-job-counterexample-workbook.json")
    stimulus = load("research/communication-job-listener-stimulus-review-workbook.json")
    learner = load("research/communication-job-learner-check.json")
    listener = load("research/communication-job-listener-outcome-protocol.json")
    multimodal_expansion = load("research/multimodal-independent-review-workbook.json")
    catalog = load("research/corpus-findings-catalog.json")
    delivery_atlas = load("research/delivery-proxy-candidate-atlas.json")
    report = {
        "schema_version": "1.0",
        "report_id": "validation-handoff",
        "status": "instruments_ready_no_human_records_received",
        "claim_boundary": "These are operational instruments and instructions, not validation results. No reviewer, learner or listener judgment is included.",
        "learner_entry": {
            "path": "writeups/learner-7-day-path.md",
            "catalog": "writeups/corpus-findings-catalog.md",
            "videos_with_candidate_practice_job": catalog["coverage"]["videos_with_candidate_practice_job"],
            "videos_without_candidate_practice_job": catalog["coverage"]["videos_without_candidate_practice_job"],
            "note": "Candidate job routing is heuristic discovery support, not validated evidence that a pattern works.",
        },
        "delivery_entry": {
            "markdown": "writeups/delivery-proxy-candidate-atlas.md",
            "browser": "writeups/delivery-proxy-candidate-atlas.html",
            "candidate_record_count": delivery_atlas["counts"]["candidate_record_count"],
            "candidate_video_count": delivery_atlas["counts"]["candidate_video_count"],
            "validator": "scripts/validate_delivery_proxy_local_reviews.py",
            "summarizer": "scripts/summarize_delivery_proxy_local_reviews.py",
            "note": "Proxy-backed clips require human delivery review; measurements are not scores or effectiveness evidence.",
        },
        "review_gates": [
            {"id": "corpus_identity", "purpose": "Verify speaker, event, upload correspondence, source provenance and duplication status before recurrence denominators are used.", "items": identity["item_count"], "workbook": "research/corpus-identity-review-workbook.json", "form": "writeups/corpus-identity-review-workbook.html", "validator": "scripts/validate_corpus_identity_review.py", "summarizer": "scripts/summarize_corpus_identity_reviews.py", "independence": identity["independence_requirement"], "does_not_establish": ["function", "delivery effectiveness", "listener outcomes"]},
            {"id": "corpus_function", "purpose": "Check heuristic speech-function labels in surrounding transcript context.", "items": function["item_count"], "workbook": "research/corpus-function-independent-review-workbook.json", "form": "writeups/corpus-function-independent-review-workbook.html", "validator": "scripts/validate_corpus_function_review.py", "summarizer": "scripts/summarize_corpus_function_review.py", "independence": function["independence_requirement"], "does_not_establish": ["delivery effectiveness", "speaker intent", "listener outcomes"]},
            {"id": "phrase_recurrence", "purpose": "Check whether phrase-form hits support the proposed function family in context.", "items": recurrence["item_count"], "workbook": "research/corpus-recurrence-independent-review-workbook.json", "form": "writeups/corpus-recurrence-independent-review-workbook.html", "validator": "scripts/validate_corpus_recurrence_review.py", "summarizer": "scripts/summarize_corpus_recurrence_review.py", "independence": recurrence["independence_requirement"], "does_not_establish": ["effectiveness", "causality", "universal recurrence"]},
            {"id": "exact_phrase_form", "purpose": "Check retrieved word forms in sampled train/holdout contexts before using exact wording or recurrence counts.", "items": phrase_forms["item_count"], "workbook": "research/corpus-phrase-form-independent-review-workbook.json", "form": "writeups/corpus-phrase-form-independent-review-workbook.html", "validator": "scripts/validate_corpus_phrase_form_review.py", "summarizer": "scripts/summarize_corpus_phrase_form_reviews.py", "independence": phrase_forms["independence_requirement"], "does_not_establish": ["delivery effectiveness", "speaker intent", "listener outcomes", "causality"]},
            {"id": "delivery", "purpose": "Complete manual observations for transcript alignment, vocal timing, visual action, setting, editing, identity and accessibility across the two-sample-per-job queue.", "items": delivery["item_count"], "workbook": "research/communication-job-delivery-sampling.json", "form": "writeups/communication-job-delivery-sampling.html", "validator": "scripts/validate_communication_job_delivery_review.py", "independence": delivery["review_schema"]["independence_note"], "does_not_establish": ["emotion", "intent", "audience response", "effectiveness"]},
            {"id": "counterexamples", "purpose": "Check absence, failure, alternate function, confound/setting and misuse limits for every provisional job.", "items": counterexamples["item_count"], "workbook": "research/communication-job-counterexample-workbook.json", "form": "writeups/communication-job-counterexample-workbook.html", "validator": "scripts/validate_communication_job_counterexample_review.py", "independence": counterexamples["independence_requirement"], "does_not_establish": ["effectiveness", "causality", "universal failure"]},
            {"id": "multimodal", "purpose": "Check transcript alignment, speaker/setting observations, modality limits and safety boundaries.", "items": multimodal_expansion["item_count"], "workbook": "research/multimodal-independent-review-workbook.json", "form": "writeups/multimodal-independent-review-workbook.html", "validator": "scripts/validate_multimodal_independent_review.py", "independence": multimodal_expansion["independence_requirement"], "does_not_establish": ["emotion", "intent", "audience response", "effectiveness"]},
            {"id": "vertical_slice", "purpose": "Review the five linked lesson packets and their evidence boundaries.", "items": slice_one["item_count"], "workbook": "research/vertical-slice-01-independent-review-workbook.json", "form": "writeups/vertical-slice-01-independent-review-workbook.html", "validator": "scripts/validate_vertical_slice_review_record.py", "independence": slice_one["independence_requirement"], "does_not_establish": ["listener outcomes", "causal communication effects"]},
        ],
        "learning_gates": [
            {"id": "listener_stimulus_review", "purpose": "Review proposition equivalence, readability, accessibility, safety and blinding before locking listener pairs; then preserve an explicit adjudicator decision.", "tasks": stimulus["item_count"], "protocol": "research/communication-job-listener-stimuli-draft.json", "form": "writeups/communication-job-listener-stimulus-review-workbook.html", "validator": "scripts/validate_listener_stimulus_review.py", "adjudication_form": "writeups/communication-job-listener-stimulus-adjudication.html", "adjudication_validator": "scripts/validate_listener_stimulus_adjudication.py", "status": stimulus["status"], "does_not_establish": ["listener comprehension", "real-world effectiveness"]},
            {"id": "learner_teachability", "purpose": learner["purpose"], "tasks": learner["task_count"], "protocol": "research/communication-job-learner-check.json", "form": "writeups/communication-job-learner-check.html", "validator": "scripts/validate_communication_job_learner_record.py", "status": learner["status"], "does_not_establish": ["original pattern effectiveness", "population learning effects"]},
            {"id": "listener_outcomes", "purpose": listener["purpose"], "tasks": len(listener["listener_tasks"]), "protocol": "research/communication-job-listener-outcome-protocol.json", "form": "writeups/communication-job-listener-record.html", "validator": "scripts/validate_communication_job_listener_record.py", "status": listener["status"], "does_not_establish": ["universal effectiveness", "speaker intent"]},
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
    entry = report["learner_entry"]
    delivery_entry = report["delivery_entry"]
    learner_path = Path(entry["path"]).name
    catalog_path = Path(entry["catalog"]).name
    delivery_path = Path(delivery_entry["markdown"]).name
    delivery_browser = Path(delivery_entry["browser"]).name
    lines = ["# Validation handoff", "", "Status: **instruments ready; no human records received**.", "", report["claim_boundary"], "", f"Start with the [seven-day learner path]({learner_path}) for practical drills. The [corpus findings catalog]({catalog_path}) currently routes {entry['videos_with_candidate_practice_job']} of 395 videos to one or more provisional practice jobs; {entry['videos_without_candidate_practice_job']} remain explicitly unclassified. This routing is heuristic discovery support, not proof that a pattern works.", "", f"For multimodal review, use the [delivery proxy candidate atlas]({delivery_path}) or its [searchable browser surface]({delivery_browser}): {delivery_entry['candidate_record_count']} transcript-linked clips across {delivery_entry['candidate_video_count']} videos. These are proxy-backed review candidates, not delivery scores or effectiveness evidence. Validate exports with `{delivery_entry['validator']}` and summarize them with `{delivery_entry['summarizer']}`; neither establishes independence.", "", "Before selecting examples, use the [corpus lesson inventory](corpus-lesson-index.html), [exact phrase-form inventory](corpus-phrase-form-inventory.html), [evidence bank](corpus-evidence-bank.html), [provisional cards](communication-job-cards.html), [delivery inventory](communication-job-delivery-inventory.md) and [shared evidence model](shared-evidence-model.md). These are discovery and routing surfaces; none is proof that a pattern works.", "", "## Independent review gates", ""]
    for gate in report["review_gates"]:
        lines += [f"### {gate['id']} — {gate['items']} items", "", gate["purpose"], "", f"- Workbook: `{gate['workbook']}`", f"- Browser form: `{gate['form']}`", f"- Validator: `{gate['validator']}`"]
        if gate.get("summarizer"): lines.append(f"- Summarizer: `{gate['summarizer']}`")
        lines += [f"- Independence: {gate['independence']}", f"- Does not establish: {', '.join(gate['does_not_establish'])}", ""]
    lines += ["## Learning and outcome gates", ""]
    for gate in report["learning_gates"]:
        lines += [f"### {gate['id']} — {gate['tasks']} tasks", "", gate["purpose"], "", f"- Protocol: `{gate['protocol']}`", f"- Form: `{gate['form']}`", f"- Validator: `{gate['validator']}`"]
        if gate.get("adjudication_form"): lines += [f"- Adjudication form: `{gate['adjudication_form']}`", f"- Adjudication validator: `{gate['adjudication_validator']}`"]
        lines += [f"- Status: `{gate['status']}`", f"- Does not establish: {', '.join(gate['does_not_establish'])}", ""]
    lines += ["## Procedure", ""] + [f"{i}. {step}" for i, step in enumerate(report["procedure"], 1)] + ["", "No gate may be marked complete merely because its workbook or form exists. Independent review records must come from a distinct reviewer; learner and listener records must be consented, pseudonymous and validated.", ""]
    (ROOT / "writeups/validation-handoff.md").write_text("\n".join(lines))
    print(json.dumps({"output": "research/validation-handoff.json", "review_gates": len(report["review_gates"]), "learning_gates": len(report["learning_gates"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
