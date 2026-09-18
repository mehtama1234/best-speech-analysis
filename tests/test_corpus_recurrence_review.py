import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusRecurrenceReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-recurrence-independent-review-workbook.json").read_text())
        cls.html = (ROOT / "writeups/corpus-recurrence-independent-review-workbook.html").read_text()

    def test_workbook_covers_stratified_queue_and_is_blank(self):
        self.assertEqual(self.workbook["item_count"], 192)
        self.assertEqual(len(self.workbook["items"]), 192)
        self.assertEqual(self.workbook["status"], "template_not_completed")
        self.assertTrue(all(all(value is None for value in item["review"].values()) for item in self.workbook["items"]))

    def test_form_has_independence_and_controlled_decisions(self):
        self.assertIn('name="independent_attestation"', self.html)
        self.assertEqual(self.html.count('name="item_1_context_decision"'), 1)
        self.assertIn("not_enough_context", self.html)

    def test_external_review_request_is_present_and_bounded(self):
        request = (ROOT / "writeups/corpus-recurrence-independent-review-request.md").read_text()
        self.assertIn("Independence and safety", request)
        self.assertIn("validate_corpus_recurrence_review.py", request)
        self.assertIn("would not establish", request)


if __name__ == "__main__":
    unittest.main()
