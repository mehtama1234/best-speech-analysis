import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SharedCurriculumIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/shared-provisional-curriculum.json").read_text())
        cls.html = (ROOT / "writeups/shared-provisional-curriculum.html").read_text()

    def test_index_combines_both_slices_without_promoting_them(self):
        self.assertEqual(self.index["lesson_count"], 18)
        self.assertEqual(self.index["status"], "18_draft_lessons_not_validated")
        self.assertEqual({row["slice"] for row in self.index["lessons"]}, {"communication-job-curriculum"})
        self.assertIn("listener_outcomes", self.index["validation_gates"])
        self.assertEqual(self.index["shared_learner_check"], "research/communication-job-learner-check.json")
        self.assertTrue((ROOT / self.index["shared_learner_check_html"]).exists())
        self.assertEqual(self.index["shared_lesson_cards"], "research/shared-lesson-cards.json")
        self.assertTrue((ROOT / self.index["shared_lesson_cards"]).exists())
        self.assertEqual(self.index["shared_lesson_cards_html"], "writeups/shared-lesson-cards.html")
        self.assertTrue((ROOT / self.index["shared_lesson_cards_html"]).exists())

    def test_every_lesson_links_existing_packet_and_lesson(self):
        for row in self.index["lessons"]:
            self.assertTrue((ROOT / row["packet"]).exists(), row["packet"])
            self.assertTrue((ROOT / row["lesson"]).exists(), row["lesson"])
            self.assertIn("not_validated", row["lesson_status"])
            self.assertGreaterEqual(row["counterexample_count"], 0)

    def test_html_has_search_slice_filter_and_all_cards(self):
        self.assertIn('id="search"', self.html)
        self.assertIn('id="slice"', self.html)
        self.assertIn("18 draft lessons", self.html)
        for row in self.index["lessons"]:
            self.assertIn(row["pattern_id"], self.html)

    def test_browser_smoke_script_is_present(self):
        self.assertTrue((ROOT / "scripts/check_shared_curriculum_browser.py").exists())

    def test_candidate_slice_has_runnable_learner_instrument(self):
        manifest = json.loads((ROOT / "research/vertical-slice-02.json").read_text())
        self.assertTrue((ROOT / manifest["learner_check_html"]).exists())
        self.assertTrue((ROOT / manifest["learner_check_validator"]).exists())


if __name__ == "__main__":
    unittest.main()
