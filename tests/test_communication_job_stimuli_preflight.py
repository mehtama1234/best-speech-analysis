import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobStimuliPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT / "research/communication-job-stimuli-preflight.json").read_text())

    def test_screen_covers_all_pairs_without_claiming_equivalence(self):
        self.assertEqual(self.audit["status"], "automated_screening_not_independent_review")
        self.assertEqual(self.audit["pair_count"], 18)
        self.assertEqual(self.audit["summary"]["pairs_requiring_manual_review"], 18)
        self.assertIn("cannot establish proposition equivalence", self.audit["claim_boundary"])

    def test_audit_fields_are_present_and_word_delta_matches_bound(self):
        self.assertLessEqual(self.audit["summary"]["max_absolute_word_count_delta"], 13)
        for record in self.audit["records"]:
            self.assertIn(record["target_marker_status"], {"present", "manual_review_required"})
            self.assertIn("same proposition and no extra outcome claim", record["manual_checks_required"])


if __name__ == "__main__":
    unittest.main()
