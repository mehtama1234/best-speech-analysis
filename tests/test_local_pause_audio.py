import unittest
import numpy as np
from scripts.audit_local_pause_audio import energy_frames, low_energy_runs, boundary_distance


class LocalPauseAudioTests(unittest.TestCase):
    def test_known_quiet_interval(self):
        samples = np.concatenate([np.ones(16000) * .1, np.zeros(8000), np.ones(16000) * .1])
        runs = low_energy_runs(energy_frames(samples), -40)
        self.assertEqual(len(runs), 1)
        self.assertAlmostEqual(runs[0]["start_seconds"], 1)
        self.assertAlmostEqual(runs[0]["duration_seconds"], .5)
        self.assertFalse(runs[0]["left_window_censored"])
        self.assertFalse(runs[0]["right_window_censored"])

    def test_threshold_sensitivity_and_censoring(self):
        frames = energy_frames(np.ones(16000) * .005)
        self.assertEqual(low_energy_runs(frames, -50), [])
        run = low_energy_runs(frames, -40)[0]
        self.assertTrue(run["left_window_censored"])
        self.assertTrue(run["right_window_censored"])
        self.assertEqual(boundary_distance(run, .5), 0)
        self.assertEqual(boundary_distance(run, 2), 1)

    def test_missing_frames_not_bridged(self):
        frames = [{"start_seconds": 0, "end_seconds": .1, "rms_dbfs": -60},
                  {"start_seconds": .2, "end_seconds": .3, "rms_dbfs": -60}]
        self.assertEqual(low_energy_runs(frames, -40), [])

    def test_short_or_nonfinite_data_not_silence(self):
        self.assertEqual(energy_frames(np.zeros(10)), [])
        frames = [{"start_seconds": 0, "end_seconds": 1, "rms_dbfs": float("nan")}]
        self.assertEqual(low_energy_runs(frames, -40), [])
