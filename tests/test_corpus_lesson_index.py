import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusLessonIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/corpus-lesson-index.json").read_text())
        cls.html = (ROOT / "writeups/corpus-lesson-index.html").read_text()

    def test_covers_every_completed_review_without_promoting_claims(self):
        self.assertEqual(self.index["status"], "transcript_derived_discovery_index_not_validated")
        self.assertEqual(self.index["review_count"], 395)
        self.assertEqual(len(self.index["entries"]), 395)
        self.assertIn("does not establish recurrence", self.index["claim_boundary"])

    def test_evidence_ids_are_from_each_review_context(self):
        reviews = {
            item["review_id"]: item
            for item in json.loads((ROOT / "research/full-context-reviews.json").read_text())["reviews"]
        }
        for entry in self.index["entries"]:
            context = set(reviews[entry["review_id"]]["context_evidence_ids"])
            for function in entry["communication_function_inventory"]:
                self.assertTrue(set(function["evidence_ids"]) <= context)
            for relation in entry["structural_relation_inventory"]:
                self.assertTrue(set(relation["from_evidence_ids"]) <= context)
                self.assertTrue(set(relation["to_evidence_ids"]) <= context)
        self.assertEqual(self.index["summary"]["missing_context_evidence_id_count"], 0)

    def test_browser_preserves_search_and_boundary(self):
        self.assertIn('id="search"', self.html)
        self.assertIn("Discovery only.", self.html)
        self.assertIn("communication functions", self.html)
        self.assertIn("listener outcomes", self.html)


if __name__ == "__main__":
    unittest.main()
