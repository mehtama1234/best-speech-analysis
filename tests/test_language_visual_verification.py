import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


class LanguageVisualVerificationTests(unittest.TestCase):
    def test_observations_bind_frames_and_candidate(self):
        review = json.loads((ROOT / 'research/language-visual-verification.json').read_text())
        for path_field, hash_field in [('candidate_path', 'candidate_sha256'),
                                      ('frame_manifest_path', 'frame_manifest_sha256'),
                                      ('prior_quality_review_path', 'prior_quality_review_sha256')]:
            self.assertEqual(digest(ROOT / review[path_field]), review[hash_field])
        manifest = json.loads((ROOT / review['frame_manifest_path']).read_text())
        candidate = json.loads((ROOT / review['candidate_path']).read_text())
        frames = {f['requested_seek_seconds']: f for f in manifest['frames']}
        self.assertEqual(len(review['frame_observations']), len(frames))
        for observation in review['frame_observations']:
            frame = frames[observation['requested_seek_seconds']]
            self.assertEqual(observation['decoded_pts_seconds'], frame['pts_seconds'])
            self.assertTrue(all(0 <= i < len(candidate['transcript']) for i in observation['comparison_candidate_ordinals']))
        self.assertFalse(review['promoted_to_corpus'])
        self.assertFalse(review['listened_to_audio'])
        self.assertFalse(review['caption_time_alignment_validated'])
        for path, expected in manifest['source_sha256'].items():
            if path.startswith('data/video/') and not (ROOT / path).exists():
                continue
            self.assertEqual(digest(ROOT / path), expected)

    def test_local_frame_bytes_when_present(self):
        manifest = json.loads((ROOT / 'research/language-verification-frames.json').read_text())
        available = [f for f in manifest['frames'] if (ROOT / f['path']).exists()]
        if not available:
            self.skipTest('Ignored frame cache unavailable')
        for frame in available:
            self.assertEqual(digest(ROOT / frame['path']), frame['sha256'])
