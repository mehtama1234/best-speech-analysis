#!/usr/bin/env python3
"""Build compact, consent-aware mobile lesson payloads from the curriculum index."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/communication-job-curriculum-index.json"
OUT_JSON = ROOT / "research/communication-job-mobile-lessons.json"
OUT_MD = ROOT / "writeups/communication-job-mobile-lessons.md"


def build() -> dict:
    index = json.loads(INDEX.read_text())
    lessons = []
    for lesson in index["lessons"]:
        lessons.append({
            "lesson_id": f"mobile:{lesson['pattern_id']}",
            "pattern_id": lesson["pattern_id"],
            "canonical_job": lesson["canonical_job"],
            "status": "provisional_not_validated",
            "claim_level": "practice_hypothesis",
            "communication_problem": lesson["communication_problem"],
            "mechanism_hypothesis": lesson["mechanism_hypothesis"],
            "evidence_links": {
                "exact_example_ids": [example["record_id"] for example in lesson["exact_examples"][:3]],
                "phrase_forms": lesson["phrase_forms"],
                "delivery_sample_ids": [item["sample_id"] for item in lesson["delivery_samples"]],
                "counterexample_types": [item["counterexample_type"] for item in lesson["counterexample_slots"]],
            },
            "steps": [
                {"step_id": "orient", "type": "read", "prompt": "Name the communication problem before trying the form."},
                {"step_id": "inspect", "type": "inspect_evidence", "prompt": "Read one exact example and note what the words are doing; delivery measurements are proxies, not meaning."},
                {"step_id": "rehearse", "type": "practice", "prompt": lesson["practice"], "response_mode": ["typed", "spoken", "captioned", "asynchronous"]},
                {"step_id": "self_check", "type": "self_check", "prompt": lesson["self_check"]},
                {"step_id": "boundary", "type": "non_fit", "prompt": lesson["non_fit"]},
                {"step_id": "listener", "type": "listener_check", "prompt": "Optional separate listener check: ask the listener to restate the point and identify what remains uncertain. Do not treat one response as effectiveness evidence."},
            ],
            "capture_schema": {
                "participant_code": "pseudonymous_required",
                "consent": "explicit_required_before_save",
                "accessibility_or_modality": "optional_text",
                "practice_response": "text_or_local_recording_reference",
                "self_check_response": "text_required",
                "non_fit_response": "text_required",
                "listener_restatement": "optional_separate_record",
                "revision_after_feedback": "optional_text",
            },
            "safety_boundary": "Do not imitate a speaker's identity, accent, personality or mannerism; do not require personal disclosure or recording; preserve privacy, accessibility and consent.",
            "validation": {"learner_observations": "not_run", "listener_outcomes": "not_run", "independent_evidence_review": "pending"},
        })
    return {
        "schema_version": "1.0",
        "payload_id": "communication-job-mobile-lessons",
        "status": "mobile_payload_provisional_not_validated",
        "source_index": "research/communication-job-curriculum-index.json",
        "lesson_count": len(lessons),
        "claim_boundary": "This payload supports mobile practice navigation and consent-aware capture. It does not make a pattern effective, recurrent, teachable or outcome-producing, and it does not upload or require recordings.",
        "accessibility": ["typed response", "captioned or written response", "asynchronous use", "no required personal disclosure", "no required recording"],
        "lessons": lessons,
    }


def main() -> int:
    payload = build()
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job mobile lessons", "", "Status: **provisional mobile payload; not validated**.", "", payload["claim_boundary"], "", f"Lessons: **{payload['lesson_count']}**.", "", "| Job | Steps | Exact examples | Delivery samples | Learner status |", "|---|---:|---:|---:|---|"]
    for lesson in payload["lessons"]:
        lines.append(f"| `{lesson['canonical_job']}` | {len(lesson['steps'])} | {len(lesson['evidence_links']['exact_example_ids'])} | {len(lesson['evidence_links']['delivery_sample_ids'])} | `{lesson['validation']['learner_observations']}` |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote mobile lesson payload ({len(payload['lessons'])} lessons)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
