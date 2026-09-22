#!/usr/bin/env python3
"""Fail closed unless the acceptance matrix and promotion audit are complete."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def report() -> dict:
    matrix = load("research/end-to-end-acceptance-matrix.json")
    readiness = load("research/communication-job-promotion-readiness.json")
    gates = load("research/external-review-gate-index.json")
    open_rows = [
        {
            "requirement_id": row["requirement_id"],
            "status": row["status"],
            "remaining": row.get("remaining", ""),
        }
        for row in matrix["rows"]
        if row["status"] not in {"complete_for_fixed_corpus", "contract_and_validators_ready"}
    ]
    open_gates = [
        {"gate_id": gate["gate_id"], "status": gate["status"], "item_count": gate["item_count"], "form": gate["form"], "validator": gate["validator"]}
        for gate in gates["gates"]
        if gate.get("status") not in {"complete", "validated"}
    ]
    return {
        "schema_version": "1.0",
        "check_id": "promotion-readiness",
        "status": "promotion_ready" if not open_rows and not open_gates and readiness["promotion_ready_count"] == readiness["card_count"] else "promotion_blocked",
        "promotion_ready_count": readiness["promotion_ready_count"],
        "card_count": readiness["card_count"],
        "open_requirement_count": len(open_rows),
        "open_requirements": open_rows,
        "open_gate_count": len(open_gates),
        "open_gates": open_gates,
        "claim_boundary": "A repository checkpoint, protocol, synthetic dry run or passing validator is not human validation or communication effectiveness evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print the complete structured report")
    parser.add_argument("--allow-blocked", action="store_true", help="return success when the report correctly remains blocked")
    args = parser.parse_args()
    result = report()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"promotion readiness: {result['status']}")
        print(f"open requirements: {result['open_requirement_count']}; open gates: {result['open_gate_count']}; ready cards: {result['promotion_ready_count']}/{result['card_count']}")
        for gate in result["open_gates"]:
            print(f"next gate: {gate['gate_id']} ({gate['item_count']} items) -> {gate['form']}; validate with {gate['validator']}")
        print(result["claim_boundary"])
    if result["status"] == "promotion_ready":
        return 0
    return 0 if args.allow_blocked else 2


if __name__ == "__main__":
    raise SystemExit(main())
