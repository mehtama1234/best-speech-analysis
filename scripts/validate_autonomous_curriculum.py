"""Adversarial consistency checks for the autonomous curriculum artifacts."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate() -> list[str]:
    errors = []
    itinerary = load("research/corpus-video-learning-itinerary.json")
    curriculum = load("research/communication-job-curriculum-index.json")
    audit = load("research/autonomous-curriculum-audit.json")
    delivery = load("research/autonomous-delivery-reconciliation.json")
    counters = load("research/autonomous-counterexample-screening.json")

    entries = itinerary.get("entries", [])
    if itinerary.get("video_count") != 395 or len(entries) != 395:
        errors.append("itinerary must contain exactly 395 videos")
    required_entry_fields = ("video_id", "title", "learning_track", "learning_form", "learning_note", "practice", "self_check", "limits", "claim_boundary", "exact_evidence")
    for number, entry in enumerate(entries):
        for field in required_entry_fields:
            if not entry.get(field):
                errors.append(f"itinerary entry {number} missing {field}")
                break
        if not entry.get("exact_evidence"):
            errors.append(f"itinerary entry {number} has no exact evidence")
    if len({entry.get("video_id") for entry in entries}) != 395:
        errors.append("itinerary video IDs are not unique")

    jobs = [lesson.get("canonical_job") for lesson in curriculum.get("lessons", [])]
    if len(jobs) != 18 or len(set(jobs)) != 18:
        errors.append("curriculum must contain 18 unique jobs")
    if len(audit.get("jobs", [])) != 18:
        errors.append("autonomous audit must contain 18 job rows")

    if delivery.get("item_count") != 36 or len(delivery.get("items", [])) != 36:
        errors.append("delivery reconciliation must contain 36 items")
    if len({item.get("sample_id") for item in delivery.get("items", [])}) != 36:
        errors.append("delivery reconciliation sample IDs are not unique")
    if any("effectiveness" not in item.get("claim_boundary", "").lower() for item in delivery.get("items", [])):
        errors.append("delivery rows must retain effectiveness boundary")

    if counters.get("item_count") != 90 or len(counters.get("items", [])) != 90:
        errors.append("counterexample screening must contain 90 items")
    counts = Counter(item.get("canonical_job") for item in counters.get("items", []))
    if set(counts) != set(jobs) or any(count != 5 for count in counts.values()):
        errors.append("counterexample screening must contain five candidates per job")
    if any(item.get("status") != "internal_screening_candidate_not_validated" for item in counters.get("items", [])):
        errors.append("counterexample candidates must remain explicitly unvalidated")

    for name, report in (("audit", audit), ("delivery", delivery), ("counterexample", counters)):
        boundary = report.get("claim_boundary", "").lower()
        if "independent" not in boundary or "effectiveness" not in boundary:
            errors.append(f"{name} report has incomplete claim boundary")
    if audit.get("status") == "validated" or delivery.get("status") == "validated":
        errors.append("autonomous artifacts must not be marked validated")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("invalid autonomous curriculum:\n" + "\n".join(f"- {problem}" for problem in problems))
        raise SystemExit(1)
    print("autonomous curriculum valid: 395 lessons, 18 jobs, 36 delivery records, 90 bounded counterexample candidates")
