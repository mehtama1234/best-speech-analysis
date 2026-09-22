#!/usr/bin/env python3
"""Validate generated native/web client contract coverage against the model."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .build_native_client_contracts import build
except ImportError:
    from build_native_client_contracts import build

ROOT = Path(__file__).resolve().parents[1]


def validate_practice_fixture() -> list[str]:
    """Check one synthetic record at the shared web/native boundary."""
    try:
        from .validate_practice_record import validate
    except ImportError:
        from validate_practice_record import validate
    path = ROOT / "clients/examples/practice_record_fixture.json"
    if not path.exists():
        return ["missing native practice-record fixture: clients/examples/practice_record_fixture.json"]
    try:
        record = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        return [f"native practice-record fixture is invalid JSON: {error}"]
    return [f"native practice-record fixture: {error}" for error in validate(record)]


def validate_mobile_lesson_fixture(model: dict) -> list[str]:
    path = ROOT / "clients/examples/mobile_lesson_fixtures.json"
    if not path.exists():
        return ["missing native mobile-lesson fixtures: clients/examples/mobile_lesson_fixtures.json"]
    try:
        lessons = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        return [f"native mobile-lesson fixtures are invalid JSON: {error}"]
    if not isinstance(lessons, list) or len(lessons) != 18:
        return ["native mobile-lesson fixtures must contain all 18 lessons"]
    required = model["entity_types"]["mobile_lesson"]["required"]
    errors = []
    for number, lesson in enumerate(lessons, 1):
        prefix = f"native mobile-lesson fixture {number}"
        errors.extend(f"{prefix} missing {field}" for field in required if lesson.get(field) in (None, ""))
        if lesson.get("status") != "provisional_not_validated":
            errors.append(f"{prefix} must remain provisional")
        if lesson.get("claim_level") != "practice_hypothesis":
            errors.append(f"{prefix} must remain a practice hypothesis")
        if len(lesson.get("steps", [])) != 6:
            errors.append(f"{prefix} must retain six bounded steps")
    return errors


def validate() -> list[str]:
    model = json.loads((ROOT / "research/shared-evidence-model.json").read_text())
    expected = build(model)
    errors = []
    for relative, content in expected.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing generated client contract: {relative}")
        elif path.read_text().rstrip() != content.rstrip():
            errors.append(f"generated client contract is stale: {relative}")
    errors.extend(validate_practice_fixture())
    errors.extend(validate_mobile_lesson_fixture(model))
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("invalid native client contracts:\n" + "\n".join(f"- {x}" for x in problems))
        raise SystemExit(1)
    print("native client contracts valid: TypeScript, Kotlin and Swift match shared evidence model")
