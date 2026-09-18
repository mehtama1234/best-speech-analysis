import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VerticalSliceTests(unittest.TestCase):
    def test_slice_manifest_has_five_linked_patterns(self):
        manifest = json.loads((ROOT / "research/vertical-slice-01.json").read_text())
        self.assertEqual(len(manifest["patterns"]), 5)
        self.assertEqual(manifest["learner_check_status"], "protocol_drafted_not_run")
        self.assertTrue((ROOT / manifest["learner_check"]).is_file())
        self.assertTrue((ROOT / manifest["validation_audit"]).is_file())
        self.assertTrue((ROOT / manifest["learner_check_instrument"]).is_file())
        self.assertTrue((ROOT / manifest["learner_task_bank"]).is_file())
        self.assertTrue((ROOT / manifest["learner_record_scorer"]).is_file())
        self.assertTrue((ROOT / manifest["media_audit"]).is_file())
        self.assertTrue((ROOT / manifest["manual_multimodal_review"]).is_file())
        self.assertTrue((ROOT / manifest["review_workbook"]).is_file())
        self.assertTrue((ROOT / manifest["review_instrument"]).is_file())
        for pattern in manifest["patterns"]:
            self.assertEqual(pattern["evidence_packet_status"], "partial_controls_recorded")
            self.assertEqual(pattern["lesson_status"], "draft_not_validated")
            self.assertTrue((ROOT / pattern["evidence_packet"]).is_file())
            self.assertTrue((ROOT / pattern["lesson"]).is_file())

    def test_validation_script_passes(self):
        from scripts.validate_vertical_slice import main
        main()

    def test_official_source_checks_are_partial_and_conservative(self):
        checks = json.loads(
            (ROOT / "research/vertical-slice-01-official-source-checks.json").read_text()
        )
        self.assertEqual(checks["status"], "partial_official_corroboration_not_event_verified")
        self.assertEqual(len(checks["checks"]), 9)
        self.assertTrue(all("unverified" in item["status"] for item in checks["checks"]))

    def test_cluster_recurrence_report_is_derived_and_bounded(self):
        report = json.loads(
            (ROOT / "research/vertical-slice-01-cluster-recurrence.json").read_text()
        )
        self.assertEqual(report["status"], "provisional_cluster_recurrence_not_event_independent")
        self.assertEqual(report["representative_occurrence_count"], 25)
        self.assertEqual(report["unique_video_id_count_across_representatives"], 13)
        self.assertEqual(report["unique_video_id_count_all_packet_occurrences"], 16)
        self.assertEqual(len(report["clusters"]), 5)
        self.assertTrue(all(c["representative_occurrence_count"] == 5 for c in report["clusters"]))

    def test_vertical_slice_02_drafts_validate(self):
        from scripts.validate_vertical_slice_02_drafts import main
        main()

    def test_independent_review_comparison_preserves_disagreements(self):
        from scripts.compare_vertical_slice_reviews import compare
        workbook = json.loads(
            (ROOT / "research/vertical-slice-01-independent-review-workbook.json").read_text()
        )

        def record(code):
            responses = {
                "reviewer_name": code,
                "reviewer_role": "external reviewer",
                "review_date": "2026-09-18",
                "review_modality": "browser form",
                "conflict_statement": "No packet creation or interpretation role.",
                "independent_attestation": True,
            }
            for number in range(1, 51):
                responses.update({
                    f"item_{number}_boundary": "correct",
                    f"item_{number}_pattern_decision": "indeterminate",
                    f"item_{number}_speech-function": "plausible",
                    f"item_{number}_safety_decision": "safe_as_written",
                    f"item_{number}_audio_proxy": "No audio claim.",
                    f"item_{number}_alternative": "Caption or context may explain this.",
                    f"item_{number}_reason": "Recorded for adjudication.",
                })
            return {
                "schema_version": "1.0",
                "record_type": "independent_review",
                "workbook_id": workbook["workbook_id"],
                "claim_boundary": "Evidence review only; not listener outcomes.",
                "responses": responses,
            }

        first, second = record("reviewer-a"), record("reviewer-b")
        second["responses"]["item_1_pattern_decision"] = "unsupported"
        report = compare([first, second], workbook)
        self.assertEqual(report["status"], "agreement_report_not_promotion_evidence")
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["disagreement_count"], 1)
        self.assertEqual(report["agreement"]["pattern_decision"]["unanimous_items"], 49)

    def test_lesson_index_is_shared_and_provisional(self):
        index = json.loads(
            (ROOT / "writeups/vertical-slice-01-lesson-index.json").read_text()
        )
        self.assertEqual(index["status"], "draft_lessons_not_validated")
        self.assertEqual(len(index["lessons"]), 5)
        self.assertTrue(
            (ROOT / "writeups/vertical-slice-01-lesson-index.html").is_file()
        )
        for lesson in index["lessons"]:
            self.assertTrue((ROOT / lesson["packet"]).is_file())
            self.assertTrue((ROOT / lesson["lesson"]).is_file())
            self.assertEqual(lesson["practice_flows"], "research/vertical-slice-01-practice-flows.json")
            self.assertEqual(lesson["learner_check"], "writeups/vertical-slice-01-learner-check.html")
        browser = (ROOT / "writeups/vertical-slice-01-lesson-index.html").read_text()
        self.assertIn("Practice flow", browser)
        self.assertIn("Learner check", browser)

    def test_practice_flow_set_links_all_lessons(self):
        flows = json.loads(
            (ROOT / "research/vertical-slice-01-practice-flows.json").read_text()
        )
        self.assertEqual(flows["status"], "draft_not_validated")
        self.assertEqual(len(flows["flows"]), 5)
        for flow in flows["flows"]:
            self.assertTrue((ROOT / flow["evidence_packet"]).is_file())
            self.assertTrue((ROOT / flow["lesson"]).is_file())
            self.assertIn("listener_check", {step["id"] for step in flow["steps"]})

    def test_validation_audit_preserves_unvalidated_boundary(self):
        from scripts.audit_vertical_slice import main
        main()
        report = json.loads(
            (ROOT / "research/vertical-slice-01-validation-audit.json").read_text()
        )
        self.assertEqual(report["status"], "not_ready_for_promotion")
        self.assertEqual(report["packets_ready_for_promotion"], 0)
        self.assertEqual(report["learner_protocol_status"], "protocol_drafted_not_run")
        self.assertEqual(report["official_source_checks"]["check_count"], 9)
        self.assertEqual(report["official_source_checks"]["event_context_corroborated"], 3)
        self.assertEqual(report["official_source_checks"]["exact_upload_event_verified"], 0)
        self.assertEqual(len(report["packets"]), 5)
        for packet in report["packets"]:
            self.assertFalse(packet["ready_for_promotion"])
            gates = {issue["gate"] for issue in packet["issues"]}
            self.assertIn("independent_review", gates)

    def test_learner_check_instrument_is_runnable_and_bounded(self):
        from scripts.build_vertical_slice_learner_check import build
        build()
        instrument = (ROOT / "writeups/vertical-slice-01-learner-check.html").read_text()
        self.assertIn("Download JSON record", instrument)
        self.assertIn("Teachability observations only", instrument)
        self.assertIn("Second-listener restatement", instrument)
        self.assertIn("contrast-recognition-01", instrument)
        self.assertIn("task_bank_ids", instrument)
        self.assertIn('name="p1_self_check_1"', instrument)
        self.assertEqual(instrument.count('<fieldset class="pattern">'), 5)

    def test_learner_record_scorer_rejects_incomplete_and_preserves_boundary(self):
        from scripts.score_vertical_slice_learner_records import summarize
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "learner.json"
            responses = {
                "participant_code": "pseudonym-01",
                "date": "2026-09-18",
                "consent": True,
            }
            for number in range(1, 6):
                responses[f"p{number}_task_bank_ids"] = ",".join([
                    [
                        "contrast-recognition-01", "contrast-transfer-01",
                        "contrast-nonfit-01", "contrast-control-01",
                    ],
                    [
                        "example-recognition-01", "example-transfer-01",
                        "example-nonfit-01", "example-control-01",
                    ],
                    [
                        "story-recognition-01", "story-transfer-01",
                        "story-nonfit-01", "story-control-01",
                    ],
                    [
                        "uncertainty-recognition-01", "uncertainty-transfer-01",
                        "uncertainty-nonfit-01", "uncertainty-control-01",
                    ],
                    [
                        "conclusion-recognition-01", "conclusion-transfer-01",
                        "conclusion-nonfit-01", "conclusion-control-01",
                    ],
                ][number - 1])
                for suffix in ("baseline", "transfer", "non_fit", "control", "listener", "revision"):
                    responses[f"p{number}_{suffix}"] = "recorded"
                responses[f"p{number}_transfer_score"] = 2
                responses[f"p{number}_boundary_score"] = 0 if number == 3 else 2
                responses[f"p{number}_listener_score"] = 1
            path.write_text(json.dumps({
                "record_type": "learner_observation",
                "claim_boundary": "Teachability observations only; not listener outcomes.",
                "responses": responses,
            }))
            report = summarize([path])
            record = json.loads(path.read_text())
            record["responses"]["p1_task_bank_ids"] = "wrong-task"
            path.write_text(json.dumps(record))
            rejected = summarize([path])
        self.assertEqual(report["valid_record_count"], 1)
        self.assertEqual(report["rejected_record_count"], 0)
        self.assertFalse(report["patterns"][2]["promotion_eligible"])
        self.assertEqual(report["patterns"][2]["boundary_failures"], 1)
        self.assertEqual(rejected["valid_record_count"], 0)
        self.assertIn("fixed task bank", " ".join(rejected["rejected_records"][0]["errors"]))

    def test_media_audit_keeps_feature_files_separate_from_raw_media(self):
        from scripts.audit_vertical_slice_media import main
        report = main()
        self.assertEqual(report["status"], "raw_media_audit_complete_manual_alignment_pending")
        self.assertGreater(report["unique_video_ids"], 0)
        self.assertEqual(report["packet_item_occurrences"], 50)
        self.assertEqual(report["unique_video_ids"], 16)
        self.assertLessEqual(
            report["unique_ids_with_raw_media"], report["unique_video_ids"]
        )
        self.assertIn("feature_files", report["occurrences"][0])

    def test_independent_review_workbook_is_blank_and_complete(self):
        from scripts.build_vertical_slice_review_workbook import build
        build()
        workbook = json.loads(
            (ROOT / "research/vertical-slice-01-independent-review-workbook.json").read_text()
        )
        self.assertEqual(workbook["status"], "template_not_completed")
        self.assertEqual(workbook["item_count"], 50)
        self.assertEqual(len(workbook["items"]), 50)
        self.assertTrue(all(item["review"]["pattern_decision"] is None for item in workbook["items"]))
        instrument = (ROOT / "writeups/vertical-slice-01-independent-review-workbook.html").read_text()
        self.assertIn("Download review JSON", instrument)
        self.assertIn("independent_attestation", instrument)
        self.assertIn("Open source at evidence timestamp", instrument)
        self.assertIn("start_seconds", workbook["items"][0])
        self.assertIn("p.className='item'", instrument)

    def test_independent_review_export_validator_checks_all_items(self):
        from scripts.validate_vertical_slice_review_record import validate
        from scripts.summarize_vertical_slice_review import summarize
        workbook = json.loads(
            (ROOT / "research/vertical-slice-01-independent-review-workbook.json").read_text()
        )
        responses = {
            "reviewer_name": "reviewer-code-01",
            "reviewer_role": "external reviewer",
            "review_date": "2026-09-18",
            "review_modality": "browser form",
            "conflict_statement": "I did not create or interpret these packets.",
            "independent_attestation": True,
        }
        for number in range(1, 51):
            responses.update({
                f"item_{number}_boundary": "correct",
                f"item_{number}_pattern_decision": "indeterminate",
                f"item_{number}_speech-function": "plausible",
                f"item_{number}_safety_decision": "safe_as_written",
                f"item_{number}_audio_proxy": "No audio claim made.",
                f"item_{number}_alternative": "Caption boundary or context may explain this.",
                f"item_{number}_reason": "Recorded for later adjudication.",
            })
        record = {
            "schema_version": "1.0",
            "record_type": "independent_review",
            "workbook_id": workbook["workbook_id"],
            "claim_boundary": "Evidence review only; not listener outcomes.",
            "responses": responses,
        }
        result = validate(record, workbook)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["validated_item_count"], 50)
        summary = summarize(record, workbook)
        self.assertEqual(summary["status"], "review_received_not_promotion_evidence")
        self.assertFalse(summary["promotion_eligible"])
        self.assertEqual(summary["item_count"], 50)
        responses["item_17_reason"] = ""
        invalid = validate(record, workbook)
        self.assertEqual(invalid["status"], "invalid")
        self.assertIn("missing item_17_reason", invalid["errors"])

    def test_learner_task_bank_has_balanced_phases(self):
        task_bank = json.loads(
            (ROOT / "research/vertical-slice-01-learner-task-bank.json").read_text()
        )
        self.assertEqual(len(task_bank["tasks"]), 20)
        by_pattern = {}
        for task in task_bank["tasks"]:
            by_pattern.setdefault(task["pattern_id"], []).append(task["phase"])
        self.assertEqual(len(by_pattern), 5)
        for phases in by_pattern.values():
            self.assertEqual(
                phases,
                ["new_example_recognition", "transfer", "misuse_non_fit", "matched_control"],
            )


if __name__ == "__main__":
    unittest.main()
