#!/usr/bin/env python3
"""Build the shared web/mobile evidence-model contract and coverage manifest."""

from __future__ import annotations

import json
from pathlib import Path


def read(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text())


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    phrase = read(root, "research/corpus-phrase-form-inventory.json")
    evidence = read(root, "research/corpus-evidence-bank.json")
    lesson = read(root, "research/shared-lesson-cards.json")
    jobs = read(root, "research/communication-job-cards.json")
    delivery = read(root, "research/delivery-evidence-index.json")
    learner = read(root, "research/communication-job-learner-check.json")
    listener = read(root, "research/communication-job-listener-outcome-protocol.json")
    counterexamples = read(root, "research/communication-job-counterexample-workbook.json")
    return {
        "schema_version": "1.0",
        "model_id": "shared-communication-evidence-model",
        "status": "contract_ready_research_evidence_incomplete",
        "claim_boundary": "This contract lets web and mobile surfaces carry provenance and uncertainty together. The presence of a linked record never promotes a provisional observation to a validated pattern, learning result or listener outcome.",
        "claim_levels": [
            {"level": "source_observation", "meaning": "Checkable wording, audio, video or setting record."},
            {"level": "contextual_interpretation", "meaning": "Bounded reading supported by surrounding context."},
            {"level": "candidate_mechanism", "meaning": "Hypothesis about why a choice might help; not outcome evidence."},
            {"level": "provisional_pattern", "meaning": "Repeated candidate with denominators and limits; independent review still required here."},
            {"level": "practice_hypothesis", "meaning": "Exercise derived from the candidate; not proof that the source behavior works."},
            {"level": "learning_evidence", "meaning": "Observed learner teachability under a separate protocol."},
            {"level": "listener_outcome_evidence", "meaning": "Observed listener task outcome under a locked matched-stimulus study."},
        ],
        "entity_types": {
            "source": {"required": ["source_id", "title", "source_url", "provenance_status"]},
            "transcript_segment": {"required": ["evidence_id", "source_id", "text", "start_seconds", "end_seconds", "caption_status"]},
            "phrase_form": {"required": ["phrase_form_id", "family", "exact_form", "recurrence", "mechanism_hypothesis", "status"]},
            "function_observation": {"required": ["function_observation_id", "evidence_ids", "raw_label", "canonical_job", "status"]},
            "delivery_observation": {"required": ["delivery_observation_id", "evidence_id", "modality", "observation", "measurement_limit", "independence_status"]},
            "pattern_card": {"required": ["pattern_id", "communication_problem", "evidence_chain", "claim_level", "status"]},
            "mechanism_hypothesis": {"required": ["hypothesis_id", "text", "status", "alternative_explanations"]},
            "practice_task": {"required": ["task_id", "pattern_id", "phase", "prompt", "boundary"]},
            "learner_observation": {"required": ["record_id", "participant_code", "task_responses", "consent", "claim_boundary"]},
            "listener_observation": {"required": ["record_id", "stimulus_id", "condition", "task_responses", "scorer_id_or_blind_code", "claim_boundary"]},
            "counterexample_observation": {"required": ["counterexample_id", "pattern_id", "counterexample_type", "evidence_ids", "status", "alternative_explanation"]},
        },
        "status_vocabulary": {
            "evidence": ["retained", "missing", "restricted", "unrepaired_caption"],
            "interpretation": ["provisional", "indeterminate", "independently_reviewed", "adjudicated"],
            "delivery": ["not_available", "derived_proxy", "internal_bounded", "independent_reviewed"],
            "lesson": ["draft", "practice_hypothesis", "teachability_observed", "promoted_with_limits"],
            "outcome": ["not_run", "designed", "data_collected", "analyzed", "replicated"],
        },
        "link_rules": [
            "Every pattern example links to one or more exact transcript_segment IDs.",
            "Every delivery observation links to an exact segment when transcript alignment is claimed; otherwise it must say raw-media-only.",
            "Every mechanism hypothesis is marked as a hypothesis until an outcome protocol supports a narrower claim.",
            "Every practice task links to a pattern and carries a non-fit or safety boundary.",
            "Learner observations and listener observations remain separate entity types and separate claim levels.",
            "Missing, disagreement and indeterminate statuses remain visible to clients.",
        ],
        "client_contract": {
            "web": ["search by communication problem, job, phrase, modality and status", "show exact context before interpretation", "show limits, counterexamples and disagreement", "never hide missing validation"],
            "mobile": ["load the same pattern ID and evidence links", "show one bounded practice task and self-check", "support text, captioned and asynchronous use", "store learner records only with consent and claim boundary"],
        },
        "current_manifest": {
            "exact_phrase_forms": {"source": "research/corpus-phrase-form-inventory.json", "form_count": phrase["form_count"], "status": phrase["status"]},
            "exact_caption_evidence": {"source": "research/corpus-evidence-bank.json", "function_record_count": evidence["summary"]["function_record_count"], "caption_segment_record_count": evidence["summary"]["caption_segment_record_count"], "status": evidence["status"]},
            "validated_shared_lesson_cards": {"source": "research/shared-lesson-cards.json", "card_count": lesson["card_count"], "status": lesson["status"]},
            "provisional_job_cards": {"source": "research/communication-job-cards.json", "card_count": jobs["card_count"], "status": jobs["status"]},
            "delivery": {"source": "research/delivery-evidence-index.json", "internal_observation_count": delivery["coverage"]["internal_manual_observation_count"], "independent_observation_count": delivery["coverage"]["independent_review_count"], "status": delivery["status"]},
            "learner": {"source": "research/communication-job-learner-check.json", "card_count": learner["card_count"], "task_count": learner["task_count"], "completed_records": 0, "status": learner["status"]},
            "listener": {"source": "research/communication-job-listener-outcome-protocol.json", "pattern_count": len(listener["patterns"]), "stimulus_pairs_locked": listener["stimulus_pairs_locked"], "completed_records": 0, "status": listener["status"]},
            "counterexamples": {"source": "research/communication-job-counterexample-workbook.json", "job_count": counterexamples["job_count"], "queued_slot_count": counterexamples["item_count"], "completed_records": 0, "status": counterexamples["status"]},
        },
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/shared-evidence-model.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    manifest = result["current_manifest"]
    lines = ["# Shared communication evidence model", "", "Status: **contract ready; research evidence incomplete**.", "", result["claim_boundary"], "", "## Current coverage", "", "| Layer | Current state |", "|---|---|"]
    for key, value in manifest.items():
        details = ", ".join(f"{field}={item}" for field, item in value.items() if field not in {"source", "status"})
        lines.append(f"| `{key}` | `{value['status']}`; {details} |")
    lines += ["", "The JSON file defines entity requirements, status vocabulary, link rules and web/mobile client constraints. It is an interface contract, not evidence that the pending gates have been completed.", ""]
    (root / "writeups/shared-evidence-model.md").write_text("\n".join(lines))
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result["current_manifest"], indent=2))
