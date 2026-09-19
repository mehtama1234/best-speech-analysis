import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SharedLessonCardsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "writeups/shared-lesson-cards.html").read_text()

    def test_page_exposes_search_filters_and_evidence_sections(self):
        for marker in ('id="search"', 'id="job"', 'id="status"', 'Why it might help', 'Exact language and context', 'Delivery evidence and missingness', 'Validation, limits and listener separation', 'Practice and self-check', 'source'):
            self.assertIn(marker, self.page)
        self.assertIn("effectiveness", self.page)

    def test_page_is_mobile_safe_and_embeds_all_cards(self):
        self.assertIn('name="viewport"', self.page)
        self.assertIn("provisional-job-opening", self.page)
        self.assertIn("provisional-job-call_to_action_or_audience_role", self.page)


if __name__ == "__main__":
    unittest.main()
