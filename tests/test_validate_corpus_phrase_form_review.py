import json
import unittest
from pathlib import Path

from scripts.validate_corpus_phrase_form_review import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateCorpusPhraseFormReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = json.loads((ROOT / "research/corpus-phrase-form-independent-review-workbook.json").read_text())

    def test_blank_or_partial_export_is_rejected(self):
        errors = validate({"record_type": "corpus_phrase_form_independent_review", "workbook_id": self.workbook["workbook_id"], "claim_boundary": "Phrase-form review only; not delivery effectiveness or audience outcome evidence.", "responses": {}}, self.workbook)
        self.assertTrue(errors)
        self.assertIn("independent_attestation must be true", errors)


if __name__ == "__main__":
    unittest.main()
