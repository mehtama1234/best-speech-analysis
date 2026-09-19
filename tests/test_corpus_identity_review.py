import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CorpusIdentityReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-identity-review-workbook.json").read_text())

    def test_covers_full_reviewed_queue_and_preserves_blank_decisions(self):
        self.assertEqual(self.workbook["status"], "metadata_preflight_independent_review_pending")
        self.assertEqual(self.workbook["item_count"], 395)
        self.assertEqual(self.workbook["registry_row_count"], 480)
        self.assertEqual(len(self.workbook["items"]), 395)
        for item in self.workbook["items"]:
            self.assertIsNone(item["review"]["speaker_identity"])
            self.assertIsNone(item["review"]["duplicate_or_compilation_status"])

    def test_metadata_is_not_presented_as_identity_proof(self):
        self.assertIn("metadata and title matches are leads, not proof", self.workbook["claim_boundary"])
        self.assertTrue((ROOT / "writeups/corpus-identity-review-workbook.html").exists())


if __name__ == "__main__":
    unittest.main()
