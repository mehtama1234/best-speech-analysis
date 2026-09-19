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


def validate(index: dict, cards: dict | None = None, learner: dict | None = None, listener: dict | None = None) -> list[str]:
    cards = cards or json.loads(CARDS.read_text())
    learner = learner or json.loads(LEARNER.read_text())
    listener = listener or json.loads(LISTENER.read_text())
    errors: list[str] = []
    lessons = index.get("lessons", [])
    if index.get("lesson_count") != len(lessons):
        errors.append("lesson_count does not match lessons")
    if index.get("status") != "18_job_provisional_curriculum_not_validated":
        errors.append("curriculum must remain explicitly provisional")
    card_jobs = {card["canonical_job"] for card in cards.get("cards", [])}
    learner_by_job = {card["canonical_job"]: card for card in learner.get("cards", [])}
    listener_by_job = {pattern["canonical_job"]: pattern for pattern in listener.get("patterns", [])}
    lesson_jobs = [lesson.get("canonical_job") for lesson in lessons]
    if set(lesson_jobs) != card_jobs:
        errors.append("curriculum jobs do not match communication-job cards")
    if len(lesson_jobs) != len(set(lesson_jobs)):
        errors.append("curriculum jobs are not unique")
    for job, lesson in zip(lesson_jobs, lessons):
        prefix = f"lesson {job}"
        for field in ("pattern_id", "communication_problem", "mechanism_hypothesis", "repeatable_form", "exact_examples", "recurrence", "phrase_forms", "delivery_samples", "counterexample_slots", "practice", "self_check", "non_fit", "learner", "listener", "validation"):
            if field not in lesson:
                errors.append(f"{prefix} missing field: {field}")
        if not lesson.get("exact_examples"):
            errors.append(f"{prefix} has no exact examples")
        if len(lesson.get("delivery_samples", [])) != 2:
            errors.append(f"{prefix} must retain two delivery samples")
        if len(lesson.get("counterexample_slots", [])) != 5:
            errors.append(f"{prefix} must retain five counterexample slots")
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
