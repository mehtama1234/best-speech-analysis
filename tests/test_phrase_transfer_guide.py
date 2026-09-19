import unittest
from pathlib import Path

from scripts.build_phrase_transfer_guide import main


ROOT = Path(__file__).resolve().parents[1]


class PhraseTransferGuideTests(unittest.TestCase):
    def test_all_inventory_forms_have_transfer_context(self):
        main()
        text = (ROOT / "writeups/phrase-transfer-guide.md").read_text()
        self.assertIn("50 exact transcript forms", text)
        self.assertIn("Transfer drill", text)
        self.assertEqual(sum(line.startswith("| `") for line in text.splitlines()), 50)
        self.assertIn("what it does not mean", text)


if __name__ == "__main__":
    unittest.main()
