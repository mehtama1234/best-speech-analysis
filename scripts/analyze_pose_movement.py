#!/usr/bin/env python3
"""Analyze observable frame-to-frame keypoint movement."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from build_segment_registry import candidate_functions


def displacement(first: dict, second: dict, names: list[str]) -> list[float]:
    values = []
    for name in names:
        left = first.get("keypoints", {}).get(name)
        right = second.get("keypoints", {}).get(name)
        if left and right:
            values.append(math.hypot(left["x_fraction"] - right["x_fraction"], left["y_fraction"] - right["y_fraction"]))
    return values


def stats(values: list[float]) -> dict:
    return {
        "count": len(values),
        "mean": round(mean(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
        "minimum": round(min(values), 5) if values else None,
        "maximum": round(max(values), 5) if values else None,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    by_video = {}
    for path in sorted((root / "data/pose-features").glob("*.json")):
        report = json.loads(path.read_text())
        frames = [frame for frame in report.get("frames", []) if frame.get("person_detected")]
        pairs = []
        for first, second in zip(frames, frames[1:]):
            all_movement = displacement(first, second, list(first.get("keypoints", {})))
            wrist_movement = displacement(first, second, ["left_wrist", "right_wrist"])
            shoulder_movement = displacement(first, second, ["left_shoulder", "right_shoulder"])
            if not all_movement:
                continue
            pairs.append({
                "start_time_seconds": first["time_seconds"],
                "end_time_seconds": second["time_seconds"],
                "midpoint_seconds": round((first["time_seconds"] + second["time_seconds"]) / 2, 3),
                "mean_keypoint_displacement": round(mean(all_movement), 5),
                "mean_wrist_displacement": round(mean(wrist_movement), 5) if wrist_movement else None,
                "mean_shoulder_displacement": round(mean(shoulder_movement), 5) if shoulder_movement else None,
                "keypoint_count": len(all_movement),
            })
        by_video[report["video_id"]] = {
            "sampled_frame_count": len(frames),
            "movement_pair_count": len(pairs),
            "pair_summary": {
                key: stats([pair[key] for pair in pairs if pair.get(key) is not None])
                for key in ["mean_keypoint_displacement", "mean_wrist_displacement", "mean_shoulder_displacement"]
            },
            "pairs": pairs,
        }

    # Join motion intervals to nearby transcript candidates. This is a
    # retrieval aid, not a verified claim that a speech function caused motion.
    label_rows = defaultdict(list)
    join_count = 0
    for video_id, report in by_video.items():
        feature_path = root / "data/features" / f"{video_id}.json"
        if not feature_path.exists():
            continue
        transcript = json.loads(feature_path.read_text()).get("aligned_transcript", [])
        for row in transcript:
            labels = candidate_functions(row.get("text", ""))
            if not labels or not report["pairs"]:
                continue
            pair = min(report["pairs"], key=lambda item: abs(item["midpoint_seconds"] - row["start_seconds"]))
            if abs(pair["midpoint_seconds"] - row["start_seconds"]) > 10:
                continue
            join_count += 1
            for label in labels:
                label_rows[label].append({
                    "video_id": video_id,
                    "evidence_id": row["evidence_id"],
                    "pair_midpoint_seconds": pair["midpoint_seconds"],
                    "frame_offset_seconds": round(pair["midpoint_seconds"] - row["start_seconds"], 3),
                    "mean_keypoint_displacement": pair["mean_keypoint_displacement"],
                    "mean_wrist_displacement": pair["mean_wrist_displacement"],
                    "mean_shoulder_displacement": pair["mean_shoulder_displacement"],
                })

    label_summary = {}
    for label, rows in sorted(label_rows.items()):
        label_summary[label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "joined_example_count": len(rows),
            "distinct_video_count": len({row["video_id"] for row in rows}),
            "metrics": {
                key: stats([row[key] for row in rows if row.get(key) is not None])
                for key in ["mean_keypoint_displacement", "mean_wrist_displacement", "mean_shoulder_displacement"]
            },
            "examples": rows[:20],
        }

    report = {
        "schema_version": "0.1",
        "measurement_policy": "Frame-to-frame keypoint displacement only; no gesture, emotion, emphasis, intent, or mental-state inference.",
        "video_count": len(by_video),
        "movement_pair_count": sum(row["movement_pair_count"] for row in by_video.values()),
        "transcript_motion_join_count": join_count,
        "video_summary": by_video,
        "heuristic_label_summary": label_summary,
    }
    output = root / "research/pose-movement-analysis.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Pose movement analysis",
        "",
        "This report measures frame-to-frame displacement of detected body keypoints. It does not identify gestures or infer emotion, emphasis, confidence, intent, or audience effect. Transcript joins are nearest-time retrieval aids and require manual review.",
        "",
        f"Videos: **{len(by_video)}**; movement pairs: **{report['movement_pair_count']}**; transcript/motion joins: **{join_count}**.",
        "",
        "## Video-level movement",
        "",
        "| Video | Pairs | Mean keypoint displacement | Mean wrist displacement | Mean shoulder displacement |",
        "|---|---:|---:|---:|---:|",
    ]
    for video_id, item in sorted(by_video.items()):
        summary = item["pair_summary"]
        lines.append(f"| `{video_id}` | {item['movement_pair_count']} | {summary['mean_keypoint_displacement']['mean']} | {summary['mean_wrist_displacement']['mean']} | {summary['mean_shoulder_displacement']['mean']} |")
    lines += [
        "",
        "## Heuristic speech-function joins",
        "",
        "| Candidate label | Joins | Videos | Mean keypoint movement | Mean wrist movement | Mean shoulder movement |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, item in label_summary.items():
        metrics = item["metrics"]
        lines.append(f"| `{label}` | {item['joined_example_count']} | {item['distinct_video_count']} | {metrics['mean_keypoint_displacement']['mean']} | {metrics['mean_wrist_displacement']['mean']} | {metrics['mean_shoulder_displacement']['mean']} |")
    lines += [
        "",
        "Movement can come from a speaker, camera motion, cuts, zooms, tracking errors, or scene changes. The measurements therefore require frame inspection and scene controls before they can support a communication principle.",
        "",
    ]
    (root / "writeups/pose-movement-analysis.md").write_text("\n".join(lines))
    print(json.dumps({"videos": len(by_video), "pairs": report["movement_pair_count"], "joins": join_count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
