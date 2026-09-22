#!/usr/bin/env python3
"""Validate cross-surface lineage for the bounded multimodal delivery layer."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def validate() -> list[str]:
    errors: list[str] = []
    queue = read("research/communication-job-delivery-sampling.json")
    preflight = read("research/communication-job-delivery-measurement-preflight.json")
    reconciled = read("research/autonomous-delivery-reconciliation.json")
    samples = queue.get("items", [])
    measurements = preflight.get("items", [])
    rows = reconciled.get("items", [])
    sample_ids = {x.get("sample_id") for x in samples}
    preflight_ids = {x.get("sample_id") for x in measurements}
    reconciled_ids = {x.get("sample_id") for x in rows}
    if len(samples) != 36 or len(measurements) != 36 or len(rows) != 36:
        errors.append("multimodal layer must have 36 queue, preflight and reconciliation rows")
    if sample_ids != preflight_ids or sample_ids != reconciled_ids:
        errors.append("queue, measurement preflight and reconciliation sample IDs differ")
    counts = Counter(x.get("canonical_job") for x in samples)
    if len(counts) != 18 or set(counts.values()) != {2}:
        errors.append(f"expected two multimodal samples per job: {dict(counts)}")
    preflight_by_id = {x.get("sample_id"): x for x in measurements}
    queue_by_id = {x.get("sample_id"): x for x in samples}
    for sample_id, item in queue_by_id.items():
        measurement = preflight_by_id.get(sample_id, {})
        if item.get("canonical_job") != measurement.get("canonical_job") or item.get("video_id") != measurement.get("video_id"):
            errors.append(f"{sample_id}: job/video mismatch across queue and measurement")
        requested = set(measurement.get("evidence_ids_requested", []))
        matched = set(measurement.get("evidence_ids_matched", []))
        if not requested or requested != matched or measurement.get("missing_evidence_ids"):
            errors.append(f"{sample_id}: transcript evidence interval is not fully matched")
        feature_file = measurement.get("feature_file")
        feature_path = ROOT / feature_file if feature_file else None
        if not feature_path or not feature_path.exists():
            errors.append(f"{sample_id}: local feature file missing")
            continue
        feature = json.loads(feature_path.read_text())
        if feature.get("video_id") != item.get("video_id") or feature.get("schema_version") != "0.2":
            errors.append(f"{sample_id}: feature file identity/schema mismatch")
        aligned = {x.get("evidence_id") for x in feature.get("aligned_transcript", [])}
        if not requested.issubset(aligned):
            errors.append(f"{sample_id}: feature file does not contain requested aligned transcript IDs")
        frame = measurement.get("nearest_sampled_frame")
        if not frame or not isinstance(frame.get("time_seconds"), (int, float)):
            errors.append(f"{sample_id}: nearest sampled frame lacks numeric time")
        if len(measurement.get("measurement_limits", [])) < 2:
            errors.append(f"{sample_id}: measurement limits are incomplete")
        if "effectiveness" not in " ".join(measurement.get("measurement_limits", [])).lower():
            errors.append(f"{sample_id}: measurement limits omit effectiveness boundary")
        if not item.get("raw_media_state") or not item.get("selection_note"):
            errors.append(f"{sample_id}: media availability/selection state missing")
    boundary = reconciled.get("claim_boundary", "").lower()
    for phrase in ("proxi", "manual listening", "independent", "effectiveness"):
        if phrase not in boundary:
            errors.append(f"multimodal reconciliation boundary missing {phrase}")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous multimodal traceability valid: 36 samples, 18 jobs, transcript/features/frame lineage intact")
