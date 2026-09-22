import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PresentationPatternPlaybookTest(unittest.TestCase):
    def test_all_55_cards_have_drafting_and_source_fields(self):
        data = json.loads((ROOT / "research/presentation-pattern-playbook.json").read_text())
        self.assertEqual(data["status"], "source_linked_drafting_playbook_not_validated")
        self.assertEqual(data["card_count"], 55)
        self.assertEqual(len(data["cards"]), 55)
        self.assertEqual(len({row["pattern_id"] for row in data["cards"]}), 55)
        for row in data["cards"]:
            self.assertTrue(row["candidate_form"])
            self.assertTrue(row["move_sequence"])
            self.assertTrue(row["use_when"])
            self.assertTrue(row["draft_prompt"])
            self.assertTrue(row["practice_check"])
            self.assertTrue(row["safety_boundary"])
            self.assertTrue(row["example_video_id"])
            self.assertTrue(row["example_evidence_ids"])

    def test_browser_and_markdown_exist(self):
        self.assertTrue((ROOT / "writeups/presentation-pattern-playbook.html").exists())
        self.assertIn("Presentation pattern playbook", (ROOT / "writeups/presentation-pattern-playbook.md").read_text())


if __name__ == "__main__":
    unittest.main()
