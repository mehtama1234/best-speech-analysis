import unittest

from scripts.validate_autonomous_web_surface_integrity import validate


class AutonomousWebSurfaceIntegrityTest(unittest.TestCase):
    def test_web_surfaces_expose_all_jobs_and_resolve_local_links(self):
        self.assertEqual(validate(), [])

    def test_listener_auxiliary_surfaces_are_in_static_audit(self):
        from scripts.validate_autonomous_web_surface_integrity import AUXILIARY_SURFACES

        self.assertEqual(len(AUXILIARY_SURFACES), 3)
        self.assertIn("writeups/communication-job-listener-record.html", AUXILIARY_SURFACES)


if __name__ == "__main__":
    unittest.main()
