#!/usr/bin/env python3
"""Build the protocol and record contract for later listener-outcome tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research/listener-outcome-protocol.json"
OUT_MD = ROOT / "writeups/listener-outcome-protocol.md"


def main() -> int:
    patterns = [
        ("provisional-contrast_or_disagreement", "show a change or distinction without inferring motive"),
        ("provisional-example", "make an abstract claim concrete without treating an example as proof"),
        ("provisional-story_or_personal_experience", "use bounded personal detail without making it universal"),
        ("provisional-uncertainty_or_qualification", "state a claim with an appropriate limit"),
        ("provisional-conclusion_or_summary", "mark a takeaway and preserve its limit"),
        ("candidate-question", "invite clarification or reflection without pressure"),
        ("candidate-definition_or_reformulation", "make a term precise without overclaiming"),
        ("candidate-call_to_action", "make an optional action specific and bounded"),
    ]
    protocol = {
        "schema_version": "1.0",
        "protocol_id": "listener-outcome-protocol",
        "status": "design_complete_not_run",
        "purpose": "Test listener comprehension and immediate recall of matched speech versions, separately from learner teachability and from claims about trust, persuasion or behavior.",
        "claim_boundary": "A result can show differences in the measured listener task under this protocol. It cannot establish that a celebrity's delivery caused trust, long-term memory, persuasion, engagement or action in general.",
        "design": {
            "unit": "listener-session-by-stimulus",
            "comparison": "randomized matched control versus pattern-informed version with the same proposition, topic, length range and factual content",
            "assignment": "randomize version order and pattern order within participant; keep scorer blind to condition where practical",
            "holdout": "Use new locally authored stimuli not copied from the source speeches; reserve a stimulus set until analysis is locked.",
            "minimum_reporting": ["participant count and exclusions", "condition counts", "stimulus IDs", "missing responses", "scoring rubric", "confidence intervals or uncertainty summary", "adverse/accessibility notes"],
        },
        "patterns": [
            {"pattern_id": pattern_id, "communication_job": job, "stimulus_requirement": "matched short speech pair; no personal disclosure required"}
            for pattern_id, job in patterns
        ],
        "listener_tasks": [
            {"task_id": "main_point_recall", "prompt": "State the speaker's main point in your own words without seeing the script.", "measure": "blind rubric score 0–2"},
            {"task_id": "evidence_or_example_identification", "prompt": "Name the example, reason or evidence the speaker used, if any.", "measure": "blind rubric score 0–2"},
            {"task_id": "limit_or_uncertainty_identification", "prompt": "State one limit, uncertainty or condition the speaker included, or say that none was clear.", "measure": "blind rubric score 0–2"},
            {"task_id": "requested_action_identification", "prompt": "What action, if any, did the speaker invite? Include owner or condition if stated.", "measure": "blind rubric score 0–2"},
            {"task_id": "confusion_and_load", "prompt": "Report what was confusing, rushed, emotionally difficult or easy to follow; do not require agreement.", "measure": "coded response plus optional rating"},
            {"task_id": "delayed_recall", "prompt": "After a defined delay, restate the main point and one supporting detail.", "measure": "blind rubric score 0–2; only if delay and consent are feasible"},
        ],
        "controls": [
            "Keep proposition, topic, vocabulary, length and reading/listening modality matched.",
            "Do not use source celebrity identity as the experimental manipulation.",
            "Pretest readability, caption quality and accessibility before data collection.",
            "Record whether a participant already knew the topic and whether they agreed with it.",
            "Treat agreement, trust and liking as separate optional measures, never as comprehension proxies.",
        ],
        "consent_and_accessibility": [
            "Use plain-language consent and allow withdrawal without penalty.",
            "Offer text, captioned audio/video and screen-reader-compatible response modes.",
            "Do not require trauma, medical, political or personal disclosures.",
            "Minimize retention of recordings; obtain separate permission for any recording.",
        ],
        "record_schema": {
            "required": ["participant_code", "date", "protocol_version", "consent", "modality", "stimulus_id", "condition", "task_responses", "scorer_id_or_blind_code"],
            "optional": ["prior_topic_familiarity", "agreement_rating", "confidence", "accessibility_accommodation", "withdrawal_or_missing_reason"],
            "condition_values": ["control", "pattern_informed", "unknown_or_blinded"],
            "score_values": [0, 1, 2, None],
        },
        "record_form": "writeups/listener-outcome-record.html",
        "analysis_plan": [
            "Report item-level and aggregate comprehension/recall with uncertainty; do not average away missingness or accessibility failures.",
            "Compare pattern-informed versus control within stimulus and, where possible, within participant.",
            "Inspect null results, reversals and condition-by-topic interactions.",
            "Pre-register primary task and exclusion rules before unblinding condition labels.",
            "Treat any result as local to the authored stimuli and tested population until replicated.",
        ],
        "not_run_reason": "The repository contains no consented listener observations or locked matched stimulus set yet.",
    }
    OUT_JSON.write_text(json.dumps(protocol, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Listener-outcome protocol", "", "Status: **design complete, not run**.", "", protocol["claim_boundary"], "",
        "## Design", "", "- Comparison: randomized matched control versus pattern-informed version.", "- Unit: listener-session-by-stimulus.", "- Analysis: blind rubric scores for comprehension and recall, with condition and stimulus uncertainty.", "",
        "## Listener tasks", "", "| Task | Measure |", "|---|---|"]
    lines += [f"| `{task['task_id']}` | {task['measure']} |" for task in protocol["listener_tasks"]]
    lines += ["", "## Safety and accessibility", ""] + [f"- {item}" for item in protocol["consent_and_accessibility"]] + ["", "## Not yet evidence", "", protocol["not_run_reason"], ""]
    OUT_MD.write_text("\n".join(lines))
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
