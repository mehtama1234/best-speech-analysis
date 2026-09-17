#!/usr/bin/env python3
"""Create a reproducible coverage report from the video registry and transcript cache."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = [json.loads(line) for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines() if line.strip()]
    statuses = {}
    status_path = root / "data/metadata/transcript-status.jsonl"
    if status_path.exists():
        statuses = {row["video_id"]: row for row in map(json.loads, status_path.read_text().splitlines()) if row}

    rows = []
    for video in registry:
        video_id = video["video_id"]
        path = root / "data/transcripts" / f"{video_id}.json"
        payload = json.loads(path.read_text()) if path.exists() else {}
        rows.append({
            "video_id": video_id,
            "title": video.get("title"),
            "playlist_memberships": video.get("playlist_memberships", []),
            "transcript_file": path.exists(),
            "transcript_status": statuses.get(video_id, {}).get("status", "not_requested"),
            "segment_count": len(payload.get("transcript") or []),
        })

    report = {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "unique_video_count": len(rows),
        "transcript_file_count": sum(row["transcript_file"] for row in rows),
        "successful_transcript_count": sum(row["transcript_status"] == "success" for row in rows),
        "failed_transcript_count": sum(row["transcript_status"] == "failed" for row in rows),
        "nonempty_transcript_count": sum(row["segment_count"] > 0 for row in rows),
        "empty_transcript_count": sum(row["transcript_file"] and row["segment_count"] == 0 for row in rows),
        "timestamped_segment_count": sum(row["segment_count"] for row in rows),
        "failed_video_ids": [row["video_id"] for row in rows if row["transcript_status"] == "failed"],
    }
    output = root / "data/metadata/transcript-coverage.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

