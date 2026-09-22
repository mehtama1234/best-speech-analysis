#!/usr/bin/env python3
"""Exercise the learner form export contract without creating learner evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from .score_vertical_slice_learner_records import expected_task_ids, load_record, summarize
    from .validate_communication_job_learner_record import validate as validate_full_record
    from .summarize_communication_job_learner_records import summarize as summarize_full_record
except ImportError:
    from score_vertical_slice_learner_records import expected_task_ids, load_record, summarize
    from validate_communication_job_learner_record import validate as validate_full_record
    from summarize_communication_job_learner_records import summarize as summarize_full_record


OUT = ROOT / "research/autonomous-learner-instrument-dry-run.json"
MD = ROOT / "writeups/autonomous-learner-instrument-dry-run.md"


def synthetic_record() -> dict:
    responses = {
        "participant_code": "synthetic-autonomous-dry-run",
        "date": "2026-09-19",
        "lesson_version": "vertical-slice-01-draft",
        "accessibility": "typed synthetic responses",
        "consent": True,
        "facilitator_feedback": "Synthetic record only; no person participated.",
        "facilitator_changes": "None",
        "unresolved_disagreement": "None",
    }
    for number, task_ids in expected_task_ids().items():
        responses[f"p{number}_task_bank_ids"] = ",".join(task_ids)
        for suffix in ("baseline", "transfer", "non_fit", "control", "listener", "revision"):
            responses[f"p{number}_{suffix}"] = f"synthetic {suffix} response for pattern {number}"
        responses[f"p{number}_transfer_score"] = 2
        responses[f"p{number}_boundary_score"] = 2
        responses[f"p{number}_listener_score"] = 2
    return {
        "schema_version": "1.0",
        "protocol_id": "vertical-slice-01-learner-check",
        "record_type": "learner_observation",
        "responses": responses,
        "claim_boundary": "Synthetic instrument dry run only; this is not a learner observation and does not measure trust, memory, persuasion or action.",
    }


def run() -> dict:
    record = synthetic_record()
    temp = ROOT / "research/.autonomous-learner-dry-run-record.json"
    temp.write_text(json.dumps(record, indent=2) + "\n")
    _, errors, patterns = load_record(temp)
    summary = summarize([temp])
    temp.unlink()
    protocol = json.loads((ROOT / "research/communication-job-learner-check.json").read_text())
    full_responses = {
        "participant_code": "synthetic-autonomous-full-curriculum",
        "date": "2026-09-19",
        "lesson_version": "communication-job-curriculum-draft",
        "facilitator_code": "synthetic-facilitator",
        "facilitator_role": "synthetic instrument test",
        "scoring_disagreement_or_uncertainty": "Synthetic record only; no person participated.",
        "consent": True,
    }
    task_ids = [task["task_id"] for task in protocol["tasks"]]
    for card in protocol["cards"]:
        card_id = card["card_id"]
        card_tasks = [task["task_id"] for task in protocol["tasks"] if task["card_id"] == card_id]
        full_responses[f"{card_id}_task_ids"] = ",".join(card_tasks)
        for task_id in card_tasks:
            full_responses[task_id] = "synthetic full-curriculum response"
        for suffix in ("listener_restatement", "revision", "boundary_note"):
            full_responses[f"{card_id}_{suffix}"] = "synthetic bounded response"
        for dimension in card.get("scoring_dimensions", []):
            full_responses[f"{card_id}_score_{dimension}"] = "2"
        full_responses[f"{card_id}_safety_issue"] = "no"
    full_record = {
        "schema_version": "1.0",
        "record_type": "communication_job_learner_observation",
        "protocol_id": protocol["protocol_id"],
        "task_bank_ids": task_ids,
        "responses": full_responses,
        "claim_boundary": "Synthetic instrument dry run only; this is not a learner observation and does not measure teachability, listener outcomes or effectiveness.",
    }
    full_errors = validate_full_record(full_record, protocol)
    full_summary = summarize_full_record([full_record], protocol) if not full_errors else None
    return {
        "schema_version": "1.0",
        "dry_run_id": "autonomous-learner-instrument-dry-run",
        "status": "instrument_export_validation_and_scoring_passed" if not errors and summary["valid_record_count"] == 1 else "failed",
        "record_type": record["record_type"],
        "pattern_count": len(patterns),
        "validation_errors": errors,
        "summary": summary,
        "full_curriculum": {
            "status": "full_18_job_synthetic_export_validated" if not full_errors and full_summary and full_summary["record_count"] == 1 else "failed",
            "job_count": protocol["card_count"],
            "task_count": protocol["task_count"],
            "record_count": full_summary["record_count"] if full_summary else 0,
            "validation_errors": full_errors,
            "claim_boundary": full_record["claim_boundary"],
        },
        "claim_boundary": record["claim_boundary"],
        "what_this_proves": "The fixed learner form shape, task-bank linkage, consent field, score bounds, validator and summary path work together on a synthetic record.",
        "what_this_does_not_prove": "No human completed the form. This does not establish learner teachability, listener comprehension, improvement or effectiveness.",
    }


def render(report: dict) -> str:
    return "\n".join([
        "# Autonomous learner-instrument dry run",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"The slice synthetic record passed validation and scoring across **{report['pattern_count']} pattern sections**; a separate synthetic export also covers **{report['full_curriculum']['job_count']} jobs and {report['full_curriculum']['task_count']} tasks**.",
        "",
        "This proves the form/export/validator path is internally coherent. It is not learner data and must not be counted as learner validation or outcome evidence.",
        "",
        "```text",
        "python3 scripts/run_autonomous_learner_dry_run.py",
        "```",
        "",
    ])


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous learner dry run: {report['status']} ({report['pattern_count']} patterns)")
    if report["status"] == "failed":
        raise SystemExit(1)
