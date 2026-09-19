#!/usr/bin/env python3
"""Extract bounded MediaPipe pose geometry from existing sampled frames.

The output is observable landmark geometry only.  It does not label gestures,
emotion, confidence, intent, speaker identity or communication effectiveness.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import mediapipe as mp
import numpy as np
from PIL import Image


LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner",
    "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left",
    "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index",
    "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel",
    "right_heel", "left_foot_index", "right_foot_index",
]


def decode_frame(video_path: Path, time_seconds: float):
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", str(time_seconds),
        "-i", str(video_path), "-frames:v", "1", "-f", "image2pipe",
        "-vcodec", "png", "pipe:1",
    ]
    try:
        raw = subprocess.check_output(command, timeout=30)
        return Image.open(io.BytesIO(raw)).convert("RGB")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None


def measure(result, image):
    if not result.pose_landmarks:
        return {
            "person_detected": False,
            "visible_keypoint_count": 0,
            "visible_wrist_count": 0,
            "keypoints": {},
            "observable_geometry_status": "no_pose_landmarks_above_detector_threshold",
        }
    landmarks = {}
    for name, landmark in zip(LANDMARK_NAMES, result.pose_landmarks.landmark):
        visibility = float(landmark.visibility)
        if visibility >= 0.5:
            landmarks[name] = {
                "x_fraction": round(float(landmark.x), 5),
                "y_fraction": round(float(landmark.y), 5),
                "z_relative": round(float(landmark.z), 5),
                "visibility": round(visibility, 5),
            }
    shoulders = [landmarks.get("left_shoulder"), landmarks.get("right_shoulder")]
    shoulder_width = None
    if all(shoulders):
        shoulder_width = abs(shoulders[0]["x_fraction"] - shoulders[1]["x_fraction"])
    return {
        "person_detected": True,
        "visible_keypoint_count": len(landmarks),
        "visible_wrist_count": sum(name in landmarks for name in ("left_wrist", "right_wrist")),
        "shoulder_width_fraction": round(float(shoulder_width), 5) if shoulder_width is not None else None,
        "keypoints": landmarks,
        "observable_geometry_status": "mediapipe_pose_landmark_geometry_only; no_gesture_or_intent_inference",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features-dir", default="data/features")
    parser.add_argument("--video-dir", default="data/video")
    parser.add_argument("--output-dir", default="data/pose-features")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--video-id", action="append", dest="video_ids")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / args.features_dir).glob("*.json"))
    if args.video_ids:
        paths = [path for path in paths if path.stem in set(args.video_ids)]
    if args.limit:
        paths = paths[:args.limit]
    out_dir = root / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    processed = 0
    frame_count = 0
    detected = 0
    with mp.solutions.pose.Pose(
        static_image_mode=True,
        model_complexity=0,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        for path in paths:
            report = json.loads(path.read_text())
            video_id = report["video_id"]
            videos = list((root / args.video_dir).glob(f"{video_id}.*"))
            if not videos:
                continue
            rows = []
            for frame in report.get("sampled_frames", []):
                image = decode_frame(videos[0], float(frame["time_seconds"]))
                if image is None:
                    continue
                result = pose.process(np.asarray(image))
                measurement = measure(result, image)
                rows.append({"time_seconds": frame["time_seconds"], **measurement})
            output = {
                "schema_version": "0.2",
                "video_id": video_id,
                "source_feature_file": str(path.relative_to(root)),
                "model": "MediaPipe Pose model_complexity=0",
                "frame_count": len(rows),
                "person_frame_count": sum(row["person_detected"] for row in rows),
                "frames": rows,
                "measurement_policy": "Observable pose landmark geometry only; no gesture, emotion, confidence, intent, identity or effectiveness inference.",
            }
            (out_dir / f"{video_id}.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
            processed += 1
            frame_count += len(rows)
            detected += output["person_frame_count"]
            print(json.dumps({"video_id": video_id, "frames": len(rows), "person_frames": output["person_frame_count"]}), flush=True)
    print(json.dumps({"processed_reports": processed, "frames": frame_count, "person_frames": detected}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
