import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = json.loads((ROOT / "research/communication-job-cards.json").read_text())
        cls.html = (ROOT / "writeups/communication-job-cards.html").read_text()

    def test_cards_are_provisional_and_cover_shared_jobs(self):
        self.assertEqual(self.cards["status"], "provisional_transcript_cards_not_validated")
        self.assertEqual(self.cards["card_count"], 18)
        self.assertIn("listener outcomes", self.cards["claim_boundary"])
        for card in self.cards["cards"]:
            self.assertTrue(card["mechanism"])
            self.assertTrue(card["practice"])
            self.assertTrue(card["non_fit"])
            self.assertIn("phrase_forms", card)
            self.assertIn("phrase_form_coverage_status", card)
            self.assertEqual(card["validation"]["learner_check"], "not_run")
            self.assertIn("delivery_evidence_status", card)
            self.assertEqual(len(card["delivery_observations"]), 2)
            for observation in card["delivery_observations"]:
                self.assertEqual(observation["delivery_evidence_status"], "internal_bounded_review_not_independent")

    def test_examples_retain_exact_caption_text_and_links(self):
        for card in self.cards["cards"]:
            self.assertGreater(card["recurrence"]["function_record_count"], 0)
            self.assertTrue(card["exact_examples"])
            for example in card["exact_examples"]:
                self.assertTrue(example["exact_segments"])
                self.assertTrue(example["source_url"].startswith("https://"))
                self.assertEqual(example["sample_scope"], "first_three_retained_segments_of_function_span")
                self.assertIn("example_quality", example)
                self.assertGreater(example["example_quality"]["lexical_word_count"], 0)
        self.assertIn("Practice hypotheses", self.html)
        self.assertIn("Exact examples", self.html)
        self.assertIn("Internal delivery observations", self.html)


if __name__ == "__main__":
    unittest.main()
