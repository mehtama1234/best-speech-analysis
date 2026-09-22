#!/usr/bin/env python3
"""Validate delivery reconciliation lineage and local measurement availability."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate() -> list[str]:
    report = json.loads((ROOT / "research/autonomous-delivery-reconciliation.json").read_text())
    preflight = json.loads((ROOT / "research/communication-job-delivery-measurement-preflight.json").read_text())
    measurements = {item.get("sample_id"): item for item in preflight.get("items", [])}
    errors = []
    items = report.get("items", [])
    if report.get("item_count") != 36 or len(items) != 36:
        errors.append("delivery reconciliation must contain 36 items")
    if report.get("job_count") != 18:
        errors.append("delivery reconciliation must cover 18 jobs")
    if len({item.get("sample_id") for item in items}) != 36:
        errors.append("delivery sample IDs must be unique")
    if any("effectiveness" not in item.get("claim_boundary", "").lower() for item in items):
        errors.append("every delivery item must retain effectiveness boundary")
    for item in items:
        sample_id = item.get("sample_id")
        measurement = measurements.get(sample_id)
        if not measurement:
            errors.append(f"{sample_id}: measurement preflight row missing")
            continue
        if measurement.get("video_id") != item.get("video_id"):
            errors.append(f"{sample_id}: video ID mismatch")
        if measurement.get("missing_evidence_ids"):
            errors.append(f"{sample_id}: missing evidence IDs present")
        feature_file = measurement.get("feature_file")
        if not feature_file or not (ROOT / feature_file).exists():
            errors.append(f"{sample_id}: feature file missing")
        if not measurement.get("nearest_sampled_frame"):
            errors.append(f"{sample_id}: nearest frame record missing")
        if not item.get("visual_observation") or not item.get("setting_observation"):
            errors.append(f"{sample_id}: bounded visual/setting observation missing")
    boundary = report.get("claim_boundary", "").lower()
    for phrase in ("manual listening", "independent observation", "effectiveness"):
        if phrase not in boundary:
            errors.append(f"report boundary missing {phrase}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("invalid autonomous delivery reconciliation:\n" + "\n".join(f"- {problem}" for problem in problems))
        raise SystemExit(1)
    print("autonomous delivery reconciliation valid: 36 rows, local lineage and proxy boundaries intact")
