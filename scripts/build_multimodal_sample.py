#!/usr/bin/env python3
"""Choose a deterministic, stratified sample for audio/video measurements."""

from __future__ import annotations

import hashlib
import json
import argparse
from collections import defaultdict
from pathlib import Path


def bucket(duration: int | None) -> str:
    if duration is None:
        return "unknown_duration"
    if duration <= 180:
        return "short_0_3m"
    if duration <= 600:
        return "medium_3_10m"
    return "long_over_10m"


def rank(video: dict) -> str:
    return hashlib.sha256(video["video_id"].encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--per-bucket",
        type=int,
        default=4,
        help="Maximum deterministic selections per duration bucket per playlist.",
    )
    parser.add_argument(
        "--output",
        default="data/metadata/multimodal-pilot.json",
        help="Manifest path to write.",
    )
    parser.add_argument(
        "--media-status",
        default="data/media-status.jsonl",
        help="Optional existing media status file to merge into the manifest.",
    )
    args = parser.parse_args()
    if args.per_bucket < 1:
        parser.error("--per-bucket must be at least 1")
    root = Path(__file__).resolve().parents[1]
    videos = [json.loads(line) for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines() if line.strip()]
    transcript_status = {}
    status_path = root / "data/metadata/transcript-status.jsonl"
    if status_path.exists():
        transcript_status = {row["video_id"]: row for row in map(json.loads, status_path.read_text().splitlines()) if row}
    sources = json.loads((root / "config/playlists.json").read_text())["sources"]
    source_ids = [source["source_id"] for source in sources]
    selected: dict[str, dict] = {}

    # Preserve the user-provided seed examples in the multimodal pilot.
    seed_ids = {source["seed_video_url"].split("v=", 1)[1] for source in sources}
    for video in videos:
        if video["video_id"] in seed_ids:
            selected[video["video_id"]] = {"video": video, "selection_reasons": ["user_seed"]}

    # Select up to N videos per duration bucket per playlist. Overlaps are
    # intentionally deduplicated while retaining all playlist memberships.
    for source_id in source_ids:
        candidates = [video for video in videos if any(m["source_id"] == source_id for m in video.get("playlist_memberships", []))]
        bins = defaultdict(list)
        for video in candidates:
            bins[bucket(video.get("duration_seconds"))].append(video)
        for duration_bucket, members in sorted(bins.items()):
            for video in sorted(members, key=rank)[:args.per_bucket]:
                row = selected.setdefault(video["video_id"], {"video": video, "selection_reasons": []})
                row["selection_reasons"].append(f"{source_id}:{duration_bucket}")

    media_status = {}
    media_status_path = root / args.media_status
    if media_status_path.exists():
        media_status = {
            row["video_id"]: row
            for line in media_status_path.read_text().splitlines()
            if line.strip()
            for row in [json.loads(line)]
        }

    output = root / args.output
    rows = []
    for video_id in sorted(selected):
        video = selected[video_id]["video"]
        status = transcript_status.get(video_id, {})
        rows.append({
            "video_id": video_id,
            "url": video["url"],
            "title": video.get("title"),
            "channel": video.get("channel"),
            "duration_seconds": video.get("duration_seconds"),
            "duration_bucket": bucket(video.get("duration_seconds")),
            "playlist_memberships": video.get("playlist_memberships", []),
            "transcript_status": status.get("status", "not_requested"),
            "transcript_segments": status.get("segments", 0),
            "selection_reasons": sorted(set(selected[video_id]["selection_reasons"])),
            "media_status": media_status.get(video["video_id"], {}).get("status", "not_requested"),
            "video_status": media_status.get(video["video_id"], {}).get("video_status", "not_requested"),
            "audio_status": media_status.get(video["video_id"], {}).get("audio_status", "not_requested"),
        })
    report = {
        "schema_version": "0.1",
        "selection_policy": f"User seeds plus deterministic stratified selection: up to {args.per_bucket} videos per duration bucket per playlist, deduplicated by video ID.",
        "selection_parameters": {"per_bucket": args.per_bucket},
        "video_count": len(rows),
        "videos": rows,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"video_count": len(rows), "duration_buckets": {key: sum(row["duration_bucket"] == key for row in rows) for key in sorted({row["duration_bucket"] for row in rows})}, "transcript_status": {key: sum(row["transcript_status"] == key for row in rows) for key in sorted({row["transcript_status"] for row in rows})}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
