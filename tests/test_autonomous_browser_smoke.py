import json
import unittest
from pathlib import Path

from scripts.run_autonomous_browser_smoke import CHECKS


ROOT = Path(__file__).resolve().parents[1]


class AutonomousBrowserSmokeTest(unittest.TestCase):
    def test_receipt_records_all_core_browser_checks(self):
        report = json.loads((ROOT / "research/autonomous-browser-smoke.json").read_text())
        self.assertEqual(report["status"], "core_browser_smoke_passed")
        self.assertEqual(report["check_count"], len(CHECKS))
        self.assertEqual(report["passed_check_count"], len(CHECKS))
        self.assertEqual([check["script"] for check in report["checks"]], CHECKS)


if __name__ == "__main__":
    unittest.main()
