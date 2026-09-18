import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusPhraseFormInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / "research/corpus-phrase-form-inventory.json").read_text())
        cls.html = (ROOT / "writeups/corpus-phrase-form-inventory.html").read_text()

    def test_scans_restricted_caption_registry_and_preserves_boundary(self):
        self.assertEqual(self.inventory["status"], "heuristic_exact_phrase_inventory_not_validated")
        self.assertEqual(self.inventory["eligible_caption_segment_count"], 102351)
        self.assertGreater(self.inventory["form_count"], 20)
        self.assertIn("not speech effectiveness", self.inventory["claim_boundary"])

    def test_forms_have_recurrence_split_examples_and_hypothesis(self):
        for item in self.inventory["forms"]:
            self.assertGreater(item["video_count"], 0)
            self.assertEqual(item["video_count"], item["train_video_count"] + item["holdout_video_count"])
            self.assertTrue(item["examples"])
            self.assertTrue(item["mechanism_hypothesis"])
            self.assertEqual(item["mechanism_status"], "bounded_hypothesis_not_outcome_evidence")
        self.assertIn("Exact examples", self.html)


if __name__ == "__main__":
    unittest.main()
