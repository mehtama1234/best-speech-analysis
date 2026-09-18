import copy
import json
import unittest
from pathlib import Path

from scripts.validate_shared_lesson_cards import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateSharedLessonCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/shared-lesson-cards.json").read_text())

    def test_current_cards_are_valid_but_provisional(self):
        self.assertEqual(validate(self.data), [])

    def test_validator_catches_missing_chain_and_status_drift(self):
        data = copy.deepcopy(self.data)
        del data["cards"][0]["evidence_chain"]["listener_outcome_check"]
        data["cards"][1]["mechanism_status"] = "validated_effective_pattern"
        data["cards"][2]["speech_function"]["status"] = "validated_function"
        errors = validate(data)
        self.assertTrue(any("missing chain fields" in error for error in errors))
        self.assertTrue(any("mechanism status is not bounded" in error for error in errors))
        self.assertTrue(any("speech function is not provisional" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
