import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeliveryIntervalFrameAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/communication-job-delivery-interval-frame-audit.json").read_text())

    def test_three_frame_audit_is_complete_and_bounded(self):
        self.assertEqual(self.report["item_count"], 36)
        self.assertEqual(len(self.report["items"]), 36)
        self.assertEqual(self.report["status"], "internal_three_frame_visual_audit_independent_review_pending")
        self.assertIn("continuous delivery", self.report["claim_boundary"])
        for item in self.report["items"]:
            self.assertEqual(item["frame_count"], 3)
            self.assertEqual(len(item["sampled_frame_times_seconds"]), 3)
            self.assertEqual(item["independence"], "not_independent")
            self.assertTrue(item["visual_sequence_observation"])

    def test_cutaways_are_explicitly_not_speaker_delivery(self):
        rows = self.report["items"]
        cutaways = [row for row in rows if row["delivery_navigation_status"] == "not_usable_for_speaker_delivery"]
        self.assertGreaterEqual(len(cutaways), 5)
        self.assertTrue(all(row["speaker_visibility"] in {"speaker_not_visible", "speakers_change", "speaker_visibility_changes"} for row in cutaways))
        counts = Counter(row["frame_sequence_type"] for row in cutaways)
        self.assertGreaterEqual(counts["graphic_or_cutaway"], 1)


if __name__ == "__main__":
    unittest.main()
