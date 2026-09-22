import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCurriculumIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text())
        cls.html = (ROOT / "writeups/communication-job-curriculum.html").read_text()

    def test_integrates_all_evidence_layers_for_18_jobs(self):
        self.assertEqual(self.index["status"], "18_job_provisional_curriculum_not_validated")
        self.assertEqual(self.index["lesson_count"], 18)
        for lesson in self.index["lessons"]:
            self.assertEqual(len(lesson["counterexample_slots"]), 5)
            self.assertEqual(len(lesson["delivery_samples"]), 2)
            self.assertEqual(lesson["learner"]["task_count"], 4)
            self.assertIn("mechanism_hypothesis", lesson)
            self.assertIn("non_fit", lesson)

    def test_missing_validation_stays_visible(self):
        self.assertIn("not present any pattern as effective", self.index["claim_boundary"])
        self.assertIn("manual observation pending", self.html)
        self.assertIn("Counterexample and limit queue", self.html)

    def test_examples_retain_context_and_recurrence_denominators(self):
        for lesson in self.index["lessons"]:
            recurrence = lesson["recurrence"]
            self.assertGreaterEqual(recurrence["function_record_count"], recurrence["video_count"])
            self.assertTrue(recurrence["denominator_status"])
            for example in lesson["exact_examples"]:
                self.assertTrue(example["record_id"])
                self.assertTrue(example["source_url"])
                self.assertTrue(example["exact_segments"])
                for segment in example["exact_segments"]:
                    self.assertTrue(segment["evidence_id"])
                    self.assertTrue(segment["source_transcript_file"])
                    self.assertLessEqual(segment["start_seconds"], segment["end_seconds"])

    def test_discovery_facets_keep_missingness_visible(self):
        for facet in ("filter-function", "filter-modality", "filter-setting", "filter-difficulty", "filter-source_quality", "filter-confidence"):
            self.assertIn(f'id="{facet}"', self.html)
        self.assertIn("unclassified", self.html)
        self.assertIn("provisional", self.html)
        self.assertIn('data-source_quality=', self.html)

    def test_curriculum_surface_has_accessible_document_and_live_count(self):
        self.assertIn('<html lang="en">', self.html)
        self.assertIn('id="count" aria-live="polite"', self.html)
        self.assertIn('<label for="search">', self.html)


if __name__ == "__main__":
    unittest.main()
