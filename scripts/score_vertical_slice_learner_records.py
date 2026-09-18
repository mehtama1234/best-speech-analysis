#!/usr/bin/env python3
"""Validate and summarize learner-check JSON records.

The scorer reports teachability observations only. It refuses to make an
outcome claim and keeps safety/boundary scores visible instead of averaging
them away.
"""
import argparse
import json
from pathlib import Path


PATTERN_COUNT = 5
REQUIRED_TEXT_SUFFIXES = ("baseline", "transfer", "non_fit", "control", "listener", "revision")
REQUIRED_SCORE_SUFFIXES = ("transfer_score", "boundary_score", "listener_score")
TASK_BANK = Path(__file__).resolve().parents[1] / "research/vertical-slice-01-learner-task-bank.json"


def expected_task_ids():
    bank = json.loads(TASK_BANK.read_text())
    grouped = {}
    order = []
    for task in bank["tasks"]:
        pattern = task["pattern_id"]
        if pattern not in grouped:
            grouped[pattern] = []
            order.append(pattern)
        grouped[pattern].append(task["task_id"])
    return {number: grouped[pattern] for number, pattern in enumerate(order, 1)}


def load_record(path):
    record = json.loads(Path(path).read_text())
    responses = record.get("responses", {})
    errors = []
    if record.get("record_type") != "learner_observation":
        errors.append("record_type must be learner_observation")
    if not record.get("claim_boundary"):
        errors.append("claim_boundary is required")
    if not responses.get("participant_code"):
        errors.append("participant_code is required")
    if not responses.get("date"):
        errors.append("date is required")
    if responses.get("consent") is not True:
        errors.append("consent must be true")

    patterns = []
    task_ids_by_pattern = expected_task_ids()
    for number in range(1, PATTERN_COUNT + 1):
        missing = [
            suffix for suffix in REQUIRED_TEXT_SUFFIXES
            if not str(responses.get(f"p{number}_{suffix}", "")).strip()
        ]
        scores = {}
        supplied_task_ids = [
            value.strip() for value in str(
                responses.get(f"p{number}_task_bank_ids", "")
            ).split(",") if value.strip()
        ]
        if supplied_task_ids != task_ids_by_pattern.get(number, []):
            errors.append(
                f"p{number}_task_bank_ids does not match the fixed task bank"
            )
        for suffix in REQUIRED_SCORE_SUFFIXES:
            value = responses.get(f"p{number}_{suffix}")
            try:
                value = int(value)
            except (TypeError, ValueError):
                missing.append(suffix)
                continue
            if value not in (0, 1, 2):
                errors.append(f"p{number}_{suffix} must be 0, 1 or 2")
            scores[suffix] = value
        if missing:
            errors.append(f"p{number} missing: {', '.join(missing)}")
        patterns.append({
            "pattern_number": number,
            "scores": scores,
            "boundary_failure": scores.get("boundary_score") == 0,
            "complete": not missing,
        })
    return record, errors, patterns


def summarize(paths):
    records = []
    rejected = []
    for path in paths:
        record, errors, patterns = load_record(path)
        if errors:
            rejected.append({"file": str(path), "errors": errors})
            continue
        records.append({"file": str(path), "patterns": patterns})

    pattern_summary = []
    for number in range(1, PATTERN_COUNT + 1):
        rows = [r["patterns"][number - 1] for r in records]
        scores = [row["scores"] for row in rows]
        boundary_failures = sum(row["boundary_failure"] for row in rows)
        pattern_summary.append({
            "pattern_number": number,
            "valid_records": len(rows),
            "mean_transfer_score": round(
                sum(s["transfer_score"] for s in scores) / len(scores), 3
            ) if scores else None,
            "mean_listener_restatement_score": round(
                sum(s["listener_score"] for s in scores) / len(scores), 3
            ) if scores else None,
            "boundary_failures": boundary_failures,
            "promotion_eligible": bool(rows) and boundary_failures == 0,
        })

    return {
        "schema_version": "1.0",
        "report_type": "vertical_slice_01_learner_observation_summary",
        "status": "observations_available" if records else "no_valid_observations",
        "claim_boundary": "Teachability observations only; this report does not measure trust, memory, persuasion, engagement or action.",
        "valid_record_count": len(records),
        "rejected_record_count": len(rejected),
        "rejected_records": rejected,
        "patterns": pattern_summary,
        "promotion_rule": "No pattern is promotion-eligible if any valid record has a boundary score of 0; external review and packet validation remain required.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = summarize(args.records)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return report


if __name__ == "__main__":
    main()
