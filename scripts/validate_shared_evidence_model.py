#!/usr/bin/env python3
"""Validate the shared web/mobile evidence-model contract and live counts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from .build_shared_evidence_model import build
except ImportError:
    from build_shared_evidence_model import build


ROOT = Path(__file__).resolve().parents[1]


def validate(model: dict, current: dict | None = None) -> list[str]:
    current = current or build(ROOT)
    errors = []
    if model.get("model_id") != "shared-communication-evidence-model": errors.append("model_id is invalid")
    if model.get("status") != "contract_ready_research_evidence_incomplete": errors.append("model must remain incomplete")
    for name in ("source", "transcript_segment", "phrase_form", "function_observation", "delivery_observation", "pattern_card", "mechanism_hypothesis", "practice_task", "learner_observation", "listener_observation", "counterexample_observation", "practice_record", "mobile_lesson"):
        if name not in model.get("entity_types", {}): errors.append(f"missing entity type: {name}")
    for rule in ("Every pattern example links", "Every delivery observation links", "Every mechanism hypothesis", "Every practice task links", "Learner observations and listener observations", "Listener task scores", "Local practice records", "Every mobile lesson carries", "Missing, disagreement"):
        if not any(rule in item for item in model.get("link_rules", [])): errors.append(f"missing link rule beginning: {rule}")
    if model.get("current_manifest") != current.get("current_manifest"): errors.append("current manifest is stale")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "research/shared-evidence-model.json"
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid shared evidence model:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("shared evidence model valid: contract and manifest reconciled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
