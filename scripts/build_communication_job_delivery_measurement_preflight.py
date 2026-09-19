#!/usr/bin/env python3
"""Attach reproducible feature measurements to the 18-job delivery queue."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
OUT_JSON = ROOT / "research/communication-job-delivery-measurement-preflight.json"
OUT_MD = ROOT / "writeups/communication-job-delivery-measurement-preflight.md"

METRICS = ("words_per_second_proxy", "transcript_gap_before_seconds", "transcript_gap_after_seconds", "mean_rms_db", "speech_activity_fraction", "mean_zero_crossing_rate", "mean_spectral_centroid_hz", "mean_pitch_hz_proxy", "mean_pitch_confidence_proxy")


def mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 5) if values else None


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    rows = []
    for item in queue["items"]:
        feature_path = ROOT / "data/features" / f"{item['video_id']}.json"
        feature = json.loads(feature_path.read_text()) if feature_path.exists() else {}
        aligned = {row["evidence_id"]: row for row in feature.get("aligned_transcript", [])}
        matched = [aligned[evidence_id] for evidence_id in item["transcript_segment_ids"] if evidence_id in aligned]
        missing = [evidence_id for evidence_id in item["transcript_segment_ids"] if evidence_id not in aligned]
        metrics = {metric: mean([float(row[metric]) for row in matched if row.get(metric) is not None]) for metric in METRICS}
        midpoint = (item["start_seconds"] + item["end_seconds"]) / 2
        frames = feature.get("sampled_frames", [])
        frame = min(frames, key=lambda f: abs(float(f.get("time_seconds", 0)) - midpoint)) if frames else None
        rows.append({
            "sample_id": item["sample_id"],
            "canonical_job": item["canonical_job"],
            "video_id": item["video_id"],
            "evidence_ids_requested": item["transcript_segment_ids"],
            "evidence_ids_matched": [row["evidence_id"] for row in matched],
            "missing_evidence_ids": missing,
            "feature_file": str(feature_path.relative_to(ROOT)) if feature_path.exists() else None,
            "feature_schema_version": feature.get("schema_version"),
            "measurement_status": "aligned_feature_measurement_available" if matched else "no_aligned_feature_measurement",
            "audio_measurements": metrics,
            "nearest_sampled_frame": ({key: frame.get(key) for key in ("time_seconds", "face_count", "smile_detector_candidate_count", "mean_luminance", "luminance_std", "face_measurement_status")} if frame else None),
            "measurement_limits": ["RMS, speech activity, spectral and pitch fields are proxies; they do not establish loudness meaning, emotion, confidence, intent or effectiveness.", "Frame face/smile counts are detector candidates, not facial emotion or engagement.", "Feature alignment does not verify speaker identity, editing, room acoustics or transcript correctness."],
        })
    matched_count = sum(bool(row["evidence_ids_matched"]) for row in rows)
    report = {
        "schema_version": "1.0",
        "preflight_id": "communication-job-delivery-measurement-preflight",
        "status": "reproducible_proxy_measurements_attached_manual_review_pending",
        "source_queue": "research/communication-job-delivery-sampling.json",
        "item_count": len(rows),
        "matched_sample_count": matched_count,
        "unmatched_sample_count": len(rows) - matched_count,
        "claim_boundary": "This report attaches reproducible transcript/audio/feature measurements to queued samples. It does not convert proxies into vocal or nonverbal meaning, verify speaker/event identity, establish editing or room causes, or establish effectiveness or audience outcomes.",
        "metric_definitions": {"words_per_second_proxy": "retained caption word count divided by caption duration", "transcript_gap_*": "gaps between adjacent retained caption boundaries", "mean_rms_db": "mean decoded-audio RMS proxy over overlapping windows", "speech_activity_fraction": "fraction of overlapping windows crossing the coarse activity threshold", "mean_pitch_hz_proxy": "coarse spectral pitch estimate where available", "nearest_sampled_frame": "closest stored frame sample to queued interval midpoint"},
        "items": rows,
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job delivery measurement preflight", "", "Status: **reproducible proxy measurements attached; manual review pending**.", "", report["claim_boundary"], "", f"Samples: **{len(rows)}** · aligned feature matches: **{matched_count}** · unmatched: **{len(rows)-matched_count}**.", "", "| Sample | Job | Video | Matched segments | W/s proxy | RMS dB | Activity proxy | Frame |", "|---|---|---|---:|---:|---:|---:|---|"]
    for row in rows:
        audio = row["audio_measurements"]
        frame = row["nearest_sampled_frame"]
        lines.append(f"| `{row['sample_id']}` | `{row['canonical_job']}` | `{row['video_id']}` | {len(row['evidence_ids_matched'])} | {audio['words_per_second_proxy']} | {audio['mean_rms_db']} | {audio['speech_activity_fraction']} | {frame['time_seconds'] if frame else ''} |")
    lines += ["", "## Limits", ""] + [f"- {limit}" for limit in rows[0]["measurement_limits"]]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote delivery measurement preflight ({len(rows)} samples; {matched_count} aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
