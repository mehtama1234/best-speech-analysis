#!/usr/bin/env python3
"""Reconcile parseable pattern arrays from a preserved local-model receipt.

This performs structural recovery only. It never invents or edits a model
judgment; raw output remains preserved in the original receipt.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/local-llm-recovered-pattern-screen.json"
OUT = ROOT / "research/local-llm-recovered-pattern-screen-reconciled.json"
MD = ROOT / "writeups/local-llm-recovered-pattern-screen-reconciled.md"


def extract_patterns(raw: str) -> list[dict]:
    marker = raw.find('"patterns"')
    if marker < 0:
        return []
    start = raw.find("[", marker)
    if start < 0:
        return []
    try:
        value, _ = json.JSONDecoder().raw_decode(raw[start:])
    except json.JSONDecodeError:
        return []
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def main() -> int:
    source = json.loads(SOURCE.read_text())
    reports = []
    all_entries = []
    for batch in source.get("batch_reports", []):
        existing = (batch.get("parsed_judgment") or {}).get("patterns", [])
        recovered = extract_patterns(batch.get("raw_output", ""))
        merged = {}
        for item in existing + recovered:
            pattern_id = item.get("pattern_id")
            if pattern_id:
                merged[pattern_id] = item
        patterns = list(merged.values())
        reports.append({
            "batch_number": batch.get("batch_number"),
            "pattern_ids": batch.get("pattern_ids", []),
            "parsed_judgment": {"patterns": patterns} if patterns else None,
            "raw_output": batch.get("raw_output", ""),
            "structural_recovery_added_count": max(0, len(patterns) - len(existing)),
        })
        all_entries.extend(patterns)
    by_id = {item["pattern_id"]: item for item in all_entries if item.get("pattern_id")}
    report = dict(source)
    report.update({
        "status": "local_model_recovered_pattern_triage_structurally_reconciled_not_validation",
        "source_receipt": str(SOURCE.relative_to(ROOT)),
        "batch_reports": reports,
        "parsed_judgment_count": len(by_id),
        "structural_reconciliation": True,
        "claim_boundary": (
            "This receipt structurally reconciles parseable patterns arrays from a "
            "preserved local-model output. It does not invent or semantically edit "
            "model judgments, and it is not human semantic validation, source "
            "identity review, recurrence evidence, delivery evidence, learner "
            "evidence, listener outcomes, causal evidence or effectiveness."
        ),
        "promotion_eligible": False,
    })
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    unresolved = sorted(set(item for batch in source.get("batch_reports", []) for item in batch.get("pattern_ids", [])) - set(by_id))
    MD.write_text("\n".join([
        "# Reconciled local-model recovered-pattern triage",
        "",
        "Status: **structurally reconciled; not validation**.",
        "",
        report["claim_boundary"],
        "",
        f"Unique parseable model entries after structural reconciliation: **{len(by_id)}**.",
        f"Entries added from preserved raw arrays: **{sum(b['structural_recovery_added_count'] for b in reports)}**.",
        f"Still unresolved from the model receipt: **{len(unresolved)}** ({', '.join(unresolved)}).",
        "",
        "No missing judgment was inferred and no model field was semantically repaired.",
    ]) + "\n")
    print(json.dumps({"unique_parseable_entries": len(by_id), "structural_entries_added": sum(b["structural_recovery_added_count"] for b in reports), "unresolved_count": len(unresolved), "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
