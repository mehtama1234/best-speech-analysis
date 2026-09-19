import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JobPhraseTransferCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/job-phrase-transfer-cards.json").read_text())

    def test_every_job_has_a_transfer_card_and_boundaries(self):
        self.assertEqual(self.report["status"], "provisional_phrase_transfer_cards_not_validated")
        self.assertEqual(self.report["card_count"], 18)
        self.assertIn("listener outcomes", self.report["claim_boundary"])
        for card in self.report["cards"]:
            self.assertTrue(card["phrase_candidates"])
            self.assertLessEqual(len(card["phrase_candidates"]), 3)
            self.assertTrue(card["practice"])
            self.assertTrue(card["non_fit"])
            self.assertTrue(card["transfer_instruction"])


if __name__ == "__main__":
    unittest.main()
