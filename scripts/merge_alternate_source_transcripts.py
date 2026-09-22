#!/usr/bin/env python3
"""Merge alternate-source transcript shards without corpus promotion."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    rows = {}
    for path in sorted((ROOT / "research/alternate-source-parts").glob("part-*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                rows[row["original_video_id"]] = row
    out = ROOT / "research/alternate-source-transcripts.jsonl"
    with out.open("w") as handle:
        for key in sorted(rows):
            handle.write(json.dumps(rows[key], ensure_ascii=False) + "\n")
    print(json.dumps({"records": len(rows), "output": str(out)}))


if __name__ == "__main__":
    main()
