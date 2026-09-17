#!/usr/bin/env python3
"""Measure conservative frame-to-frame face and scene movement in the pilot."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from build_segment_registry import candidate_functions


def largest_face(frame: dict) -> dict | None:
    faces = frame.get("faces", [])
    return max(faces, key=lambda face: face.get("area_fraction", 0.0), default=None)


def summary(values: list[float]) -> dict:
    return {
        "video_count": len(values),
        "mean": round(mean(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
    }


def nearest_labels(frames: list[dict], rows: list[dict], frame: dict) -> list[str]:
    if not rows:
        return ["unclassified"]
    time = frame["time_seconds"]
    closest = min(rows, key=lambda row: abs(((row["start_seconds"] + row["end_seconds"]) / 2) - time))
    return candidate_functions(closest.get("text", ""))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    per_label_video = defaultdict(lambda: defaultdict(list))
    video_summary = {}
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        frames = sorted(report.get("sampled_frames", []), key=lambda frame: frame["time_seconds"])
        rows = report.get("aligned_transcript", [])
        movements = []
        for previous, current in zip(frames, frames[1:]):
            before = largest_face(previous)
            after = largest_face(current)
            face_move = None
            face_area_change = None
            if before and after:
                face_move = ((before["center_x_fraction"] - after["center_x_fraction"]) ** 2 + (before["center_y_fraction"] - after["center_y_fraction"]) ** 2) ** 0.5
                face_area_change = abs(before["area_fraction"] - after["area_fraction"])
            scene_change = abs(current.get("mean_luminance", 0) - previous.get("mean_luminance", 0))
            measurement = {
                "face_center_movement": face_move,
                "face_area_change": face_area_change,
                "scene_luminance_change": scene_change,
                "face_presence_transition": int(bool(before) != bool(after)),
                "time_seconds": current["time_seconds"],
            }
            movements.append(measurement)
            for label in nearest_labels(frames, rows, current):
                per_label_video[label][report["video_id"]].append(measurement)
        video_summary[report["video_id"]] = {
            "sampled_frame_count": len(frames),
            "face_present_frames": sum(frame.get("face_count", 0) > 0 for frame in frames),
            "movement_pairs": len(movements),
        }

    patterns = {}
    for label, by_video in sorted(per_label_video.items()):
        video_means = {}
        for video_id, measurements in by_video.items():
            video_means[video_id] = {}
            for key in ("face_center_movement", "face_area_change", "scene_luminance_change", "face_presence_transition"):
                values = [m[key] for m in measurements if m[key] is not None]
                video_means[video_id][key] = mean(values) if values else None
        patterns[label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "video_count": len(video_means),
            "video_weighted_metrics": {
                key: summary([row[key] for row in video_means.values() if row[key] is not None])
                for key in ("face_center_movement", "face_area_change", "scene_luminance_change", "face_presence_transition")
            },
        }
    report = {
        "schema_version": "0.1",
        "measurement_policy": "Face geometry and scene-pixel changes only; no emotion or intent inference.",
        "video_summary": video_summary,
        "patterns": patterns,
    }
    output = root / "research/visual-movement-analysis.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Pilot visual movement analysis",
        "",
        "This report measures changes in detected face geometry and scene luminance between sampled frames. It is not facial-expression recognition and does not infer emotion, confidence, or intent. Speech-function labels are heuristic retrieval aids.",
        "",
        "| Candidate label | Videos | Face-center movement | Face-area change | Scene luminance change | Face-presence transitions |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, item in patterns.items():
        metrics = item["video_weighted_metrics"]
        lines.append(f"| `{label}` | {item['video_count']} | {metrics['face_center_movement']['mean']} | {metrics['face_area_change']['mean']} | {metrics['scene_luminance_change']['mean']} | {metrics['face_presence_transition']['mean']} |")
    lines += [
        "",
        "## Limits",
        "",
        "A change in detected face position can result from camera movement, cuts, zoom, tracking error, posture, or actual head movement. The current pilot does not measure hands, posture, gaze direction, or facial muscle action units.",
        "",
    ]
    (root / "writeups/visual-movement-analysis.md").write_text("\n".join(lines))
    print(f"wrote {output} and visual movement report for {len(patterns)} labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
