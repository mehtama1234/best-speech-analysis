#!/usr/bin/env python3
"""Normalize the eight draft packets into one web/mobile lesson-card model."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/shared-provisional-curriculum.json"
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
OUT = ROOT / "research/shared-lesson-cards.json"

LABELS = {
    "provisional-contrast_or_disagreement": "contrast_or_disagreement",
    "provisional-example": "example",
    "provisional-story_or_personal_experience": "story_or_personal_experience",
    "provisional-uncertainty_or_qualification": "uncertainty_or_qualification",
    "provisional-conclusion_or_summary": "conclusion_or_summary",
    "candidate-question": "question",
    "candidate-definition_or_reformulation": "definition",
    "candidate-call_to_action": "call_to_action",
}

MECHANISMS = {
    "contrast_or_disagreement": "Hypothesis: naming both sides can make a change or distinction visible and reduce the need for a listener to infer the speaker's replacement claim or motive.",
    "example": "Hypothesis: a concrete case can give an abstract claim a handle the listener can inspect, while the explicit return to the claim prevents the case from being mistaken for proof.",
    "story_or_personal_experience": "Hypothesis: a bounded event with time, place or action can give an abstract point human and temporal scale; a boundary keeps one experience from being treated as universal evidence.",
    "uncertainty_or_qualification": "Hypothesis: an explicit qualifier can mark whether a statement is observed, predicted, interpreted or recommended, helping the listener locate its certainty and revision conditions.",
    "conclusion_or_summary": "Hypothesis: a summary marker can compress preceding material and direct attention to the intended takeaway, while a stated limit reduces overgeneralization.",
    "question": "Hypothesis: a question form can allocate attention or a conversational turn toward inquiry, reflection or shared orientation, but its effect depends on whether the listener can answer without pressure.",
    "definition": "Hypothesis: a small operational meaning can reduce ambiguity around an unfamiliar term; stating what it excludes can prevent the definition from being overextended.",
    "call_to_action": "Hypothesis: naming an action, owner, time horizon and limit can turn a broad aspiration into a bounded choice that a listener can evaluate against real authority and resources.",
}

PRACTICE_SELF_CHECKS = {
    "question": [
        "Can I name whether the question seeks information, opens reflection, checks shared attention or manages a turn?",
        "Could the listener answer without being pressured to agree?",
        "Did I test whether a direct statement or transition would serve the job better?",
        "Did I avoid treating a question marker as proof of engagement?",
    ],
    "definition": [
        "Did I give an operational meaning rather than an accusation or persuasion disguised as a definition?",
        "Did I state one boundary or exclusion?",
        "Is the definition needed for this audience and moment?",
        "Can a listener restate the term without extending it beyond its stated limit?",
    ],
    "call_to_action": [
        "Did I name a feasible action rather than only an aspiration?",
        "Did I identify the owner, resources and time horizon?",
        "Did I include consent, opt-out or safety limits where relevant?",
        "Did I state what the action cannot solve?",
    ],
}


def normalize_example(example: dict, context_lookup: dict | None = None, video_rows: dict[str, list[dict]] | None = None) -> dict:
    evidence_id = example.get("evidence_id")
    source_row = context_lookup.get(evidence_id, {}) if context_lookup and evidence_id else {}
    context = example.get("context", [])
    if not context and evidence_id and context_lookup and video_rows:
        row = source_row
        if row:
            rows = video_rows.get(row.get("video_id"), [])
            index = next((i for i, candidate in enumerate(rows) if candidate.get("evidence_id") == evidence_id), None)
            if index is not None:
                context = [
                    {
                        "evidence_id": candidate.get("evidence_id"),
                        "start_seconds": candidate.get("start_seconds"),
                        "end_seconds": candidate.get("end_seconds"),
                        "text": candidate.get("text", ""),
                    }
                    for candidate in rows[max(0, index - 2): index + 3]
                ]
    video_id = example.get("video_id") or (evidence_id.split(":", 1)[0] if evidence_id and ":" in evidence_id else None)
    return {
        "evidence_id": evidence_id,
        "video_id": video_id,
        "title": example.get("title") or source_row.get("title"),
        "start_seconds": example.get("start_seconds", source_row.get("start_seconds")),
        "end_seconds": example.get("end_seconds", source_row.get("end_seconds")),
        "source_url": example.get("url") or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None),
        "exact_text": example.get("text") or source_row.get("text"),
        "surrounding_context": context,
        "observed_function": example.get("reviewed_speech_function", example.get("function_hypothesis")),
        "interpretation": example.get("interpretation"),
        "boundary": example.get("boundary"),
        "measurement_status": example.get("measurement_status"),
    }


def normalize_counterexample(example: dict, context_lookup: dict | None = None, video_rows: dict[str, list[dict]] | None = None) -> dict:
    """Normalize a control/failure candidate without upgrading its status."""
    item = normalize_example(example, context_lookup, video_rows)
    item["counterexample_status"] = example.get("status", "control_or_alternate_case")
    item["why_selected"] = example.get("why_selected", example.get("why_it_is_a_control"))
    item["what_it_can_support"] = example.get("what_it_can_support")
    item["what_it_cannot_support"] = example.get("what_it_cannot_support")
    item["required_followup"] = example.get("required_followup", [])
    return item


def main() -> int:
    index = json.loads(INDEX.read_text())
    atlas = json.loads(ATLAS.read_text())
    context_lookup = {}
    video_rows = {}
    with (ROOT / "research/segment-registry.jsonl").open() as registry:
        for line in registry:
            row = json.loads(line)
            context_lookup[row["evidence_id"]] = row
            video_rows.setdefault(row["video_id"], []).append(row)
    delivery_items = []
    for report_name in (
        "research/vertical-slice-01-manual-multimodal-review.json",
        "research/vertical-slice-02-manual-multimodal-review.json",
        "research/multimodal-expansion-manual-review.json",
        "research/multimodal-expansion-manual-review-02.json",
    ):
        report = json.loads((ROOT / report_name).read_text())
        delivery_items.extend(report.get("items", []))
    delivery_by_evidence = {item.get("evidence_id"): item for item in delivery_items if item.get("evidence_id")}
    recurrence = atlas["phrase_forms"]
    task_banks = [
        json.loads((ROOT / "research/vertical-slice-01-learner-task-bank.json").read_text()),
        json.loads((ROOT / "research/vertical-slice-02-learner-task-bank.json").read_text()),
    ]
    tasks = [task for bank in task_banks for task in bank["tasks"]]
    cards = []
    for row in index["lessons"]:
        packet = json.loads((ROOT / row["packet"]).read_text())
        pattern_id = row["pattern_id"]
        family = LABELS[pattern_id]
        card_tasks = [task for task in tasks if task["pattern_id"] == pattern_id]
        independence = packet.get("independence_status")
        independence_status = independence.get("status") if isinstance(independence, dict) else independence
        delivery_observations = []
        for example in packet.get("representative_examples", []):
            observation = delivery_by_evidence.get(example.get("evidence_id"))
            if observation:
                delivery_observations.append({
                    "evidence_id": observation.get("evidence_id"),
                    "sampled_time_seconds": observation.get("sampled_time_seconds"),
                    "frame_observation": observation.get("frame_observation"),
                    "alignment_decision": observation.get("alignment_decision"),
                    "alignment_limit": observation.get("alignment_limit"),
                    "measured_audio_proxy": observation.get("measured_audio_proxy"),
                    "nearest_frame_measurement": observation.get("nearest_frame_measurement"),
                    "feature_limit": observation.get("feature_limit"),
                    "review_status": observation.get("review_status"),
                })
        packet_counterexamples = [normalize_example(example, context_lookup, video_rows) for example in packet.get("counterexamples", [])]
        counterexample_status = packet.get("counterexample_status", {})
        if family == "contrast_or_disagreement" and not packet_counterexamples:
            for example in counterexample_status.get("controls_recorded", []):
                packet_counterexamples.append(normalize_counterexample(example, context_lookup, video_rows))
            for example in counterexample_status.get("alternate_function_controls", []):
                packet_counterexamples.append(normalize_counterexample(example, context_lookup, video_rows))
            for example in counterexample_status.get("failed_or_ineffective_candidates", []):
                packet_counterexamples.append(normalize_counterexample(example, context_lookup, video_rows))
        card = {
            "card_id": pattern_id,
            "slice": row["slice"],
            "status": row["lesson_status"],
            "evidence_level": row["evidence_level"],
            "claim_boundary": packet.get("claim_boundary", packet.get("source_policy")),
            "communication_problem": packet["communication_job"],
            "speech_function": {
                "candidate_family": family,
                "observed_example_functions": sorted({
                    example.get("reviewed_speech_function", example.get("function_hypothesis"))
                    for example in packet.get("representative_examples", [])
                    if example.get("reviewed_speech_function", example.get("function_hypothesis"))
                }),
                "status": "provisional_transcript_function_label_requires_context_and_independent_review",
            },
            "speech_function_hypothesis": packet.get("practice_hypothesis"),
            "mechanism_hypothesis": MECHANISMS[family],
            "mechanism_status": "bounded_hypothesis_not_outcome_evidence",
            "source_packet": row["packet"],
            "lesson_writeup": row["lesson"],
            "examples": [normalize_example(example, context_lookup, video_rows) for example in packet.get("representative_examples", [])],
            "counterexamples": packet_counterexamples,
            "delivery_evidence": {
                "status": packet.get("multimodal_status"),
                "observations": delivery_observations,
                "boundary": "Delivery observations are partial and do not establish effectiveness.",
            },
            "recurrence": {
                "phrase_family": family,
                "phrase_forms": recurrence[family]["phrase_forms"],
                "retrieval_samples": recurrence[family]["sample_occurrences"][:5],
                "atlas_status": recurrence[family]["status"],
                "eligible_video_hit_count": recurrence[family]["video_hit_count"],
                "eligible_segment_hit_count": recurrence[family]["segment_hit_count"],
                "event_level_holdout": recurrence[family]["event_level_holdout"],
            },
            "practice": {
                "hypothesis": packet.get("practice_hypothesis"),
                "task_count": len(card_tasks),
                "tasks": card_tasks,
                "self_check": packet.get("learner_lesson", {}).get("self_check", []) or PRACTICE_SELF_CHECKS.get(family, []),
            },
            "validation": {
                "independent_review": row["independent_review_status"],
                "learner_status": row["learner_status"],
                "listener_outcomes": "not_tested",
                "speaker_event_independence": independence_status,
            },
            "limits": {
                "counterexample_count": len(packet.get("counterexamples", [])),
                "next_actions": packet.get("next_action", packet.get("next_actions", [])),
                "do_not_claim": ["causal effectiveness", "listener outcomes", "speaker intent", "universal best practice"],
            },
        }
        card["evidence_chain"] = {
            "communication_problem": {
                "value": card["communication_problem"],
                "status": "lesson_problem_statement",
            },
            "exact_language_and_function": {
                "phrase_family": family,
                "phrase_forms": card["recurrence"]["phrase_forms"],
                "example_evidence_ids": [example["evidence_id"] for example in card["examples"] if example.get("evidence_id")],
                "function_status": card["speech_function"]["status"],
                "candidate_family": card["speech_function"]["candidate_family"],
                "observed_example_functions": card["speech_function"]["observed_example_functions"],
            },
            "delivery_evidence": {
                "evidence_ids": [observation["evidence_id"] for observation in delivery_observations if observation.get("evidence_id")],
                "status": card["delivery_evidence"]["status"],
                "boundary": card["delivery_evidence"]["boundary"],
            },
            "mechanism_hypothesis": {
                "text": card["mechanism_hypothesis"],
                "status": card["mechanism_status"],
            },
            "cross_talk_recurrence": {
                "video_hit_count": card["recurrence"]["eligible_video_hit_count"],
                "segment_hit_count": card["recurrence"]["eligible_segment_hit_count"],
                "event_level_holdout": card["recurrence"]["event_level_holdout"],
                "status": card["recurrence"]["atlas_status"],
            },
            "counterexamples_and_limits": {
                "counterexample_evidence_ids": [example["evidence_id"] for example in card["counterexamples"] if example.get("evidence_id")],
                "do_not_claim": card["limits"]["do_not_claim"],
                "status": "bounded_not_sufficient_for_effectiveness",
            },
            "practice": {
                "task_count": card["practice"]["task_count"],
                "task_ids": [task.get("task_id") for task in card_tasks if task.get("task_id")],
                "status": "draft_practice_hypothesis",
            },
            "learner_check": {
                "artifact": row.get("learner_check"),
                "status": card["validation"]["learner_status"],
            },
            "listener_outcome_check": {
                "protocol": "research/listener-outcome-protocol.json",
                "status": card["validation"]["listener_outcomes"],
            },
        }
        cards.append(card)
    output = {
        "schema_version": "1.0",
        "model_id": "shared-lesson-cards",
        "status": "eight_draft_cards_not_validated",
        "claim_boundary": "This is a shared web/mobile data model for provisional evidence-linked lessons. It does not promote any pattern or claim learner or listener success.",
        "source_index": "research/shared-provisional-curriculum.json",
        "card_count": len(cards),
        "cards": cards,
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
