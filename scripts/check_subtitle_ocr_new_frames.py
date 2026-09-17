#!/usr/bin/env python3
"""Apply frozen subtitle OCR to eight declared new-frame probes."""
import json
import os
import subprocess
from pathlib import Path
import cv2
import imageio_ffmpeg
from ocr_language_verification_frames import select_words, digest, ROI
from audit_pause_media_timeline import first_frame_pts

ROOT = Path(__file__).resolve().parents[1]
TIMES = [0, 20, 160, 300, 440, 580, 720, 843]
FROZEN_SCRIPT_HASH = '6a13d96dd684fa40a4ca48c2f52ca5d9906e4d6c6071c0407dce60edb019afd3'


def main():
    helper = ROOT / 'scripts/ocr_language_verification_frames.py'
    if digest(helper) != FROZEN_SCRIPT_HASH:
        raise ValueError('Frozen pilot implementation changed')
    pilot_path = ROOT / 'research/subtitle-ocr-pilot.json'
    pilot = json.loads(pilot_path.read_text())
    for path, expected in pilot['source_sha256'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('Pilot input changed: ' + path)
    if cv2.__version__ != pilot['opencv_version']:
        raise ValueError('OpenCV version changed')
    video = ROOT / 'data/video/05RW7gx-gG4.mp4'
    runtime = ROOT / 'data/cache/ocr-runtime/root'
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = str(runtime / 'usr/lib/x86_64-linux-gnu')
    env['OMP_THREAD_LIMIT'] = '1'
    cache = ROOT / 'data/cache/subtitle-ocr-new-frames' / digest(video)[:16]
    cache.mkdir(parents=True, exist_ok=True)
    paths = [video, pilot_path, helper, Path(__file__).resolve(), ROOT / 'scripts/audit_pause_media_timeline.py']
    report = {'schema_version': '1.0', 'video_id': '05RW7gx-gG4', 'requested_times': TIMES,
              'selection': 'Six fixed-spaced interior timestamps (20 through 720 every 140 seconds), plus opening 0 and ending 843. Declared before viewing or OCR. Same upload as pilot, not random or independent review.',
              'frozen_pilot_sha256': FROZEN_SCRIPT_HASH, 'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in paths},
              'roi_pixels': ROI, 'page_segmentation_mode': 6, 'scale_factor': 2,
              'modality': 'editorial_subtitle_ocr', 'promoted_to_corpus': False, 'frames': []}
    for time in TIMES:
        result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-copyts', '-ss', str(time),
                                 '-i', str(video), '-vf', 'showinfo', '-frames:v', '1', '-c:v', 'png', '-f', 'image2pipe', '-'],
                                check=True, capture_output=True, timeout=45)
        frame = cache / f'{time}.png'
        frame.write_bytes(result.stdout)
        pixels = cv2.imread(str(frame))
        if pixels is None or pixels.shape[:2] != (360, 640):
            raise ValueError('Unexpected frame geometry')
        crop = cv2.resize(pixels[ROI['top']:ROI['bottom'], ROI['left']:ROI['right']], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        ok, png = cv2.imencode('.png', crop)
        if not ok:
            raise ValueError('Could not encode ROI')
        output = subprocess.run([str(runtime / 'usr/bin/tesseract'), 'stdin', 'stdout', '--tessdata-dir',
                                 str(runtime / 'usr/share/tesseract-ocr/4.00/tessdata'), '-l', 'eng', '--psm', '6', 'tsv'],
                                input=png.tobytes(), check=True, capture_output=True, env=env, timeout=30)
        selected = select_words(output.stdout.decode(), {'left': 0, 'top': 0, 'right': crop.shape[1], 'bottom': crop.shape[0]})
        for word in selected['words']:
            word['left'] = ROI['left'] + word['left'] / 2
            word['top'] = ROI['top'] + word['top'] / 2
            word['width'] /= 2
            word['height'] /= 2
        row = {'requested_seek_seconds': time, **first_frame_pts(result.stderr.decode(errors='replace')),
               'frame_path': str(frame.relative_to(ROOT)), 'frame_sha256': digest(frame), **selected}
        report['frames'].append(row)
        print(json.dumps({'time': time, 'frame': row['frame_path'], 'text': row['text']}), flush=True)
    (ROOT / 'research/subtitle-ocr-new-frames.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
