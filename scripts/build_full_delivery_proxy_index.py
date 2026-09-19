#!/usr/bin/env python3
"""Summarize locally available synchronized delivery-proxy reports."""

from __future__ import annotations

import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURE_DIR = ROOT / "data/features"
QUEUE = ROOT / "research/full-reading-queue.json"
OUT_JSON = ROOT / "research/full-delivery-proxy-index.json"
OUT_MD = ROOT / "writeups/full-delivery-proxy-index.md"


def mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 4) if values else None


def summarize(report: dict, metadata: dict) -> dict:
    windows = report.get("audio_windows", [])
    frames = report.get("sampled_frames", [])
    aligned = report.get("aligned_transcript", [])
    rms = [x["rms_db"] for x in windows if x.get("rms_db") is not None]
    wps = [x["words_per_second_proxy"] for x in aligned if x.get("words_per_second_proxy") is not None]
    activity = [float(x["speech_activity_proxy"]) for x in windows if x.get("speech_activity_proxy") is not None]
    face_counts = [x["face_count"] for x in frames if isinstance(x.get("face_count"), int)]
    face_frames = sum(count > 0 for count in face_counts)
    return {
        "video_id": report["video_id"],
        "title": metadata.get("title", report["video_id"]),
        "source_url": f"https://www.youtube.com/watch?v={report['video_id']}",
        "feature_file": f"data/features/{report['video_id']}.json",
        "audio_duration_seconds": report.get("audio_duration_seconds"),
        "audio_window_count": len(windows),
        "sampled_frame_count": len(frames),
        "aligned_transcript_segment_count": len(aligned),
        "mean_rms_db_proxy": mean(rms),
        "mean_words_per_second_proxy": mean(wps),
        "speech_activity_fraction_proxy": mean(activity),
        "face_count_observable_frame_count": len(face_counts),
        "face_present_frame_count": face_frames,
        "face_presence_fraction_proxy": round(face_frames / len(face_counts), 4) if face_counts else None,
        "mean_face_count_proxy": mean([float(x) for x in face_counts]),
        "visual_measurement_status": report.get("visual_measurement_status"),
        "audio_measurement_status": report.get("audio_measurement_status"),
        "missingness": {
            "has_audio_windows": bool(windows),
            "has_sampled_frames": bool(frames),
            "has_aligned_transcript": bool(aligned),
            "face_detection_available": bool(face_counts),
        },
    }


def main() -> int:
    inventory = json.loads(QUEUE.read_text())
    metadata = {row["video_id"]: row for row in inventory["videos"]}
    reports = []
    for path in sorted(FEATURE_DIR.glob("*.json")):
        reports.append(summarize(json.loads(path.read_text()), metadata.get(path.stem, {})))
    counts = {
        "feature_report_count": len(reports),
        "with_audio_windows": sum(x["missingness"]["has_audio_windows"] for x in reports),
        "with_sampled_frames": sum(x["missingness"]["has_sampled_frames"] for x in reports),
        "with_aligned_transcript": sum(x["missingness"]["has_aligned_transcript"] for x in reports),
        "with_face_detection_counts": sum(x["missingness"]["face_detection_available"] for x in reports),
    }
    result = {
        "schema_version": "1.0",
        "index_id": "full-delivery-proxy-index",
        "status": "proxy_measurement_navigation_not_delivery_validation",
        "claim_boundary": "These are locally generated acoustic, transcript-alignment, frame and face-presence proxies. They do not establish gesture meaning, emotion, intent, speaker identity, audience response, delivery quality or effectiveness.",
        "source": "data/features/*.json",
        "counts": counts,
        "measurement_limits": [
            "RMS, spectral and pitch values are recording- and content-dependent proxies.",
            "Words-per-second and gaps inherit caption timing and alignment errors.",
            "Face detectors report candidates or presence only; they do not infer expression or emotion.",
            "Sampled frames do not establish continuous movement, gaze, gesture or editing context.",
            "Feature availability does not verify speaker/event identity or raw-media alignment.",
        ],
        "videos": reports,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Full delivery proxy index",
        "",
        "Status: **364 locally measured proxy reports; not audiovisual validation**.",
        "",
        result["claim_boundary"],
        "",
        f"Coverage: **{counts['feature_report_count']}** feature reports; audio windows **{counts['with_audio_windows']}**, sampled frames **{counts['with_sampled_frames']}**, aligned transcripts **{counts['with_aligned_transcript']}**, face-detection counts **{counts['with_face_detection_counts']}**.",
        "",
        "Use this index to choose clips for human listening and visual review. Do not rank speakers or infer nonverbal meaning from the summary columns.",
        "",
        "| Video | Audio s | Frames | Aligned captions | Mean RMS proxy | Mean W/s proxy | Face-present frame fraction |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in reports:
        lines.append(
            f"| [{row['title'][:80]}](https://www.youtube.com/watch?v={row['video_id']}) `{row['video_id']}` | {row['audio_duration_seconds']} | {row['sampled_frame_count']} | {row['aligned_transcript_segment_count']} | {row['mean_rms_db_proxy']} | {row['mean_words_per_second_proxy']} | {row['face_presence_fraction_proxy']} |"
        )
    lines += ["", "## Measurement limits", ""] + [f"- {limit}" for limit in result["measurement_limits"]]
    lines += ["", "For human delivery observations and practice, use the [delivery learning guide](delivery-learning-guide.md) and [validation handoff](validation-handoff.md).", ""]
    OUT_MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT_JSON.relative_to(ROOT)), "counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
