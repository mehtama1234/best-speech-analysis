import unittest

from scripts.check_public_claim_boundaries import audit


class PublicClaimBoundaryTests(unittest.TestCase):
    def test_public_documents_preserve_validation_boundary(self):
        result = audit()
        self.assertEqual(result["status"], "public_claim_boundaries_valid")
        self.assertEqual(result["violations"], [])
        self.assertEqual(result["missing_disclosures"], [])


if __name__ == "__main__":
    unittest.main()
