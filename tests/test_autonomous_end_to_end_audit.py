import json
import unittest
from pathlib import Path

from scripts.build_autonomous_end_to_end_audit import build


ROOT = Path(__file__).resolve().parents[1]


class AutonomousEndToEndAuditTest(unittest.TestCase):
    def test_all_autonomous_layers_join(self):
        report = build()
        self.assertEqual(report["status"], "autonomous_release_candidate_reconciled_not_promotion_validated")
        self.assertEqual(report["passed_check_count"], report["check_count"])
        self.assertEqual(report["failed_layers"], [])
        self.assertIn("learner observations", report["claim_boundary"])

    def test_generated_report_is_shareable(self):
        report = json.loads((ROOT / "research/autonomous-end-to-end-audit.json").read_text())
        markdown = (ROOT / "writeups/autonomous-end-to-end-audit.md").read_text()
        self.assertEqual(report["audit_id"], "autonomous-end-to-end-audit")
        self.assertIn("Checks passed: **27/27**", markdown)
        self.assertIn("Open outcome gates", markdown)

    def test_native_layer_names_all_client_helper_projections(self):
        report = json.loads((ROOT / "research/autonomous-end-to-end-audit.json").read_text())
        layer = next(item for item in report["checks"] if item["layer"] == "native client contract outputs")
        self.assertIn("clients/examples/mobile_lesson_helpers.ts", layer["evidence"])
        self.assertIn("clients/examples/MobileLessonHelpers.kt", layer["evidence"])
        self.assertIn("clients/examples/MobileLessonHelpers.swift", layer["evidence"])


if __name__ == "__main__":
    unittest.main()
