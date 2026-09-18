import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeliveryEvidenceIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/delivery-evidence-index.json").read_text())

    def test_separates_raw_derived_internal_and_independent_layers(self):
        self.assertEqual(self.index["status"], "delivery_evidence_reconciled_independent_review_pending")
        coverage = self.index["coverage"]
        self.assertEqual(coverage["selected_video_count"], 41)
        self.assertEqual(coverage["raw_audio_video_with_transcript_count"], 21)
        self.assertEqual(coverage["internal_manual_observation_count"], 21)
        self.assertEqual(coverage["independent_review_count"], 0)
        self.assertIn("do not establish emotion", self.index["claim_boundary"])

    def test_internal_items_retain_limits_and_review_status(self):
        self.assertEqual(len(self.index["internal_multimodal_observations"]), 21)
        for item in self.index["internal_multimodal_observations"]:
            self.assertTrue(item["feature_limit"])
            self.assertEqual(item["review_status"], "internal_bounded_review_not_independent")


if __name__ == "__main__":
    unittest.main()
