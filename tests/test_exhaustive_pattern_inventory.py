import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExhaustivePatternInventoryTests(unittest.TestCase):
    def test_all_reviews_and_source_linked_themes_are_present(self):
        report = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
        self.assertEqual(report["status"], "all_review_records_mined_candidate_themes_unvalidated")
        self.assertEqual(report["review_count"], 395)
        self.assertGreater(report["episode_record_count"], 40000)
        self.assertGreater(report["relation_record_count"], 25000)
        self.assertEqual(report["theme_count"], 22)
        self.assertEqual(report["relation_pattern_count"], 18)
        self.assertEqual(report["unmatched_cluster_count"], 15)
        self.assertGreaterEqual(report["coverage"]["episode_labels_with_keyword_theme_match"], 1500)
        self.assertGreaterEqual(report["coverage"]["relation_types_with_keyword_theme_match"], 800)
        for theme in report["themes"]:
            self.assertTrue(theme["examples"])
            self.assertTrue(all(item["evidence_ids"] for item in theme["examples"]))
            self.assertEqual(theme["status"], "candidate_theme_requires_contextual_and_independent_review")
        for pattern in report["relation_patterns"]:
            self.assertEqual(pattern["status"], "candidate_structural_pattern_requires_contextual_and_independent_review")
        for cluster in report["unmatched_clusters"]:
            self.assertTrue(cluster["examples"])
            self.assertEqual(cluster["status"], "unmatched_label_cluster_requires_semantic_review")


if __name__ == "__main__":
    unittest.main()
