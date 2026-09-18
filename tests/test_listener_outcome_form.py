import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ListenerOutcomeFormTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "writeups/listener-outcome-record.html").read_text()

    def test_form_has_consent_condition_tasks_and_boundary(self):
        for marker in ('name="consent"', 'name="condition"', 'response_main_point_recall', 'response_delayed_recall', 'listener-outcome-protocol'):
            self.assertIn(marker, self.page)
        self.assertIn("does not measure trust", self.page)

    def test_form_is_mobile_safe(self):
        self.assertIn('name="viewport"', self.page)


if __name__ == "__main__":
    unittest.main()
