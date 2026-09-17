#!/usr/bin/env python3
"""Optional real-browser playback smoke test; never a semantic audiovisual review."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

if __package__:
    from .serve_pause_review import handler
    from .build_pause_review_browser import digest
else:
    from serve_pause_review import handler
    from build_pause_review_browser import digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    report = {'purpose': 'Automated UI and media decoding checks, not listening, comprehension, alignment validation or independent review.', 'checks': []}
    inputs = ['writeups/pause-review-browser.html', 'research/pause-review-packet.json',
              'scripts/serve_pause_review.py', 'scripts/check_pause_review_browser.py']
    report['source_sha256'] = {path: digest(ROOT / path) for path in inputs}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            report['browser_version'] = browser.version
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            count = page.locator('#case option').count()
            assert count == 7, count
            for index in range(count):
                page.select_option('#case', str(index))
                page.wait_for_function("document.querySelector('#player').readyState >= 2", timeout=45000)
                page.click('#target')
                page.wait_for_function("!document.querySelector('#player').seeking")
                before = page.locator('#player').evaluate('(v)=>v.currentTime')
                page.locator('#player').evaluate('(v)=>{v.muted=true; return v.play();}')
                page.wait_for_function('(t)=>document.querySelector("#player").currentTime > t + 0.4', arg=before)
                page.locator('#player').evaluate('(v)=>v.pause()')
                result = page.locator('#player').evaluate('(v)=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,decodedAudioBytes:v.webkitAudioDecodedByteCount??null})')
                assert result['width'] > 0 and result['height'] > 0
                result['evidence_id'] = page.locator('#case option:checked').text_content()
                result['seek_and_play_advanced'] = True
                report['checks'].append(result)
            page.fill('#notes', 'Automated smoke-test draft, not a research observation.')
            page.reload()
            # Reload selects first case; the last-case draft remains isolated.
            assert page.input_value('#notes') == ''
            page.select_option('#case', '6')
            assert page.input_value('#notes').startswith('Automated smoke-test')
            with page.expect_download() as info:
                page.click('#export')
            exported = json.loads(Path(info.value.path()).read_text())
            assert exported['status'] == 'unadjudicated_draft'
            assert exported['watched'] is False and exported['listened'] is False
            assert exported['alignment_status'] == 'not_verified_by_application'
            report['isolated_draft_persistence_and_export'] = True
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            report['mobile_no_horizontal_overflow'] = True
            assert not errors, errors
            report['javascript_errors'] = errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    (ROOT / 'research/pause-browser-smoke-test.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
