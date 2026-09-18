import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PatternAdmissionReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/pattern-admission-reconciliation.json").read_text())

    def test_distinguishes_legacy_five_from_shared_eight(self):
        self.assertEqual(self.report["legacy_contextual_pattern_count"], 5)
        self.assertEqual(self.report["shared_draft_card_count"], 8)
        self.assertEqual(self.report["status"], "terminology_reconciled_no_pattern_promoted")
        self.assertIn("independent semantic validation", self.report["claim_boundary"])

    def test_shared_validation_remains_pending(self):
        for row in self.report["patterns"]:
            if row["shared_card_present"]:
                self.assertNotEqual(row["shared_card_status"], "validated_best_practice")


if __name__ == "__main__":
    unittest.main()
