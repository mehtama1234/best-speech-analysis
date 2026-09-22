import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExpandedPatternCandidateCardsTests(unittest.TestCase):
    def test_cards_are_source_linked_and_separate_from_validated_lessons(self):
        report = json.loads((ROOT / "research/expanded-pattern-candidate-cards.json").read_text())
        self.assertEqual(report["status"], "source_linked_discovery_cards_not_validated")
        self.assertEqual(report["card_count"], 33)
        self.assertEqual(report["relation_card_count"], 18)
        self.assertEqual(report["unmatched_cluster_card_count"], 15)
        for card in report["cards"]:
            self.assertTrue(card["evidence_ids"])
            self.assertTrue(card["examples"])
            self.assertEqual(card["status"], "candidate_discovery_not_validated")
            self.assertIn("not a validated best practice", card["claim_boundary"])

    def test_local_practice_surface_contains_all_cards_and_search(self):
        page = (ROOT / "writeups/expanded-pattern-candidate-cards.html").read_text()
        self.assertIn('id="search"', page)
        self.assertIn('id="cards"', page)
        self.assertIn('id="generate"', page)
        self.assertIn('id="save"', page)
        self.assertIn('id="load"', page)
        self.assertIn("expanded-pattern-draft", page)
        self.assertIn('id="download"', page)
        self.assertIn('id="download-record"', page)
        self.assertIn('local_expanded_pattern_practice_record', page)
        self.assertIn('id="listener-restatement"', page)
        self.assertIn('id="still-unclear"', page)
        self.assertIn('id="non-fit"', page)
        self.assertIn('id="next-revision"', page)
        self.assertIn('id="shortlist-only"', page)
        self.assertIn('id="sequence-preset"', page)
        self.assertIn('id="apply-sequence"', page)
        self.assertEqual(page.count('data-shortlisted="true"'), 2)
        self.assertIn('presentation-outline.md', page)
        self.assertEqual(page.count('class="card'), 33)


if __name__ == "__main__":
    unittest.main()
