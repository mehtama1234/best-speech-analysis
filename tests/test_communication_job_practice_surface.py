import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobPracticeSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "research/communication-job-mobile-lessons.json").read_text())
        cls.page = (ROOT / "writeups/communication-job-practice.html").read_text()

    def test_surface_is_backed_by_all_18_mobile_lessons(self):
        self.assertEqual(self.payload["lesson_count"], 18)
        self.assertIn("local_communication_practice_record", self.page)
        self.assertIn("Download local practice JSON", self.page)
        self.assertIn("nothing is sent to this repository", self.page)
        self.assertIn("consent", self.page)
        self.assertIn("Indexed phrase forms", self.page)
        self.assertIn("the point is", self.page)
        self.assertIn("Inspect exact examples", self.page)
        self.assertIn("<video", self.page)
        self.assertIn("Optional local rehearsal recording", self.page)
        self.assertIn("getUserMedia", self.page)
        self.assertIn("Nothing is uploaded", self.page)
        self.assertIn("learner-field-guide.md", self.page)
        for lesson in self.payload["lessons"]:
            self.assertIn(lesson["canonical_job"], self.page)


if __name__ == "__main__":
    unittest.main()
