import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LocalLlmExpandedPatternJudgeTests(unittest.TestCase):
    def test_receipt_screens_all_expanded_cards_and_stays_non_promotional(self):
        report = json.loads((ROOT / "research/local-llm-expanded-pattern-judge.json").read_text())
        self.assertEqual(report["status"], "local_model_candidate_screen_recorded_review_open")
        self.assertEqual(report["model_id"], "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(report["candidate_card_count"], 33)
        self.assertEqual(report["judgment_scope"], "33_expanded_candidate_pattern_aggregate_screen")
        self.assertIn("retained_caption_excerpts", report["input_scope"])
        self.assertFalse(report["promotion_eligible"])
        self.assertEqual(report["parsed_judgment_count"], 1)
        self.assertIn("not contextual semantic validation", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
