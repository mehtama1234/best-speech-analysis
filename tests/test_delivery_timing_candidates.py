import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeliveryTimingCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/communication-job-delivery-timing-candidates.json").read_text())

    def test_only_limited_intervals_are_routed(self):
        self.assertEqual(self.report["status"], "proxy_timing_candidates_manual_listening_pending")
        self.assertEqual(self.report["item_count"], 26)
        self.assertEqual(self.report["candidate_count"], 12)
        self.assertIn("intentional pause", self.report["claim_boundary"])
        for item in self.report["items"]:
            self.assertEqual(item["status"], "proxy_candidate_requires_manual_listening")
            self.assertEqual(item["independence"], "not_independent")
            self.assertEqual(len(item["evidence_ids"]), 3)
            self.assertTrue(item["practice_test"])

    def test_cutaway_candidates_are_not_routed(self):
        ids = {item["sample_id"] for item in self.report["items"]}
        self.assertNotIn("delivery:closing:01", ids)
        self.assertNotIn("delivery:persuasion_or_advocacy:02", ids)


if __name__ == "__main__":
    unittest.main()
