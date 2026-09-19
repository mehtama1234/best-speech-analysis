#!/usr/bin/env python3
"""Link transcript job evidence to locally measured delivery proxies."""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
FEATURE_DIR = ROOT / "data/features"
OUT_JSON = ROOT / "research/delivery-proxy-candidate-atlas.json"
OUT_MD = ROOT / "writeups/delivery-proxy-candidate-atlas.md"


def avg(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 4) if values else None


def main() -> int:
    records = json.loads(EVIDENCE.read_text())["records"]
    feature_reports = {path.stem: json.loads(path.read_text()) for path in FEATURE_DIR.glob("*.json")}
    candidates = []
    for record in records:
        job = record.get("canonical_job")
        report = feature_reports.get(record.get("video_id"))
        if not job or job == "unclassified" or not report:
            continue
        start = float(record.get("start_seconds") or 0)
        end = float(record.get("end_seconds") or start)
        windows = [
            window for window in report.get("audio_windows", [])
            if window.get("end_seconds", 0) > start and window.get("start_seconds", 0) < end
        ]
        aligned = next(
            (segment for segment in report.get("aligned_transcript", []) if segment.get("evidence_id") in {x.get("evidence_id") for x in record.get("segments", [])}),
            None,
        )
        midpoint = (start + end) / 2
        frames = report.get("sampled_frames", [])
        nearest_frame = min(frames, key=lambda frame: abs(frame.get("time_seconds", 0) - midpoint), default=None)
        candidates.append({
            "record_id": record.get("record_id"),
            "evidence_id": record.get("segments", [{}])[0].get("evidence_id") or record.get("record_id"),
            "video_id": record["video_id"],
            "title": record.get("title", record["video_id"]),
            "canonical_job": job,
            "source_url": record.get("source_url") or f"https://www.youtube.com/watch?v={record['video_id']}&t={int(start)}s",
            "start_seconds": start,
            "end_seconds": end,
            "transcript_excerpt": " ".join(record.get("assembled_caption_text", "").split())[:320],
            "feature_file": f"data/features/{record['video_id']}.json",
            "alignment": "exact_evidence_id_in_feature_report" if aligned else ("overlapping_audio_windows" if windows else "no_overlapping_audio_window"),
            "audio_proxy_summary": {
                "overlapping_window_count": len(windows),
                "mean_rms_db": avg([x["rms_db"] for x in windows if x.get("rms_db") is not None]),
                "mean_pitch_hz_proxy": avg([x["pitch_hz_proxy"] for x in windows if x.get("pitch_hz_proxy") is not None]),
                "mean_spectral_centroid_hz": avg([x["spectral_centroid_hz"] for x in windows if x.get("spectral_centroid_hz") is not None]),
                "speech_activity_fraction": avg([float(x["speech_activity_proxy"]) for x in windows if x.get("speech_activity_proxy") is not None]),
            },
            "nearest_sampled_frame_proxy": {
                "time_seconds": nearest_frame.get("time_seconds") if nearest_frame else None,
                "face_count": nearest_frame.get("face_count") if nearest_frame else None,
                "face_measurement_status": nearest_frame.get("face_measurement_status") if nearest_frame else "not_available",
            },
            "candidate_status": "proxy_backed_clip_requires_human_delivery_review",
        })
    by_job: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        by_job[candidate["canonical_job"]].append(candidate)
    selected = {
        job: [items[index] for index in range(0, len(items), max(1, len(items) // 3))][:3]
        for job, items in sorted(by_job.items())
    }
    result = {
        "schema_version": "1.0",
        "atlas_id": "delivery-proxy-candidate-atlas",
        "status": "proxy_backed_candidate_clips_not_delivery_validation",
        "claim_boundary": "Each row links a heuristic transcript job record to overlapping local audio/frame proxies. These rows identify clips for human review; they do not establish delivery meaning, speaker identity, intent, emotion, audience response, quality or effectiveness.",
        "source_evidence": "research/corpus-evidence-bank.json",
        "source_features": "data/features/*.json",
        "counts": {
            "candidate_record_count": len(candidates),
            "candidate_video_count": len({x["video_id"] for x in candidates}),
            "job_count": len(by_job),
            "exact_alignment_count": sum(x["alignment"] == "exact_evidence_id_in_feature_report" for x in candidates),
            "overlap_only_count": sum(x["alignment"] == "overlapping_audio_windows" for x in candidates),
        },
        "measurement_limits": [
            "Canonical jobs and evidence records are heuristic transcript labels.",
            "Acoustic values depend on recording, music, noise, speakers and segmentation.",
            "A nearest frame is not a continuous visual observation and face count is not expression or emotion.",
            "Human review must inspect full sequence, turns, editing, identity and accessibility before any delivery lesson is promoted.",
        ],
        "selected_review_clips": selected,
        "candidates": candidates,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Delivery proxy candidate atlas",
        "",
        "Status: **proxy-backed candidate clips; not delivery validation**.",
        "",
        result["claim_boundary"],
        "",
        f"Coverage: **{result['counts']['candidate_record_count']}** candidate records across **{result['counts']['candidate_video_count']}** videos and **{result['counts']['job_count']}** heuristic jobs; exact evidence alignment **{result['counts']['exact_alignment_count']}**, overlap-only **{result['counts']['overlap_only_count']}**.",
        "",
        "Use the clips below as a human listening/visual-review queue. The values are navigation proxies, not scores.",
        "",
        "| Job | Candidate clips | Proxy observations |",
        "|---|---|---|",
    ]
    for job, items in selected.items():
        clips = []
        observations = []
        for item in items:
            clips.append(f"[{item['video_id']} @ {int(item['start_seconds'])}s]({item['source_url']})")
            audio = item["audio_proxy_summary"]
            observations.append(f"RMS {audio['mean_rms_db']}; W/s {audio['speech_activity_fraction']}; frame face-count {item['nearest_sampled_frame_proxy']['face_count']}")
        lines.append(f"| `{job}` | {'; '.join(clips)} | {' / '.join(observations)} |")
    lines += ["", "## Review checklist", "", "For each selected clip, verify transcript-to-speaker alignment, listen for timing/turns/emphasis, inspect continuous visible action and editing, record missingness/accessibility, and preserve an alternate-function or non-fit explanation. Use the [delivery learning guide](delivery-learning-guide.md) and [validation handoff](validation-handoff.md).", ""]
    OUT_MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT_JSON.relative_to(ROOT)), "counts": result["counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
