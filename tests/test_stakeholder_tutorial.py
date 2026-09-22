import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WRITEUPS = ROOT / "writeups"


class StakeholderTutorialTest(unittest.TestCase):
    def test_markdown_tutorial_has_required_sections_and_local_links(self):
        path = WRITEUPS / "stakeholder-tutorial.md"
        text = path.read_text(encoding="utf-8")
        for heading in (
            "## What this is",
            "## What has been covered",
            "## The learner workflow",
            "## Verbal, vocal and nonverbal practice",
            "## Six useful starting patterns",
            "## Exact forms to study",
            "## One complete practice lesson",
            "## Evidence levels and boundaries",
            "## What external stakeholders can review",
            "## Sharing this tutorial",
        ):
            self.assertIn(heading, text)

        links = re.findall(r"\]\(([^)#]+)", text)
        for link in links:
            if "://" not in link and not link.startswith("mailto:"):
                self.assertTrue((WRITEUPS / link).is_file(), link)

    def test_html_tutorial_is_standalone_and_links_to_markdown(self):
        path = WRITEUPS / "stakeholder-tutorial.html"
        text = path.read_text(encoding="utf-8")
        self.assertIn("<!doctype html>", text.lower())
        self.assertIn('name="viewport"', text)
        self.assertIn('href="stakeholder-tutorial.md"', text)
        self.assertIn("Verbal, vocal and nonverbal practice", text)
        self.assertIn("Exact forms to study", text)
        self.assertIn("One complete practice lesson", text)
        self.assertIn("Language reconciliation", text)
        self.assertIn("Evidence levels and boundaries", text)


if __name__ == "__main__":
    unittest.main()
