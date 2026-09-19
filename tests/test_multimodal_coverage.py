import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MultimodalCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/multimodal-coverage-audit.json").read_text())

    def test_report_reconciles_expansion_and_preserves_pending_boundary(self):
        self.assertEqual(self.report["selected_video_count"], 41)
        self.assertEqual(self.report["status"], "raw_media_reconciled_manual_review_pending")
        self.assertEqual(self.report["internal_manual_review_count"], 21)
        self.assertEqual(self.report["raw_audio_video_without_transcript_count"], 8)
        self.assertEqual(self.report["raw_audio_video_with_transcript_count"], 22)
        self.assertEqual(len(self.report["internal_manual_review_reports"]), 2)
        self.assertEqual(self.report["independent_review_status"], "pending")
        self.assertTrue((ROOT / self.report["independent_review_workbook"]).exists())
        self.assertTrue((ROOT / self.report["independent_review_form"]).exists())
        self.assertGreaterEqual(self.report["raw_audio_video_present_count"], 10)
        self.assertLessEqual(
            self.report["raw_audio_video_present_count"], self.report["selected_video_count"]
        )

    def test_every_selected_video_has_file_and_measurement_fields(self):
        self.assertEqual(len(self.report["videos"]), self.report["selected_video_count"])
        for row in self.report["videos"]:
            self.assertTrue(row["video_id"])
            self.assertIn(row["media_state"], {"raw_audio_video_present", "partial_raw_media", "derived_features_only", "raw_media_missing"})
            self.assertIn("feature_files", row)
            self.assertIn("candidate_function_counts", row)

    def test_manual_queue_contains_only_raw_complete_transcribed_items(self):
        for row in self.report["manual_review_queue"]:
            self.assertEqual(row["media_state"], "raw_audio_video_present")
            self.assertGreater(row["transcript_segments"], 0)
            self.assertEqual(row["review_status"], "not_manually_reviewed")

    def test_raw_only_queue_is_explicitly_not_transcript_evidence(self):
        self.assertEqual(len(self.report["raw_media_only_queue"]), 8)
        for row in self.report["raw_media_only_queue"]:
            self.assertEqual(row["transcript_segments"], 0)
            self.assertEqual(row["review_status"], "raw_media_present_but_no_retained_transcript")


if __name__ == "__main__":
    unittest.main()
