import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunicationJobCounterexampleWorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/communication-job-counterexample-workbook.json").read_text())

    def test_all_jobs_have_all_five_blank_counterexample_types(self):
        self.assertEqual(self.workbook["job_count"], 18)
        self.assertEqual(self.workbook["item_count"], 90)
        jobs = {}
        for item in self.workbook["items"]:
            jobs.setdefault(item["canonical_job"], []).append(item["counterexample_type"])
            self.assertIsNone(item["candidate"]["evidence_id"])
            self.assertIsNone(item["review"]["evidence_status"])
        self.assertEqual(len(jobs), 18)
        for types in jobs.values():
            self.assertEqual(len(types), 5)
            self.assertEqual(len(set(types)), 5)

    def test_claim_boundary_and_outputs(self):
        self.assertIn("Blank slots are not evidence", self.workbook["claim_boundary"])
        self.assertTrue((ROOT / "writeups/communication-job-counterexample-workbook.html").exists())
        self.assertTrue((ROOT / "writeups/communication-job-counterexample-review-request.md").exists())


if __name__ == "__main__":
    unittest.main()
