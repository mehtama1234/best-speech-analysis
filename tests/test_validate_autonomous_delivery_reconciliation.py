import unittest

from scripts.validate_autonomous_delivery_reconciliation import validate


class ValidateAutonomousDeliveryReconciliationTest(unittest.TestCase):
    def test_delivery_lineage_and_boundaries_pass(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
