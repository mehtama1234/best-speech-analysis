#!/usr/bin/env python3
"""Exercise the listener-outcome export and summary path with synthetic data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scripts.summarize_communication_job_listener_records import summarize
    from scripts.validate_communication_job_listener_record import validate
except ImportError:
    from summarize_communication_job_listener_records import summarize
    from validate_communication_job_listener_record import validate

PROTOCOL = ROOT / "research/communication-job-listener-outcome-protocol.json"
OUT = ROOT / "research/autonomous-listener-instrument-dry-run.json"
MD = ROOT / "writeups/autonomous-listener-instrument-dry-run.md"


def synthetic_record(condition: str, participant: str) -> dict:
    protocol = json.loads(PROTOCOL.read_text())
    responses = {
        "participant_code": participant,
        "date": "2026-09-19",
        "protocol_version": "communication-job-listener-outcome-protocol-draft",
        "modality": "text_synthetic",
        "stimulus_id": protocol["patterns"][0]["draft_stimulus_id"],
        "condition": condition,
        "scorer_id_or_blind_code": "synthetic-blind-code",
        "consent": True,
        "accessibility_issue": "no",
    }
    for task in protocol["listener_tasks"]:
        responses[f"task_{task['task_id']}"] = f"synthetic {task['task_id']} response"
        responses[f"score_{task['task_id']}"] = 2
    return {
        "schema_version": "1.0",
        "record_type": "communication_job_listener_outcome_observation",
        "protocol_id": protocol["protocol_id"],
        "responses": responses,
        "claim_boundary": "Synthetic instrument dry run only; no listener participated and no outcome claim is made.",
    }


def run() -> dict:
    protocol = json.loads(PROTOCOL.read_text())
    records = [synthetic_record("control", "synthetic-listener-control"), synthetic_record("pattern_informed", "synthetic-listener-pattern")]
    errors = [error for record in records for error in validate(record, protocol, allow_unlocked_synthetic=True)]
    summary = summarize(records, protocol, allow_unlocked_synthetic=True) if not errors else None
    full_records = []
    for index, pattern in enumerate(protocol["patterns"]):
        for condition in ("control", "pattern_informed"):
            record = synthetic_record(condition, f"synthetic-listener-full-{index}-{condition}")
            record["responses"]["stimulus_id"] = pattern["draft_stimulus_id"]
            full_records.append(record)
    full_errors = [error for record in full_records for error in validate(record, protocol, allow_unlocked_synthetic=True)]
    full_summary = summarize(full_records, protocol, allow_unlocked_synthetic=True) if not full_errors else None
    report = {
        "schema_version": "1.0",
        "dry_run_id": "autonomous-listener-instrument-dry-run",
        "status": "instrument_export_validation_and_summary_passed" if not errors and summary and summary["record_count"] == 2 else "failed",
        "record_count": len(records),
        "validation_errors": errors,
        "summary": summary,
        "full_curriculum": {
            "status": "full_18_job_synthetic_export_validated" if not full_errors and full_summary and full_summary["record_count"] == 36 and not full_summary["promotion_eligible"] else "failed",
            "job_count": len(protocol["patterns"]),
            "record_count": len(full_records),
            "validation_errors": full_errors,
            "promotion_eligible": full_summary["promotion_eligible"] if full_summary else False,
            "claim_boundary": "Synthetic instrument dry run only; no listener participated and no outcome claim is made.",
        },
        "claim_boundary": "Synthetic instrument dry run only; no listener participated and no outcome claim is made.",
        "what_this_proves": "The listener form record shape, consent field, task scoring, validator and summary path work together on synthetic records.",
        "what_this_does_not_prove": "No listener comprehension, recall, cognitive-load, trust, persuasion, behavior or general effectiveness result.",
    }
    return report


def render(report: dict) -> str:
    return "\n".join([
        "# Autonomous listener-instrument dry run",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Two slice condition records passed validation and summary generation; a separate synthetic run covers **{report['full_curriculum']['job_count']} jobs and {report['full_curriculum']['record_count']} balanced condition records**. `promotion_eligible` remains `{report['summary']['promotion_eligible'] if report['summary'] else False}`.",
        "",
        "This is an instrument check, not listener evidence.",
        "",
        "```text",
        "python3 scripts/run_autonomous_listener_dry_run.py",
        "```",
        "",
    ])


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous listener dry run: {report['status']} ({report['record_count']} records)")
    if report["status"] == "failed":
        raise SystemExit(1)
