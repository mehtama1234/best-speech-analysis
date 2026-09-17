#!/usr/bin/env python3
"""OCR visible subtitles as an editorial-text witness, never as spoken words."""
import csv
import hashlib
import io
import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parents[1]
ROI = {'left': 0, 'top': 245, 'right': 640, 'bottom': 360}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_words(tsv, roi):
    words = []
    for row in csv.DictReader(io.StringIO(tsv), delimiter='\t'):
        if row.get('level') != '5' or not row.get('text', '').strip():
            continue
        try:
            left, top, width, height = (int(row[k]) for k in ['left', 'top', 'width', 'height'])
            confidence = float(row['conf'])
        except (ValueError, KeyError):
            continue
        if left < roi['left'] or top < roi['top'] or left + width > roi['right'] or top + height > roi['bottom']:
            continue
        words.append({'text': row['text'], 'left': left, 'top': top, 'width': width, 'height': height,
                      'ocr_confidence': confidence, 'line_key': [int(row[k]) for k in ['block_num', 'par_num', 'line_num']]})
    groups = defaultdict(list)
    for word in words:
        groups[tuple(word['line_key'])].append(word)
    lines = sorted(groups.values(), key=lambda group: (min(w['top'] for w in group), min(w['left'] for w in group)))
    ordered = [sorted(line, key=lambda word: word['left']) for line in lines]
    return {'words': [w for line in ordered for w in line],
            'text': '\n'.join(' '.join(w['text'] for w in line) for line in ordered)}


def main():
    runtime = ROOT / 'data/cache/ocr-runtime/root'
    executable = runtime / 'usr/bin/tesseract'
    trained = runtime / 'usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata'
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = str(runtime / 'usr/lib/x86_64-linux-gnu')
    env['OMP_THREAD_LIMIT'] = '1'
    manifest_path = ROOT / 'research/language-verification-frames.json'
    manifest = json.loads(manifest_path.read_text())
    inputs = [manifest_path, Path(__file__).resolve(), executable, trained]
    inputs.extend(runtime / ('usr/lib/x86_64-linux-gnu/' + name) for name in ['libtesseract.so.4', 'liblept.so.5'])
    inputs.extend(sorted((ROOT / 'data/cache/ocr-runtime/debs').glob('*.deb')))
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    report = {'schema_version': '1.0', 'video_id': manifest['video_id'], 'source_sha256': hashes,
              'modality': 'editorial_subtitle_ocr', 'roi_pixels': ROI, 'page_segmentation_mode': 6,
              'opencv_version': cv2.__version__,
              'preprocessing': 'Crop fixed subtitle rectangle in memory and upscale 2x with cubic interpolation before recognition. Store boxes mapped back to source frame coordinates. No source image modified.',
              'version': subprocess.run([str(executable), '--version'], env=env, check=True, capture_output=True, text=True).stdout.splitlines()[0],
              'frames': [], 'promoted_to_corpus': False,
              'limitations': 'Fixed layout-specific box chosen after inspecting these frames; not a held-out layout test. May omit clipped words or include unrelated overlays. Confidence is engine output, not calibrated correctness. Frame appearance time is not speech onset or subtitle duration. No listening or spoken-word verification.'}
    for frame in manifest['frames']:
        path = ROOT / frame['path']
        if digest(path) != frame['sha256']:
            raise ValueError('Frame bytes changed')
        result = subprocess.run([str(executable), str(path), 'stdout', '--tessdata-dir', str(trained.parent),
                                 '-l', 'eng', '--psm', '11', 'tsv'],
                                env=env, check=True, capture_output=True, text=True, timeout=30)
        baseline = select_words(result.stdout, ROI)
        pixels = cv2.imread(str(path))
        if pixels is None or pixels.shape[:2] != (360, 640):
            raise ValueError('Unexpected frame size for fixed ROI')
        crop = pixels[ROI['top']:ROI['bottom'], ROI['left']:ROI['right']]
        crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        ok, encoded = cv2.imencode('.png', crop)
        if not ok:
            raise ValueError('Could not encode analysis region')
        result = subprocess.run([str(executable), 'stdin', 'stdout', '--tessdata-dir', str(trained.parent),
                                 '-l', 'eng', '--psm', '6', 'tsv'], input=encoded.tobytes(),
                                env=env, check=True, capture_output=True, timeout=30)
        selected = select_words(result.stdout.decode(), {'left': 0, 'top': 0, 'right': crop.shape[1], 'bottom': crop.shape[0]})
        for word in selected['words']:
            word['left'] = ROI['left'] + word['left'] / 2
            word['top'] = ROI['top'] + word['top'] / 2
            word['width'] /= 2
            word['height'] /= 2
        row = {'frame_path': frame['path'], 'frame_sha256': frame['sha256'],
               'decoded_pts_seconds': frame['pts_seconds'], 'whole_frame_then_filter_baseline': baseline, **selected}
        report['frames'].append(row)
        print(json.dumps({'time': row['decoded_pts_seconds'], 'text': row['text']}), flush=True)
    (ROOT / 'research/subtitle-ocr-pilot.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
