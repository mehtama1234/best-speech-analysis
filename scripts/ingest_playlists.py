#!/usr/bin/env python3
"""Enumerate configured YouTube playlists into a stable, auditable registry."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def enumerate_playlist(url: str) -> dict:
    command = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-single-json",
        url,
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/playlists.json")
    parser.add_argument("--output-dir", default="data/metadata")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text())
    output_dir = Path(args.output_dir)
    snapshots = output_dir / "playlist-snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    registry = {}
    memberships = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    for source in config["sources"]:
        snapshot = enumerate_playlist(source["url"])
        source_id = source["source_id"]
        (snapshots / f"{source_id}.json").write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
        )
        entries = snapshot.get("entries") or []
        for position, entry in enumerate(entries, start=1):
            if not entry or not entry.get("id"):
                continue
            video_id = entry["id"]
            record = registry.setdefault(video_id, {
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": entry.get("title"),
                "duration_seconds": entry.get("duration"),
                "channel": entry.get("channel") or entry.get("uploader"),
                "channel_id": entry.get("channel_id"),
                "uploader_id": entry.get("uploader_id"),
                "availability": entry.get("availability"),
                "live_status": entry.get("live_status"),
                "playlist_memberships": [],
                "transcript_status": "not_requested",
            })
            membership = {
                "source_id": source_id,
                "playlist_title": snapshot.get("title"),
                "position": position,
            }
            record["playlist_memberships"].append(membership)
            memberships.append({"video_id": video_id, **membership})

    registry_path = output_dir / "video-registry.jsonl"
    with registry_path.open("w") as handle:
        for video_id in sorted(registry):
            handle.write(json.dumps(registry[video_id], ensure_ascii=False) + "\n")

    summary = {
        "schema_version": "0.1",
        "fetched_at": fetched_at,
        "playlist_count": len(config["sources"]),
        "membership_count": len(memberships),
        "unique_video_count": len(registry),
        "duplicate_membership_count": len(memberships) - len(registry),
        "playlists": [
            {
                "source_id": source["source_id"],
                "title": next((m["playlist_title"] for m in memberships if m["source_id"] == source["source_id"]), None),
                "video_count": sum(1 for m in memberships if m["source_id"] == source["source_id"]),
            }
            for source in config["sources"]
        ],
    }
    (output_dir / "inventory-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

