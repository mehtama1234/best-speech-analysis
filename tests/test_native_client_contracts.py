import unittest
from pathlib import Path

from scripts.validate_native_client_contracts import validate


class NativeClientContractTests(unittest.TestCase):
    def test_generated_contracts_match_shared_model(self):
        self.assertEqual(validate(), [])

    def test_generated_contracts_include_local_practice_record(self):
        root = Path(__file__).resolve().parents[1]
        for relative in (
            "clients/generated/shared_evidence_contract.ts",
            "clients/generated/SharedEvidenceContract.kt",
            "clients/generated/SharedEvidenceContract.swift",
        ):
            self.assertIn("PracticeRecord", (root / relative).read_text())
            self.assertIn("MobileLesson", (root / relative).read_text())
        for relative in ("clients/examples/MobileLessonHelpers.kt", "clients/examples/MobileLessonHelpers.swift"):
            self.assertIn("MobileLessonHelpers", (root / relative).read_text())

    def test_swift_recursive_record_value_is_indirect(self):
        root = Path(__file__).resolve().parents[1]
        source = (root / "clients/generated/SharedEvidenceContract.swift").read_text()
        self.assertIn("public indirect enum RecordValue: Codable", source)

    def test_native_helpers_enforce_provisional_safety_boundary(self):
        root = Path(__file__).resolve().parents[1]
        kotlin = (root / "clients/examples/MobileLessonHelpers.kt").read_text()
        swift = (root / "clients/examples/MobileLessonHelpers.swift").read_text()
        for source in (kotlin, swift):
            self.assertIn("provisional_not_validated", source)
            self.assertIn("practice_hypothesis", source)
            self.assertIn("safety_boundary", source)
            self.assertIn("exact_example_ids", source)
            self.assertIn("createPracticeRecord", source)
            self.assertIn("changedResponses", source)
        self.assertIn("as? String", kotlin)

    def test_synthetic_cross_client_fixture_is_validated(self):
        self.assertEqual(validate(), [])
        root = Path(__file__).resolve().parents[1]
        import json
        fixtures = json.loads((root / "clients/examples/mobile_lesson_fixtures.json").read_text())
        self.assertEqual(len(fixtures), 18)


if __name__ == "__main__":
    unittest.main()
