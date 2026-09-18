#!/usr/bin/env python3
"""Produce a conservative readiness audit for vertical slice 01.

This report distinguishes structural evidence from validation evidence. It is
deliberately unable to promote a packet merely because its JSON is complete.
"""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    "contrast-or-disagreement",
    "example",
    "story",
    "uncertainty",
    "conclusion",
]
OUT_JSON = ROOT / "research/vertical-slice-01-validation-audit.json"
OUT_MD = ROOT / "writeups/vertical-slice-01-validation-audit.md"


def load(path):
    return json.loads(path.read_text())


def audit_packet(name):
    packet = load(ROOT / f"research/vertical-slice-01-{name}.json")
    controls = packet.get("counterexample_status", {})
    review = packet.get("independent_review", {})
    independence = packet.get("independence_status", {})
    multimodal = packet.get("multimodal_status", {})
    issues = []

    if len(packet.get("representative_examples", [])) < 3:
        issues.append({"gate": "representative_examples", "severity": "blocking"})
    if not controls:
        issues.append({"gate": "counterexamples", "severity": "blocking"})
    if independence.get("status") != "verified_speaker_and_event_independence":
        issues.append({
            "gate": "speaker_event_independence",
            "severity": "blocking",
            "status": independence.get("status", "missing"),
        })
    if multimodal.get("visual_alignment") != "manually_verified":
        issues.append({
            "gate": "visual_alignment",
            "severity": "blocking",
            "status": multimodal.get("visual_alignment", "missing"),
        })
    if review.get("status") != "complete":
        issues.append({
            "gate": "independent_review",
            "severity": "blocking",
            "status": review.get("status", "missing"),
        })
    return {
        "packet": f"research/vertical-slice-01-{name}.json",
        "pattern_id": packet["pattern_id"],
        "packet_status": packet.get("status"),
        "representative_example_count": len(packet.get("representative_examples", [])),
        "control_status": controls.get("status", "missing"),
        "independent_review_status": review.get("status", "missing"),
        "speaker_event_status": independence.get("status", "missing"),
        "visual_alignment_status": multimodal.get("visual_alignment", "missing"),
        "issues": issues,
        "ready_for_promotion": not issues,
    }


def main():
    learner = load(ROOT / "research/vertical-slice-01-learner-check.json")
    media = load(ROOT / "research/vertical-slice-01-media-audit.json")
    manual_review = load(ROOT / "research/vertical-slice-01-manual-multimodal-review.json")
    official_checks = load(ROOT / "research/vertical-slice-01-official-source-checks.json")
    packets = [audit_packet(name) for name in NAMES]
    learner_ready = learner.get("status") == "complete"
    report = {
        "schema_version": "1.0",
        "audit_id": "vertical-slice-01-validation-audit",
        "status": "not_ready_for_promotion",
        "claim_boundary": "This audit proves repository readiness conditions only; it does not prove listener, trust, memory, persuasion or action outcomes.",
        "packet_count": len(packets),
        "packets_ready_for_promotion": sum(p["ready_for_promotion"] for p in packets),
        "learner_protocol_status": learner.get("status", "missing"),
        "learner_observations_available": learner_ready,
        "media_audit": {
            "path": "research/vertical-slice-01-media-audit.json",
            "packet_item_occurrences": media["packet_item_occurrences"],
            "unique_video_ids": media["unique_video_ids"],
            "unique_ids_with_raw_media": media["unique_ids_with_raw_media"],
            "contradiction_count": media["contradiction_count"],
        },
        "manual_multimodal_review": {
            "path": "research/vertical-slice-01-manual-multimodal-review.json",
            "status": manual_review["status"],
            "independence": manual_review["independence"],
            "item_count": len(manual_review["items"]),
        },
        "official_source_checks": {
            "path": "research/vertical-slice-01-official-source-checks.json",
            "status": official_checks["status"],
            "check_count": len(official_checks["checks"]),
            "event_context_corroborated": sum(
                check["status"].startswith((
                    "event_and_participants_corroborated",
                    "event_context_corroborated",
                ))
                for check in official_checks["checks"]
            ),
            "exact_upload_event_verified": sum(
                "exact_upload_event_verified" in check["status"]
                for check in official_checks["checks"]
            ),
        },
        "learner_gate": {
            "status": "blocked_pending_run" if not learner_ready else "complete",
            "required_protocol": "research/vertical-slice-01-learner-check.json",
        },
        "packets": packets,
        "next_actions": [
            "Obtain independent review with reviewer identity, per-item decisions and disagreements.",
            "Verify remaining speaker/event identity and manually inspect audio/video alignment.",
            "Run the learner protocol with consented participants and record rubric-level results.",
            "Revise lessons from observed failures before any promotion claim.",
        ],
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")

    lines = [
        "# Vertical slice 01 validation audit",
        "",
        "Status: **not ready for promotion**.",
        "",
        report["claim_boundary"],
        "",
        f"Packets ready: **{report['packets_ready_for_promotion']}/{report['packet_count']}**.",
        f"Learner protocol: **{report['learner_protocol_status']}**.",
        "",
        "## Packet gates",
        "",
        "| Packet | Examples | Review | Speaker/event | Visual alignment | Result |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for packet in packets:
        result = "ready" if packet["ready_for_promotion"] else "not ready"
        lines.append(
            f"| `{packet['pattern_id']}` | {packet['representative_example_count']} | "
            f"{packet['independent_review_status']} | {packet['speaker_event_status']} | "
            f"{packet['visual_alignment_status']} | {result} |"
        )
    lines += [
        "",
        "## Provenance checks",
        "",
        f"Official-source checks recorded: **{report['official_source_checks']['check_count']}**; event contexts corroborated: **{report['official_source_checks']['event_context_corroborated']}**; exact upload/event matches verified: **{report['official_source_checks']['exact_upload_event_verified']}**.",
        "Partial corroboration does not change packet independence status.",
        "",
        "## Required next actions",
        "",
    ]
    lines.extend(f"{i}. {action}" for i, action in enumerate(report["next_actions"], 1))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(f"validation audit: {report['packets_ready_for_promotion']}/{report['packet_count']} packets ready; learner={report['learner_protocol_status']}")


if __name__ == "__main__":
    main()
