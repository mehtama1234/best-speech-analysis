#!/usr/bin/env python3
"""Validate the external-review launch manifest without treating it as evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/external-review-launch-manifest.json"
GATES = ROOT / "research/external-review-gate-index.json"


def split_paths(value: str | None) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def validate(manifest: dict, gates: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    operations = manifest.get("operations", [])
    gate_by_id = {gate["gate_id"]: gate for gate in gates.get("gates", [])}

    if manifest.get("manifest_id") != "external-review-launch-manifest":
        errors.append("unexpected manifest_id")
    if manifest.get("status") != "operations_ready_no_human_records_received":
        errors.append("manifest must remain operations_ready_no_human_records_received")
    if manifest.get("promotion_ready_cards") != 0:
        errors.append("manifest must keep promotion_ready_cards at zero")
    if len(operations) != 8:
        errors.append(f"expected eight operations, found {len(operations)}")

    seen: set[str] = set()
    for expected_order, operation in enumerate(operations, start=1):
        operation_id = operation.get("id")
        if operation.get("order") != expected_order:
            errors.append(f"operation order is not contiguous at {operation_id}")
        if not operation_id or operation_id in seen:
            errors.append(f"missing or duplicate operation id: {operation_id}")
        seen.add(operation_id)
        if operation.get("status") == "completed":
            errors.append(f"human operation cannot be marked completed without returned records: {operation_id}")
        for dependency in operation.get("depends_on", []):
            prior = next((item.get("order") for item in operations if item.get("id") == dependency), None)
            if prior is None or prior >= operation.get("order", 0):
                errors.append(f"dependency order is invalid for {operation_id}: {dependency}")
        for field in ("form", "validator", "comparison", "adjudication"):
            for relative in split_paths(operation.get(field)):
                if not (root / relative).is_file():
                    errors.append(f"{operation_id} references missing {field}: {relative}")

    expected_counts = {
        "identity_function_recurrence": sum(gate_by_id.get(gate_id, {}).get("item_count", 0) for gate_id in ("identity", "function", "phrase_forms", "recurrence")),
        "delivery_and_multimodal": sum(gate_by_id.get(gate_id, {}).get("item_count", 0) for gate_id in ("delivery", "multimodal")),
        "counterexamples": gate_by_id.get("counterexamples", {}).get("item_count"),
        "learner_teachability": gate_by_id.get("learner", {}).get("item_count"),
        "listener_stimulus_review": gate_by_id.get("listener_stimuli", {}).get("item_count"),
        "listener_outcomes": gate_by_id.get("listener_outcomes", {}).get("item_count"),
    }
    for operation in operations:
        operation_id = operation.get("id")
        expected = expected_counts.get(operation_id)
        if expected is not None and operation.get("items") != expected:
            errors.append(f"item count mismatch for {operation_id}: {operation.get('items')} != {expected}")

    if [operation.get("id") for operation in operations[:1]] != ["priority_pattern_review"]:
        errors.append("priority_pattern_review must be the first operation")
    if manifest.get("first_action") != "priority_pattern_review":
        errors.append("first_action must be priority_pattern_review")
    listener = next((operation for operation in operations if operation.get("id") == "listener_outcomes"), {})
    if listener.get("status") != "blocked_until_stimuli_locked":
        errors.append("listener outcomes must remain blocked until stimuli are locked")

    return errors


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    errors = validate(manifest, gates)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"external review launch manifest valid: {len(manifest.get('operations', []))} operations, dependencies and referenced instruments reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
