import unittest

from scripts.validate_autonomous_claim_boundaries import validate


class AutonomousClaimBoundariesTest(unittest.TestCase):
    def test_provisional_surfaces_cannot_be_promoted_by_schema_drift(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
