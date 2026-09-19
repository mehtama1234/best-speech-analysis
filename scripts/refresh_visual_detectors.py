#!/usr/bin/env python3
"""Refresh optional face/scene detector fields on existing sampled frames.

This does not change audio, transcript alignment or frame selection.  Face and
smile detector outputs are geometry/candidate measurements only; they are not
emotion, intent, gaze, confidence or effectiveness findings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from extract_pilot_features import frame_feature


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--video-id", action="append", dest="video_ids")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / "data/features").glob("*.json"))
    if args.video_ids:
        wanted = set(args.video_ids)
        paths = [path for path in paths if path.stem in wanted]
    if args.limit:
        paths = paths[:args.limit]
    refreshed = 0
    frame_count = 0
    unavailable = 0
    for path in paths:
        report = json.loads(path.read_text())
        video_id = report["video_id"]
        video_candidates = list((root / "data/video").glob(f"{video_id}.*"))
        if not video_candidates:
            continue
        rows = []
        for old in report.get("sampled_frames", []):
            row = frame_feature(video_candidates[0], float(old["time_seconds"]))
            if row is None:
                row = old
                unavailable += 1
            rows.append(row)
        report["sampled_frames"] = rows
        report["visual_measurement_status"] = "scene_pixels_plus_optional_haar_geometry; no_emotion_or_intent_inference"
        report["visual_detector_refresh"] = {
            "status": "refreshed_existing_sampled_frames",
            "detector": "OpenCV Haar frontal-face and smile candidate detectors",
            "selection_unchanged": True,
            "claim_boundary": "Detector outputs are observable geometry/candidate counts only; they do not establish emotion, gaze, intent, confidence, delivery meaning or effectiveness.",
        }
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        refreshed += 1
        frame_count += len(rows)
        print(json.dumps({"video_id": video_id, "frames": len(rows), "face_observable": sum(isinstance(x.get("face_count"), int) for x in rows)}), flush=True)
    print(json.dumps({"refreshed_reports": refreshed, "frames": frame_count, "frame_refresh_failures": unavailable}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
