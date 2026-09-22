import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExpandedPatternLlmShortlistTests(unittest.TestCase):
    def test_shortlist_is_derived_and_non_promotional(self):
        report = json.loads((ROOT / "research/expanded-pattern-llm-shortlist.json").read_text())
        self.assertEqual(report["status"], "local_model_shortlist_for_practice_review_not_promotion")
        self.assertEqual(report["candidate_count"], 2)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("local-llm-expanded-pattern-judge", report["source_judge"])
        for card in report["cards"]:
            self.assertTrue(card["evidence_ids"])
            self.assertTrue(card["examples"])
            self.assertIn("model_reason", card)


if __name__ == "__main__":
    unittest.main()
