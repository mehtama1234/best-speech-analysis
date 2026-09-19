#!/usr/bin/env python3
"""Summarize validated listener task scores without claiming general effectiveness."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from scripts.validate_communication_job_listener_record import validate

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/communication-job-listener-outcome-protocol.json"


def summarize(records: list[dict], protocol: dict | None = None) -> dict:
    protocol = protocol or json.loads(PROTOCOL.read_text())
    if not records:
        raise ValueError("at least one listener record is required")
    for record in records:
        errors = validate(record, protocol)
        if errors:
            raise ValueError("invalid listener record: " + "; ".join(errors[:8]))
    pattern_by_stimulus = {pattern["draft_stimulus_id"]: pattern for pattern in protocol["patterns"]}
    buckets = defaultdict(list)
    for record in records:
        responses = record["responses"]
        pattern = pattern_by_stimulus.get(responses["stimulus_id"])
        job = pattern["canonical_job"] if pattern else "unknown_stimulus"
        buckets[(job, responses["condition"])].append(responses)
    rows = []
    for (job, condition), bucket in sorted(buckets.items()):
        task_scores = {}
        for task in protocol["listener_tasks"]:
            values = [r[f"score_{task['task_id']}"] for r in bucket]
            observed = [value for value in values if value is not None]
            task_scores[task["task_id"]] = {
                "count": len(values),
                "observed_count": len(observed),
                "missing_count": len(values) - len(observed),
                "mean": round(sum(observed) / len(observed), 4) if observed else None,
                "distribution": {str(score): observed.count(score) for score in (0, 1, 2)},
            }
        rows.append({
            "canonical_job": job,
            "condition": condition,
            "record_count": len(bucket),
            "accessibility_issue_count": sum(r["accessibility_issue"] == "yes" for r in bucket),
            "task_scores": task_scores,
        })
    return {
        "schema_version": "1.0",
        "record_type": "communication_job_listener_outcome_summary",
        "status": "validated_local_listener_task_summary_non_promotional",
        "protocol_id": protocol["protocol_id"],
        "record_count": len(records),
        "participant_codes": [record["responses"]["participant_code"] for record in records],
        "by_job_and_condition": rows,
        "promotion_eligible": False,
        "claim_boundary": "This summarizes blind rubric scores and reported accessibility flags for the authored stimuli and observed listeners. It does not establish that a speech pattern causes trust, persuasion, retention, behavior or general effectiveness.",
        "next_step": "Inspect missingness, accessibility failures, condition balance, scorer agreement and item-level reversals before any replication or broader claim.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = summarize([json.loads(path.read_text()) for path in args.records])
    rendered = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
