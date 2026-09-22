#!/usr/bin/env python3
"""Merge parallel recovered-audio shards into the canonical candidate ledger."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    rows = {}
    for path in sorted((ROOT / "research/recovered-audio-parts").glob("part-*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                rows[row["video_id"]] = row
    out = ROOT / "research/recovered-audio-transcripts.jsonl"
    with out.open("w") as handle:
        for video_id in sorted(rows):
            handle.write(json.dumps(rows[video_id], ensure_ascii=False) + "\n")
    print(json.dumps({"shards": len(list((ROOT / 'research/recovered-audio-parts').glob('part-*.jsonl'))), "records": len(rows), "output": str(out)}))


if __name__ == "__main__":
    main()
