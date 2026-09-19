import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeliveryExperimentMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/delivery-experiment-matrix.json").read_text())
        cls.md = (ROOT / "writeups/delivery-experiment-matrix.md").read_text()

    def test_covers_all_shared_jobs_with_boundaries(self):
        self.assertEqual(self.data["job_count"], 18)
        self.assertEqual(len(self.data["rows"]), 18)
        self.assertIn("not findings", self.data["claim_boundary"])
        for row in self.data["rows"]:
            for field in ("vocal_variable", "observable_body_or_setting_variable", "accessible_alternate", "experiment", "listener_self_check", "anti_imitation"):
                self.assertTrue(row[field])
        self.assertIn("hold wording and content constant", self.md)


if __name__ == "__main__":
    unittest.main()
