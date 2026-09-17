#!/usr/bin/env python3
"""Create a reproducible coverage report from the video registry and transcript cache."""

from __future__ import annotations

import json
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def classify_payload(payload):
    if not isinstance(payload, dict):
        return 'invalid', []
    value = payload.get('transcript')
    if isinstance(value, list):
        return ('nonempty' if value else 'empty'), value
    if payload.get('notFound') is True:
        return 'provider_not_found', []
    if 'transcript' in payload and value is None:
        return 'null_transcript', []
    return 'invalid', []


def summarize(rows):
    counts = Counter((r['transcript_status'], r['cache_state']) for r in rows)
    return {
        'unique_video_count': len(rows),
        'transcript_file_count': sum(r['transcript_file'] for r in rows),
        'successful_transcript_count': sum(r['transcript_status'] == 'success' for r in rows),
        'failed_transcript_count': sum(r['transcript_status'] == 'failed' for r in rows),
        'status_logged_video_count': sum(r['transcript_status'] != 'unlogged' for r in rows),
        'nonempty_transcript_count': sum(r['cache_state'] == 'nonempty' for r in rows),
        'empty_transcript_count': sum(r['cache_state'] == 'empty' for r in rows),
        'null_transcript_count': sum(r['cache_state'] == 'null_transcript' for r in rows),
        'provider_not_found_count': sum(r['cache_state'] == 'provider_not_found' for r in rows),
        'cached_without_segments_count': sum(r['transcript_file'] and r['cache_state'] != 'nonempty' for r in rows),
        'invalid_transcript_count': sum(r['cache_state'] == 'invalid' for r in rows),
        'missing_transcript_count': sum(r['cache_state'] == 'missing' for r in rows),
        'timestamped_segment_count': sum(r['segment_count'] for r in rows),
        'cached_unlogged_video_ids': [r['video_id'] for r in rows if r['transcript_file'] and r['transcript_status'] == 'unlogged'],
        'unavailable_with_caption_tracks_video_ids': [r['video_id'] for r in rows if r['cache_state'] != 'nonempty' and r.get('caption_tracks')],
        'failed_video_ids': [r['video_id'] for r in rows if r['transcript_status'] == 'failed'],
        'status_cache_cross_tab': [{'status': status, 'cache_state': state, 'video_count': n}
                                 for (status, state), n in sorted(counts.items())],
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = [json.loads(line) for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines() if line.strip()]
    statuses = {}
    status_path = root / "data/metadata/transcript-status.jsonl"
    if status_path.exists():
        statuses = {row["video_id"]: row for row in map(json.loads, status_path.read_text().splitlines()) if row}

    rows = []
    source_hashes = {}
    for p in (root / 'data/metadata/video-registry.jsonl', status_path, Path(__file__).resolve()):
        if p.exists():
            source_hashes[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for video in registry:
        video_id = video["video_id"]
        path = root / "data/transcripts" / f"{video_id}.json"
        payload, state, segments = {}, 'missing', []
        if path.exists():
            raw = path.read_bytes()
            source_hashes[str(path.relative_to(root))] = hashlib.sha256(raw).hexdigest()
            try:
                payload = json.loads(raw)
                state, segments = classify_payload(payload)
            except (ValueError, UnicodeError):
                state = 'invalid'
        rows.append({
            "video_id": video_id,
            "title": video.get("title"),
            "playlist_memberships": video.get("playlist_memberships", []),
            "transcript_file": path.exists(),
            "transcript_status": statuses.get(video_id, {}).get("status", "unlogged"),
            "cache_state": state,
            "provider_success": payload.get('success') if isinstance(payload, dict) else None,
            "provider_not_found": payload.get('notFound') if isinstance(payload, dict) else None,
            "alternate_text_present": bool(payload.get('transcript_only_text')) if isinstance(payload, dict) else False,
            "caption_tracks": [{"language_code": t.get('languageCode'), "kind": t.get('kind')}
                               for t in (payload.get('captionTracks') or []) if isinstance(t, dict)] if isinstance(payload, dict) and isinstance(payload.get('captionTracks', []), list) else [],
            "segment_count": len(segments),
        })

    report = {
        "schema_version": "0.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **summarize(rows),
        "counting_policy": "Success/failure counts refer to latest per-video corpus status records, not all requests or retry attempts. Provider success:true can coexist with transcript:null or notFound:true. An unlogged cache is not an unrequested video. Cache counts and status counts are separate partitions. empty_transcript_count now means an actual empty list; historical reports collapsed null and notFound into empty. Nonempty means a nonempty transcript list, not validated transcript quality or semantic review.",
        "source_sha256": source_hashes,
        "videos": rows,
    }
    output = root / "data/metadata/transcript-coverage.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_sha256', 'videos')}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
