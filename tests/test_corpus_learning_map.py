import unittest
from pathlib import Path

from scripts.build_corpus_learning_map import main


ROOT = Path(__file__).resolve().parents[1]


class CorpusLearningMapTests(unittest.TestCase):
    def test_map_is_generated_from_full_corpus_and_has_usable_routes(self):
        main()
        text = (ROOT / "writeups/corpus-learning-map.md").read_text()
        self.assertIn("395 videos", text)
        self.assertIn("Job-to-practice index", text)
        self.assertIn("the point is", text)
        self.assertIn("delivery-learning-guide.md", text)
        self.assertIn("without either route", text)
        self.assertGreaterEqual(text.count("| `"), 18)


if __name__ == "__main__":
    unittest.main()
