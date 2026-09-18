import json
import unittest
from pathlib import Path

from scripts.build_corpus_function_taxonomy import classify


ROOT = Path(__file__).resolve().parents[1]


class CorpusFunctionTaxonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy = json.loads((ROOT / "research/corpus-function-taxonomy.json").read_text())
        cls.lesson_index = json.loads((ROOT / "research/corpus-lesson-index.json").read_text())

    def test_preserves_scope_and_non_promotional_boundary(self):
        self.assertEqual(self.taxonomy["status"], "heuristic_canonicalization_not_independently_validated")
        self.assertEqual(self.taxonomy["summary"]["review_count"], 395)
        self.assertEqual(self.taxonomy["summary"]["function_item_count"], 4016)
        self.assertIn("establish speaker intent", self.taxonomy["claim_boundary"])

    def test_every_item_is_mapped_or_explicitly_unclassified(self):
        total = 0
        for entry in self.taxonomy["entries"]:
            for item in entry["functions"]:
                total += 1
                self.assertIn(item["canonical_job"], self.taxonomy["canonical_jobs"])
                self.assertTrue(item["mapping_rule"])
        self.assertEqual(total, self.taxonomy["summary"]["function_item_count"])
        self.assertEqual(
            self.taxonomy["summary"]["unclassified_item_count"],
            len(self.taxonomy["unclassified_review_queue"]),
        )

    def test_mapping_is_deterministic_and_original_inventory_is_unchanged(self):
        original = sum(len(entry["communication_function_inventory"]) for entry in self.lesson_index["entries"])
        self.assertEqual(original, 4016)
        self.assertEqual(classify("question_reframed_from_moment_to_collective_process")[0], "question")
        self.assertEqual(classify("personal story anchor")[0], "story_or_personal_experience")
        self.assertEqual(classify("Publisher promotion")[0], "media_or_publisher")
        self.assertEqual(classify("")[0], "unclassified")


if __name__ == "__main__":
    unittest.main()
