#!/usr/bin/env python3
"""Validate the autonomous counterexample screening without promoting candidates."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate() -> list[str]:
    screening = json.loads((ROOT / "research/autonomous-counterexample-screening.json").read_text())
    cards = json.loads((ROOT / "research/corpus-learner-card-inventory.json").read_text()).get("cards", [])
    jobs = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text()).get("lessons", [])
    card_ids = {card.get("card_id") for card in cards}
    evidence_ids = {
        evidence.get("evidence_id")
        for card in cards
        for evidence in card.get("exact_evidence", [])
    }
    errors = []
    items = screening.get("items", [])
    if screening.get("item_count") != 90 or len(items) != 90:
        errors.append("screening must contain exactly 90 items")
    if screening.get("job_count") != 18 or screening.get("items_per_job") != 5:
        errors.append("screening must declare 18 jobs and five items per job")
    if screening.get("unique_source_videos_per_job") != 5:
        errors.append("screening must declare five distinct source videos per job")
    expected_jobs = {lesson.get("canonical_job") for lesson in jobs}
    observed_jobs = {item.get("canonical_job") for item in items}
    if observed_jobs != expected_jobs:
        errors.append("screening job set does not match curriculum job set")
    pair_counts = Counter((item.get("canonical_job"), item.get("counterexample_type")) for item in items)
    if len(pair_counts) != 90 or any(count != 1 for count in pair_counts.values()):
        errors.append("each job/type pair must occur exactly once")
    for job in expected_jobs:
        job_items = [item for item in items if item.get("canonical_job") == job]
        if len({item.get("candidate", {}).get("video_id") for item in job_items}) != 5:
            errors.append(f"job {job} must use five distinct source videos")
    if len({item.get("screening_item_id") for item in items}) != 90:
        errors.append("screening item IDs must be unique")
    allowed_types = {
        "absent_but_speech_works",
        "present_but_limit_visible",
        "alternate_function_or_phrase",
        "setting_or_delivery_confound",
        "safety_accessibility_screen",
    }
    for number, item in enumerate(items):
        candidate = item.get("candidate", {})
        if item.get("counterexample_type") not in allowed_types:
            errors.append(f"item {number} has unknown counterexample type")
        if item.get("status") != "internal_screening_candidate_not_validated":
            errors.append(f"item {number} was promoted beyond screening")
        if item.get("source_card_id") not in card_ids:
            errors.append(f"item {number} source card is not in the card inventory")
        if candidate.get("evidence_id") not in evidence_ids:
            errors.append(f"item {number} evidence ID is not in the card inventory")
        boundary = item.get("claim_boundary", "").lower()
        if "does not establish" not in boundary or "failure" not in boundary:
            errors.append(f"item {number} has incomplete claim boundary")
    report_boundary = screening.get("claim_boundary", "").lower()
    if "not independent" not in report_boundary or "effectiveness" not in report_boundary:
        errors.append("screening report boundary is incomplete")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("invalid autonomous counterexample screening:\n" + "\n".join(f"- {problem}" for problem in problems))
        raise SystemExit(1)
    print("autonomous counterexample screening valid: 90 bounded candidates, no promotions")
