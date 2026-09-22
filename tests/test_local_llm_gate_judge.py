import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LocalLlmGateJudgeTests(unittest.TestCase):
    def test_gate_screen_prioritizes_without_closing_gates(self):
        report = json.loads((ROOT / "research/local-llm-gate-judge.json").read_text())
        self.assertEqual(report["status"], "local_model_gate_prioritization_recorded_human_gates_open")
        self.assertEqual(report["model_id"], "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(report["gate_count"], 10)
        self.assertEqual(report["parsed_judgment_count"], 1)
        self.assertEqual(report["judgment"]["overall"], "prioritized_not_completed")
        self.assertTrue(report["judgment"]["priority_gates"])
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("not independent human review", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
