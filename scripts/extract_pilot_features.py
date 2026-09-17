#!/usr/bin/env python3
"""Extract synchronized, directly measurable pilot audio/video features.

This extractor deliberately reports acoustic and scene measurements, not
emotion, confidence, honesty, or personality. Facial-expression analysis is
marked unavailable unless a separately validated face model is installed.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import cv2
from PIL import Image
from scipy.signal import welch


SAMPLE_RATE = 16_000
WINDOW_SECONDS = 1.0


def decode_audio(path: Path) -> np.ndarray:
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(path),
        "-f", "f32le", "-ac", "1", "-ar", str(SAMPLE_RATE), "pipe:1",
    ]
    raw = subprocess.check_output(command)
    return np.frombuffer(raw, dtype=np.float32)


def audio_windows(samples: np.ndarray) -> list[dict]:
    width = int(SAMPLE_RATE * WINDOW_SECONDS)
    rows = []
    for start in range(0, len(samples), width):
        chunk = samples[start:start + width]
        if len(chunk) < SAMPLE_RATE * 0.1:
            continue
        rms = float(np.sqrt(np.mean(np.square(chunk)) + 1e-12))
        centered = chunk - np.mean(chunk)
        zcr = float(np.mean(np.abs(np.diff(np.signbit(centered)))))
        frequencies, power = welch(chunk, fs=SAMPLE_RATE, nperseg=min(2048, len(chunk)))
        power_sum = float(np.sum(power) + 1e-12)
        centroid = float(np.sum(frequencies * power) / power_sum)
        # This is a coarse fundamental-frequency proxy, not a validated pitch
        # tracker. Restricting the spectral peak to a voice-like band makes the
        # measurement useful for broad comparisons while keeping its limits
        # explicit for music, noise, and overlapping speakers.
        pitch_mask = (frequencies >= 60.0) & (frequencies <= 400.0)
        pitch_power = power[pitch_mask]
        pitch_frequencies = frequencies[pitch_mask]
        pitch_index = int(np.argmax(pitch_power)) if len(pitch_power) else 0
        pitch_hz = float(pitch_frequencies[pitch_index]) if len(pitch_frequencies) else None
        pitch_confidence = float(np.max(pitch_power) / (np.sum(pitch_power) + 1e-12)) if len(pitch_power) else None
        rows.append({
            "start_seconds": round(start / SAMPLE_RATE, 3),
            "end_seconds": round((start + len(chunk)) / SAMPLE_RATE, 3),
            "rms": rms,
            "rms_db": round(20 * np.log10(rms + 1e-6), 3),
            "zero_crossing_rate": zcr,
            "spectral_centroid_hz": round(centroid, 3),
            "speech_activity_proxy": rms > 0.01,
            "pitch_hz_proxy": round(pitch_hz, 3) if pitch_hz is not None and rms > 0.01 else None,
            "pitch_confidence_proxy": round(pitch_confidence, 5) if pitch_confidence is not None and rms > 0.01 else None,
        })
    return rows


def frame_feature(video_path: Path, time_seconds: float) -> dict | None:
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", str(time_seconds),
        "-i", str(video_path), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1",
    ]
    try:
        raw = subprocess.check_output(command, timeout=30)
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        pixels = np.asarray(image, dtype=np.float32)
        gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        smile_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
        face_records = []
        smile_candidates = 0
        for x, y, width, height in faces:
            roi = gray[y:y + height, x:x + width]
            smiles = smile_detector.detectMultiScale(roi, scaleFactor=1.7, minNeighbors=20, minSize=(12, 12))
            smile_candidates += len(smiles)
            face_records.append({
                "x": int(x), "y": int(y), "width": int(width), "height": int(height),
                "center_x_fraction": round(float((x + width / 2) / image.width), 4),
                "center_y_fraction": round(float((y + height / 2) / image.height), 4),
                "area_fraction": round(float(width * height / (image.width * image.height)), 5),
            })
        return {
            "time_seconds": round(time_seconds, 3),
            "width": image.width,
            "height": image.height,
            "mean_luminance": round(float(np.mean(pixels)), 3),
            "luminance_std": round(float(np.std(pixels)), 3),
            "mean_red": round(float(np.mean(pixels[:, :, 0])), 3),
            "mean_green": round(float(np.mean(pixels[:, :, 1])), 3),
            "mean_blue": round(float(np.mean(pixels[:, :, 2])), 3),
            "faces": face_records,
            "face_count": len(face_records),
            "smile_detector_candidate_count": smile_candidates,
            "face_measurement_status": "haar_face_and_smile_candidates_only; no_emotion_inference",
        }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None


def aligned_transcript(video_id: str, root: Path, windows: list[dict]) -> list[dict]:
    payload = json.loads((root / "data/transcripts" / f"{video_id}.json").read_text())
    segments = payload.get("transcript") or []
    rows = []
    parsed = []
    for segment in segments:
        start = float(segment.get("startMs", 0)) / 1000
        end = float(segment.get("endMs", start * 1000)) / 1000
        parsed.append((start, end, " ".join(str(segment.get("text", "")).split())))
    for ordinal, (start, end, text) in enumerate(parsed):
        overlaps = [window for window in windows if window["end_seconds"] > start and window["start_seconds"] < end]
        word_count = len(text.split())
        previous_end = parsed[ordinal - 1][1] if ordinal else None
        next_start = parsed[ordinal + 1][0] if ordinal + 1 < len(parsed) else None
        gap_before = max(0.0, start - previous_end) if previous_end is not None else None
        gap_after = max(0.0, next_start - end) if next_start is not None else None
        rows.append({
            "evidence_id": f"{video_id}:{ordinal:05d}",
            "video_id": video_id,
            "start_seconds": round(start, 3),
            "end_seconds": round(end, 3),
            "text": text,
            "word_count": word_count,
            "words_per_second_proxy": round(word_count / max(end - start, 0.001), 3),
            "transcript_gap_before_seconds": round(gap_before, 3) if gap_before is not None else None,
            "transcript_gap_after_seconds": round(gap_after, 3) if gap_after is not None else None,
            "audio_window_count": len(overlaps),
            "mean_rms_db": round(float(np.mean([x["rms_db"] for x in overlaps])), 3) if overlaps else None,
            "speech_activity_fraction": round(float(np.mean([x["speech_activity_proxy"] for x in overlaps])), 3) if overlaps else None,
            "mean_zero_crossing_rate": round(float(np.mean([x["zero_crossing_rate"] for x in overlaps])), 5) if overlaps else None,
            "mean_spectral_centroid_hz": round(float(np.mean([x["spectral_centroid_hz"] for x in overlaps])), 3) if overlaps else None,
            "mean_pitch_hz_proxy": round(float(np.mean([x["pitch_hz_proxy"] for x in overlaps if x.get("pitch_hz_proxy") is not None])), 3) if any(x.get("pitch_hz_proxy") is not None for x in overlaps) else None,
            "mean_pitch_confidence_proxy": round(float(np.mean([x["pitch_confidence_proxy"] for x in overlaps if x.get("pitch_confidence_proxy") is not None])), 5) if any(x.get("pitch_confidence_proxy") is not None for x in overlaps) else None,
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/media-status.jsonl")
    parser.add_argument("--output-dir", default="data/features")
    parser.add_argument("--frame-step", type=float, default=10.0)
    parser.add_argument("--reuse-frames", action="store_true", help="Keep existing sampled frames while refreshing audio/transcript features.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    statuses = [json.loads(line) for line in Path(args.manifest).read_text().splitlines() if line.strip()]
    for status in statuses:
        video_id = status["video_id"]
        audio_candidates = list((root / "data/audio").glob(f"{video_id}.*"))
        video_candidates = list((root / "data/video").glob(f"{video_id}.*"))
        if not audio_candidates or not video_candidates:
            continue
        samples = decode_audio(audio_candidates[0])
        windows = audio_windows(samples)
        duration = len(samples) / SAMPLE_RATE
        existing_report = output_dir / f"{video_id}.json"
        existing_frames = []
        if args.reuse_frames and existing_report.exists():
            existing_frames = json.loads(existing_report.read_text()).get("sampled_frames", [])
        frames = existing_frames
        if not frames:
            for time_seconds in np.arange(0, duration, args.frame_step):
                feature = frame_feature(video_candidates[0], float(time_seconds))
                if feature:
                    frames.append(feature)
        report = {
            "schema_version": "0.2",
            "video_id": video_id,
            "audio_source": str(audio_candidates[0].relative_to(root)),
            "video_source": str(video_candidates[0].relative_to(root)),
            "audio_sample_rate": SAMPLE_RATE,
            "audio_duration_seconds": round(duration, 3),
            "audio_windows": windows,
            "aligned_transcript": aligned_transcript(video_id, root, windows),
            "sampled_frames": frames,
            "visual_measurement_status": "scene_pixel_features_only; face_expression_not_analyzed",
            "audio_measurement_status": "rms_zcr_spectral_centroid_and_coarse_spectral_pitch_proxy; not_a_validated_pitch_tracker",
        }
        (output_dir / f"{video_id}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(f"saved {video_id}: {len(windows)} audio windows, {len(frames)} frames", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
