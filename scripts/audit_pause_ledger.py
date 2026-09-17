#!/usr/bin/env python3
"""Summarize reviewed pause examples and their confounds."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = [json.loads(line) for line in (root / "research/pause-review-ledger.jsonl").read_text().splitlines() if line.strip()]
    report = {
        "schema_version": "0.1",
        "reviewed_pause_example_count": len(rows),
        "confidence_counts": Counter(row["confidence"] for row in rows),
        "context_counts": Counter(row["reviewed_context"] for row in rows),
        "policy": "Small qualitative review; measured silence is not assumed to be intentional rhetoric.",
        "examples": rows,
    }
    report["confidence_counts"] = dict(report["confidence_counts"])
    report["context_counts"] = dict(report["context_counts"])
    (root / "research/pause-review-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# Reviewed pause examples", "", "The pilot contains measurable low-energy gaps, but context determines whether a gap is plausibly rhetorical. This review records film edits, dialogue turns, caption boundaries, and stage handoffs as confounds.", "", "| Evidence | Context | Pause before | Confidence | Interpretation |", "|---|---|---:|---|---|"]
    for row in rows:
        lines.append(f"| `{row['evidence_id']}` | {row['reviewed_context']} | {row['pause_before_seconds']}s | {row['confidence']} | {row['pause_interpretation']} |")
    (root / "writeups/reviewed-pause-examples.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({key: report[key] for key in ("reviewed_pause_example_count", "confidence_counts", "context_counts")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

