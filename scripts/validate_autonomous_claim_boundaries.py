#!/usr/bin/env python3
"""Audit that provisional lessons and protocols retain their non-promotion boundaries."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def validate() -> list[str]:
    errors: list[str] = []
    cards_payload = read("research/shared-lesson-cards.json")
    mobile_payload = read("research/communication-job-mobile-lessons.json")
    learner = read("research/communication-job-learner-check.json")
    listener = read("research/communication-job-listener-outcome-protocol.json")
    if cards_payload.get("status") != "18_draft_cards_not_validated":
        errors.append("shared cards status is not draft/not validated")
    if mobile_payload.get("status") != "mobile_payload_provisional_not_validated":
        errors.append("mobile payload status is not provisional/not validated")
    required_claim_terms = {
        "shared cards": ("not", "listener", "success"),
        "mobile payload": ("not", "effective", "outcome-producing"),
        "learner": ("not", "listener outcomes", "improves"),
        "listener": ("cannot establish", "trust", "generally"),
    }
    for name, payload in (("shared cards", cards_payload), ("mobile payload", mobile_payload), ("learner", learner), ("listener", listener)):
        boundary = payload.get("claim_boundary", "").lower()
        for term in required_claim_terms[name]:
            if term not in boundary:
                errors.append(f"{name} claim boundary lacks {term}")
    if len(cards_payload.get("cards", [])) != 18 or len(mobile_payload.get("lessons", [])) != 18:
        errors.append("lesson payloads do not contain 18 records")
    prohibited = {"causal effectiveness", "listener outcomes", "universal best practice", "speaker intent"}
    for card in cards_payload.get("cards", []):
        job = card.get("canonical_job")
        if card.get("status") != "provisional_not_validated":
            errors.append(f"{job}: card promotes status")
        validation = card.get("validation", {})
        for key in ("independent_function_review", "independent_recurrence_review", "learner_status", "listener_outcomes", "speaker_event_independence"):
            if not validation.get(key) or validation[key] in {"complete", "validated", "passed"}:
                errors.append(f"{job}: validation field {key} is missing or promoted")
        do_not_claim = set(card.get("limits", {}).get("do_not_claim", []))
        if not prohibited.issubset(do_not_claim):
            errors.append(f"{job}: limits do_not_claim misses {sorted(prohibited - do_not_claim)}")
        if {x.get("status") for x in card.get("counterexamples", [])} != {"pending"}:
            errors.append(f"{job}: counterexample queue contains a promoted status")
    for lesson in mobile_payload.get("lessons", []):
        job = lesson.get("canonical_job")
        if lesson.get("claim_level") != "practice_hypothesis" or lesson.get("status") != "provisional_not_validated":
            errors.append(f"{job}: mobile lesson status/claim level promoted")
        validation = lesson.get("validation", {})
        if validation.get("learner_observations") != "not_run" or validation.get("listener_outcomes") != "not_run":
            errors.append(f"{job}: mobile learner/listener status is not explicitly not_run")
        if not lesson.get("safety_boundary") or not lesson.get("delivery_boundary"):
            errors.append(f"{job}: mobile safety or delivery boundary missing")
    if listener.get("status") != "design_complete_not_run" or not listener.get("not_run_reason"):
        errors.append("listener protocol does not explicitly remain not run")
    if learner.get("status") != "protocol_drafted_not_run" or not learner.get("outcome_boundary"):
        errors.append("learner protocol does not explicitly remain not run")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous claim-boundary audit valid: 18 cards and 18 mobile lessons remain explicitly provisional")
