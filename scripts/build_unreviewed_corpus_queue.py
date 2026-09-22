#!/usr/bin/env python3
"""Build a queue for inventoried videos not in the canonical review queue."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/metadata/video-registry.jsonl"
REVIEW_QUEUE = ROOT / "research/full-reading-queue.json"
OUTPUT = ROOT / "research/unreviewed-corpus-queue.json"


if __name__ == "__main__":
    registry = [json.loads(line) for line in REGISTRY.read_text().splitlines() if line.strip()]
    reviewed = json.loads(REVIEW_QUEUE.read_text())
    reviewed_ids = {row["video_id"] for row in reviewed["videos"]}
    videos = [
        {
            "video_id": row["video_id"],
            "title": row.get("title"),
            "source_url": row.get("source_url") or f"https://www.youtube.com/watch?v={row['video_id']}",
        }
        for row in registry
        if row["video_id"] not in reviewed_ids
    ]
    report = {
        "schema_version": "1.0",
        "status": "inventory_items_without_canonical_full_context_review",
        "source_registry": "data/metadata/video-registry.jsonl",
        "canonical_review_queue": "research/full-reading-queue.json",
        "video_count": len(videos),
        "videos": videos,
        "claim_boundary": "This queue identifies missing canonical review coverage. Media recovery or transcript recovery does not by itself constitute full-context analysis.",
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"unreviewed_video_count": len(videos), "output": str(OUTPUT)}))
