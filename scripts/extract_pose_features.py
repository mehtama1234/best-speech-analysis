#!/usr/bin/env python3
"""Extract observable human-keypoint geometry from sampled pilot frames.

The detector reports visible person/keypoint geometry only. It does not infer
gestures, emotion, confidence, intent, or meaning. Model weights are obtained
through torchvision's official cache and are not stored in this repository.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import torch
from PIL import Image
from torchvision.models.detection import (
    KeypointRCNN_ResNet50_FPN_Weights,
    keypointrcnn_resnet50_fpn,
)


KEYPOINT_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


def decode_frame(video_path: Path, time_seconds: float) -> Image.Image | None:
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


def prediction_measurement(prediction: dict, image: Image.Image) -> dict:
    scores = prediction.get("scores", torch.empty(0)).detach().cpu().numpy()
    if len(scores) == 0 or float(scores[0]) < 0.7:
        return {
            "person_detected": False,
            "person_score": round(float(scores[0]), 5) if len(scores) else None,
            "image_width": image.width,
            "image_height": image.height,
            "keypoints": {},
            "visible_keypoint_count": 0,
            "visible_wrist_count": 0,
            "observable_geometry_status": "no_person_above_score_threshold",
        }

    keypoints = prediction["keypoints"][0].detach().cpu().numpy()
    box = prediction["boxes"][0].detach().cpu().numpy()
    # KeypointRCNN returns x, y, confidence for each COCO keypoint.
    visible = {}
    for name, (x, y, confidence) in zip(KEYPOINT_NAMES, keypoints):
        if float(confidence) >= 0.5:
            visible[name] = {
                "x_fraction": round(float(x / image.width), 5),
                "y_fraction": round(float(y / image.height), 5),
                "confidence": round(float(confidence), 5),
            }

    shoulders = [visible.get("left_shoulder"), visible.get("right_shoulder")]
    shoulder_width = None
    if all(shoulders):
        shoulder_width = abs(shoulders[0]["x_fraction"] - shoulders[1]["x_fraction"])
    return {
        "person_detected": True,
        "person_score": round(float(scores[0]), 5),
        "person_box": {
            "x_min_fraction": round(float(box[0] / image.width), 5),
            "y_min_fraction": round(float(box[1] / image.height), 5),
            "x_max_fraction": round(float(box[2] / image.width), 5),
            "y_max_fraction": round(float(box[3] / image.height), 5),
        },
        "image_width": image.width,
        "image_height": image.height,
        "keypoints": visible,
        "visible_keypoint_count": len(visible),
        "visible_wrist_count": sum(name in visible for name in ("left_wrist", "right_wrist")),
        "shoulder_width_fraction": round(float(shoulder_width), 5) if shoulder_width is not None else None,
        "observable_geometry_status": "keypoint_geometry_only; no_gesture_or_intent_inference",
    }


def frame_measurements(model, transform, images: list[Image.Image], device: torch.device) -> list[dict]:
    tensors = [transform(image).to(device) for image in images]
    with torch.inference_mode():
        predictions = model(tensors)
    return [prediction_measurement(prediction, image) for prediction, image in zip(predictions, images)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features-dir", default="data/features")
    parser.add_argument("--video-dir", default="data/video")
    parser.add_argument("--output-dir", default="data/pose-features")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--frame-limit", type=int)
    parser.add_argument("--batch-size", type=int, default=4)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    feature_paths = sorted((root / args.features_dir).glob("*.json"))
    if args.limit:
        feature_paths = feature_paths[:args.limit]
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    torch.set_num_threads(min(8, os.cpu_count() or 1))
    weights = KeypointRCNN_ResNet50_FPN_Weights.DEFAULT
    model = keypointrcnn_resnet50_fpn(weights=weights, min_size=320, max_size=640).eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    transform = weights.transforms()
    print(json.dumps({"device": str(device), "video_count": len(feature_paths)}), flush=True)

    for feature_path in feature_paths:
        report = json.loads(feature_path.read_text())
        video_id = report["video_id"]
        video_candidates = list((root / args.video_dir).glob(f"{video_id}.*"))
        if not video_candidates:
            continue
        sampled_frames = report.get("sampled_frames", [])
        if args.frame_limit:
            if len(sampled_frames) > args.frame_limit:
                indices = np.linspace(0, len(sampled_frames) - 1, args.frame_limit, dtype=int)
                sampled_frames = [sampled_frames[index] for index in sorted(set(indices))]
            else:
                sampled_frames = sampled_frames[:args.frame_limit]
        rows = []
        for start in range(0, len(sampled_frames), args.batch_size):
            batch = sampled_frames[start:start + args.batch_size]
            images = []
            valid_frames = []
            for frame in batch:
                image = decode_frame(video_candidates[0], float(frame["time_seconds"]))
                if image is not None:
                    images.append(image)
                    valid_frames.append(frame)
            measurements = frame_measurements(model, transform, images, device) if images else []
            for frame, measurement in zip(valid_frames, measurements):
                rows.append({
                    "time_seconds": frame["time_seconds"],
                    **measurement,
                })
        output = {
            "schema_version": "0.1",
            "video_id": video_id,
            "source_feature_file": str(feature_path.relative_to(root)),
            "model": "torchvision Keypoint R-CNN ResNet-50 FPN COCO weights",
            "measurement_policy": "Observable person/keypoint geometry only; no gesture, emotion, confidence, intent, or mental-state inference.",
            "frame_count": len(rows),
            "frames": rows,
        }
        (output_dir / f"{video_id}.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"video_id": video_id, "frames": len(rows), "person_frames": sum(row["person_detected"] for row in rows)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
