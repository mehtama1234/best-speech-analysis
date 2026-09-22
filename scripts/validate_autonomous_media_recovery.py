#!/usr/bin/env python3
"""Validate fixed-corpus media recovery routing and partial-download boundaries."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def files_for(directory: Path, video_id: str) -> list[Path]:
    return [p for p in directory.glob(f"{video_id}.*") if p.is_file() and p.stat().st_size > 0]


def validate() -> list[str]:
    errors: list[str] = []
    coverage = json.loads((ROOT / "research/full-corpus-media-coverage.json").read_text())
    queue = json.loads((ROOT / "research/full-corpus-media-recovery-queue.json").read_text())
    videos = {x.get("video_id"): x for x in coverage.get("videos", [])}
    items = queue.get("items", [])
    if coverage.get("video_count") != 395 or len(videos) != 395:
        errors.append("media coverage must contain 395 unique videos")
    if queue.get("item_count") != 41 or len(items) != 41:
        errors.append("recovery queue must contain 41 routed items")
    if len({x.get("video_id") for x in items}) != len(items):
        errors.append("recovery queue video IDs are not unique")
    coverage_states = Counter(x.get("media_state") for x in videos.values())
    queue_states = Counter(x.get("media_state") for x in items)
    if queue_states != Counter({"derived_features_only": 5, "transcript_only_no_local_media": 35, "video_only": 1}):
        errors.append(f"unexpected recovery media states: {dict(queue_states)}")
    if sum(coverage_states[state] for state in queue_states) != 41:
        errors.append("recovery queue does not account for its coverage states")
    video_dir, audio_dir = ROOT / "data/video", ROOT / "data/audio"
    for item in items:
        video_id = item.get("video_id")
        state = item.get("media_state")
        coverage_row = videos.get(video_id)
        if not coverage_row or coverage_row.get("media_state") != state:
            errors.append(f"{video_id}: queue/coverage media state mismatch")
        if not item.get("source_url", "").endswith(video_id):
            errors.append(f"{video_id}: source URL does not preserve ID")
        video_files = files_for(video_dir, video_id)
        audio_files = files_for(audio_dir, video_id)
        if item.get("video_download_status") == "downloaded" and not video_files:
            errors.append(f"{video_id}: ledger says video downloaded but no non-empty file exists")
        if item.get("audio_download_status") == "downloaded" and not audio_files:
            errors.append(f"{video_id}: ledger says audio downloaded but no non-empty file exists")
        if state == "derived_features_only" and (video_files or audio_files):
            errors.append(f"{video_id}: feature-only state has unclassified media files")
        if state == "transcript_only_no_local_media" and (video_files or audio_files):
            errors.append(f"{video_id}: transcript-only state has unclassified media files")
        if state == "video_only" and (not video_files or audio_files):
            errors.append(f"{video_id}: video-only state does not match local files")
        if "Recovery routing only" not in item.get("claim_boundary", ""):
            errors.append(f"{video_id}: recovery claim boundary missing")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous media recovery valid: 41 routed records, partial media kept out of raw A/V coverage")
