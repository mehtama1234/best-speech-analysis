#!/usr/bin/env python3
"""Build an audiovisual review packet; muxing is not synchronization validation."""
import hashlib
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    inputs = ['research/local-pause-audio-audit.json', 'research/pause-visual-reviews.json',
              'research/pause-media-timeline-audit.json', 'research/segment-registry.jsonl',
              'scripts/build_pause_review_browser.py', 'templates/pause-review.html']
    hashes = {p: digest(ROOT / p) for p in inputs}
    audit = json.loads((ROOT / inputs[0]).read_text())
    visuals = {r['evidence_id']: r for r in json.loads((ROOT / inputs[1]).read_text())['reviews']}
    timeline = {r['evidence_id']: r for r in json.loads((ROOT / inputs[2]).read_text())['examples']}
    wanted = {r['source']['video_id'] for r in audit['examples']}
    transcripts = {v: [] for v in wanted}
    for line in (ROOT / inputs[3]).open():
        row = json.loads(line)
        if row['video_id'] in wanted:
            transcripts[row['video_id']].append(row)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    version = subprocess.run([ffmpeg, '-version'], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    rows = []
    for example in audit['examples']:
        source = example['source']
        vid = source['video_id']
        start, end = max(0, source['start_seconds'] - 8), source['end_seconds'] + 8
        video, audio = ROOT / f'data/video/{vid}.mp4', ROOT / f'data/audio/{vid}.m4a'
        row = {'evidence_id': example['evidence_id'], 'title': source.get('title', vid),
               'start_seconds': start, 'end_seconds': end, 'target': source,
               'alignment': 'Unverified: both source streams trimmed at the same requested time; no offset estimated or applied.',
               'quiet_runs': example['threshold_runs'], 'legacy_status': 'Unresolved; historical support is not adjudication.',
               'visual_review': visuals.get(example['evidence_id']), 'frame_timeline': timeline.get(example['evidence_id']),
               'context': [r for r in transcripts[vid] if r['end_seconds'] >= start and r['start_seconds'] <= end]}
        if not video.exists() or not audio.exists():
            row['media_error'] = 'Local audio or video missing'
        else:
            for path in (video, audio):
                key = str(path.relative_to(ROOT))
                if key not in hashes:
                    hashes[key] = digest(path)
            recipe = {'video': hashes[str(video.relative_to(ROOT))], 'audio': hashes[str(audio.relative_to(ROOT))],
                      'start': start, 'end': end, 'decoder': version, 'recipe_version': 1}
            cache_id = hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest()[:20]
            output = ROOT / f'data/cache/pause-review-clips/{cache_id}.webm'
            output.parent.mkdir(parents=True, exist_ok=True)
            if not output.exists():
                partial = output.with_suffix('.partial.webm')
                command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
                           '-ss', str(start), '-i', str(video), '-ss', str(start), '-i', str(audio),
                           '-t', str(end - start), '-map', '0:v:0', '-map', '1:a:0',
                           '-c:v', 'libvpx-vp9', '-deadline', 'realtime', '-cpu-used', '8', '-b:v', '350k',
                           '-c:a', 'libopus', '-b:a', '64k', str(partial)]
                try:
                    subprocess.run(command, check=True, capture_output=True, timeout=120)
                    partial.replace(output)
                except subprocess.SubprocessError as exc:
                    row['media_error'] = type(exc).__name__
            if output.exists():
                row['clip'] = {'path': str(output.relative_to(ROOT)), 'sha256': digest(output),
                               'recipe': recipe, 'time_mapping': 'Approximate original time = player time + requested trim start; encoded timing/AV sync not independently validated.'}
        rows.append(row)
        print(row['evidence_id'], row.get('media_error', 'clip ready'), flush=True)
    packet = {'schema_version': '1.0', 'source_sha256': hashes, 'examples': rows,
              'review_status': 'Prepared for continuous review; no listening or viewing is asserted by generation.'}
    (ROOT / 'research/pause-review-packet.json').write_text(json.dumps(packet, indent=2) + '\n')
    payload = json.dumps(packet, ensure_ascii=False).replace('<', '\\u003c')
    template = (ROOT / 'templates/pause-review.html').read_text()
    (ROOT / 'writeups/pause-review-browser.html').write_text(template.replace('__PACKET_JSON__', payload))


if __name__ == '__main__':
    main()
