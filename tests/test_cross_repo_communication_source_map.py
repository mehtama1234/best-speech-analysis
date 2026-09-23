import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "cross_repo_source_map", ROOT / "scripts/build_cross_repo_communication_source_map.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CrossRepoCommunicationSourceMapTest(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder()
        self.map_path = ROOT / "research/cross-repo-communication-source-map.json"
        self.writeup_path = ROOT / "writeups/cross-repo-communication-source-map.md"

    def test_map_is_current_and_keeps_source_types_separate(self):
        self.assertEqual(self.builder.main(), 0)
        source_map = json.loads(self.map_path.read_text())
        rows = {row["corpus_id"]: row for row in source_map["sources"]}
        self.assertEqual(source_map["summary"]["fixed_corpus_inventory_videos"], 480)
        self.assertEqual(source_map["summary"]["fixed_corpus_full_context_reviews"], 395)
        self.assertEqual(source_map["summary"]["external_source_corpora"], 14)
        self.assertEqual(source_map["summary"]["external_provisional_candidates"], 19)
        self.assertEqual(rows["ali-siddiq-wave-2"]["transcripts_available"], 202)
        self.assertEqual(rows["dry-bar-comedy-wave-2-starter"]["transcripts_available"], 37)
        self.assertEqual(rows["ted-wave-2-starter"]["transcripts_available"], 38)
        self.assertEqual(rows["stand-up-studios-wave-3-starter"]["transcripts_available"], 1)
        self.assertIn("Not included", rows["stand-up-studios-wave-3-starter"]["integration_state"])
        self.assertEqual(rows["ali-siddiq-wave-2"]["best_for"], "long stories, escalation, callbacks, and point of view")
        self.assertEqual(
            [chapter["number"] for chapter in rows["charisma-on-command-wave-1"]["companion_chapters"]],
            ["08", "09", "12"],
        )
        self.assertEqual(
            [chapter["number"] for chapter in rows["chad-littlefield-wave-1"]["companion_chapters"]],
            ["25"],
        )
        self.assertEqual(rows["chad-littlefield-wave-1"]["integration_state"], "Used directly in the companion guide.")
        self.assertEqual(source_map["summary"]["core_corpora_with_published_companion_chapters"], 10)
        text = self.writeup_path.read_text()
        self.assertIn("Do not add the two video counts together", text)
        self.assertIn("Comedy, coaching, and polished talks stay separate", text)
        self.assertIn("What to borrow from each kind of source", text)
        self.assertIn("## Where to start", text)
        self.assertIn("You need to handle a difficult conversation", text)
        self.assertIn("Published guide trail", text)
        self.assertIn("companion/speaking-practice.html#chapter-08", text)
        self.assertIn("companion/speaking-practice.html#chapter-25", text)


if __name__ == "__main__":
    unittest.main()
