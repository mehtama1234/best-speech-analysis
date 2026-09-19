import json
import unittest
from pathlib import Path

from scripts.validate_blinded_review_packet import validate


ROOT = Path(__file__).resolve().parents[1]


class BlindedReviewPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads((ROOT / "research/blinded-review-packet.json").read_text())
        cls.html = (ROOT / "writeups/blinded-review-packet.html").read_text()

    def test_packet_has_expected_gates_and_hides_labels(self):
        self.assertEqual(validate(self.packet), [])
        self.assertEqual(self.packet["gates"]["function"]["item_count"], 187)
        self.assertEqual(self.packet["gates"]["recurrence"]["item_count"], 192)
        self.assertEqual(self.packet["gates"]["phrase_form"]["item_count"], 50)
        self.assertEqual(self.html.count("<fieldset>"), 430)
        self.assertIn("Download blinded review export", self.html)
        self.assertNotIn("candidate_function", self.html)


if __name__ == "__main__":
    unittest.main()
