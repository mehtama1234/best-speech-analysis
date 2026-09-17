#!/usr/bin/env python3
"""Build baseline corpus statistics without making psychological inferences."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
STOPWORDS = {
    "a", "about", "after", "all", "also", "am", "an", "and", "are", "as", "at", "be", "because", "been", "but", "by", "can", "could", "did", "do", "does", "for", "from", "get", "go", "had", "has", "have", "he", "her", "here", "him", "his", "how", "i", "if", "in", "into", "is", "it", "its", "just", "like", "me", "more", "my", "no", "not", "of", "on", "one", "or", "our", "out", "said", "say", "she", "so", "some", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "to", "too", "up", "us", "was", "we", "were", "what", "when", "where", "which", "who", "will", "with", "would", "you", "your"
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = [json.loads(line) for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines() if line.strip()]
    by_video = {row["video_id"]: row for row in registry}
    per_playlist = defaultdict(lambda: {"memberships": 0, "unique_videos": set(), "transcript_videos": set(), "nonempty_videos": set(), "segments_by_video": {}, "words_by_video": {}})
    all_words = Counter()
    all_bigrams = Counter()
    rows = []

    for video_id, video in by_video.items():
        path = root / "data/transcripts" / f"{video_id}.json"
        payload = json.loads(path.read_text()) if path.exists() else {}
        segments = payload.get("transcript") or []
        text = " ".join(str(segment.get("text", "")) for segment in segments)
        words = [word.lower().replace("’", "'") for word in WORD_RE.findall(text)]
        content_words = [word for word in words if word not in STOPWORDS and len(word) > 2]
        starts = [int(segment.get("startMs", 0)) for segment in segments if str(segment.get("startMs", "")).isdigit()]
        ends = [int(segment.get("endMs", 0)) for segment in segments if str(segment.get("endMs", "")).isdigit()]
        transcript_duration = max(ends) / 1000 if ends else None
        row = {
            "video_id": video_id,
            "title": video.get("title"),
            "channel": video.get("channel"),
            "playlist_memberships": video.get("playlist_memberships", []),
            "transcript_file": path.exists(),
            "segment_count": len(segments),
            "word_count": len(words),
            "transcript_duration_seconds": transcript_duration,
            "approx_words_per_minute": round(len(words) / (transcript_duration / 60), 1) if transcript_duration else None,
        }
        rows.append(row)
        all_words.update(content_words)
        all_bigrams.update(zip(content_words, content_words[1:]))
        for membership in video.get("playlist_memberships", []):
            bucket = per_playlist[membership["source_id"]]
            bucket["memberships"] += 1
            bucket["unique_videos"].add(video_id)
            if path.exists():
                bucket["transcript_videos"].add(video_id)
            if segments:
                bucket["nonempty_videos"].add(video_id)
            bucket["segments_by_video"][video_id] = len(segments)
            bucket["words_by_video"][video_id] = len(words)

    playlist_report = {}
    for source_id, bucket in per_playlist.items():
        playlist_report[source_id] = {
            "memberships": bucket["memberships"],
            "unique_videos": len(bucket["unique_videos"]),
            "transcript_files": len(bucket["transcript_videos"]),
            "nonempty_transcripts": len(bucket["nonempty_videos"]),
            "segments": sum(bucket["segments_by_video"].values()),
            "words": sum(bucket["words_by_video"].values()),
        }

    report = {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "video_count": len(rows),
        "transcript_file_count": sum(row["transcript_file"] for row in rows),
        "nonempty_transcript_count": sum(row["segment_count"] > 0 for row in rows),
        "segment_count": sum(row["segment_count"] for row in rows),
        "word_count": sum(row["word_count"] for row in rows),
        "playlist_summary": playlist_report,
        "top_content_words": [{"term": term, "count": count} for term, count in all_words.most_common(100)],
        "top_content_bigrams": [{"term": " ".join(term), "count": count} for term, count in all_bigrams.most_common(100)],
        "videos": sorted(rows, key=lambda row: row["video_id"]),
    }
    output = root / "research/corpus-overview.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("video_count", "transcript_file_count", "nonempty_transcript_count", "segment_count", "word_count", "playlist_summary")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
