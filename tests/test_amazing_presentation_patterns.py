import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AmazingPresentationPatternTests(unittest.TestCase):
    def test_browser_contains_every_inventory_pattern(self):
        inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
        evidence = json.loads((ROOT / "research/all-55-pattern-evidence.json").read_text()).get("patterns", [])
        candidates = json.loads((ROOT / "research/recovered-pattern-candidate-cards.json").read_text()).get("cards", [])
        page = (ROOT / "writeups/amazing-presentation-patterns.html").read_text()
        guide = (ROOT / "writeups/amazing-presentation-patterns.md").read_text()
        expected = inventory["theme_count"] + inventory["relation_pattern_count"] + inventory["unmatched_cluster_count"]
        self.assertEqual(expected, 55)
        inventory_ids = {
            item[key]
            for collection, key in (("themes", "theme_id"), ("relation_patterns", "relation_type"), ("unmatched_clusters", "cluster_id"))
            for item in inventory[collection]
        }
        self.assertEqual({row["pattern_id"] for row in evidence}, inventory_ids)
        self.assertEqual({row["pattern_id"] for row in candidates}, inventory_ids)
        self.assertEqual(len(candidates), 2431)
        allowed_unvalidated = {
            "not_human_reviewed",
            "identity_and_content_not_verified",
            "source_identity_and_alignment_not_human_verified",
        }
        self.assertTrue(all(row.get("source_review_status") in allowed_unvalidated for row in candidates))
        self.assertIn('"category": "core theme"', page)
        self.assertIn('"category": "structural subtheme"', page)
        self.assertIn('"category": "additional subtheme"', page)
        for collection, key in (("themes", "theme_id"), ("relation_patterns", "relation_type"), ("unmatched_clusters", "cluster_id")):
            for item in inventory[collection]:
                self.assertIn(item[key], page)
        self.assertEqual(len(re.findall(r"^### \d+\. ", guide, flags=re.MULTILINE)), 22)
        for item in inventory["relation_patterns"] + inventory["unmatched_clusters"]:
            pattern_id = item.get("relation_type") or item.get("cluster_id")
            self.assertIn(f"`{pattern_id}`", guide)
        for row in evidence:
            self.assertTrue(row["example_writeup"])
            self.assertTrue(row["example_evidence_ids"])
            self.assertIn(row["example_writeup"], guide)
        self.assertIn("How to use:", page)
        self.assertIn("source anchor", page)
        self.assertIn("Download local worksheet", page)
        self.assertIn("downloadWorksheet", page)
        self.assertIn("Desired outcome", page)
        self.assertIn("direct recovery candidates", page)
        self.assertIn("recovered-pattern-candidate-cards.md", page)
        self.assertIn("recovered-pattern-independent-review.html", page)

    def test_written_guide_has_no_patch_marker_headings(self):
        guide = (ROOT / "writeups/amazing-presentation-patterns.md").read_text()
        self.assertFalse(any(line.startswith("+") for line in guide.splitlines()))


if __name__ == "__main__":
    unittest.main()
