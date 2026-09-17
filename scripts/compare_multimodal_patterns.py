#!/usr/bin/env python3
"""Compare pilot acoustic/visual measurements by heuristic speech function."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from build_segment_registry import candidate_functions


METRICS = ["mean_rms_db", "speech_activity_fraction", "mean_zero_crossing_rate", "mean_spectral_centroid_hz"]


def summary(values: list[float]) -> dict:
    return {
        "video_count": len(values),
        "mean": round(mean(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
        "minimum": round(min(values), 5) if values else None,
        "maximum": round(max(values), 5) if values else None,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    per_label_video: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    visual = {}
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        video_id = report["video_id"]
        frames = report.get("sampled_frames", [])
        face_frames = [frame for frame in frames if frame.get("face_count", 0) > 0]
        areas = [face["area_fraction"] for frame in face_frames for face in frame.get("faces", [])]
        visual[video_id] = {
            "sampled_frame_count": len(frames),
            "face_detected_frame_count": len(face_frames),
            "face_detection_fraction": round(len(face_frames) / len(frames), 5) if frames else None,
            "mean_face_area_fraction": round(mean(areas), 5) if areas else None,
            "smile_detector_candidate_count": sum(frame.get("smile_detector_candidate_count", 0) for frame in frames),
        }
        for row in report.get("aligned_transcript", []):
            labels = candidate_functions(row.get("text", ""))
            for label in labels:
                per_label_video[label][video_id].append(row)

    patterns = {}
    for label, by_video in sorted(per_label_video.items()):
        video_rows = {}
        for video_id, rows in by_video.items():
            video_rows[video_id] = {
                metric: mean([row[metric] for row in rows if row.get(metric) is not None])
                for metric in METRICS
            }
            video_rows[video_id]["segment_count"] = len(rows)
        patterns[label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "video_count": len(video_rows),
            "segment_count": sum(row["segment_count"] for row in video_rows.values()),
            "video_weighted_metrics": {
                metric: summary([row[metric] for row in video_rows.values() if row[metric] is not None])
                for metric in METRICS
            },
            "per_video": video_rows,
        }

    visual_values = {video_id: row for video_id, row in visual.items()}
    output = root / "research/multimodal-pattern-comparison.json"
    output.write_text(json.dumps({
        "schema_version": "0.1",
        "pilot_video_count": len(visual_values),
        "measurement_policy": "Video-weighted summaries; heuristic labels are retrieval aids, not verified speech-function annotations.",
        "patterns": patterns,
        "visual_video_level": visual_values,
    }, ensure_ascii=False, indent=2) + "\n")

    markdown = [
        "# Pilot multimodal pattern comparison",
        "",
        "This report compares directly measured pilot features against heuristic transcript markers. It does not establish general speech principles. Labels must be manually reviewed, and all face measurements are detector outputs rather than emotion judgments.",
        "",
        f"Pilot videos: **{len(visual_values)}**",
        "",
        "## Acoustic comparison",
        "",
        "| Candidate label | Videos | Segments | Mean RMS dB | Speech activity | Zero-crossing rate | Spectral centroid Hz |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, item in patterns.items():
        rms = item["video_weighted_metrics"]["mean_rms_db"]["mean"]
        activity = item["video_weighted_metrics"]["speech_activity_fraction"]["mean"]
        zcr = item["video_weighted_metrics"]["mean_zero_crossing_rate"]["mean"]
        centroid = item["video_weighted_metrics"]["mean_spectral_centroid_hz"]["mean"]
        markdown.append(f"| `{label}` | {item['video_count']} | {item['segment_count']} | {rms} | {activity} | {zcr} | {centroid} |")
    markdown += [
        "",
        "## Visual coverage",
        "",
        "Visual results currently describe face detection and geometry only. They do not identify emotional expression.",
        "",
        "| Video | Sampled frames | Frames with detected face | Detection fraction | Mean face area | Smile candidates |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for video_id, item in sorted(visual.items()):
        markdown.append(f"| `{video_id}` | {item['sampled_frame_count']} | {item['face_detected_frame_count']} | {item['face_detection_fraction']} | {item['mean_face_area_fraction']} | {item['smile_detector_candidate_count']} |")
    markdown += [
        "",
        "## Interpretation boundary",
        "",
        "A difference in loudness, spectral centroid, speech activity, face visibility, or face position is an observation. It is not evidence by itself of confidence, emotion, persuasion, honesty, or comprehension. The next research step is manual review of timestamped examples and counterexamples, followed by better speech-function annotation.",
        "",
    ]
    report_path = root / "writeups/multimodal-pattern-comparison.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(markdown))
    print(f"wrote {output} and {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

