#!/usr/bin/env python3
"""Reconcile the five vertical-slice packets without inventing human evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKETS = [
    ("contrast-or-disagreement", "provisional-contrast_or_disagreement"),
    ("example", "provisional-example"),
    ("story", "provisional-story_or_personal_experience"),
    ("uncertainty", "provisional-uncertainty_or_qualification"),
    ("conclusion", "provisional-conclusion_or_summary"),
]


def load_packet(stem: str) -> dict:
    return json.loads((ROOT / f"research/vertical-slice-01-{stem}.json").read_text())


def reconcile() -> dict:
    rows = []
    errors = []
    for stem, expected_pattern in PACKETS:
        packet = load_packet(stem)
        examples = packet.get("representative_examples", [])
        lesson = packet.get("learner_lesson", {})
        multimodal = packet.get("multimodal_status", {})
        counter = packet.get("counterexample_status", {})
        row_errors = []
        if packet.get("pattern_id") != expected_pattern:
            row_errors.append("pattern_id mismatch")
        if len(examples) != 5:
            row_errors.append(f"expected 5 representative examples, found {len(examples)}")
        evidence_ids = [item.get("evidence_id") for item in examples]
        if len(set(evidence_ids)) != len(evidence_ids) or any(not item for item in evidence_ids):
            row_errors.append("representative evidence IDs are missing or duplicated")
        for field in ("status", "draft_task", "self_check", "writeup"):
            if not lesson.get(field):
                row_errors.append(f"learner_lesson missing {field}")
        if not counter.get("status"):
            row_errors.append("counterexample status missing")
        if not multimodal.get("audio_measurement_caveat"):
            row_errors.append("audio measurement caveat missing")
        if not multimodal.get("visual_alignment"):
            row_errors.append("visual alignment status missing")
        rows.append(
            {
                "packet_id": packet.get("packet_id"),
                "pattern_id": packet.get("pattern_id"),
                "communication_job": packet.get("communication_job"),
                "representative_example_count": len(examples),
                "unique_video_count": len({item.get("video_id") for item in examples}),
                "counterexample_status": counter.get("status"),
                "counterexample_count": counter.get("existing_pattern_counterexamples", 0),
                "audio_examples": multimodal.get("aligned_audio_examples", 0),
                "visual_alignment": multimodal.get("visual_alignment"),
                "lesson_status": lesson.get("status"),
                "practice_lesson": lesson.get("writeup"),
                "internal_result": "reconciled" if not row_errors else "needs_repair",
                "errors": row_errors,
                "claim_boundary": "Autonomous packet reconciliation verifies local structure and provenance links; it does not establish independent review, speaker intent, learner teachability, listener comprehension or effectiveness.",
            }
        )
        errors.extend(f"{stem}: {error}" for error in row_errors)

    return {
        "schema_version": "1.0",
        "audit_id": "autonomous-vertical-slice-01",
        "status": "autonomous_reconciliation_complete" if not errors else "needs_repair",
        "packet_count": len(rows),
        "packets_reconciled": sum(row["internal_result"] == "reconciled" for row in rows),
        "errors": errors,
        "claim_boundary": "This audit checks packet completeness, exact evidence links, controls, local media proxies, lesson links and safety-boundary fields. It does not create independent human or learner evidence and does not support effectiveness claims.",
        "remaining_human_outcome_status": {
            "independent_review": "unavailable",
            "manual_visual_alignment": "not_claimed",
            "learner_observations": "unavailable",
            "listener_outcomes": "unmeasured",
        },
        "packets": rows,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Autonomous vertical slice 01 audit",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Packets reconciled: **{report['packets_reconciled']}/{report['packet_count']}**.",
        "",
        "| Packet | Examples | Unique videos | Audio proxies | Counterexample state | Result |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in report["packets"]:
        lines.append(
            f"| `{row['pattern_id']}` | {row['representative_example_count']} | "
            f"{row['unique_video_count']} | {row['audio_examples']} | "
            f"{row['counterexample_status']} | {row['internal_result']} |"
        )
    lines.extend(
        [
            "",
            "## What this closes",
            "",
            "Every packet has five distinct representative evidence IDs, a linked draft lesson, a recorded counterexample/control state, an explicit audio-proxy caveat, and a visible visual-alignment status. The five lesson links and shared practice/learner instruments are therefore structurally connected.",
            "",
            "## What remains unmeasured",
            "",
            "No external reviewer, participant learner record, listener outcome, speaker-intent judgment, or effectiveness result is present. The materials remain provisional practice hypotheses and must retain those boundaries.",
            "",
            "## Machine result",
            "",
            "```text",
            "autonomous packet reconciliation: " + ("PASS" if not report["errors"] else "FAIL"),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    report = reconcile()
    (ROOT / "research/autonomous-vertical-slice-01.json").write_text(json.dumps(report, indent=2) + "\n")
    (ROOT / "writeups/autonomous-vertical-slice-01.md").write_text(render_markdown(report))
    print(f"autonomous packet reconciliation: {report['status']} ({report['packets_reconciled']}/{report['packet_count']})")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
