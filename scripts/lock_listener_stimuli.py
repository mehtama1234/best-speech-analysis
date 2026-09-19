#!/usr/bin/env python3
"""Reduce two independent stimulus reviews and an adjudication into a lock audit.

The command never treats a browser export or reviewer agreement as a lock by
itself. A locked artifact is emitted only when every pair is independently
reviewed, explicitly adjudicated, and marked safe/accessibility-ready.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate_listener_stimulus_review import validate as validate_review
from scripts.validate_listener_stimulus_adjudication import validate as validate_adjudication


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "research/communication-job-listener-stimulus-review-workbook.json"
DRAFT = ROOT / "research/communication-job-listener-stimuli-draft.json"
REQUIRED_REVIEW = {
    "proposition_equivalence": "equivalent",
    "readability_match": "matched",
    "target_isolation": "isolated",
    "accessibility": "pass",
    "safety": "pass",
    "condition_order_or_blinding": "adequate",
    "lock_decision": "lock_for_pilot",
}


def build_lock(review_a: dict, review_b: dict, adjudication: dict, workbook: dict | None = None, draft: dict | None = None) -> dict:
    workbook = workbook or json.loads(WORKBOOK.read_text())
    draft = draft or json.loads(DRAFT.read_text())
    errors = validate_review(review_a, workbook) + validate_review(review_b, workbook) + validate_adjudication(adjudication, workbook)
    reviewer_a = review_a.get("responses", {}).get("reviewer_name")
    reviewer_b = review_b.get("responses", {}).get("reviewer_name")
    if reviewer_a == reviewer_b: errors.append("independent review codes must be distinct")
    if errors: raise ValueError("invalid lock inputs: " + "; ".join(errors[:12]))

    rows = []
    for number, item in enumerate(workbook["items"], 1):
        prefix = f"item_{number}_"
        decisions = [review_a["responses"][prefix + field] for field in REQUIRED_REVIEW]
        final_decision = adjudication["responses"][prefix + "final_decision"]
        safety = adjudication["responses"][prefix + "accessibility_safety"]
        eligible = final_decision == "lock_for_pilot" and safety == "pass" and all(
            value == expected for value, expected in zip(decisions, REQUIRED_REVIEW.values())
        ) and all(
            review["responses"][prefix + field] == expected
            for review in (review_a, review_b)
            for field, expected in REQUIRED_REVIEW.items()
        )
        rows.append({
            "stimulus_id": item["stimulus_id"],
            "canonical_job": item["canonical_job"],
            "final_decision": final_decision,
            "accessibility_safety": safety,
            "eligible_for_lock": eligible,
            "adjudication_rationale": adjudication["responses"][prefix + "rationale"],
        })
    locked_count = sum(row["eligible_for_lock"] for row in rows)
    status = "locked_for_pilot" if locked_count == len(rows) else "not_locked"
    result = {
        "schema_version": "1.0",
        "record_type": "listener_stimulus_lock_audit",
        "status": status,
        "workbook_id": workbook["workbook_id"],
        "source_draft": "research/communication-job-listener-stimuli-draft.json",
        "review_a_code": reviewer_a,
        "review_b_code": reviewer_b,
        "adjudicator_code": adjudication["adjudicator_code"],
        "pair_count": len(rows),
        "locked_pair_count": locked_count,
        "pairs": rows,
        "claim_boundary": "A locked_for_pilot status means the authored pairs passed the recorded review and adjudication gates for a pilot. It does not establish listener comprehension, communication effectiveness, causality or universal best practice.",
    }
    if status == "locked_for_pilot":
        result["locked_stimuli"] = draft["records"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_a", type=Path)
    parser.add_argument("review_b", type=Path)
    parser.add_argument("adjudication", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_lock(json.loads(args.review_a.read_text()), json.loads(args.review_b.read_text()), json.loads(args.adjudication.read_text()))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "status": result["status"], "pair_count": result["pair_count"], "locked_pair_count": result["locked_pair_count"]}, indent=2))
    return 0 if result["status"] == "locked_for_pilot" else 2


if __name__ == "__main__":
    raise SystemExit(main())
