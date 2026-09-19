from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IndependentReviewFormsBrowserSmokeTest(unittest.TestCase):
    def test_browser_smoke_script_exists(self):
        self.assertTrue((ROOT / "scripts/check_independent_review_forms_browser.py").is_file())
