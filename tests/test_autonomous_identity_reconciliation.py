import unittest

from scripts.build_autonomous_identity_reconciliation import build


class AutonomousIdentityReconciliationTest(unittest.TestCase):
    def test_fixed_corpus_metadata_and_review_links_reconcile(self):
        report = build()
        self.assertEqual(report["status"], "metadata_reconciliation_complete_identity_not_proven")
        self.assertEqual(report["video_count"], 395)
        self.assertEqual(report["metadata_consistent_count"], 395)
        self.assertEqual(report["issue_count"], 0)
        self.assertIn("does not prove", report["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
