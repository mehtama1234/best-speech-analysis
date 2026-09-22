import unittest

from scripts.run_model_assisted_gate_judge import run


class ModelAssistedGateJudgeTests(unittest.TestCase):
    def test_judge_is_conservative_and_keeps_human_gates_open(self):
        report = run()
        self.assertEqual(report["status"], "model_assisted_readiness_complete_human_evidence_open")
        self.assertEqual(report["judge_type"], "language_model_assisted_readiness_preflight")
        self.assertEqual(report["human_gate_closed_count"], 0)
        self.assertFalse(report["promotion_eligible"])
        self.assertTrue(all(gate["instrument_ready"] for gate in report["gates"]))


if __name__ == "__main__":
    unittest.main()
