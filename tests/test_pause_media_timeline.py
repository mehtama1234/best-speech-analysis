import json
import unittest
from pathlib import Path
from scripts.audit_pause_media_timeline import parse_metadata, first_frame_pts, digest


class PauseTimelineTests(unittest.TestCase):
    def test_streams_and_rounding(self):
        row = parse_metadata('Duration: 01:02:03.45, start: -0.020000, bitrate: 60 kb/s\n'
                             ' Stream #0:0[0x1](und): Video: av1\n'
                             'Output #0, null\n Stream #0:0: Audio: synthetic\n')
        self.assertAlmostEqual(row['duration_seconds'], 3723.45)
        self.assertEqual(row['container_start_seconds'], -0.02)
        self.assertTrue(row['has_video'])
        self.assertFalse(row['has_audio'])
        self.assertIsNone(parse_metadata('Duration: N/A')['duration_seconds'])

    def test_pts_not_requested_seek(self):
        row = first_frame_pts('[showinfo] n: 0 pts:2025984 pts_time:131.9 duration:512')
        self.assertEqual(row, {'pts': 2025984, 'pts_seconds': 131.9})
        exact = first_frame_pts('config in time_base: 1/15360\nn: 0 pts:2025984 pts_time:131.9')
        self.assertEqual(exact['time_base_denominator'], 15360)
        with self.assertRaises(ValueError):
            first_frame_pts('no decoded timestamp')

    def test_saved_pixel_binding_and_provenance(self):
        root = Path(__file__).resolve().parents[1]
        report = json.loads((root / 'research/pause-media-timeline-audit.json').read_text())
        self.assertFalse(report['audio_video_sync_verified'])
        manifest = json.loads((root / 'research/pause-visual-probes.json').read_text())
        probes = {p['evidence_id']: p for p in manifest['probes']}
        self.assertEqual({r['evidence_id'] for r in report['examples']}, set(probes))
        for path, expected in report['source_sha256'].items():
            if path.startswith(('data/audio/', 'data/video/')) and not (root / path).exists():
                continue
            self.assertEqual(digest(root / path), expected, path)
        for example in report['examples']:
            expected_frames = probes[example['evidence_id']]['frames']
            self.assertEqual(len(example['frames']), len(expected_frames))
            for frame, original in zip(example['frames'], expected_frames):
                self.assertEqual(frame['requested_seek_seconds'], original['requested_seek_seconds'])
                self.assertEqual(frame['reviewed_png_sha256'], original['sha256'])
                if 'error' in frame:
                    continue
                self.assertEqual(frame['matches_reviewed_pixels'], frame['redecoded_png_sha256'] == original['sha256'])
                self.assertAlmostEqual(frame['pts_minus_requested_seconds'], frame['pts_seconds'] - frame['requested_seek_seconds'])
