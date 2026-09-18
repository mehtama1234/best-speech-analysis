import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusFunctionReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-function-independent-review-workbook.json").read_text())
        cls.html = (ROOT / "writeups/corpus-function-independent-review-workbook.html").read_text()

    def test_workbook_covers_function_queue_and_is_blank(self):
        self.assertEqual(self.workbook["item_count"], 187)
        self.assertEqual(len(self.workbook["items"]), 187)
        self.assertEqual(self.workbook["status"], "template_not_completed")
        self.assertTrue(all(all(value is None for value in item["review"].values()) for item in self.workbook["items"]))

    def test_form_has_independence_and_controlled_decisions(self):
        self.assertIn('name="independent_attestation"', self.html)
        self.assertEqual(self.html.count('name="item_1_candidate_label_decision"'), 1)
        self.assertIn("indeterminate", self.html)


if __name__ == "__main__":
    unittest.main()
