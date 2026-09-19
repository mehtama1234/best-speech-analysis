import json
import unittest
from pathlib import Path

from scripts.validate_delivery_proxy_local_reviews import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateDeliveryProxyLocalReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads((ROOT / "research/delivery-proxy-candidate-atlas.json").read_text())
        cls.record_id = cls.atlas["candidates"][0]["record_id"]

    def test_valid_bounded_record_passes(self):
        record = {
            "record_id": self.record_id,
            "reviewer": "reviewer-1",
            "alignment": "indeterminate",
            "identity": "not_reviewed",
            "updated_at": "2026-09-19T00:00:00Z",
            "vocal": "not reviewed",
            "visual": "not available",
            "setting": "not reviewed",
            "access": "captions available; audio not reviewed",
            "alternate": "not reviewed",
        }
        self.assertEqual(validate([record], self.atlas), [])

    def test_unknown_record_and_blank_observation_fail(self):
        errors = validate([{"record_id": "missing", "alignment": "bad"}], self.atlas)
        self.assertIn("unknown atlas record_id", " ".join(errors))
        self.assertIn("missing vocal", " ".join(errors))


if __name__ == "__main__":
    unittest.main()
