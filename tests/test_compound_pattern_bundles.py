import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CompoundPatternBundleTests(unittest.TestCase):
    def test_bundles_are_source_linked_and_have_minimum_recurrence(self):
        report = json.loads((ROOT / "research/compound-pattern-bundles.json").read_text())
        self.assertEqual(report["status"], "source_linked_compound_candidates_not_validated")
        self.assertEqual(report["bundle_count"], 24)
        self.assertEqual(report["candidate_bundle_count"], 136)
        self.assertEqual(report["minimum_cooccurrence_reviews"], 3)
        for bundle in report["bundles"]:
            self.assertGreaterEqual(bundle["cooccurrence_review_count"], 3)
            self.assertTrue(bundle["examples"])
            self.assertTrue(bundle["examples"][0]["left_excerpt"] or bundle["examples"][0]["right_excerpt"])
            self.assertTrue(bundle["candidate_form"])
            self.assertIn("not", bundle["non_fit_warning"])

    def test_browser_receipt_covers_practice_path(self):
        receipt = json.loads((ROOT / "research/compound-pattern-browser-smoke.json").read_text())
        self.assertEqual(receipt["status"], "compound_pattern_browser_smoke_passed")
        self.assertEqual(receipt["bundle_count"], 24)
        self.assertTrue(all(receipt["checks"].values()))


if __name__ == "__main__":
    unittest.main()
