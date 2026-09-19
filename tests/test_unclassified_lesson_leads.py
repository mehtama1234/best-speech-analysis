import unittest
from pathlib import Path

from scripts.build_unclassified_lesson_leads import main


ROOT = Path(__file__).resolve().parents[1]


class UnclassifiedLessonLeadTests(unittest.TestCase):
    def test_every_unrouted_video_has_a_reviewable_lead(self):
        main()
        text = (ROOT / "writeups/unclassified-lesson-leads.md").read_text()
        self.assertIn("160 transcript-derived inspection leads", text)
        self.assertIn("canonical practice labels assigned", text)
        data_rows = [line for line in text.splitlines() if line.startswith("| ") and line[2].isdigit()]
        self.assertEqual(len(data_rows), 160)
        self.assertIn("Review discipline", text)


if __name__ == "__main__":
    unittest.main()
