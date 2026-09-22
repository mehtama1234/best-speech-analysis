import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PresentationSequenceLibraryTests(unittest.TestCase):
    def test_sequences_link_to_candidate_cards(self):
        report = json.loads((ROOT / "research/presentation-sequence-library.json").read_text())
        cards = {card["card_id"] for card in json.loads((ROOT / "research/expanded-pattern-candidate-cards.json").read_text())["cards"]}
        self.assertEqual(report["status"], "source_linked_candidate_sequences_not_validated")
        self.assertEqual(report["sequence_count"], 6)
        for sequence in report["sequences"]:
            self.assertGreaterEqual(len(sequence["steps"]), 3)
            self.assertEqual(len(sequence["draft_template"]), len(sequence["steps"]))
            for section in sequence["draft_template"]:
                self.assertTrue(section["sentence_stem"])
                self.assertTrue(section["listener_check"])
                self.assertTrue(section["boundary_check"])
            self.assertTrue(set(sequence["pattern_ids"]).issubset(cards))
            self.assertEqual(sequence["status"], "candidate_presentation_architecture_not_validated")


if __name__ == "__main__":
    unittest.main()
