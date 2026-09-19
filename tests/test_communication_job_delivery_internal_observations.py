import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobDeliveryInternalObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/communication-job-delivery-internal-observations.json").read_text())

    def test_raw_media_midpoints_are_bounded_and_non_independent(self):
        self.assertEqual(self.report["item_count"], 36)
        self.assertEqual(len(self.report["items"]), 36)
        self.assertEqual(self.report["status"], "internal_midpoint_frame_observations_complete_independent_review_pending")
        self.assertIn("manual vocal listening", self.report["method"]["not_performed"])
        self.assertIn("effectiveness", self.report["claim_boundary"])
        for item in self.report["items"]:
            self.assertEqual(item["independence"], "not_independent")
            self.assertTrue(item["visual_observation"])
            self.assertTrue(item["missingness_or_accessibility_note"])
            self.assertTrue(item["audio_measurements"])
            self.assertEqual(item["audio_measurement_status"], "aligned_feature_measurement_available")
            self.assertNotIn("data/features/None", item["audio_measurement_and_limit"])
            self.assertIn("data/features/", item["audio_measurement_and_limit"])

    def test_timestamp_spot_audit_keeps_cutaways_and_corrected_settings(self):
        by_id = {item["sample_id"]: item for item in self.report["items"]}
        self.assertIn("Mitty", by_id["delivery:opening:01"]["visual_observation"])
        self.assertEqual(by_id["delivery:closing:01"]["transcript_alignment"], "indeterminate")
        self.assertIn("no live speaker", by_id["delivery:closing:01"]["visual_observation"])
        self.assertIn("television screen", by_id["delivery:callback_or_repetition:02"]["visual_observation"])
        self.assertEqual(by_id["delivery:persuasion_or_advocacy:02"]["transcript_alignment"], "indeterminate")


if __name__ == "__main__":
    unittest.main()
