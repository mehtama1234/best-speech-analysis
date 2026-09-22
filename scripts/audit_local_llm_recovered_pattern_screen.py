#!/usr/bin/env python3
"""Audit completeness of the local-model recovered-pattern triage receipt."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/local-llm-recovered-pattern-screen-complete.json"
RAW_SOURCE = ROOT / "research/local-llm-recovered-pattern-screen.json"
MATRIX = ROOT / "research/all-55-pattern-evidence.json"
OUT = ROOT / "research/local-llm-recovered-pattern-screen-audit.json"
MD = ROOT / "writeups/local-llm-recovered-pattern-screen-audit.md"


def main() -> int:
    source = json.loads(SOURCE.read_text())
    expected = {row["pattern_id"] for row in json.loads(MATRIX.read_text())["patterns"]}
    entries = []
    for batch in source.get("batch_reports", []):
        judgment = batch.get("parsed_judgment") or {}
        for item in judgment.get("patterns", []):
            entries.append(item)
    by_id = {item.get("pattern_id"): item for item in entries if item.get("pattern_id")}
    complete = []
    variant = []
    invalid = []
    for pattern_id, item in sorted(by_id.items()):
        required = {"clarity", "concerns", "recommended_review_priority"}
        missing = sorted(required - item.keys())
        if not missing:
            complete.append(pattern_id)
        elif "clarity" not in item and "clarification" in item:
            variant.append(pattern_id)
        else:
            invalid.append({"pattern_id": pattern_id, "missing": missing})
    unresolved = sorted(expected - set(by_id))
    report = {
        "schema_version": "1.0",
        "status": "local_model_triage_schema_audit_not_validation",
        "source_report": str(SOURCE.relative_to(ROOT)),
        "raw_source_report": str(RAW_SOURCE.relative_to(ROOT)),
        "source_receipts": source.get("source_receipts", []),
        "expected_pattern_count": len(expected),
        "model_entry_count": len(entries),
        "unique_model_pattern_count": len(by_id),
        "complete_schema_count": len(complete),
        "field_variant_count": len(variant),
        "invalid_entry_count": len(invalid),
        "unresolved_pattern_count": len(unresolved),
        "field_variant_pattern_ids": variant,
        "invalid_entries": invalid,
        "unresolved_pattern_ids": unresolved,
        "promotion_eligible": False,
        "claim_boundary": (
            "This is a schema-completeness audit of a local-model triage receipt. "
            "It does not validate semantic accuracy, source identity, recurrence, "
            "delivery meaning, learner transfer, listener outcomes or effectiveness."
        ),
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Local-model recovered-pattern triage audit",
        "",
        f"Expected patterns: **{report['expected_pattern_count']}** · unique model entries: **{report['unique_model_pattern_count']}** · complete schemas: **{report['complete_schema_count']}** · field variants: **{report['field_variant_count']}** · unresolved: **{report['unresolved_pattern_count']}**.",
        "",
        report["claim_boundary"],
        "",
        "The audit preserves missing and variant model fields. It does not infer a missing judgment or repair model content.",
    ]) + "\n")
    print(json.dumps({k: report[k] for k in ("expected_pattern_count", "unique_model_pattern_count", "complete_schema_count", "field_variant_count", "unresolved_pattern_count", "promotion_eligible")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
