import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusFindingsCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "research/corpus-findings-catalog.json").read_text())
        cls.cards = json.loads((ROOT / "research/communication-job-cards.json").read_text())
        cls.markdown = (ROOT / "writeups/corpus-findings-catalog.md").read_text()

    def test_full_video_and_observation_coverage_remains_present(self):
        self.assertEqual(self.catalog["coverage"]["review_count"], 395)
        self.assertEqual(len(self.catalog["video_findings"]), 395)
        self.assertEqual(self.catalog["coverage"]["function_observation_count"], 4016)
        self.assertEqual(self.catalog["coverage"]["relation_observation_count"], 2800)

    def test_candidate_routing_split_is_explicit_and_card_backed(self):
        coverage = self.catalog["coverage"]
        self.assertEqual(coverage["videos_with_candidate_practice_job"], 207)
        self.assertEqual(coverage["videos_without_candidate_practice_job"], 188)
        card_jobs = {card["canonical_job"] for card in self.cards["cards"]}
        for row in self.catalog["video_findings"]:
            self.assertTrue(set(row["candidate_job_forms"]).issubset(card_jobs))

    def test_unlabelled_structural_claims_are_visible(self):
        self.assertIn("Structural claims are shown for reading", self.markdown)
        self.assertIn("unlabelled: The responsibility contract", self.markdown)
        self.assertIn("`unclassified` items remain out of that route", self.markdown)


if __name__ == "__main__":
    unittest.main()
