import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class UnifiedPatternLibraryBrowserTests(unittest.TestCase):
    def test_browser_joins_fixed_and_expansion_layers(self):
        page = (ROOT / "writeups/unified-pattern-library.html").read_text()
        self.assertIn("Unified speaking pattern library", page)
        self.assertIn('fixed corpus', page)
        self.assertIn('expansion source', page)
        self.assertIn('candidate_pattern_not_effectiveness_validated', page)
        self.assertIn('provisional_contextual_review_required', page)
        self.assertIn('communication-job-practice.html', page)

    def test_browser_keeps_candidate_boundary_visible(self):
        page = (ROOT / "writeups/unified-pattern-library.html").read_text()
        self.assertIn("independent review, learner outcomes, listener outcomes and effectiveness remain open", page)


if __name__ == "__main__":
    unittest.main()
