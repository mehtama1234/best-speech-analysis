#!/usr/bin/env python3
"""Validate the unpromoted second-slice draft packets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKETS = [
    ("question", "candidate-question"),
    ("definition", "candidate-definition_or_reformulation"),
    ("call-to-action", "candidate-call_to_action"),
]


def load(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    registry_ids = set()
    for line in (ROOT / "research/segment-registry.jsonl").read_text().splitlines():
        if line.strip():
            registry_ids.add(load_json_line(line)["evidence_id"])
    plan = load(ROOT / "research/vertical-slice-02-candidate-plan.json")
    assert plan["status"] == "candidate_plan_not_validated"
    assert len(plan["candidates"]) == 3
    manifest = load(ROOT / "research/vertical-slice-02.json")
    assert manifest["status"] == "candidate_not_validated"
    assert manifest["independent_review"] == "not_started"
    assert manifest["learner_check"] == "not_started"
    assert manifest["validator"] == "scripts/validate_vertical_slice_02_drafts.py"
    manual = load(ROOT / manifest["manual_multimodal_review"])
    assert manual["status"] == "internal_sample_review_complete_independent_review_pending"
    assert manual["independence"] == "not_independent"
    assert len(manual["items"]) == 8
    for item in manual["items"]:
        video_id = item["evidence_id"].split(":", 1)[0]
        assert (ROOT / f"data/video/{video_id}.mp4").is_file(), item["evidence_id"]
        assert (ROOT / f"data/audio/{video_id}.m4a").is_file(), item["evidence_id"]
    tasks = load(ROOT / manifest["learner_task_bank"])
    assert tasks["status"] == "candidate_tasks_not_piloted"
    assert len(tasks["tasks"]) == 12
    assert {task["phase"] for task in tasks["tasks"]} == {"recognition", "transfer", "non_fit", "control"}
    assert (ROOT / manifest["learner_check_html"]).is_file()
    assert (ROOT / manifest["learner_check_validator"]).is_file()
    assert (ROOT / manifest["learner_check_browser_smoke_test"]).is_file()
    workbook = load(ROOT / manifest["review_workbook"])
    assert workbook["status"] == "template_not_completed"
    assert workbook["item_count"] == 15
    assert len(workbook["items"]) == 15
    assert (ROOT / manifest["review_request"]).is_file()
    assert (ROOT / manifest["review_workbook_html"]).is_file()
    assert (ROOT / manifest["review_browser_smoke_test"]).is_file()
    packet_ids = []
    for name, pattern_id in PACKETS:
        path = ROOT / f"research/vertical-slice-02-{name}-draft.json"
        packet = load(path)
        assert packet["status"] == "draft_candidate_packet_not_validated"
        assert packet["pattern_id"] == pattern_id
        reps = packet["representative_examples"]
        counters = packet["counterexamples"]
        assert len(reps) == 3
        assert len(counters) >= 2
        for item in reps + counters:
            assert item["evidence_id"] in registry_ids, item["evidence_id"]
            assert item["video_id"] == item["evidence_id"].split(":", 1)[0]
        assert packet["independence_status"] == "not_verified"
        assert packet["learner_status"] == "not_started"
        entry = next(item for item in manifest["patterns"] if item["pattern_id"] == pattern_id)
        assert entry["packet"] == str(path.relative_to(ROOT))
        assert (ROOT / entry["lesson"]).is_file()
        packet_ids.append(packet["packet_id"])
    assert len(set(packet_ids)) == 3
    print("vertical slice 02 drafts valid: 3 packets, not promotion-ready")


def load_json_line(line: str):
    return json.loads(line)


if __name__ == "__main__":
    main()
