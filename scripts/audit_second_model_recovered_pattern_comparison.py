#!/usr/bin/env python3
"""Audit structural quality and agreement risk in the second-model receipt."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/second-model-recovered-pattern-comparison.json"
OUT = ROOT / "research/second-model-recovered-pattern-comparison-audit.json"
MD = ROOT / "writeups/second-model-recovered-pattern-comparison-audit.md"


def main() -> int:
    source = json.loads(SOURCE.read_text())
    reports = source["reports"]
    parsed = [row for row in reports if isinstance(row.get("parsed_judgment"), dict)]
    required = {"pattern_id", "assessment", "concerns", "priority"}
    complete = [row for row in parsed if required <= set(row["parsed_judgment"])]
    malformed = [
        {"requested_pattern_id": row["pattern_id"], "keys": sorted(row["parsed_judgment"])}
        for row in parsed if required > set(row["parsed_judgment"])
    ]
    missing = [row["pattern_id"] for row in reports if not row.get("parsed_judgment")]
    assessments = {}
    priorities = {}
    for row in parsed:
        judgment = row["parsed_judgment"]
        assessments[judgment.get("assessment")] = assessments.get(judgment.get("assessment"), 0) + 1
        priorities[judgment.get("priority")] = priorities.get(judgment.get("priority"), 0) + 1
    report = {
        "schema_version": "1.0",
        "status": "second_model_comparison_quality_warning_not_validation",
        "source_report": str(SOURCE.relative_to(ROOT)),
        "requested_pattern_count": len(reports),
        "parsed_output_count": len(parsed),
        "complete_schema_count": len(complete),
        "malformed_output_count": len(malformed),
        "missing_output_count": len(missing),
        "malformed_outputs": malformed,
        "missing_pattern_ids": missing,
        "assessment_counts": assessments,
        "priority_counts": priorities,
        "promotion_eligible": False,
        "use_for_corroboration": False,
        "claim_boundary": (
            "The second local model is not independent human evidence. This audit "
            "records schema and output-concentration risk only. Agreement or apparent "
            "support from these small local models must not be treated as semantic "
            "validation, recurrence, delivery, learner, listener, causal or effectiveness evidence."
        ),
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Second-model recovered-pattern comparison audit",
        "",
        "Status: **quality warning; not validation**.",
        "",
        report["claim_boundary"],
        "",
        f"Requested: **{report['requested_pattern_count']}** · parsed: **{report['parsed_output_count']}** · complete schemas: **{report['complete_schema_count']}** · malformed: **{report['malformed_output_count']}** · missing: **{report['missing_output_count']}**.",
        f"Assessment concentration: **{assessments.get('supports', 0)}** parsed outputs marked `supports`; priority concentration: **{priorities.get('high', 0)}** marked `high`.",
        "",
        "This receipt is retained as a warning and is not eligible for corroboration or promotion.",
    ]) + "\n")
    print(json.dumps({k: report[k] for k in ("requested_pattern_count", "parsed_output_count", "complete_schema_count", "malformed_output_count", "missing_output_count", "use_for_corroboration")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
