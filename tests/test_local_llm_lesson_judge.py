import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LocalLlmLessonJudgeTests(unittest.TestCase):
    def test_receipt_is_conservative_and_covers_all_cards(self):
        report = json.loads((ROOT / "research/local-llm-lesson-judge.json").read_text())
        self.assertEqual(report["status"], "local_model_judgment_recorded_human_validation_open")
        self.assertEqual(report["model_id"], "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(report["card_count"], 18)
        self.assertEqual(report["judgment_scope"], "18_card_per_card_and_aggregate_metadata_screen")
        self.assertEqual(len(report["per_card_judgments"]), 18)
        self.assertEqual(sum(bool(item["raw_model_output"]) for item in report["per_card_judgments"]), 18)
        self.assertLessEqual(report["per_card_judgment_count"], 18)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("not independent human review", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
