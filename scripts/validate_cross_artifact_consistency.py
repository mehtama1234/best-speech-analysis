#!/usr/bin/env python3
"""Check that the primary status and handoff artifacts agree on scope."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def validate() -> list[str]:
    status = load("research/end-to-end-status.json")
    matrix = load("research/end-to-end-acceptance-matrix.json")
    readiness = load("research/communication-job-promotion-readiness.json")
    gates = load("research/external-review-gate-index.json")
    errors = []
    stages = status["stages"]

    expected = {
        "transcript_reviews": (stages["transcript_context"]["video_count"], 395),
        "cards": (stages["communication_job_cards"]["card_count"], readiness["card_count"]),
        "delivery_samples": (stages["communication_job_delivery_sampling"]["queued_sample_count"], 36),
        "learner_tasks": (stages["communication_job_learner_check"]["task_count"], 72),
        "listener_jobs": (stages["communication_job_listener_outcomes"]["pattern_count"], 18),
        "listener_tasks": (stages["communication_job_listener_outcomes"]["listener_task_count"], 6),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            errors.append(f"{label}: expected {required}, found {actual}")

    media = stages["full_corpus_media_coverage"]
    media_total = sum(media.get(key, 0) for key in ("raw_audio_video_present", "audio_only", "video_only", "derived_features_only", "transcript_only_no_local_media"))
    if media_total != media["video_count"]:
        errors.append(f"full-corpus media states sum to {media_total}, not {media['video_count']}")
    if matrix["open_requirement_count"] != sum(row["status"] not in {"complete_for_fixed_corpus", "contract_and_validators_ready"} for row in matrix["rows"]):
        errors.append("acceptance matrix open_requirement_count is stale")
    if readiness["promotion_ready_count"] != 0 or len(readiness["cards"]) != readiness["card_count"]:
        errors.append("promotion readiness count or card rows is inconsistent")
    readiness_stage = status["stages"].get("promotion_readiness", {})
    if readiness_stage.get("card_count") != readiness["card_count"] or readiness_stage.get("promotion_ready_count") != readiness["promotion_ready_count"]:
        errors.append("end-to-end promotion readiness stage is stale")

    gate_counts = {gate["gate_id"]: gate["item_count"] for gate in gates["gates"]}
    for gate_id, count in {"identity": 395, "delivery": 36, "learner": 72, "listener_stimuli": 18, "listener_outcomes": 18}.items():
        if gate_counts.get(gate_id) != count:
            errors.append(f"gate {gate_id}: expected {count}, found {gate_counts.get(gate_id)}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("cross-artifact consistency invalid:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("cross-artifact consistency valid: status, acceptance, readiness and gates reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
