#!/usr/bin/env python3
"""Summarize reviewed heuristic-label support and false positives."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from review_evidence import load_annotations, label_supported


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = load_annotations(root)
    by_label = defaultdict(lambda: {"reviewed_occurrences": 0, "supported": 0, "unsupported": 0, "contextual_assistant_review_count": 0, "evidence_ids": []})
    for row in rows:
        for label in row["candidate_labels"]:
            item = by_label[label]
            item["reviewed_occurrences"] += 1
            item["contextual_assistant_review_count"] += "contextual_review_id" in row
            item["supported" if label_supported(row, label) else "unsupported"] += 1
            item["evidence_ids"].append(row["evidence_id"])
    for item in by_label.values():
        item["support_rate"] = round(item["supported"] / item["reviewed_occurrences"], 3)
    report = {
        "schema_version": "0.1",
        "reviewed_example_count": len(rows),
        "contextual_assistant_review_count": sum("contextual_review_id" in row for row in rows),
        "legacy_provenance_only_count": sum("contextual_review_id" not in row for row in rows),
        "review_provenance": "Contextual overrides are assistant transcript-only judgments; remaining legacy reviewer identities are unknown. These counts do not establish independent human validation.",
        "policy": "This is a small review sample, not a validated precision estimate.",
        "by_candidate_label": dict(sorted(by_label.items())),
    }
    output = root / "research/annotation-ledger-audit.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
