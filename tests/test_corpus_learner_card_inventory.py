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
        self.assertEqual(self.data["summary"]["cards_with_shared_job_template"], 1473)
        self.assertEqual(self.data["summary"]["non_speech_or_publisher_boundary_cards"], 149)
        self.assertEqual(self.data["summary"]["unclassified_cards"], 2394)
        self.assertIn("does not establish", self.data["claim_boundary"])

    def test_cards_retain_exact_evidence_and_usable_fields(self):
        self.assertGreater(self.data["summary"]["cards_with_exact_evidence"], 3900)
        for card in self.data["cards"]:
            for field in ("raw_function_label", "observed_move", "repeatable_form", "practice", "self_check", "non_fit", "claim_boundary"):
                self.assertIn(field, card)
        self.assertIn("Search, inspect the full context", self.html)
        self.assertIn("Exact evidence", self.html)


if __name__ == "__main__":
    unittest.main()
