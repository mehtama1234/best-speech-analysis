import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PresentationPatternAtlasTests(unittest.TestCase):
    def test_atlas_reconciles_discovery_and_practice_layers(self):
        report = json.loads((ROOT / "research/presentation-pattern-atlas.json").read_text())
        self.assertEqual(report["status"], "corpus_mined_candidate_system_indexed_for_practice")
        self.assertEqual(report["coverage"]["full_context_reviews"], 395)
        self.assertEqual(report["discovery_layers"]["expanded_cards"], 33)
        self.assertEqual(report["discovery_layers"]["all_compound_bundles"], 136)
        self.assertEqual(report["discovery_layers"]["practice_compound_bundles"], 24)
        self.assertEqual(report["discovery_layers"]["all_compound_triads"], 160)
        self.assertEqual(report["discovery_layers"]["practice_compound_triads"], 24)
        self.assertEqual(report["discovery_layers"]["presentation_sequences"], 6)
        self.assertEqual(len(report["practice_surfaces"]), 6)
        self.assertIn("not", report["claim_boundary"])
        atlas_html = (ROOT / "writeups/presentation-pattern-atlas.html").read_text()
        self.assertIn("Presentation pattern atlas", atlas_html)
        self.assertIn("expanded-pattern-candidate-cards.html", atlas_html)
        self.assertIn("compound-pattern-triads.html", atlas_html)


if __name__ == "__main__":
    unittest.main()
