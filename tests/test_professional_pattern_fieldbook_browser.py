import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfessionalPatternFieldbookBrowserTest(unittest.TestCase):
    def test_smoke_receipt(self):
        data = json.loads((ROOT / "research/professional-pattern-fieldbook-browser-smoke.json").read_text())
        self.assertEqual(data["status"], "professional_pattern_fieldbook_browser_smoke_passed")
        self.assertEqual(data["checks"]["research_index_entries"], 55)
        self.assertEqual(data["checks"]["speaking_job_chapters"], 7)
        self.assertTrue(data["checks"]["all_index_details_opened"])
        self.assertTrue(data["checks"]["all_55_invented_before_after_examples_opened"])
        self.assertTrue(data["checks"]["source_links_resolve"])
        self.assertTrue(data["checks"]["print_index_visible_and_interactive_index_hidden"])


if __name__ == "__main__":
    unittest.main()
