#!/usr/bin/env python3
"""Merge the bounded gap receipt into the structurally reconciled receipt."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/local-llm-recovered-pattern-screen-reconciled.json"
GAP = ROOT / "research/local-llm-recovered-pattern-gap-screen.json"
OUT = ROOT / "research/local-llm-recovered-pattern-screen-complete.json"
MD = ROOT / "writeups/local-llm-recovered-pattern-screen-complete.md"


def main() -> int:
    base = json.loads(BASE.read_text())
    gap = json.loads(GAP.read_text())
    reports = list(base.get("batch_reports", []))
    for item in gap.get("batch_reports", []):
        judgment = item.get("parsed_judgment")
        reports.append({
            "batch_number": "gap:" + item["pattern_id"],
            "pattern_ids": [item["pattern_id"]],
            "parsed_judgment": {"patterns": [judgment]} if judgment else None,
            "raw_output": item.get("raw_output", ""),
            "structural_recovery_added_count": 0,
        })
    entries = [
        item
        for report in reports
        for item in (report.get("parsed_judgment") or {}).get("patterns", [])
        if item.get("pattern_id")
    ]
    by_id = {item["pattern_id"]: item for item in entries}
    report = dict(base)
    report.update({
        "status": "local_model_recovered_pattern_triage_complete_not_validation",
        "source_receipts": [
            str(BASE.relative_to(ROOT)),
            str(GAP.relative_to(ROOT)),
        ],
        "batch_reports": reports,
        "parsed_judgment_count": len(by_id),
        "gap_screen_pattern_count": len(gap.get("requested_pattern_ids", [])),
        "promotion_eligible": False,
        "claim_boundary": (
            "This receipt combines structurally reconciled and bounded gap-screen "
            "outputs from a local language model. It is not human semantic validation, "
            "source identity review, recurrence evidence, delivery evidence, learner "
            "evidence, listener outcomes, causal evidence or effectiveness. Field "
            "variants remain visible and no missing semantic judgment is inferred."
        ),
    })
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Complete local-model recovered-pattern triage receipt",
        "",
        "Status: **machine triage complete; not validation**.",
        "",
        report["claim_boundary"],
        "",
        f"Unique pattern entries: **{len(by_id)} / 55**.",
        "The original raw receipt, structural reconciliation and five-pattern gap receipt are retained as separate sources.",
    ]) + "\n")
    print(json.dumps({"unique_entries": len(by_id), "pattern_count": report["pattern_count"], "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
