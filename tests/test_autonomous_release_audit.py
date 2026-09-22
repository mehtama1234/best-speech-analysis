import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AutonomousReleaseAuditTest(unittest.TestCase):
    def test_release_receipt_records_passed_core_steps(self):
        report = json.loads((ROOT / "research/autonomous-release-audit.json").read_text())
        self.assertEqual(report["status"], "release_audit_passed")
        self.assertIn(report["step_count"], (9, 10, 11, 12, 13, 14, 15, 16, 17))
        self.assertEqual(report["passed_step_count"], report["step_count"])

    def test_full_test_mode_places_regenerating_suite_first(self):
        from scripts.run_autonomous_release_audit import step_plan

        plan = step_plan(include_full_tests=True)
        names = [name for name, _ in plan]
        self.assertEqual(names[0], "core release receipt preflight")
        self.assertEqual(names[1], "reproducibility manifest preflight build")
        self.assertEqual(names[2], "full repository test suite")
        self.assertLess(names.index("acceptance matrix build"), names.index("aggregate end-to-end audit"))
        self.assertLess(names.index("cross-artifact consistency"), names.index("aggregate end-to-end audit"))
        self.assertLess(names.index("fail-closed promotion readiness"), names.index("aggregate end-to-end audit"))
        self.assertLess(names.index("model-assisted gate readiness"), names.index("aggregate end-to-end audit"))
        self.assertEqual(names[-1], "reproducibility manifest validation")


if __name__ == "__main__":
    unittest.main()
