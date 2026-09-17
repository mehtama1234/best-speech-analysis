#!/usr/bin/env python3
"""Resumably fetch transcripts for every video in the corpus registry."""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from download_transcripts import load_key


ENDPOINT = "https://api.scrapecreators.com/v1/youtube/video/transcript"


def fetch(video: dict, key: str, language: str, cache_max_age: str, retries: int) -> tuple[str, str, int | str]:
    video_id = video["video_id"]
    url = f"https://www.youtube.com/watch?v={video_id}"
    query = urlencode({"url": url, "language": language, "cache_max_age": cache_max_age})
    request = Request(f"{ENDPOINT}?{query}", headers={"x-api-key": key, "Accept": "application/json"})
    last_error = "unknown error"
    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=90) as response:
                payload = json.load(response)
            return video_id, "success", payload
        except Exception as exc:  # retry transient provider/network errors
            last_error = str(exc)
            if attempt < retries:
                time.sleep(2 ** attempt)
    return video_id, last_error, "failed"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="data/metadata/video-registry.jsonl")
    parser.add_argument("--output-dir", default="data/transcripts")
    parser.add_argument("--status-file", default="data/metadata/transcript-status.jsonl")
    parser.add_argument("--language", default="en")
    parser.add_argument("--cache-max-age", default="30d", choices=["1d", "3d", "7d", "14d", "30d"])
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--key-file", type=Path)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    status_path = Path(args.status_file)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if status_path.exists():
        for line in status_path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["video_id"]] = row

    videos = [json.loads(line) for line in Path(args.registry).read_text().splitlines() if line.strip()]
    pending = [v for v in videos if not (output_dir / f"{v['video_id']}.json").exists()]
    key = load_key(args.key_file)
    print(f"registry={len(videos)} cached={len(videos)-len(pending)} pending={len(pending)} workers={args.workers}", flush=True)

    results = dict(existing)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(fetch, video, key, args.language, args.cache_max_age, args.retries): video
            for video in pending
        }
        for index, future in enumerate(as_completed(futures), start=1):
            video = futures[future]
            video_id, status, payload = future.result()
            if status == "success":
                target = output_dir / f"{video_id}.json"
                target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
                segment_count = len(payload.get("transcript") or [])
                results[video_id] = {"video_id": video_id, "status": "success", "segments": segment_count}
                print(f"[{index}/{len(pending)}] saved {video_id}: {segment_count} segments", flush=True)
            else:
                results[video_id] = {"video_id": video_id, "status": "failed", "error": status}
                print(f"[{index}/{len(pending)}] failed {video_id}: {status}", flush=True)

    with status_path.open("w") as handle:
        for video_id in sorted(results):
            handle.write(json.dumps(results[video_id], ensure_ascii=False) + "\n")
    success = sum(row.get("status") == "success" for row in results.values())
    failed = sum(row.get("status") == "failed" for row in results.values())
    print(f"complete success={success} failed={failed} total={len(videos)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

