import json
import unittest
from pathlib import Path

from scripts.validate_shared_evidence_model import validate


ROOT = Path(__file__).resolve().parents[1]


class SharedEvidenceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads((ROOT / "research/shared-evidence-model.json").read_text())

    def test_contract_is_incomplete_and_preserves_separate_claim_levels(self):
        self.assertEqual(self.model["status"], "contract_ready_research_evidence_incomplete")
        self.assertEqual(self.model["current_manifest"]["exact_caption_evidence"]["caption_segment_record_count"], 102816)
        self.assertEqual(self.model["current_manifest"]["delivery"]["independent_observation_count"], 0)
        self.assertEqual(self.model["current_manifest"]["listener"]["completed_records"], 0)
        self.assertIn("listener_outcome_evidence", [item["level"] for item in self.model["claim_levels"]])
        self.assertIn("counterexample_observation", self.model["entity_types"])
        self.assertIn("practice_record", self.model["entity_types"])
        self.assertIn("mobile_lesson", self.model["entity_types"])
        self.assertTrue(any("Every mobile lesson carries" in rule for rule in self.model["link_rules"]))
        self.assertEqual(self.model["current_manifest"]["counterexamples"]["queued_slot_count"], 90)
        self.assertEqual(self.model["current_manifest"]["counterexample_candidates"]["candidate_count"], 90)
        self.assertEqual(self.model["current_manifest"]["counterexample_candidates"]["confirmed_counterexample_count"], 0)
        self.assertEqual(self.model["current_manifest"]["mobile_lessons"]["lesson_count"], 18)

    def test_contract_reconciles_with_live_artifacts(self):
        self.assertEqual(validate(self.model), [])


if __name__ == "__main__":
    unittest.main()
