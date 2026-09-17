#!/usr/bin/env python3
"""Summarize observable pose geometry and cautious transcript alignment."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from build_segment_registry import candidate_functions


METRICS = ["visible_keypoint_count", "visible_wrist_count", "shoulder_width_fraction"]


def numeric_summary(values: list[float]) -> dict:
    return {
        "count": len(values),
        "mean": round(mean(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
        "minimum": round(min(values), 5) if values else None,
        "maximum": round(max(values), 5) if values else None,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    pose_reports = {}
    for path in sorted((root / "data/pose-features").glob("*.json")):
        pose_reports[path.stem] = json.loads(path.read_text())

    per_video = {}
    for video_id, report in pose_reports.items():
        frames = report.get("frames", [])
        detected = [frame for frame in frames if frame.get("person_detected")]
        per_video[video_id] = {
            "sampled_frame_count": len(frames),
            "person_detected_frame_count": len(detected),
            "person_detection_fraction": round(len(detected) / len(frames), 5) if frames else None,
            "mean_visible_keypoint_count": numeric_summary([frame["visible_keypoint_count"] for frame in detected]),
            "mean_visible_wrist_count": numeric_summary([frame["visible_wrist_count"] for frame in detected]),
            "mean_shoulder_width_fraction": numeric_summary([frame["shoulder_width_fraction"] for frame in detected if frame.get("shoulder_width_fraction") is not None]),
        }

    # Match a transcript segment to the nearest sampled pose frame only when it
    # is within five seconds. These are retrieval joins, not verified function
    # annotations or claims about what a gesture means.
    by_label = defaultdict(list)
    aligned_join_count = 0
    for video_id, pose_report in pose_reports.items():
        frames = [frame for frame in pose_report.get("frames", []) if frame.get("person_detected")]
        transcript_path = root / "data/features" / f"{video_id}.json"
        if not transcript_path.exists() or not frames:
            continue
        feature_report = json.loads(transcript_path.read_text())
        for row in feature_report.get("aligned_transcript", []):
            candidates = candidate_functions(row.get("text", ""))
            if not candidates:
                continue
            nearest = min(frames, key=lambda frame: abs(frame["time_seconds"] - row["start_seconds"]))
            if abs(nearest["time_seconds"] - row["start_seconds"]) > 5:
                continue
            aligned_join_count += 1
            for label in candidates:
                by_label[label].append({
                    "video_id": video_id,
                    "transcript_evidence_id": row["evidence_id"],
                    "frame_time_seconds": nearest["time_seconds"],
                    "frame_offset_seconds": round(nearest["time_seconds"] - row["start_seconds"], 3),
                    "visible_keypoint_count": nearest["visible_keypoint_count"],
                    "visible_wrist_count": nearest["visible_wrist_count"],
                    "shoulder_width_fraction": nearest.get("shoulder_width_fraction"),
                })

    label_summary = {}
    for label, rows in sorted(by_label.items()):
        label_summary[label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "joined_example_count": len(rows),
            "distinct_video_count": len({row["video_id"] for row in rows}),
            "metrics": {
                metric: numeric_summary([row[metric] for row in rows if row.get(metric) is not None])
                for metric in METRICS
            },
            "examples": rows[:20],
        }

    output = root / "research/pose-geometry-analysis.json"
    report = {
        "schema_version": "0.1",
        "measurement_policy": "Torchvision COCO keypoint geometry only; no gesture, emotion, confidence, intent, or mental-state inference.",
        "pose_video_count": len(pose_reports),
        "pose_frame_count": sum(item["sampled_frame_count"] for item in per_video.values()),
        "transcript_pose_join_count": aligned_join_count,
        "video_summary": per_video,
        "heuristic_label_summary": label_summary,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Pose geometry analysis",
        "",
        "This report measures visible person/keypoint geometry only. It does not identify gestures, emotional expressions, confidence, intent, or meaning. Transcript-to-frame joins are nearest-time retrieval aids and require manual review.",
        "",
        f"Pose records: **{len(pose_reports)}** videos and **{report['pose_frame_count']}** sampled frames; person detections: **{sum(item['person_detected_frame_count'] for item in per_video.values())}**; transcript/frame joins: **{aligned_join_count}**.",
        "",
        "## Video coverage",
        "",
        "| Video | Frames | Person frames | Detection fraction | Mean visible keypoints | Mean visible wrists | Mean shoulder width |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for video_id, item in sorted(per_video.items()):
        lines.append(
            f"| `{video_id}` | {item['sampled_frame_count']} | {item['person_detected_frame_count']} | {item['person_detection_fraction']} | {item['mean_visible_keypoint_count']['mean']} | {item['mean_visible_wrist_count']['mean']} | {item['mean_shoulder_width_fraction']['mean']} |"
        )
    lines += [
        "",
        "## Heuristic speech-function joins",
        "",
        "| Candidate label | Joined examples | Videos | Mean visible keypoints | Mean visible wrists | Mean shoulder width |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, item in label_summary.items():
        metrics = item["metrics"]
        lines.append(
            f"| `{label}` | {item['joined_example_count']} | {item['distinct_video_count']} | {metrics['visible_keypoint_count']['mean']} | {metrics['visible_wrist_count']['mean']} | {metrics['shoulder_width_fraction']['mean']} |"
        )
    lines += [
        "",
        "A difference in keypoint visibility, wrist visibility, or shoulder geometry is an observable difference in sampled frames. It is not evidence of a gesture, emotion, emphasis, persuasion, or audience effect. The next step is manual review of matched frames and expansion beyond four sampled frames per video.",
        "",
    ]
    (root / "writeups/pose-geometry-analysis.md").write_text("\n".join(lines))
    print(json.dumps({"pose_videos": len(pose_reports), "pose_frames": report["pose_frame_count"], "joins": aligned_join_count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
