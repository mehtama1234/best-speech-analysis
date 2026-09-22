#!/usr/bin/env python3
"""Validate traceability from bounded evidence into every lesson and practice task."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def validate() -> list[str]:
    errors: list[str] = []
    cards_payload = read("research/shared-lesson-cards.json")
    mobile_payload = read("research/communication-job-mobile-lessons.json")
    learner_payload = read("research/communication-job-learner-check.json")
    counter_payload = read("research/communication-job-counterexample-workbook.json")
    delivery_payload = read("research/communication-job-delivery-sampling.json")
    evidence_payload = read("research/corpus-evidence-bank.json")
    jobs = {x["canonical_job"] for x in cards_payload["cards"]}
    if jobs != {x["canonical_job"] for x in mobile_payload["lessons"]}:
        errors.append("shared and mobile job sets differ")
    if jobs != {x["canonical_job"] for x in learner_payload["cards"]}:
        errors.append("shared and learner job sets differ")
    if len(jobs) != 18:
        errors.append(f"expected 18 jobs, found {len(jobs)}")

    evidence_ids = {
        segment.get("evidence_id")
        for record in evidence_payload.get("records", [])
        for segment in record.get("segments", [])
        if segment.get("evidence_id")
    }
    delivery_ids = {x.get("sample_id") for x in delivery_payload.get("items", [])}
    counter_by_job: dict[str, set[str]] = {}
    for item in counter_payload.get("items", []):
        counter_by_job.setdefault(item.get("canonical_job"), set()).add(item.get("counterexample_type"))
    required_counter_types = {"absent_but_speech_works", "present_but_speech_fails", "alternate_function", "confound_or_setting", "misuse_or_copying_risk"}
    learner_by_job: dict[str, list[dict]] = {}
    for task in learner_payload.get("tasks", []):
        learner_by_job.setdefault(task.get("canonical_job"), []).append(task)

    mobile_by_job = {x["canonical_job"]: x for x in mobile_payload["lessons"]}
    for card in cards_payload["cards"]:
        job = card.get("canonical_job")
        if card.get("status") != "provisional_not_validated":
            errors.append(f"{job} card status is not provisional")
        if "causal effectiveness" not in card.get("claim_boundary", ""):
            errors.append(f"{job} card lacks effectiveness boundary")
        examples = card.get("examples", [])
        if len(examples) != 8 or len({x.get("video_id") for x in examples}) != 8:
            errors.append(f"{job} must have eight distinct-video examples")
        example_record_ids = {x.get("record_id") for x in examples}
        segment_ids = set()
        for example in examples:
            if not example.get("source_url") or not example.get("exact_segments"):
                errors.append(f"{job} example lacks source or exact segments")
            for segment in example.get("exact_segments", []):
                evidence_id = segment.get("evidence_id")
                segment_ids.add(evidence_id)
                if evidence_id not in evidence_ids:
                    errors.append(f"{job} references missing evidence {evidence_id}")
                if not (ROOT / segment.get("source_transcript_file", "missing")).exists():
                    errors.append(f"{job} references missing transcript file for {evidence_id}")
        practice = card.get("practice", {})
        for field in ("hypothesis", "repeatable_form", "self_check", "non_fit"):
            if not practice.get(field):
                errors.append(f"{job} practice missing {field}")
        if practice.get("task_count") != 4:
            errors.append(f"{job} practice task count is not 4")
        if set(card.get("evidence_chain", {}).get("exact_language_and_function", {}).get("example_evidence_ids", [])) != segment_ids:
            errors.append(f"{job} evidence-chain IDs do not equal example segment IDs")
        if set(card.get("evidence_chain", {}).get("delivery_evidence", {}).get("evidence_ids", [])) - evidence_ids:
            errors.append(f"{job} delivery evidence points outside evidence bank")
        if set(x.get("counterexample_type") for x in card.get("counterexamples", [])) != required_counter_types:
            errors.append(f"{job} card counterexample slots are incomplete")
        if counter_by_job.get(job) != required_counter_types:
            errors.append(f"{job} counterexample workbook slots are incomplete")

        mobile = mobile_by_job.get(job, {})
        links = mobile.get("evidence_links", {})
        if set(links.get("exact_example_ids", [])) != set(x.get("record_id") for x in examples[:3]):
            errors.append(f"{job} mobile example links do not match the card examples")
        if len(links.get("delivery_sample_ids", [])) != 2 or not set(links["delivery_sample_ids"]).issubset(delivery_ids):
            errors.append(f"{job} mobile delivery links are incomplete")
        if set(links.get("counterexample_types", [])) != required_counter_types:
            errors.append(f"{job} mobile counterexample links are incomplete")
        step_types = {step.get("type") for step in mobile.get("steps", [])}
        if len(mobile.get("steps", [])) != 6 or not {"read", "inspect_evidence", "practice", "self_check", "non_fit", "listener_check"}.issubset(step_types):
            errors.append(f"{job} mobile lesson does not expose all six practice stages")

        tasks = learner_by_job.get(job, [])
        if len(tasks) != 4 or {x.get("phase") for x in tasks} != {"new_example_recognition", "plain_language_explanation", "transfer", "misuse_non_fit"}:
            errors.append(f"{job} learner tasks do not cover recognition/explanation/transfer/non-fit")
        for task in tasks:
            if task.get("card_id") != card.get("card_id") or not task.get("boundary") or not task.get("required_features"):
                errors.append(f"{job} learner task is not linked and bounded: {task.get('task_id')}")
    if len(delivery_ids) != 36:
        errors.append(f"delivery sampling queue is not 36 rows: {len(delivery_ids)}")
    if learner_payload.get("task_count") != 72:
        errors.append("learner protocol is not 72 tasks")
    if "not" not in learner_payload.get("claim_boundary", "").lower() or "outcome" not in learner_payload.get("claim_boundary", "").lower():
        errors.append("learner protocol lacks outcome boundary")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous evidence-to-practice traceability valid: 18 jobs, 144 examples, 72 learner tasks, 36 delivery links")
