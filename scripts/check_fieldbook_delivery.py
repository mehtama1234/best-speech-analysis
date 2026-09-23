#!/usr/bin/env python3
"""Check the extracted deliverable, not a second copy of the source generator."""
from pathlib import Path
from hashlib import sha256
import json
import re
import tempfile
import zipfile
import pymupdf
from playwright.sync_api import sync_playwright
from fieldbook_editorial_lessons import LESSONS
from fieldbook_core_chapters import JOB_CHAPTERS
from fieldbook_book_sections import INTRODUCTION, WORKED_PRESENTATION, CONCLUSION, COMPANION_GUIDE
from fieldbook_public_source_readings import PUBLIC_SOURCE_READINGS
from fieldbook_companion_crosswalk import COMPANION_CROSSWALK
from build_professional_pattern_fieldbook import (
    read_core_themes,
    read_subtheme_tables,
    read_video_passage_links,
)
from json import loads

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deliverables/speaking-patterns-fieldbook'


def norm(text):
    # PDF extraction inserts whitespace after line-ending hyphens/dashes.
    return re.sub(r'([—–-])\s+', r'\1', ' '.join(text.split()))


def main():
    catalog = json.loads((ROOT / 'research/presentation-pattern-playbook.json').read_text())['cards']
    core_themes = read_core_themes(catalog)
    subtheme_groups = read_subtheme_tables(catalog)
    source_video_links = read_video_passage_links()
    mapped = [key for chapter in JOB_CHAPTERS for key in chapter['pattern_ids']]
    assert len(mapped) == 55 and len(set(mapped)) == 55
    assert set(mapped) == {card['pattern_id'] for card in catalog}
    with tempfile.TemporaryDirectory(prefix='fieldbook-delivery-check-') as temporary:
        folder = Path(temporary)
        with zipfile.ZipFile(OUT / 'speaking-patterns-fieldbook.zip') as archive:
            for name in archive.namelist():
                target = (folder / name).resolve()
                assert target.is_relative_to(folder.resolve())
            archive.extractall(folder)
        manifest = json.loads((folder / 'manifest.json').read_text())
        readme_text = ' '.join((folder / 'README.md').read_text().split())
        for phrase in ['22 main themes', '18 smaller speaking moves', '15 more ideas', '395 videos', '480-video inventory', 'does not recheck all 395']:
            assert phrase in readme_text, phrase
        source_map = folder / 'writeups/cross-repo-communication-source-map.md'
        assert source_map.is_file()
        source_map_text = source_map.read_text()
        assert 'direct source trails for 10 of the ten core' in source_map_text
        assert 'Chad Littlefield Videos' in source_map_text
        assert 'companion/speaking-practice.html#chapter-08' in source_map_text
        source_map_json = folder / 'research/cross-repo-communication-source-map.json'
        assert source_map_json.is_file()
        source_map_data = json.loads(source_map_json.read_text())
        companion_sources = json.loads((folder / 'writeups/companion/sources.json').read_text())['sources']
        chad_sources = [row for row in companion_sources if row['channel'] == 'Chad Littlefield']
        assert len(chad_sources) == 1 and chad_sources[0]['chapters'] == ['25']
        companion_chapters = {}
        for row in companion_sources:
            companion_chapters.setdefault(row['channel'], set()).update(row['chapters'])
        source_channel_aliases = {
            'Communication Coach Alexander Lyon Videos': 'Alexander Lyon Communication Coach',
        }
        for row in source_map_data['sources']:
            if not row['corpus_id'].endswith('wave-1'):
                continue
            channel = source_channel_aliases.get(row['source'], row['source'].removesuffix(' Videos'))
            expected = {chapter['number'] for chapter in row['companion_chapters']}
            assert expected, f"Missing published guide trail for {row['source']}"
            assert expected <= companion_chapters.get(channel, set()), (
                f"Bundled source index does not match map for {row['source']}"
            )
        for name, digest in manifest.items():
            assert sha256((folder / name).read_bytes()).hexdigest() == digest
            assert (folder / name).read_bytes() == (ROOT / name).read_bytes(), f'Stale bundle: {name}'
        with pymupdf.open(folder / 'speaking-patterns-fieldbook.pdf') as document:
            pdf_text = norm(' '.join(page.get_text(clip=pymupdf.Rect(0, 0, page.rect.width, page.rect.height - 35)) for page in document))
            for chapter in JOB_CHAPTERS:
                assert norm(chapter['title']) in pdf_text
                assert norm(chapter['check']) in pdf_text
            for title, _ in INTRODUCTION + WORKED_PRESENTATION + CONCLUSION + COMPANION_GUIDE:
                assert norm(title) in pdf_text
            assert 'All 27 approaches: where they connect' in pdf_text
            assert '22 broad themes' in pdf_text
            assert '33 smaller patterns' in pdf_text
            for theme in core_themes:
                assert norm(theme['title']) in pdf_text
                assert norm(theme['form']) in pdf_text
                assert norm(theme['use']) in pdf_text
            for _, entries in subtheme_groups:
                for item in entries:
                    assert norm(item['title']) in pdf_text
                    assert norm(item['when']) in pdf_text
                    assert norm(item['how']) in pdf_text
            for number, title, fit, pattern_ids, reason in COMPANION_CROSSWALK:
                assert norm(f'{number:02d}. {title} — {fit}') in pdf_text
                assert norm(reason) in pdf_text
            for card in catalog:
                lesson = LESSONS[card['pattern_id']]
                assert norm(lesson['title']) in pdf_text
                for field in ['worked_title', 'before', 'after', 'worked_explanation', 'transfer', 'exercise', 'self_check', 'failure_case']:
                    assert norm(lesson[field]) in pdf_text, (lesson['title'], field)
                for variation in lesson['variations']:
                    assert norm(variation) in pdf_text, (lesson['title'], variation)
            for paragraphs in PUBLIC_SOURCE_READINGS.values():
                for paragraph in paragraphs:
                    assert norm(paragraph) in pdf_text
            pdf_uris = {
                link.get('uri')
                for page in document
                for link in page.get_links()
                if link.get('uri')
            }
            expected_video_uris = {
                link['url']
                for anchors in source_video_links.values()
                for link in anchors
            }
            assert expected_video_uris <= pdf_uris
            pdf_pages = len(document)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            network = []
            errors = []
            page.on('request', lambda request: network.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto((folder / 'writeups/speaking-patterns-fieldbook.html').as_uri())
            assert page.locator('.job-chapter').count() == len(JOB_CHAPTERS)
            assert page.locator('.card').count() == 55
            assert page.locator('#companion-crosswalk').count() == 1
            assert page.locator('#core-themes .theme-item').count() == 22
            assert page.locator('#subthemes .theme-item').count() == 55 - 22
            for theme in core_themes:
                assert page.locator(f'#core-themes a[href="#pattern-{theme["pattern_id"]}"]').count() == 1
            for _, entries in subtheme_groups:
                for item in entries:
                    assert page.locator(f'#subthemes a[href="#pattern-{item["pattern_id"]}"]').count() == 1
            for _, _, _, pattern_ids, _ in COMPANION_CROSSWALK:
                for pattern_id in pattern_ids:
                    assert page.locator(f'a[href="#pattern-{pattern_id}"]').count() >= 1
                    assert page.locator(f'#pattern-{pattern_id}').count() == 1
            for link in page.locator('a[href]').evaluate_all('(nodes)=>nodes.map(a=>a.getAttribute("href"))'):
                if link.startswith('#'):
                    assert page.locator(link).count() == 1, link
                elif not link.startswith(('http:', 'https:')):
                    local_path = link.split('#', 1)[0]
                    assert (folder / 'writeups' / local_path).resolve().is_file(), link
            for width in [320, 390, 768, 1280]:
                page.set_viewport_size({'width':width, 'height':900})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
            page.locator('.card button').first.focus()
            page.keyboard.press('Enter')
            assert page.locator('#move-dialog').is_visible()
            assert page.evaluate('document.getElementById("move-dialog").contains(document.activeElement)')
            assert page.locator('#move-content a[href^="https://www.youtube.com/watch?v="]').count() > 0
            page.keyboard.press('Escape')
            assert not page.locator('#move-dialog').is_visible()
            assert page.locator('.card button').first.evaluate('(button)=>button===document.activeElement')
            assert not network and not errors, (network, errors)
            companion = browser.new_page()
            companion_errors = []
            companion.on('pageerror', lambda error: companion_errors.append(str(error)))
            companion.goto((folder / 'writeups/companion/speaking-practice.html').as_uri())
            assert companion.locator('article.approach').count() == 27
            assert companion.locator('article.learning-path').count() == 11
            for number in range(1, 28):
                assert companion.locator(f'#chapter-{number:02d}').count() == 1
            assert 'Chad Littlefield' in companion.locator('#chapter-25').inner_text()
            assert companion.locator('#source-zChjPuhdgHs').count() == 1
            assert not companion_errors, companion_errors
            context = browser.new_context(java_script_enabled=False)
            static = context.new_page()
            static.goto((folder / 'writeups/speaking-patterns-fieldbook.html').as_uri())
            assert static.locator('.job-chapter').count() == len(JOB_CHAPTERS)
            assert 'The revised presentation' in static.locator('#worked-presentation').inner_text()
            browser.close()
    result = {'status':'delivery_checks_passed', 'speaking_job_chapters':len(JOB_CHAPTERS), 'research_index_entries':55, 'broad_themes':len(core_themes), 'smaller_patterns':sum(len(entries) for _, entries in subtheme_groups), 'source_video_links':sum(len(links) for links in source_video_links.values()), 'worked_examples':len(LESSONS), 'companion_approaches':len(COMPANION_CROSSWALK), 'pdf_pages':pdf_pages,
              'pdf_content_checked':'All 7 chapters, 22 broad themes, 33 smaller patterns, 55 worked entries, source summaries, full practice presentation and 27 companion links',
              'extracted_bundle_matches_sources':True, 'local_links_resolve':True,
              'offline_network_requests':0, 'javascript_errors':0,
              'tested_viewport_widths':[320,390,768,1280],
              'keyboard_dialog_and_focus_return':True, 'chapters_readable_without_javascript':True,
              'boundary':'Content preservation and functional checks, not independent source verification, legal clearance or measured teaching effectiveness.'}
    (OUT / 'delivery-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
