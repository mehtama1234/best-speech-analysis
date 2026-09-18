#!/usr/bin/env python3
"""Validate the evidence-to-practice vertical-slice records without upgrading claims."""
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    "contrast-or-disagreement",
    "example",
    "story",
    "uncertainty",
    "conclusion",
]


def load(path):
    return json.loads(path.read_text())


def check_anchor(item):
    evidence_id = item["evidence_id"]
    video_id, ordinal = evidence_id.rsplit(":", 1)
    transcript = load(ROOT / "data/transcripts" / f"{video_id}.json")["transcript"]
    index = int(ordinal)
    assert 0 <= index < len(transcript), f"anchor outside transcript: {evidence_id}"


def main():
    manifest_path = ROOT / "research/vertical-slice-01.json"
    manifest = load(manifest_path)
    assert len(manifest["patterns"]) == 5
    audit = ROOT / "research/vertical-slice-01-source-event-independence.json"
    validation_audit = ROOT / "research/vertical-slice-01-validation-audit.json"
    media_audit = ROOT / "research/vertical-slice-01-media-audit.json"
    manual_review = ROOT / "research/vertical-slice-01-manual-multimodal-review.json"
    review_workbook = ROOT / "research/vertical-slice-01-independent-review-workbook.json"
    review_instrument = ROOT / "writeups/vertical-slice-01-independent-review-workbook.html"
    learner_instrument = ROOT / "writeups/vertical-slice-01-learner-check.html"
    learner_scorer = ROOT / "scripts/score_vertical_slice_learner_records.py"
    learner = ROOT / "research/vertical-slice-01-learner-check.json"
    task_bank = ROOT / "research/vertical-slice-01-learner-task-bank.json"
    official_checks = ROOT / "research/vertical-slice-01-official-source-checks.json"
    assert audit.is_file() and validation_audit.is_file() and media_audit.is_file() and manual_review.is_file() and review_workbook.is_file() and review_instrument.is_file() and learner.is_file() and task_bank.is_file() and official_checks.is_file()
    assert learner_instrument.is_file()
    assert learner_scorer.is_file()
    audit_data = load(audit)
    validation_audit_data = load(validation_audit)
    media_audit_data = load(media_audit)
    manual_review_data = load(manual_review)
    review_workbook_data = load(review_workbook)
    learner_data = load(learner)
    task_bank_data = load(task_bank)
    official_checks_data = load(official_checks)
    assert len(audit_data["packets"]) == 5
    assert validation_audit_data["status"] == "not_ready_for_promotion"
    assert validation_audit_data["packets_ready_for_promotion"] == 0
    assert len(validation_audit_data["packets"]) == 5
    assert media_audit_data["status"] == "raw_media_audit_complete_manual_alignment_pending"
    assert media_audit_data["packet_item_occurrences"] == 50
    assert media_audit_data["unique_video_ids"] == 16
    assert manual_review_data["status"] == "internal_manual_review_complete_independent_review_pending"
    assert manual_review_data["independence"] == "not_independent"
    assert len(manual_review_data["items"]) == 13
    assert review_workbook_data["status"] == "template_not_completed"
    assert review_workbook_data["item_count"] == 50
    assert len(learner_data["patterns"]) == 5
    assert official_checks_data["status"] == "partial_official_corroboration_not_event_verified"
    assert len(official_checks_data["checks"]) == 9
    packet_evidence_ids = set()
    for name in NAMES:
        packet_data = load(ROOT / f"research/vertical-slice-01-{name}.json")
        def collect_evidence(value):
            if isinstance(value, dict):
                if isinstance(value.get("evidence_id"), str):
                    packet_evidence_ids.add(value["evidence_id"])
                for child in value.values():
                    collect_evidence(child)
            elif isinstance(value, list):
                for child in value:
                    collect_evidence(child)
        collect_evidence(packet_data)
    for check in official_checks_data["checks"]:
        assert check["video_id"] and check["official_source"].startswith("https://")
        assert "unverified" in check["status"]
        for occurrence in check["packet_occurrences"]:
            assert occurrence.split(":", 1)[1] in packet_evidence_ids

    for name in NAMES:
        packet_path = ROOT / f"research/vertical-slice-01-{name}.json"
        packet = load(packet_path)
        assert packet["status"] == "evidence_packet_partial_not_validated"
        lesson = ROOT / packet["learner_lesson"]["writeup"]
        assert lesson.is_file()
        assert packet["independent_review"]["status"] in {
            "not_started", "pending_external_reviewer"
        }
        assert packet["independence_status"]["audit"] == str(
            Path("research/vertical-slice-01-source-event-independence.json")
        )
        for item in packet["representative_examples"]:
            check_anchor(item)
        for item in packet.get("counterexamples", []):
            check_anchor(item)
        controls = packet.get("counterexample_status", {})
        for key in ("controls_recorded", "alternate_function_controls",
                    "failed_or_ineffective_candidates"):
            for item in controls.get(key, []):
                check_anchor(item)

    assert learner_data["status"] == "protocol_drafted_not_run"
    assert len(learner_data["patterns"]) == 5
    assert task_bank_data["status"] == "draft_not_piloted"
    assert len(task_bank_data["tasks"]) == 20
    print("vertical slice valid: five partial packets, linked lessons, source audit, learner protocol")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError) as error:
        print(f"vertical slice invalid: {error}", file=sys.stderr)
        raise SystemExit(1)
