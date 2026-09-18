import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CorpusAtlasPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "writeups/corpus-pattern-atlas.html").read_text()

    def test_page_exposes_search_filters_and_transcript_boundary(self):
        for marker in ('id="search"', 'id="family"', 'id="function"', 'id="split"', 'Retrieval denominators', 'candidate speech-function labels', 'source'):
            self.assertIn(marker, self.page)

    def test_page_embeds_corpus_and_holdout_data(self):
        self.assertIn("2fWJh-_UG5s", self.page)
        self.assertIn("holdout", self.page)
        self.assertIn("UCeY5YPd2I0", self.page)


if __name__ == "__main__":
    unittest.main()
