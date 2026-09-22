#!/usr/bin/env python3
"""Build a synthetic practice record shared by web/native contract checks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "research/communication-job-mobile-lessons.json"
OUT = ROOT / "clients/examples/practice_record_fixture.json"


def main() -> int:
    lesson = json.loads(LESSONS.read_text())["lessons"][0]
    record = {
        "record_type": "local_communication_practice_record",
        "schema_version": "1.0",
        "lesson_id": lesson["lesson_id"],
        "pattern_id": lesson["pattern_id"],
        "canonical_job": lesson["canonical_job"],
        "source_evidence_ids": [
            segment["evidence_id"]
            for example in lesson["exact_examples"]
            for segment in example["segments"]
        ],
        "delivery_sample_ids": [sample["sample_id"] for sample in lesson["delivery_samples"]],
        "participant_code": "synthetic-native-contract-check",
        "consent": True,
        "accessibility_or_modality": "typed",
        "step_responses": {"rehearse": "synthetic response"},
        "claim_boundary": "Synthetic contract fixture; not learner-validation evidence or effectiveness evidence.",
        "saved_at": "2026-09-19T00:00:00Z",
    }
    OUT.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
