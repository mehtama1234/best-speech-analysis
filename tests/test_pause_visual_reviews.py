import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


class PauseVisualReviewTests(unittest.TestCase):
    def test_review_binds_exact_probe_and_measurements(self):
        review = json.loads((ROOT / 'research/pause-visual-reviews.json').read_text())
        manifest_path = ROOT / review['probe_manifest']
        self.assertEqual(digest(manifest_path), review['probe_manifest_sha256'])
        manifest = json.loads(manifest_path.read_text())
        probes = {p['evidence_id']: p for p in manifest['probes']}
        self.assertEqual(len(review['reviews']), 3)
        self.assertEqual({r['evidence_id'] for r in review['reviews']}, set(probes))
        self.assertFalse(review['listened_to_audio'])
        self.assertFalse(review['watched_continuous_video'])
        self.assertFalse(review['audio_video_sync_verified'])
        for row in review['reviews']:
            probe = probes[row['evidence_id']]
            self.assertEqual([f['requested_seek_seconds'] for f in row['frames']],
                             [f['requested_seek_seconds'] for f in probe['frames']])
            self.assertEqual(len(row['frames']), 3)
            self.assertTrue(all(f['observation'] for f in row['frames']))
            self.assertEqual(row['rhetorical_pause_status'], 'unresolved')
            self.assertIn(row['quiet_interval_seconds'],
                          [[r['start_seconds'], r['end_seconds']]
                           for r in probe['quiet_runs_minus40_dbfs']])
        # Tracked inputs must always be present; ignored media may be absent on a clone.
        for path, expected in manifest['source_sha256'].items():
            if path.startswith('data/video/') and not (ROOT / path).exists():
                continue
            self.assertEqual(digest(ROOT / path), expected, path)

    def test_cached_frame_bytes_when_available(self):
        manifest = json.loads((ROOT / 'research/pause-visual-probes.json').read_text())
        frames = [f for p in manifest['probes'] for f in p['frames']]
        self.assertEqual(len(frames), 9)
        available = [f for f in frames if (ROOT / f['path']).exists()]
        if not available:
            self.skipTest('Ignored frame cache not available; no local pixel verification')
        for frame in available:
            self.assertEqual(digest(ROOT / frame['path']), frame['sha256'], frame['path'])
