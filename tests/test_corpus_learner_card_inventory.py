import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusLearnerCardInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/corpus-learner-card-inventory.json").read_text())
        cls.html = (ROOT / "writeups/corpus-learner-card-inventory.html").read_text()

    def test_indexes_every_function_item_and_keeps_boundary(self):
        self.assertEqual(self.data["status"], "transcript_derived_practice_navigation_not_validated")
        self.assertEqual(self.data["summary"]["review_count"], 395)
        self.assertEqual(self.data["summary"]["card_count"], 4016)
        self.assertEqual(self.data["summary"]["structural_card_count"], 2800)
        self.assertEqual(self.data["summary"]["total_card_count"], 6816)
        self.assertGreater(self.data["summary"]["cards_with_phrase_handles"], 2000)
        self.assertGreater(self.data["summary"]["phrase_handle_count"], 7000)
        self.assertGreater(self.data["summary"]["cards_with_local_delivery_proxy"], 6000)
        self.assertGreater(self.data["summary"]["cards_with_pose_proxy"], 6000)
        self.assertEqual(self.data["summary"]["cards_with_shared_job_template"], 1473)
        self.assertEqual(self.data["summary"]["non_speech_or_publisher_boundary_cards"], 149)
        self.assertEqual(self.data["summary"]["unclassified_cards"], 2394)
        self.assertIn("does not establish", self.data["claim_boundary"])

    def test_cards_retain_exact_evidence_and_usable_fields(self):
        self.assertGreater(self.data["summary"]["cards_with_exact_evidence"], 3900)
        self.assertEqual(self.data["summary"]["structural_cards_with_exact_evidence"], 2795)
        for card in self.data["cards"]:
            for field in ("raw_function_label", "observed_move", "repeatable_form", "practice", "self_check", "non_fit", "claim_boundary"):
                self.assertIn(field, card)
            self.assertIn("delivery_proxy", card)
        self.assertIn("Search, inspect the full context", self.html)
        self.assertIn("Exact evidence", self.html)
        self.assertIn("Exact phrase handles", self.html)
        self.assertIn("Start a practice card", self.html)
        self.assertIn("Next visible card", self.html)


if __name__ == "__main__":
    unittest.main()
