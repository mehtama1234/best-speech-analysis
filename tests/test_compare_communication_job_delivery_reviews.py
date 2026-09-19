import json
import unittest
from pathlib import Path

from scripts.compare_communication_job_delivery_reviews import compare

ROOT = Path(__file__).resolve().parents[1]


class CompareCommunicationJobDeliveryReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads((ROOT / "research/communication-job-delivery-sampling.json").read_text())

    def record(self, name: str, disagreement: bool = False) -> dict:
        responses = {field: "synthetic session" for field in self.queue["review_schema"]["required_session_fields"]}
        for number in range(1, self.queue["item_count"] + 1):
            for field in self.queue["review_schema"]["required_item_fields"]:
                responses[f"item_{number}_{field}"] = "partially_aligned" if disagreement and field == "transcript_alignment" and number == 1 else "synthetic observation"
            responses[f"item_{number}_reviewer_code"] = name
            responses[f"item_{number}_transcript_alignment"] = "partially_aligned" if disagreement and number == 1 else "aligned"
        responses["reviewer_name"] = name
        responses["reviewer_role"] = "independent"
        responses["conflict_statement"] = "none"
        return {"record_type": "communication_job_delivery_sampling_review", "sampling_id": self.queue["sampling_id"], "claim_boundary": "Manual delivery observation only; not effectiveness evidence.", "responses": responses}

    def test_disagreement_is_preserved_and_not_promoted(self):
        report = compare([self.record("r1"), self.record("r2", True)], self.queue)
        self.assertEqual(report["disagreement_count"], 1)
        self.assertFalse(report["promotion_eligible"])
        self.assertIn("Adjudicate", report["next_step"])

    def test_duplicate_reviewer_is_rejected(self):
        with self.assertRaises(ValueError):
            compare([self.record("same"), self.record("same")])


if __name__ == "__main__":
    unittest.main()
