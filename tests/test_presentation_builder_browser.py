import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PresentationBuilderBrowserReceiptTest(unittest.TestCase):
    def test_receipt_is_present_and_bounded(self):
        data = json.loads((ROOT / "research/presentation-builder-browser-smoke.json").read_text())
        self.assertEqual(data["status"], "presentation_builder_browser_smoke_passed")
        self.assertEqual(data["checks"]["pattern_moves_selected"], 2)
        self.assertIn("not learner", data["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
