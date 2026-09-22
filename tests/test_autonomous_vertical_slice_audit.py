import json
import unittest
from pathlib import Path

from scripts.build_autonomous_vertical_slice_audit import reconcile


ROOT = Path(__file__).resolve().parents[1]


class AutonomousVerticalSliceAuditTest(unittest.TestCase):
    def test_all_five_packets_reconcile(self):
        report = reconcile()
        self.assertEqual(report["status"], "autonomous_reconciliation_complete")
        self.assertEqual(report["packets_reconciled"], 5)
        self.assertEqual(report["errors"], [])
        self.assertTrue(all(row["representative_example_count"] == 5 for row in report["packets"]))

    def test_report_and_markdown_are_generated(self):
        report = json.loads((ROOT / "research/autonomous-vertical-slice-01.json").read_text())
        markdown = (ROOT / "writeups/autonomous-vertical-slice-01.md").read_text()
        self.assertEqual(report["audit_id"], "autonomous-vertical-slice-01")
        self.assertIn("external reviewer", markdown.lower())
        self.assertIn("Packets reconciled: **5/5**", markdown)


if __name__ == "__main__":
    unittest.main()
