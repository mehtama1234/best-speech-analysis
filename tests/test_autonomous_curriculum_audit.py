import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AutonomousCurriculumAuditTest(unittest.TestCase):
    def test_audit_reconciles_the_fixed_corpus_and_preserves_boundaries(self):
        report = json.loads((ROOT / "research/autonomous-curriculum-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "internal_reconciliation_checkpoint_not_promotion_validation")
        self.assertEqual(report["coverage"]["fixed_corpus_videos"], 395)
        self.assertEqual(report["coverage"]["communication_jobs"], 18)
        self.assertEqual(len(report["jobs"]), 18)
        self.assertEqual(report["review_queues"]["delivery_items"], 36)
        self.assertEqual(report["review_queues"]["counterexample_items"], 90)
        boundary = report["claim_boundary"].lower()
        self.assertIn("independent review", boundary)
        self.assertIn("effectiveness", boundary)

    def test_audit_markdown_is_shareable(self):
        text = (ROOT / "writeups/autonomous-curriculum-audit.md").read_text(encoding="utf-8")
        self.assertIn("## Coverage snapshot", text)
        self.assertIn("## Review queues", text)
        self.assertIn("0/2", text)
        self.assertIn("0/5", text)


if __name__ == "__main__":
    unittest.main()
