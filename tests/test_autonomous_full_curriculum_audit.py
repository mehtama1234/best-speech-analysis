import unittest

from scripts.build_autonomous_full_curriculum_audit import build


class AutonomousFullCurriculumAuditTest(unittest.TestCase):
    def test_all_18_job_surfaces_reconcile(self):
        report = build()
        self.assertEqual(report["status"], "full_18_job_surface_reconciled_not_validated")
        self.assertEqual(report["job_count"], 18)
        self.assertEqual(report["passed_check_count"], report["check_count"])
        self.assertEqual(report["failed_layers"], [])


if __name__ == "__main__":
    unittest.main()
