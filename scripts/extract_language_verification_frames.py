#!/usr/bin/env python3
"""Prepare three source-bound frames for a recovered-language quality check."""
import hashlib
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg
from audit_pause_media_timeline import digest, first_frame_pts

ROOT = Path(__file__).resolve().parents[1]


def main():
    video = ROOT / 'data/video/05RW7gx-gG4.mp4'
    candidate = ROOT / 'data/transcript-recovery/05RW7gx-gG4-hi-1bf3c099302d.json'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    paths = [video, candidate, Path(__file__).resolve(), ROOT / 'scripts/audit_pause_media_timeline.py']
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    cache = ROOT / 'data/cache/language-verification' / hashes[str(video.relative_to(ROOT))][:16]
    cache.mkdir(parents=True, exist_ok=True)
    frames = []
    for time in [60, 100, 378]:
        result = subprocess.run([ffmpeg, '-hide_banner', '-copyts', '-ss', str(time), '-i', str(video),
                                 '-vf', 'showinfo', '-frames:v', '1', '-c:v', 'png', '-f', 'image2pipe', '-'],
                                capture_output=True, check=True, timeout=45)
        frame = cache / f'{time}.png'
        frame.write_bytes(result.stdout)
        frames.append({'requested_seek_seconds': time, **first_frame_pts(result.stderr.decode(errors='replace')),
                       'path': str(frame.relative_to(ROOT)), 'sha256': hashlib.sha256(result.stdout).hexdigest()})
    report = {'schema_version': '1.0', 'video_id': '05RW7gx-gG4', 'source_sha256': hashes,
              'candidate_path': str(candidate.relative_to(ROOT)), 'frames': frames,
              'selection': 'Purposive stills near previously inspected candidate material. Not continuous viewing, listening or a representative sample.',
              'acquisition': {'url': 'https://www.youtube.com/watch?v=05RW7gx-gG4', 'format_id': '396',
                              'date': '2026-09-17', 'video_only': True, 'new_audio_downloaded': False},
              'ffmpeg_version': subprocess.run([ffmpeg, '-version'], capture_output=True, check=True, text=True).stdout.splitlines()[0],
              'limitation': 'Visible subtitles are editorial evidence, not independently validated spoken words. Decoded video times do not prove recovered-caption or audio alignment.'}
    (ROOT / 'research/language-verification-frames.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(frames))


if __name__ == '__main__':
    main()
