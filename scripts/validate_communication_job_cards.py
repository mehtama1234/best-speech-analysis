#!/usr/bin/env python3
"""Validate the provisional communication-job cards against their evidence bank."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/communication-job-cards.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"

REQUIRED_CARD_FIELDS = ("card_id", "canonical_job", "problem", "mechanism", "form", "practice", "self_check", "non_fit", "recurrence", "exact_examples", "delivery_evidence_status", "delivery_observations", "validation")
REQUIRED_VALIDATION_FIELDS = ("independent_function_review", "independent_recurrence_review", "delivery_review", "learner_check", "listener_outcome")


def validate(cards: dict, evidence_bank: dict | None = None) -> list[str]:
    evidence_bank = evidence_bank or json.loads(EVIDENCE.read_text())
    errors: list[str] = []
    rows = cards.get("cards", [])
    if cards.get("card_count") != len(rows):
        errors.append("card_count does not match cards")
    if cards.get("status") != "provisional_transcript_cards_not_validated":
        errors.append("card set must remain explicitly provisional")
    ids = [row.get("card_id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("card IDs are not unique")
    evidence_ids = {segment["evidence_id"] for record in evidence_bank.get("records", []) for segment in record.get("segments", [])}
    for index, card in enumerate(rows):
        prefix = f"card {index}"
        for field in REQUIRED_CARD_FIELDS:
            if field not in card or card[field] is None or (isinstance(card[field], str) and not card[field].strip()):
                errors.append(f"{prefix} missing required field: {field}")
        recurrence = card.get("recurrence", {})
        for field in ("function_record_count", "video_count"):
            if not isinstance(recurrence.get(field), int) or recurrence[field] <= 0:
                errors.append(f"{prefix} recurrence {field} must be a positive integer")
        for example_index, example in enumerate(card.get("exact_examples", [])):
            eprefix = f"{prefix} example {example_index}"
            if not example.get("source_url", "").startswith("https://"):
                errors.append(f"{eprefix} source_url is not https")
            quality = example.get("example_quality", {})
            if quality.get("lexical_speech_present") is not True or not isinstance(quality.get("lexical_word_count"), int) or quality["lexical_word_count"] <= 0:
                errors.append(f"{eprefix} lacks lexical speech quality evidence")
            segments = example.get("exact_segments", [])
            if not segments:
                errors.append(f"{eprefix} has no exact segments")
            for segment in segments:
                evidence_id = segment.get("evidence_id")
                if evidence_id not in evidence_ids:
                    errors.append(f"{eprefix} references unknown evidence_id: {evidence_id}")
                if not str(segment.get("text", "")).strip():
                    errors.append(f"{eprefix} has an empty transcript segment")
        for observation in card.get("delivery_observations", []):
            if observation.get("delivery_evidence_status") != "internal_bounded_review_not_independent":
                errors.append(f"{prefix} delivery observation has an invalid independence status")
        for field in REQUIRED_VALIDATION_FIELDS:
            if field not in card.get("validation", {}):
                errors.append(f"{prefix} validation missing field: {field}")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CARDS
    errors = validate(json.loads(path.read_text()))
    if errors:
        print("invalid communication-job cards:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("communication-job cards valid: 18 provisional evidence-linked cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
