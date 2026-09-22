import unittest

from scripts.run_autonomous_listener_dry_run import run


class AutonomousListenerDryRunTest(unittest.TestCase):
    def test_synthetic_listener_pipeline_passes_without_promotion(self):
        report = run()
        self.assertEqual(report["status"], "instrument_export_validation_and_summary_passed")
        self.assertEqual(report["record_count"], 2)
        self.assertFalse(report["summary"]["promotion_eligible"])
        self.assertEqual(report["full_curriculum"]["job_count"], 18)
        self.assertEqual(report["full_curriculum"]["record_count"], 36)
        self.assertIn("no listener participated", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
