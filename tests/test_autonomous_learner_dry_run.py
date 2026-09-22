import unittest

from scripts.run_autonomous_learner_dry_run import run


class AutonomousLearnerDryRunTest(unittest.TestCase):
    def test_synthetic_form_export_and_scoring_path_passes(self):
        report = run()
        self.assertEqual(report["status"], "instrument_export_validation_and_scoring_passed")
        self.assertEqual(report["pattern_count"], 5)
        self.assertEqual(report["summary"]["valid_record_count"], 1)
        self.assertEqual(report["full_curriculum"]["job_count"], 18)
        self.assertEqual(report["full_curriculum"]["task_count"], 72)
        self.assertIn("not a learner observation", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
