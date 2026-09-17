#!/usr/bin/env python3
"""Bind decoded frame times to reviewed pixels; do not infer audiovisual sync."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_metadata(log):
    log = log.split('Output #', 1)[0]
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+), start: (-?[\d.]+)', log)
    streams = [line.strip() for line in log.splitlines()
               if re.search(r'Stream #0:\d+.*: (Audio|Video):', line)]
    return {
        'duration_seconds': (3600 * int(duration[1]) + 60 * int(duration[2]) + float(duration[3])) if duration else None,
        'container_start_seconds': float(duration[4]) if duration else None,
        'stream_descriptions': streams,
        'has_audio': any(': Audio:' in line for line in streams),
        'has_video': any(': Video:' in line for line in streams),
    }


def first_frame_pts(log):
    matches = re.findall(r'\bn:\s*0\s+pts:\s*(-?\d+)\s+pts_time:\s*(-?[\d.eE+]+)', log)
    if len(matches) != 1:
        raise ValueError('Expected one first decoded frame timestamp')
    result = {'pts': int(matches[0][0]), 'pts_seconds': float(matches[0][1])}
    timebase = re.search(r'config in time_base: (\d+)/(\d+)', log)
    if timebase:
        result['time_base_numerator'] = int(timebase[1])
        result['time_base_denominator'] = int(timebase[2])
    return result


def main():
    root = Path(__file__).resolve().parents[1]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    manifest_path = root / 'research/pause-visual-probes.json'
    manifest = json.loads(manifest_path.read_text())
    hashes = {str(p.relative_to(root)): digest(p) for p in (manifest_path, Path(__file__).resolve())}
    report = {
        'schema_version': '1.0',
        'method': 'Re-decode each requested seek with -copyts, showinfo and one PNG to stdout. Bind first frame PTS to prior review only when PNG bytes have the same SHA256. Container metadata is displayed rounded by ffmpeg; it is not precise packet timing.',
        'ffmpeg_version': subprocess.run([ffmpeg, '-version'], check=True, capture_output=True, text=True).stdout.splitlines()[0],
        'source_sha256': hashes,
        'audio_video_sync_verified': False,
        'limitation': 'Matching container starts and similar durations do not establish content synchronization, local offset, drift, lip synchronization or transcript alignment. Video-only sources provide no common audio waveform for direct correlation. No listening or continuous viewing performed.',
        'examples': [],
    }
    for probe in manifest['probes']:
        video_id = probe['evidence_id'].split(':')[0]
        video = root / probe['video_path']
        audio = root / 'data/audio' / (video_id + '.m4a')
        row = {'evidence_id': probe['evidence_id'], 'streams': {}, 'frames': []}
        for kind, path in [('audio', audio), ('video', video)]:
            if not path.exists():
                row['streams'][kind] = {'error': 'local_source_missing'}
                continue
            hashes[str(path.relative_to(root))] = digest(path)
            result = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path), '-t', '0', '-f', 'null', '-'],
                                    capture_output=True, timeout=45)
            if result.returncode:
                row['streams'][kind] = {'error': 'metadata_decode_failed', 'returncode': result.returncode}
                continue
            row['streams'][kind] = parse_metadata(result.stderr.decode(errors='replace'))
        if video.exists():
            for frame in probe['frames']:
                item = {'requested_seek_seconds': frame['requested_seek_seconds'], 'reviewed_png_sha256': frame.get('sha256')}
                result = subprocess.run([ffmpeg, '-hide_banner', '-copyts', '-ss', str(frame['requested_seek_seconds']),
                                         '-i', str(video), '-vf', 'showinfo', '-frames:v', '1',
                                         '-c:v', 'png', '-f', 'image2pipe', '-'], capture_output=True, timeout=45)
                if result.returncode or not result.stdout:
                    item['error'] = 'frame_decode_failed'
                else:
                    item.update(first_frame_pts(result.stderr.decode(errors='replace')))
                    item['redecoded_png_sha256'] = hashlib.sha256(result.stdout).hexdigest()
                    item['matches_reviewed_pixels'] = item['redecoded_png_sha256'] == item['reviewed_png_sha256']
                    item['pts_minus_requested_seconds'] = round(item['pts_seconds'] - item['requested_seek_seconds'], 9)
                    item['reviewed_frame_pts_status'] = 'verified_by_identical_png' if item['matches_reviewed_pixels'] else 'not_bound_to_reviewed_pixels'
                row['frames'].append(item)
        report['examples'].append(row)
        print(json.dumps(row), flush=True)
    (root / 'research/pause-media-timeline-audit.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
