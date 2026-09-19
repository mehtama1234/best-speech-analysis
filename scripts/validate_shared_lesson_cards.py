#!/usr/bin/env python3
"""Validate the shared web/mobile lesson-card evidence contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_FILE = ROOT / "research/shared-lesson-cards.json"
REQUIRED_CARD_FIELDS = {
    "card_id", "communication_problem", "speech_function_hypothesis",
    "speech_function",
    "mechanism_hypothesis", "mechanism_status", "examples", "counterexamples",
    "delivery_evidence", "recurrence", "practice", "validation", "limits",
    "evidence_chain",
}
REQUIRED_CHAIN_FIELDS = {
    "communication_problem", "exact_language_and_function", "delivery_evidence",
    "mechanism_hypothesis", "cross_talk_recurrence", "counterexamples_and_limits",
    "practice", "learner_check", "listener_outcome_check",
}


def validate(data: dict) -> list[str]:
    errors = []
    if data.get("model_id") != "shared-lesson-cards": errors.append("model_id is invalid")
    if data.get("card_count") != len(data.get("cards", [])): errors.append("card_count does not match cards")
    if data.get("status") != "18_draft_cards_not_validated": errors.append("unexpected promotion status")
    for number, card in enumerate(data.get("cards", []), 1):
        missing = REQUIRED_CARD_FIELDS - set(card)
        if missing: errors.append(f"card {number} missing fields: {sorted(missing)}")
        if not card.get("communication_problem"): errors.append(f"card {number} has no communication problem")
        if card.get("speech_function", {}).get("status") != "provisional_transcript_function_label_requires_context_and_independent_review": errors.append(f"card {number} speech function is not provisional")
        if not card.get("speech_function", {}).get("candidate_family"): errors.append(f"card {number} has no candidate speech-function family")
        if not card.get("examples"): errors.append(f"card {number} has no examples")
        if not card.get("counterexamples"): errors.append(f"card {number} has no counterexamples")
        if card.get("mechanism_status") != "bounded_hypothesis_not_outcome_evidence": errors.append(f"card {number} mechanism status is not bounded")
        chain = card.get("evidence_chain", {})
        missing_chain = REQUIRED_CHAIN_FIELDS - set(chain)
        if missing_chain: errors.append(f"card {number} missing chain fields: {sorted(missing_chain)}")
        if chain.get("listener_outcome_check", {}).get("status") != "not_tested": errors.append(f"card {number} listener status is not not_tested")
        if chain.get("learner_check", {}).get("status") != card.get("validation", {}).get("learner_status"): errors.append(f"card {number} learner status mismatch")
        if chain.get("mechanism_hypothesis", {}).get("status") != card.get("mechanism_status"): errors.append(f"card {number} mechanism status mismatch")
        if chain.get("exact_language_and_function", {}).get("phrase_family") != card.get("recurrence", {}).get("phrase_family"): errors.append(f"card {number} phrase family mismatch")
        if not isinstance(chain.get("cross_talk_recurrence", {}).get("event_level_holdout"), dict): errors.append(f"card {number} missing event-level recurrence")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CARD_FILE
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid shared lesson cards:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("shared lesson cards valid: evidence chain present; promotion remains provisional")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
