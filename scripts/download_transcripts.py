#!/usr/bin/env python3
"""Download timestamped YouTube transcripts through ScrapeCreators.

The client accepts either SCRAPECREATORS_API_KEY or a raw-token file. The
workspace's existing /home/mehtama1/git-repo/.env is intentionally supported
because it contains the credential as a single line rather than KEY=value.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


ENDPOINT = "https://api.scrapecreators.com/v1/youtube/video/transcript"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,}$")


def video_id(value: str) -> str:
    value = value.strip()
    if VIDEO_ID_RE.fullmatch(value):
        return value
    parsed = urlparse(value)
    query_id = parse_qs(parsed.query).get("v", [None])[0]
    if query_id and VIDEO_ID_RE.fullmatch(query_id):
        return query_id
    if parsed.path.startswith("/shorts/"):
        candidate = parsed.path.split("/", 2)[2]
        if VIDEO_ID_RE.fullmatch(candidate):
            return candidate
    raise ValueError(f"Could not identify a YouTube video ID from: {value}")


def load_key(raw_file: Path | None) -> str:
    value = os.environ.get("SCRAPECREATORS_API_KEY", "").strip()
    if value:
        return value
    candidates = [raw_file] if raw_file else []
    candidates.append(Path(__file__).resolve().parents[2] / ".env")
    for path in candidates:
        if not path or not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("SCRAPECREATORS_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
            if "=" not in line:
                return line
    raise RuntimeError("No ScrapeCreators key found in SCRAPECREATORS_API_KEY or the raw token file")


def fetch(url: str, key: str, language: str, cache_max_age: str) -> dict:
    query = f"url={url}&language={language}&cache_max_age={cache_max_age}"
    request = Request(
        f"{ENDPOINT}?{query}",
        headers={"x-api-key": key, "Accept": "application/json"},
    )
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="YouTube video URLs or IDs")
    parser.add_argument("--output-dir", default="data/transcripts")
    parser.add_argument("--language", default="en")
    parser.add_argument("--cache-max-age", default="30d", choices=["1d", "3d", "7d", "14d", "30d"])
    parser.add_argument("--key-file", type=Path)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    args = parser.parse_args()

    key = load_key(args.key_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for raw in args.urls:
        try:
            identifier = video_id(raw)
            output = output_dir / f"{identifier}.json"
            if output.exists():
                print(f"cached {identifier}")
                continue
            canonical_url = f"https://www.youtube.com/watch?v={identifier}"
            payload = fetch(canonical_url, key, args.language, args.cache_max_age)
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            count = len(payload.get("transcript") or [])
            print(f"saved {identifier}: {count} segments")
            if args.sleep_seconds:
                time.sleep(args.sleep_seconds)
        except Exception as exc:  # preserve the batch and report each failure
            failures += 1
            print(f"failed {raw}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

