#!/usr/bin/env python3
"""Validate one browser/native local practice record against the shared model."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = json.loads((ROOT / "research/shared-evidence-model.json").read_text())
SCHEMA = json.loads((ROOT / "research/practice-record.schema.json").read_text())
REQUIRED = SCHEMA["required"]
LESSONS = json.loads((ROOT / "research/communication-job-mobile-lessons.json").read_text())["lessons"]
LESSONS_BY_ID = {lesson["lesson_id"]: lesson for lesson in LESSONS}


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["practice record must be an object"]
    for field in REQUIRED:
        if field not in record:
            errors.append(f"missing practice record field: {field}")
    if record.get("record_type") != "local_communication_practice_record":
        errors.append("record_type is invalid")
    if record.get("schema_version") != "1.0":
        errors.append("schema_version is invalid")
    if not isinstance(record.get("participant_code"), str) or not record.get("participant_code", "").strip():
        errors.append("participant_code must be a non-empty pseudonymous string")
    if record.get("consent") is not True:
        errors.append("consent must be true before a record is saved")
    if not isinstance(record.get("step_responses"), dict):
        errors.append("step_responses must be an object")
    elif any(not isinstance(key, str) or not isinstance(value, str) for key, value in record["step_responses"].items()):
        errors.append("step_responses keys and values must be text")
    boundary = str(record.get("claim_boundary", "")).lower()
    if "not" not in boundary or "effectiveness" not in boundary:
        errors.append("claim_boundary must preserve the non-effectiveness boundary")
    for field in ("lesson_id", "pattern_id", "canonical_job", "accessibility_or_modality"):
        if not isinstance(record.get(field), str):
            errors.append(f"{field} must be text")
    for field in ("source_evidence_ids", "delivery_sample_ids"):
        if not isinstance(record.get(field), list) or any(not isinstance(item, str) or not item for item in record.get(field, [])):
            errors.append(f"{field} must be a list of non-empty evidence IDs")
    try:
        datetime.fromisoformat(str(record.get("saved_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("saved_at must be an ISO-8601 timestamp")
    lesson = LESSONS_BY_ID.get(record.get("lesson_id"))
    if lesson is None:
        errors.append("lesson_id is not present in the shared mobile lesson payload")
    else:
        if record.get("pattern_id") != lesson.get("pattern_id"):
            errors.append("pattern_id does not match lesson_id")
        if record.get("canonical_job") != lesson.get("canonical_job"):
            errors.append("canonical_job does not match lesson_id")
        valid_evidence = {
            segment.get("evidence_id")
            for example in lesson.get("exact_examples", [])
            for segment in example.get("segments", [])
        }
        invalid_evidence = sorted(set(record.get("source_evidence_ids", [])) - valid_evidence)
        if invalid_evidence:
            errors.append(f"source_evidence_ids are not linked to lesson: {', '.join(invalid_evidence)}")
        valid_delivery = {sample.get("sample_id") for sample in lesson.get("delivery_samples", [])}
        invalid_delivery = sorted(set(record.get("delivery_sample_ids", [])) - valid_delivery)
        if invalid_delivery:
            errors.append(f"delivery_sample_ids are not linked to lesson: {', '.join(invalid_delivery)}")
    return errors


def validate_all_lesson_links() -> list[str]:
    """Validate a synthetic, evidence-linked record for every shared lesson."""
    errors: list[str] = []
    for lesson in LESSONS:
        record = {
            "record_type": "local_communication_practice_record",
            "schema_version": "1.0",
            "lesson_id": lesson["lesson_id"],
            "pattern_id": lesson["pattern_id"],
            "canonical_job": lesson["canonical_job"],
            "source_evidence_ids": [
                segment["evidence_id"]
                for example in lesson.get("exact_examples", [])
                for segment in example.get("segments", [])
            ],
            "delivery_sample_ids": [sample["sample_id"] for sample in lesson.get("delivery_samples", [])],
            "participant_code": "synthetic-curriculum-check",
            "consent": True,
            "accessibility_or_modality": "typed",
            "step_responses": {},
            "claim_boundary": "Synthetic contract check; not learner-validation evidence or effectiveness evidence.",
            "saved_at": "2026-09-19T00:00:00Z",
        }
        errors.extend(f"{lesson['lesson_id']}: {error}" for error in validate(record))
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_practice_record.py PATH", file=sys.stderr)
        return 2
    if len(sys.argv) == 2 and sys.argv[1] == "--audit-lessons":
        errors = validate_all_lesson_links()
    elif len(sys.argv) == 2:
        errors = validate(json.loads(Path(sys.argv[1]).read_text()))
    else:
        print("usage: validate_practice_record.py PATH | --audit-lessons", file=sys.stderr)
        return 2
    if errors:
        print("invalid practice record:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("practice record valid: contract shape and lesson links only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
