#!/usr/bin/env python3
"""Safely attempt resumable low-resolution A/V recovery for the fixed corpus.

This is a recovery operation only. A downloaded file still requires identity,
alignment and delivery review before it becomes evidence.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def files_for(directory: Path, video_id: str) -> list[Path]:
    return sorted(p for p in directory.glob(f"{video_id}.*") if p.is_file())


def attempt(command: list[str], timeout: int) -> str:
    try:
        subprocess.run(command, check=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "failed:timeout"
    except FileNotFoundError:
        return "failed:missing_yt_dlp"
    except subprocess.CalledProcessError as exc:
        return f"failed:{exc.returncode}"
    return "downloaded"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default="research/full-reading-queue.json")
    parser.add_argument("--status", default="data/full-corpus-media-recovery.jsonl")
    parser.add_argument("--video-dir", default="data/video")
    parser.add_argument("--audio-dir", default="data/audio")
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Skip this many sorted candidates before applying --limit.",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry sources with a recorded failed attempt; skipped by default.",
    )
    args = parser.parse_args()

    queue = json.loads(Path(args.queue).read_text())
    videos = queue.get("videos", queue.get("items", []))
    video_dir, audio_dir = Path(args.video_dir), Path(args.audio_dir)
    video_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    status_path = Path(args.status)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    prior = {}
    if status_path.exists():
        for line in status_path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                prior[row["video_id"]] = row

    candidates = []
    for video in videos:
        video_id = video.get("video_id") or video.get("id")
        url = video.get("url") or video.get("source_url") or f"https://www.youtube.com/watch?v={video_id}"
        row = prior.get(video_id, {"video_id": video_id, "source_url": url})
        if files_for(video_dir, video_id) and files_for(audio_dir, video_id):
            row.update({"video_status": "downloaded", "audio_status": "downloaded", "decision": "cached"})
            prior[video_id] = row
            continue
        if not args.retry_failed and (
            str(row.get("video_status", "")).startswith("failed:")
            or str(row.get("audio_status", "")).startswith("failed:")
        ):
            continue
        candidates.append((video_id, url, row))
    # Complete partial media first: recovering the missing side converts an
    # incomplete record into usable A/V coverage, while all-failed records can
    # remain in the retry pool for later attempts.
    candidates.sort(
        key=lambda item: (
            0 if (files_for(video_dir, item[0]) or files_for(audio_dir, item[0])) else 1,
            item[0],
        )
    )
    if args.offset < 0:
        parser.error("--offset must be non-negative")
    candidates = candidates[args.offset :]
    if args.limit is not None:
        candidates = candidates[: args.limit]

    for video_id, url, row in candidates:
        print(json.dumps({"video_id": video_id, "status": "attempting"}), flush=True)
        video_pattern = str(video_dir / f"{video_id}.%(ext)s")
        audio_pattern = str(audio_dir / f"{video_id}.%(ext)s")
        if not files_for(video_dir, video_id):
            row["video_status"] = attempt([
                "yt-dlp", "--no-playlist", "--no-part", "--retries", "1",
                "--format", "worstvideo[protocol=https]/worstvideo/worst",
                "--output", video_pattern, url,
            ], args.timeout)
        else:
            row["video_status"] = "downloaded"
        if not files_for(audio_dir, video_id):
            row["audio_status"] = attempt([
                "yt-dlp", "--no-playlist", "--no-part", "--retries", "1",
                "--format", "worstaudio[protocol=https]/worstaudio",
                "--output", audio_pattern, url,
            ], args.timeout)
        else:
            row["audio_status"] = "downloaded"
        row["decision"] = "attempted"
        prior[video_id] = row
        print(json.dumps(row), flush=True)

    with status_path.open("w") as handle:
        for video_id in sorted(prior):
            handle.write(json.dumps(prior[video_id], ensure_ascii=False) + "\n")
    attempted = len(candidates)
    recovered = sum(1 for _, _, row in candidates if row.get("video_status") == "downloaded" and row.get("audio_status") == "downloaded")
    print(json.dumps({"attempted": attempted, "recovered_audio_video": recovered, "status_file": str(status_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
