#!/usr/bin/env python3
"""Join the current delivery queue, proxy measurements and bounded observations.

This is an inspection inventory, not a delivery-pattern or effectiveness
report. It deliberately keeps proxy values and human-readable frame notes
separate from any interpretation of vocal meaning, intent or audience effect.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
MEASUREMENTS = ROOT / "research/communication-job-delivery-measurement-preflight.json"
OBSERVATIONS = ROOT / "research/communication-job-delivery-internal-observations.json"
OUT = ROOT / "research/communication-job-delivery-inventory.json"
MD = ROOT / "writeups/communication-job-delivery-inventory.md"

NUMERIC_METRICS = (
    "words_per_second_proxy",
    "mean_rms_db",
    "speech_activity_fraction",
    "mean_zero_crossing_rate",
    "mean_spectral_centroid_hz",
    "mean_pitch_hz_proxy",
    "mean_pitch_confidence_proxy",
)


def average(rows: list[dict], key: str) -> float | None:
    values = [row["audio_measurements"].get(key) for row in rows]
    values = [float(value) for value in values if value is not None]
    return round(mean(values), 5) if values else None


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    measurements = {row["sample_id"]: row for row in json.loads(MEASUREMENTS.read_text())["items"]}
    observations = {row["sample_id"]: row for row in json.loads(OBSERVATIONS.read_text())["items"]}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in queue["items"]:
        measurement = measurements.get(item["sample_id"], {})
        observation = observations.get(item["sample_id"], {})
        grouped[item["canonical_job"]].append({
            "sample_id": item["sample_id"],
            "video_id": item["video_id"],
            "title": item["title"],
            "source_url": item["source_url"],
            "evidence_id": item["evidence_id"],
            "start_seconds": item["start_seconds"],
            "end_seconds": item["end_seconds"],
            "transcript_excerpt": item["transcript_excerpt"],
            "raw_media_state": item["raw_media_state"],
            "feature_file": measurement.get("feature_file"),
            "measurement_status": measurement.get("measurement_status"),
            "audio_measurements": measurement.get("audio_measurements", {}),
            "nearest_sampled_frame": measurement.get("nearest_sampled_frame"),
            "transcript_alignment": observation.get("transcript_alignment"),
            "visual_observation": observation.get("visual_observation"),
            "setting_editing_music_observation": observation.get("setting_editing_music_observation"),
            "vocal_timing_observation": observation.get("vocal_timing_observation"),
            "observation_independence": observation.get("independence", "not_available"),
        })

    jobs = []
    for job in sorted(grouped):
        samples = sorted(grouped[job], key=lambda row: row["sample_id"])
        proxy_means = {key: average(samples, key) for key in NUMERIC_METRICS}
        jobs.append({
            "canonical_job": job,
            "sample_count": len(samples),
            "proxy_means": proxy_means,
            "samples": samples,
            "learner_use": "Inspect the linked source clips and compare the two contexts; do not treat proxy means or midpoint notes as a recipe.",
        })

    report = {
        "schema_version": "1.0",
        "inventory_id": "communication-job-delivery-inventory",
        "status": "inspection_inventory_not_validated_delivery_pattern",
        "source_queue": str(QUEUE.relative_to(ROOT)),
        "source_measurements": str(MEASUREMENTS.relative_to(ROOT)),
        "source_internal_observations": str(OBSERVATIONS.relative_to(ROOT)),
        "job_count": len(jobs),
        "sample_count": sum(job["sample_count"] for job in jobs),
        "claim_boundary": "This joins transcript-aligned clips, reproducible proxy measurements and bounded internal midpoint-frame notes so a learner or reviewer can inspect them. It does not identify a best vocal/nonverbal pattern, establish intent or effectiveness, or substitute for independent review and listening.",
        "metric_boundary": "Words/second, RMS, activity, spectral and pitch fields are proxies. Frame measurements are detector or scene-pixel fields. They are not emotion, confidence, emphasis, eye contact, gesture meaning or audience response.",
        "jobs": jobs,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Communication-job delivery inventory",
        "",
        "Status: **inspection inventory; not a validated delivery-pattern library**.",
        "",
        report["claim_boundary"],
        "",
        f"Jobs: **{len(jobs)}** · aligned samples: **{report['sample_count']}**.",
        "",
        "| Job | Samples | Mean W/s proxy | Mean RMS proxy | Mean activity | Internal frame note |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for job in jobs:
        means = job["proxy_means"]
        notes = " ".join(sample.get("visual_observation") or "" for sample in job["samples"])
        lines.append(f"| `{job['canonical_job']}` | {job['sample_count']} | {means['words_per_second_proxy']} | {means['mean_rms_db']} | {means['speech_activity_fraction']} | {notes} |")
    lines += ["", "## How to use this inventory", "", "- Open both source clips for a job and compare the transcript function with what is actually visible and audible.", "- Record uncertainty when the speaker, turn, edit or caption alignment is unclear.", "- Treat the numbers as navigation aids and the midpoint notes as bounded observations, not as instructions to imitate.", "- Promotion requires the independent delivery, counterexample, learner and listener gates in the [end-to-end goal](end-to-end-goal.md).", ""]
    MD.write_text("\n".join(lines))
    print(f"wrote delivery inventory ({len(jobs)} jobs; {report['sample_count']} samples)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
