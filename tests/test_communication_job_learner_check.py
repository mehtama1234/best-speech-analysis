import copy
import json
import unittest
from pathlib import Path

from scripts.validate_communication_job_learner_record import validate


ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobLearnerCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((ROOT / "research/communication-job-learner-check.json").read_text())
        cls.html = (ROOT / "writeups/communication-job-learner-check.html").read_text()

    def test_fixed_protocol_covers_all_job_cards(self):
        self.assertEqual(self.protocol["status"], "protocol_drafted_not_run")
        self.assertEqual(self.protocol["card_count"], 18)
        self.assertEqual(self.protocol["task_count"], 72)
        self.assertIn("listener outcomes", self.protocol["claim_boundary"])
        self.assertIn("participant_code", self.html)
        self.assertIn("Download JSON record", self.html)

    def test_exact_phrase_forms_are_linked_without_forcing_unindexed_jobs(self):
        self.assertEqual(self.protocol["exact_phrase_form_count"], 50)
        matched = [card for card in self.protocol["cards"] if card["phrase_form_coverage_status"] == "indexed_family_match"]
        unmatched = [card for card in self.protocol["cards"] if card["phrase_form_coverage_status"] == "no_direct_family_match"]
        self.assertEqual(len(matched), 8)
        self.assertEqual(len(unmatched), 10)
        self.assertTrue(all(card["phrase_forms"] for card in matched))
        self.assertTrue(all(not card["phrase_forms"] for card in unmatched))

    def test_validator_accepts_complete_synthetic_shape_and_rejects_missing(self):
        record = {
            "record_type": "communication_job_learner_observation",
            "protocol_id": self.protocol["protocol_id"],
            "claim_boundary": self.protocol["claim_boundary"],
            "task_bank_ids": [task["task_id"] for task in self.protocol["tasks"]],
            "responses": {"participant_code": "synthetic", "date": "2026-09-18", "lesson_version": "test", "consent": True},
        }
        for card in self.protocol["cards"]:
            tasks = [task["task_id"] for task in self.protocol["tasks"] if task["card_id"] == card["card_id"]]
            record["responses"][f"{card['card_id']}_task_ids"] = ",".join(tasks)
            for task_id in tasks:
                record["responses"][task_id] = "synthetic response"
            for suffix in ("listener_restatement", "revision", "boundary_note"):
                record["responses"][f"{card['card_id']}_{suffix}"] = "synthetic note"
            for dimension in card["scoring_dimensions"]:
                record["responses"][f"{card['card_id']}_score_{dimension}"] = "2"
            record["responses"][f"{card['card_id']}_safety_issue"] = "no"
        self.assertEqual(validate(record, self.protocol), [])
        incomplete = copy.deepcopy(record)
        del incomplete["responses"]["opening-recognition-01"]
        self.assertTrue(any("opening-recognition-01" in error for error in validate(incomplete, self.protocol)))


if __name__ == "__main__":
    unittest.main()
