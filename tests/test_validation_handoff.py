import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT / "research/validation-handoff.json").read_text())
        cls.markdown = (ROOT / "writeups/validation-handoff.md").read_text()

    def test_handoff_covers_all_human_gates_without_claiming_results(self):
        self.assertEqual(self.report["status"], "instruments_ready_no_human_records_received")
        self.assertEqual(len(self.report["review_gates"]), 8)
        self.assertEqual(len(self.report["learning_gates"]), 3)
        self.assertIn("No reviewer", self.report["claim_boundary"])
        for gate in self.report["review_gates"] + self.report["learning_gates"]:
            self.assertTrue(gate["validator"])
            self.assertTrue(gate["does_not_establish"])
        self.assertIn("Do not send credentials", self.markdown)

    def test_learner_entry_links_resolve_from_writeups_directory(self):
        entry = self.report["learner_entry"]
        self.assertTrue((ROOT / entry["path"]).is_file())
        self.assertTrue((ROOT / entry["catalog"]).is_file())
        self.assertIn("(learner-7-day-path.md)", self.markdown)
        self.assertIn("(corpus-findings-catalog.md)", self.markdown)
        self.assertNotIn("(writeups/learner-7-day-path.md)", self.markdown)
        self.assertNotIn("(writeups/corpus-findings-catalog.md)", self.markdown)

    def test_delivery_atlas_is_in_handoff(self):
        entry = self.report["delivery_entry"]
        self.assertEqual(entry["candidate_record_count"], 1505)
        self.assertEqual(entry["candidate_video_count"], 188)
        self.assertTrue((ROOT / entry["markdown"]).is_file())
        self.assertTrue((ROOT / entry["browser"]).is_file())
        self.assertTrue((ROOT / entry["validator"]).is_file())
        self.assertTrue((ROOT / entry["summarizer"]).is_file())
        self.assertIn("delivery-proxy-candidate-atlas.md", self.markdown)
        self.assertIn("delivery-proxy-candidate-atlas.html", self.markdown)
        self.assertIn("validate_delivery_proxy_local_reviews.py", self.markdown)

    def test_blinded_packet_is_in_handoff(self):
        entry = self.report["blinded_review_entry"]
        self.assertEqual(entry["function_items"], 187)
        self.assertEqual(entry["recurrence_items"], 192)
        self.assertEqual(entry["phrase_form_items"], 50)
        for field in ("packet", "browser", "private_key", "export_validator", "adjudication_reducer", "adjudication_form_builder", "adjudication_export_validator"):
            self.assertTrue((ROOT / entry[field]).is_file())
        self.assertIn("blinded-review-packet.html", self.markdown)
        self.assertIn("reduce_blinded_review_export.py", self.markdown)


if __name__ == "__main__":
    unittest.main()
