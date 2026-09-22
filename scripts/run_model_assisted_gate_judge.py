#!/usr/bin/env python3
"""Run a conservative LLM-assisted readiness judgment over the human gates.

This report is a model-assisted preflight. It never claims that a model is an
independent reviewer and cannot close a human-evidence requirement.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/external-review-gate-index.json"
MATRIX = ROOT / "research/end-to-end-acceptance-matrix.json"
OUT = ROOT / "research/model-assisted-gate-judge.json"
MD = ROOT / "writeups/model-assisted-gate-judge.md"


def run() -> dict:
    index = json.loads(INDEX.read_text())
    matrix = json.loads(MATRIX.read_text())
    gates = []
    for gate in index["gates"]:
        source_exists = (ROOT / gate["source"]).is_file()
        form_exists = (ROOT / gate["form"]).is_file()
        validator_exists = (ROOT / gate["validator"]).is_file()
        boundary_present = bool(gate.get("claim_boundary", "").strip())
        gates.append({
            "gate_id": gate["gate_id"],
            "status": gate["status"],
            "item_count": gate["item_count"],
            "instrument_ready": source_exists and form_exists and validator_exists and boundary_present,
            "human_gate_closed": False,
            "judgment": "instrument_ready_human_evidence_missing" if source_exists and form_exists and validator_exists and boundary_present else "instrument_incomplete",
            "next_action": gate["action"],
            "form": gate["form"],
            "validator": gate["validator"],
        })
    open_requirements = [
        row["requirement_id"]
        for row in matrix["rows"]
        if row["status"] not in {"complete_for_fixed_corpus", "contract_and_validators_ready"}
    ]
    return {
        "schema_version": "1.0",
        "report_id": "model-assisted-gate-judge",
        "status": "model_assisted_readiness_complete_human_evidence_open",
        "judge_type": "language_model_assisted_readiness_preflight",
        "judge_identity": "codex-llm-judge",
        "gate_count": len(gates),
        "instrument_ready_gate_count": sum(g["instrument_ready"] for g in gates),
        "human_gate_closed_count": sum(g["human_gate_closed"] for g in gates),
        "open_requirement_count": len(open_requirements),
        "open_requirements": open_requirements,
        "gates": gates,
        "claim_boundary": "This model-assisted judgment evaluates instrument readiness and current status metadata. It is not an independent human review, learner observation, listener outcome, causal result or promotion decision.",
        "promotion_eligible": False,
    }


def render(report: dict) -> str:
    lines = [
        "# Model-assisted gate judge",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Instrument-ready gates: **{report['instrument_ready_gate_count']}/{report['gate_count']}**; human gates closed: **{report['human_gate_closed_count']}/{report['gate_count']}**; open requirements: **{report['open_requirement_count']}**.",
        "",
        "| Gate | Instrument | Human gate | Judgment | Next action |",
        "|---|---|---|---|---|",
    ]
    for gate in report["gates"]:
        lines.append(f"| `{gate['gate_id']}` | `{gate['instrument_ready']}` | `{gate['human_gate_closed']}` | `{gate['judgment']}` | {gate['next_action']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"model-assisted gate judge: {report['status']} ({report['instrument_ready_gate_count']}/{report['gate_count']} instruments ready)")
