import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JobPhraseCandidateInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/job-phrase-candidate-inventory.json").read_text())

    def test_all_jobs_have_contextual_phrase_candidates(self):
        self.assertTrue((ROOT / "writeups/job-phrase-candidate-inventory.html").exists())
        self.assertEqual(self.report["status"], "heuristic_multiword_phrase_candidates_not_validated")
        self.assertEqual(self.report["job_count"], 18)
        self.assertEqual(self.report["form_count"], 209)
        self.assertEqual(len(self.report["forms_per_job"]), 18)
        self.assertIn("speaker intent", self.report["claim_boundary"])
        self.assertTrue(all(row["status"].endswith("independent_review") for row in self.report["forms"]))

    def test_forms_are_bounded_and_have_source_examples(self):
        counts = Counter(row["canonical_job"] for row in self.report["forms"])
        self.assertLessEqual(max(counts.values()), 12)
        for row in self.report["forms"]:
            self.assertGreaterEqual(len(row["phrase_form"].split()), 2)
            self.assertLessEqual(len(row["phrase_form"].split()), 4)
            self.assertGreaterEqual(row["video_count"], 4)
            self.assertTrue(row["examples"])


if __name__ == "__main__":
    unittest.main()
