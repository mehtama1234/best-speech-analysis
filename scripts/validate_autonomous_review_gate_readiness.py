#!/usr/bin/env python3
"""Check that every external-review/data gate is runnable without calling it complete."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .validate_blinded_review_packet import validate as validate_blinded_packet
except ImportError:
    from validate_blinded_review_packet import validate as validate_blinded_packet

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/external-review-gate-index.json"
PACKET = ROOT / "research/blinded-review-packet.json"


def validate() -> list[str]:
    errors: list[str] = []
    index = json.loads(INDEX.read_text())
    if index.get("status") != "review_operations_ready_research_evidence_incomplete":
        errors.append("gate index does not preserve incomplete-evidence status")
    gates = index.get("gates", [])
    if len(gates) != 10:
        errors.append(f"expected 10 external gates, found {len(gates)}")
    for gate in gates:
        for field in ("source", "form", "validator", "comparator_or_summarizer"):
            relative = gate.get(field)
            if not relative or not (ROOT / relative).exists():
                errors.append(f"{gate.get('gate_id')} missing {field}: {relative}")
        source = gate.get("source")
        if source and (ROOT / source).exists():
            payload = json.loads((ROOT / source).read_text())
            if not payload.get("claim_boundary"):
                errors.append(f"{gate.get('gate_id')} source lacks claim boundary")
            if gate.get("item_count", 0) <= 0:
                errors.append(f"{gate.get('gate_id')} has no routed items")
    packet = json.loads(PACKET.read_text())
    errors.extend(validate_blinded_packet(packet))
    packet_items = sum(len(gate.get("items", [])) for gate in packet.get("gates", {}).values())
    if packet_items != 429:
        errors.append(f"blinded packet item count is {packet_items}, expected 429")
    if packet.get("status") != "blinded_operational_packet_no_human_records":
        errors.append("blinded packet status incorrectly implies completed review")
    if "not evidence" not in packet.get("claim_boundary", "").lower():
        errors.append("blinded packet boundary does not say it is not evidence")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous review-gate readiness valid: 10 runnable gates, 429 blinded items, no human records")
