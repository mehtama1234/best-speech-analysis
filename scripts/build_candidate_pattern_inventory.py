#!/usr/bin/env python3
"""Aggregate heuristic transcript labels into reviewable candidate patterns."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
if __package__:
    from .source_restrictions import load_restrictions
else:
    from source_restrictions import load_restrictions


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    restrictions = load_restrictions(root)
    excluded = Counter()
    patterns = defaultdict(lambda: {"segments": 0, "videos": set(), "channels": set(), "examples": []})
    for line in (root / "research/segment-registry.jsonl").open():
        row = json.loads(line)
        if row['video_id'] in restrictions:
            excluded[row['video_id']] += 1
            continue
        for label in row["candidate_speech_functions"]:
            item = patterns[label]
            item["segments"] += 1
            item["videos"].add(row["video_id"])
            if row.get("channel"):
                item["channels"].add(row["channel"])
            if len(item["examples"]) < 12:
                item["examples"].append({
                    "evidence_id": row["evidence_id"],
                    "video_id": row["video_id"],
                    "title": row.get("title"),
                    "start_seconds": row["start_seconds"],
                    "end_seconds": row["end_seconds"],
                    "text": row["text"],
                })
    report = {}
    for label, item in sorted(patterns.items()):
        report[label] = {
            "candidate_status": "heuristic_retrieval_aid_requires_manual_review",
            "segment_count": item["segments"],
            "video_count": len(item["videos"]),
            "channel_count": len(item["channels"]),
            "examples": item["examples"],
        }
    output = root / "research/candidate-patterns.json"
    output.write_text(json.dumps({"schema_version": "0.2", "patterns": report,
        "scope": "Heuristic candidates excluding explicitly restricted sources; absence of a restriction is not verification.",
        "excluded_source_segments": dict(sorted(excluded.items())),
        "source_restrictions": restrictions}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({label: {key: value for key, value in item.items() if key != "examples"} for label, item in report.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
