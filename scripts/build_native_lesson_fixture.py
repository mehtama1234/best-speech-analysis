#!/usr/bin/env python3
"""Materialize one current mobile lesson as a native/client contract fixture."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/communication-job-mobile-lessons.json"
OUT = ROOT / "clients/examples/mobile_lesson_fixture.json"
OUT_ALL = ROOT / "clients/examples/mobile_lesson_fixtures.json"


def build() -> dict:
    lessons = json.loads(SOURCE.read_text())["lessons"]
    lesson = lessons[0]
    fields = ("lesson_id", "pattern_id", "canonical_job", "status", "claim_level", "communication_problem", "evidence_links", "steps", "safety_boundary", "validation")
    return {field: lesson[field] for field in fields}


def build_all() -> list[dict]:
    lessons = json.loads(SOURCE.read_text())["lessons"]
    fields = ("lesson_id", "pattern_id", "canonical_job", "status", "claim_level", "communication_problem", "evidence_links", "steps", "safety_boundary", "validation")
    return [{field: lesson[field] for field in fields} for lesson in lessons]


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n")
    OUT_ALL.write_text(json.dumps(build_all(), ensure_ascii=False, indent=2) + "\n")
    print(f"native mobile lesson fixtures written: {OUT.relative_to(ROOT)} and {OUT_ALL.relative_to(ROOT)}")
