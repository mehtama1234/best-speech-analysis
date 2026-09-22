#!/usr/bin/env python3
"""Validate that every provisional communication-job lesson joins the required layers."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/communication-job-curriculum-index.json"
CARDS = ROOT / "research/communication-job-cards.json"
LEARNER = ROOT / "research/communication-job-learner-check.json"
LISTENER = ROOT / "research/communication-job-listener-outcome-protocol.json"
CANDIDATE_QUEUE = ROOT / "research/communication-job-counterexample-candidate-queue.json"


def validate(index: dict, cards: dict | None = None, learner: dict | None = None, listener: dict | None = None) -> list[str]:
    cards = cards or json.loads(CARDS.read_text())
    learner = learner or json.loads(LEARNER.read_text())
    listener = listener or json.loads(LISTENER.read_text())
    candidates = json.loads(CANDIDATE_QUEUE.read_text())
    errors: list[str] = []
    lessons = index.get("lessons", [])
    if index.get("lesson_count") != len(lessons):
        errors.append("lesson_count does not match lessons")
    if index.get("status") != "18_job_provisional_curriculum_not_validated":
        errors.append("curriculum must remain explicitly provisional")
    card_jobs = {card["canonical_job"] for card in cards.get("cards", [])}
    learner_by_job = {card["canonical_job"]: card for card in learner.get("cards", [])}
    listener_by_job = {pattern["canonical_job"]: pattern for pattern in listener.get("patterns", [])}
    candidates_by_job = {}
    for candidate in candidates.get("items", []):
        candidates_by_job.setdefault(candidate.get("canonical_job"), {})[candidate.get("counterexample_type")] = candidate
    lesson_jobs = [lesson.get("canonical_job") for lesson in lessons]
    if set(lesson_jobs) != card_jobs:
        errors.append("curriculum jobs do not match communication-job cards")
    if len(lesson_jobs) != len(set(lesson_jobs)):
        errors.append("curriculum jobs are not unique")
    for job, lesson in zip(lesson_jobs, lessons):
        prefix = f"lesson {job}"
        for field in ("pattern_id", "communication_problem", "mechanism_hypothesis", "repeatable_form", "exact_examples", "recurrence", "phrase_forms", "delivery_samples", "counterexample_slots", "counterexample_candidates", "practice", "self_check", "non_fit", "learner", "listener", "validation"):
            if field not in lesson:
                errors.append(f"{prefix} missing field: {field}")
        if not lesson.get("exact_examples"):
            errors.append(f"{prefix} has no exact examples")
        for example_number, example in enumerate(lesson.get("exact_examples", []), 1):
            example_prefix = f"{prefix} example {example_number}"
            for field in ("record_id", "video_id", "source_url", "exact_segments"):
                if not example.get(field):
                    errors.append(f"{example_prefix} missing {field}")
            segments = example.get("exact_segments", [])
            if not segments:
                errors.append(f"{example_prefix} has no timestamped segments")
            for segment_number, segment in enumerate(segments, 1):
                segment_prefix = f"{example_prefix} segment {segment_number}"
                for field in ("evidence_id", "start_seconds", "end_seconds", "text", "source_transcript_file"):
                    if segment.get(field) in (None, ""):
                        errors.append(f"{segment_prefix} missing {field}")
                if segment.get("start_seconds") is not None and segment.get("end_seconds") is not None:
                    if segment["end_seconds"] < segment["start_seconds"]:
                        errors.append(f"{segment_prefix} ends before it starts")
        recurrence = lesson.get("recurrence", {})
        for field in ("function_record_count", "video_count", "denominator_status"):
            if recurrence.get(field) in (None, ""):
                errors.append(f"{prefix} recurrence missing {field}")
        if recurrence.get("function_record_count", 0) < recurrence.get("video_count", 0):
            errors.append(f"{prefix} recurrence function count is below video count")
        if len(lesson.get("delivery_samples", [])) != 2:
            errors.append(f"{prefix} must retain two delivery samples")
        for sample_number, sample in enumerate(lesson.get("delivery_samples", []), 1):
            sample_prefix = f"{prefix} delivery sample {sample_number}"
            for field in ("video_id", "start_seconds", "end_seconds", "raw_media_state"):
                if sample.get(field) in (None, ""):
                    errors.append(f"{sample_prefix} missing {field}")
            if sample.get("start_seconds") is not None and sample.get("end_seconds") is not None:
                if sample["end_seconds"] < sample["start_seconds"]:
                    errors.append(f"{sample_prefix} ends before it starts")
        if len(lesson.get("counterexample_slots", [])) != 5:
            errors.append(f"{prefix} must retain five counterexample slots")
        candidate_rows = lesson.get("counterexample_candidates", [])
        if len(candidate_rows) != 5:
            errors.append(f"{prefix} must retain five routed counterexample candidates")
        elif any(row.get("candidate_status") != "candidate_requires_check" for row in candidate_rows):
            errors.append(f"{prefix} contains a promoted counterexample candidate")
        for candidate_number, row in enumerate(candidate_rows, 1):
            if not row.get("claim_boundary"):
                errors.append(f"{prefix} counterexample candidate {candidate_number} lacks claim boundary")
        expected_candidates = candidates_by_job.get(job, {})
        if {row.get("counterexample_type") for row in candidate_rows} != set(expected_candidates):
            errors.append(f"{prefix} counterexample candidate types are stale")
        learner_row = learner_by_job.get(job)
        if not learner_row:
            errors.append(f"{prefix} has no learner protocol row")
        elif lesson.get("learner", {}).get("task_count") != learner_row.get("task_count"):
            errors.append(f"{prefix} learner task count is stale")
        listener_row = listener_by_job.get(job)
        if not listener_row:
            errors.append(f"{prefix} has no listener protocol row")
        elif lesson.get("listener", {}).get("pattern_id") != listener_row.get("pattern_id"):
            errors.append(f"{prefix} listener pattern link is stale")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else INDEX
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid communication-job curriculum:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("communication-job curriculum valid: 18 provisional lessons join evidence and validation queues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
