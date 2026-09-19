import json
import unittest
from pathlib import Path

from scripts.validate_timing_candidate_reviews import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateTimingCandidateReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads((ROOT / "research/full-corpus-timing-candidate-atlas.json").read_text())

    def test_valid_record_and_html_surface(self):
        self.assertTrue((ROOT / "writeups/full-corpus-timing-candidate-atlas.html").exists())
        row = self.atlas["items"][0]
        record = {
            "candidate_id": row["candidate_id"],
            "reviewer": "reviewer-a",
            "alignment": "partial",
            "cause": "missing_or_unclear",
            "observation": "Cause cannot be separated from caption timing.",
            "accessibility": "Audio and captions reviewed; visual meaning not required.",
            "updated_at": "2026-09-19T00:00:00Z",
        }
        self.assertEqual(validate([record], self.atlas), [])

    def test_unknown_and_incomplete_records_fail(self):
        errors = validate([{"candidate_id": "unknown"}], self.atlas)
        self.assertIn("record 0 references an unknown candidate_id", errors)
        self.assertIn("record 0 reviewer is required", errors)
        self.assertIn("record 0 observation is required", errors)


if __name__ == "__main__":
    unittest.main()
