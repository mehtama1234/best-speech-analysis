#!/usr/bin/env python3
"""Summarize counterexample review decisions without promoting them to proof."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from scripts.validate_communication_job_counterexample_review import validate

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-counterexample-workbook.json"


def summarize(records: list[dict], workbook: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    if not records:
        raise ValueError("at least one counterexample review export is required")
    for record in records:
        errors = validate(record, workbook)
        if errors:
            raise ValueError("invalid counterexample review: " + "; ".join(errors[:8]))
    by_slot = defaultdict(list)
    item_by_number = {number: item for number, item in enumerate(workbook["items"], 1)}
    for record in records:
        responses = record["responses"]
        for number, item in item_by_number.items():
            by_slot[(item["canonical_job"], item["counterexample_type"])].append(responses[f"item_{number}_evidence_status"])
    rows = []
    for (job, counterexample_type), statuses in sorted(by_slot.items()):
        rows.append({"canonical_job": job, "counterexample_type": counterexample_type, "review_count": len(statuses), "status_counts": {status: statuses.count(status) for status in workbook["decision_vocabulary"]["evidence_status"]}})
    return {
        "schema_version": "1.0",
        "record_type": "communication_job_counterexample_summary",
        "status": "validated_counterexample_review_summary_non_promotional",
        "workbook_id": workbook["workbook_id"],
        "record_count": len(records),
        "by_job_and_type": rows,
        "promotion_eligible": False,
        "claim_boundary": "This summarizes reviewer decisions about candidate counterexamples, alternate functions, confounds and misuse risks. It does not establish that a pattern works, fails causally, changes audience outcomes or generalizes.",
        "next_step": "Inspect confirmed candidates, source identity, disagreements, safety notes and no-candidate decisions before revising any pattern card.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize([json.loads(path.read_text()) for path in args.records])
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
