#!/usr/bin/env python3
"""Audit promotion blockers for every provisional communication-job card."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research/communication-job-promotion-readiness.json"
OUT_MD = ROOT / "writeups/communication-job-promotion-readiness.md"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def build() -> dict:
    cards = load("research/communication-job-cards.json")["cards"]
    delivery = load("research/communication-job-delivery-sampling.json")
    counter = load("research/communication-job-counterexample-workbook.json")
    learner = load("research/communication-job-learner-check.json")
    listener = load("research/communication-job-listener-outcome-protocol.json")
    function = load("research/corpus-function-independent-review-workbook.json")
    recurrence = load("research/corpus-recurrence-independent-review-workbook.json")
    phrase = load("research/corpus-phrase-form-independent-review-workbook.json")
    identity = load("research/corpus-identity-review-workbook.json")
    multimodal = load("research/multimodal-independent-review-workbook.json")
    delivery_by_job = {}
    for item in delivery["items"]:
        delivery_by_job.setdefault(item["canonical_job"], []).append(item)
    counter_by_job = {}
    for item in counter["items"]:
        counter_by_job.setdefault(item["canonical_job"], []).append(item)
    rows = []
    for card in cards:
        job = card["canonical_job"]
        blockers = [
            "independent_function_review_pending" if function["status"] != "completed" else None,
            "independent_recurrence_review_pending" if recurrence["status"] != "completed" else None,
            "independent_phrase_form_review_pending" if phrase["status"] != "completed" else None,
            "independent_identity_review_pending" if identity["status"] != "completed" else None,
            "delivery_observations_pending" if not any(item["review"].get("reviewer_code") for item in delivery_by_job.get(job, [])) else None,
            "counterexamples_pending" if not all(item["review"].get("evidence_status") for item in counter_by_job.get(job, [])) else None,
            "independent_multimodal_review_pending" if multimodal["status"] != "completed" else None,
            "learner_protocol_not_run" if learner["status"] != "completed" else None,
            "listener_stimuli_not_locked" if not listener["stimulus_pairs_locked"] else None,
        ]
        blockers = [blocker for blocker in blockers if blocker]
        rows.append({"card_id": card["card_id"], "canonical_job": job, "status": "provisional_not_promotion_ready", "exact_example_count": len(card["exact_examples"]), "delivery_sample_count": len(delivery_by_job.get(job, [])), "counterexample_slot_count": len(counter_by_job.get(job, [])), "blockers": blockers, "promotion_eligible": False})
    return {"schema_version": "1.0", "readiness_id": "communication-job-promotion-readiness", "status": "promotion_checkpoint_open", "claim_boundary": "This audit reports promotion prerequisites; it does not turn structural completeness, protocols or passing tests into independent evidence or effectiveness claims.", "card_count": len(rows), "promotion_ready_count": sum(row["promotion_eligible"] for row in rows), "cards": rows}


def main() -> int:
    report = build()
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job promotion readiness", "", "Status: **promotion checkpoint open**.", "", report["claim_boundary"], "", "| Job | Examples | Delivery samples | Counterexample slots | Promotion eligible | Blockers |", "|---|---:|---:|---:|---|---|"]
    for row in report["cards"]:
        lines.append(f"| `{row['canonical_job']}` | {row['exact_example_count']} | {row['delivery_sample_count']} | {row['counterexample_slot_count']} | `{row['promotion_eligible']}` | {', '.join(row['blockers'])} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(OUT_JSON.relative_to(ROOT)), "card_count": report["card_count"], "promotion_ready_count": report["promotion_ready_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
