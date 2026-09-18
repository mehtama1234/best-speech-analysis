import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SharedLessonCardsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "writeups/shared-lesson-cards.html").read_text()

    def test_page_exposes_search_filters_and_evidence_sections(self):
        for marker in ('id="search"', 'id="slice"', 'id="status"', 'Why it might help', 'Exact phrase forms', 'Exact reviewed examples', 'Counterexamples, controls and failure candidates', 'Audio/video observations', 'Evidence chain and validation gates', 'Practise this choice', 'shared-learner-check.html', 'source'):
            self.assertIn(marker, self.page)
        self.assertIn("effectiveness", self.page)

    def test_page_is_mobile_safe_and_embeds_all_cards(self):
        self.assertIn('name="viewport"', self.page)
        self.assertIn("provisional-contrast_or_disagreement", self.page)
        self.assertIn("candidate-call_to_action", self.page)


if __name__ == "__main__":
    unittest.main()
