import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ListenerStimulusReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-listener-stimulus-review-workbook.json").read_text())

    def test_all_pairs_are_present_and_unlocked(self):
        self.assertEqual(self.workbook["status"], "manual_equivalence_review_pending")
        self.assertEqual(self.workbook["item_count"], 18)
        for item in self.workbook["items"]:
            self.assertIsNone(item["review"]["lock_decision"])
            self.assertEqual(item["automated_preflight"]["automated_status"], "screened_not_independently_equated")

    def test_claim_boundary_keeps_review_separate_from_outcomes(self):
        self.assertIn("does not establish", self.workbook["claim_boundary"])
        self.assertTrue((ROOT / "writeups/communication-job-listener-stimulus-review-workbook.html").exists())

    def test_browser_smoke_script_covers_export_path(self):
        self.assertTrue((ROOT / "scripts/check_listener_stimulus_review_browser.py").exists())


if __name__ == "__main__":
    unittest.main()
