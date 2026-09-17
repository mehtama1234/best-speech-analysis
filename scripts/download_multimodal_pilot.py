#!/usr/bin/env python3
"""Download local-only pilot audio/video streams with resumable status."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/metadata/multimodal-pilot.json")
    parser.add_argument("--audio-dir", default="data/audio")
    parser.add_argument("--video-dir", default="data/video")
    parser.add_argument("--status-file", default="data/media-status.jsonl")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text())
    audio_dir = Path(args.audio_dir)
    video_dir = Path(args.video_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)
    status_path = Path(args.status_file)
    existing = {}
    if status_path.exists():
        existing = {row["video_id"]: row for row in map(json.loads, status_path.read_text().splitlines()) if row.strip()}
    videos = manifest["videos"][:args.limit] if args.limit else manifest["videos"]
    results = dict(existing)

    for video in videos:
        video_id = video["video_id"]
        url = video["url"]
        row = results.setdefault(video_id, {"video_id": video_id, "url": url})
        video_pattern = str(video_dir / f"{video_id}.%(ext)s")
        audio_pattern = str(audio_dir / f"{video_id}.%(ext)s")
        try:
            subprocess.run([
                "yt-dlp", "--no-playlist", "--no-part", "--format", "bestvideo[height<=360][ext=mp4]/bestvideo[height<=360]/worstvideo",
                "--output", video_pattern, url,
            ], check=True)
            row["video_status"] = "downloaded"
        except subprocess.CalledProcessError as exc:
            row["video_status"] = f"failed:{exc.returncode}"
        try:
            subprocess.run([
                "yt-dlp", "--no-playlist", "--no-part", "--format", "bestaudio[ext=m4a]/bestaudio",
                "--output", audio_pattern, url,
            ], check=True)
            row["audio_status"] = "downloaded"
        except subprocess.CalledProcessError as exc:
            row["audio_status"] = f"failed:{exc.returncode}"
        print(json.dumps(row), flush=True)

    with status_path.open("w") as handle:
        for video_id in sorted(results):
            handle.write(json.dumps(results[video_id], ensure_ascii=False) + "\n")
    return 0 if all(row.get("video_status") == "downloaded" and row.get("audio_status") == "downloaded" for row in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

