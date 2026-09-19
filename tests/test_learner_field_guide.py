import unittest
from pathlib import Path

from scripts.build_learner_field_guide import main


ROOT = Path(__file__).resolve().parents[1]


class LearnerFieldGuideTests(unittest.TestCase):
    def test_guide_covers_all_jobs_and_preserves_boundary(self):
        main()
        guide = (ROOT / "writeups/learner-field-guide.md").read_text()
        self.assertEqual(guide.count("### "), 18)
        self.assertIn("not a validated best-practice library", guide)
        self.assertIn("Do not copy a speaker’s identity", guide)
        self.assertIn("communication jobs", guide.lower())
        self.assertIn("Exact phrase-form index", guide)
        self.assertIn("repeatable verbal moves", guide)
        phrase_section = guide.split("## Exact phrase-form index", 1)[1]
        self.assertEqual(phrase_section.count("| `"), 100)


if __name__ == "__main__":
    unittest.main()
