import copy
import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_cards import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateCommunicationJobCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = json.loads((ROOT / "research/communication-job-cards.json").read_text())
        cls.evidence = json.loads((ROOT / "research/corpus-evidence-bank.json").read_text())

    def test_current_cards_are_evidence_linked_and_provisional(self):
        self.assertEqual(validate(self.cards, self.evidence), [])

    def test_unknown_evidence_id_is_rejected(self):
        broken = copy.deepcopy(self.cards)
        broken["cards"][0]["exact_examples"][0]["exact_segments"][0]["evidence_id"] = "missing"
        self.assertTrue(any("unknown evidence_id" in error for error in validate(broken, self.evidence)))


if __name__ == "__main__":
    unittest.main()
