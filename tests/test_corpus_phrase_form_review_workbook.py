import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CorpusPhraseFormReviewWorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / "research/corpus-phrase-form-inventory.json").read_text())
        cls.workbook = json.loads((ROOT / "research/corpus-phrase-form-independent-review-workbook.json").read_text())

    def test_has_one_blank_review_item_per_inventory_form(self):
        self.assertEqual(self.workbook["status"], "template_not_completed")
        self.assertEqual(self.workbook["item_count"], 50)
        self.assertEqual(len(self.workbook["items"]), len(self.inventory["forms"]))
        self.assertEqual({x["phrase_form"] for x in self.workbook["items"]}, {x["phrase_form"] for x in self.inventory["forms"]})
        for item in self.workbook["items"]:
            self.assertTrue(item["examples"])
            self.assertIsNone(item["review"]["form_match_decision"])
            self.assertIsNone(item["review"]["recurrence_decision"])

    def test_claim_boundary_and_views_are_present(self):
        self.assertIn("does not establish delivery effectiveness", self.workbook["claim_boundary"])
        self.assertTrue((ROOT / "writeups/corpus-phrase-form-independent-review-workbook.html").exists())
        self.assertTrue((ROOT / "writeups/corpus-phrase-form-independent-review-request.md").exists())


if __name__ == "__main__":
    unittest.main()
