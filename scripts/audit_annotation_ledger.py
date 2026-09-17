#!/usr/bin/env python3
"""Summarize reviewed heuristic-label support and false positives."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = [json.loads(line) for line in (root / "research/annotation-ledger.jsonl").read_text().splitlines() if line.strip()]
    by_label = defaultdict(lambda: {"reviewed_occurrences": 0, "supported": 0, "unsupported": 0, "evidence_ids": []})
    for row in rows:
        for label in row["candidate_labels"]:
            item = by_label[label]
            item["reviewed_occurrences"] += 1
            item["supported" if row["candidate_label_supported"] else "unsupported"] += 1
            item["evidence_ids"].append(row["evidence_id"])
    for item in by_label.values():
        item["support_rate"] = round(item["supported"] / item["reviewed_occurrences"], 3)
    report = {
        "schema_version": "0.1",
        "reviewed_example_count": len(rows),
        "policy": "This is a small review sample, not a validated precision estimate.",
        "by_candidate_label": dict(sorted(by_label.items())),
    }
    output = root / "research/annotation-ledger-audit.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

