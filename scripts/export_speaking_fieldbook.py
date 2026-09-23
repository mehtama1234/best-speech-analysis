#!/usr/bin/env python3
"""Export and inspect a portable fieldbook PDF and source-linked reading bundle."""
from pathlib import Path
from hashlib import sha256
import json
import re
import shutil
import tempfile
import zipfile

import pymupdf as fitz
from playwright.sync_api import sync_playwright
from fieldbook_editorial_lessons import LESSONS
from fieldbook_core_chapters import JOB_CHAPTERS
from fieldbook_book_sections import INTRODUCTION, WORKED_PRESENTATION, CONCLUSION, COMPANION_GUIDE
from fieldbook_companion_crosswalk import COMPANION_CROSSWALK
from fieldbook_public_source_readings import PUBLIC_SOURCE_READINGS
from build_professional_pattern_fieldbook import (
    read_core_themes,
    read_subtheme_tables,
    read_video_passage_links,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deliverables/speaking-patterns-fieldbook'
COMPANION_SOURCE = ROOT.parent / 'speaking-humor-and-communication-concepts-research' / 'deliverables/speaking-practice'
COMPANION_COPY = ROOT / 'writeups/companion'


def norm(text):
    """Normalize PDF line wrapping and end-of-line hyphenation for comparisons."""
    text = re.sub(r'\[([^\]]+)\]\((?:https?://[^)\s]+|#[A-Za-z0-9_-]+|[A-Za-z0-9._/-]+\.(?:html|pdf|zip)(?:#[A-Za-z0-9_-]+)?)\)', r'\1', text)
    return re.sub(r'([—–-])\s+', r'\1', ' '.join(text.split()))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((ROOT / 'research/presentation-pattern-playbook.json').read_text())['cards']
    core_themes = read_core_themes(catalog)
    subtheme_groups = read_subtheme_tables(catalog)
    source_video_links = read_video_passage_links()
    COMPANION_COPY.mkdir(parents=True, exist_ok=True)
    for name in ('speaking-practice.html', 'speaking-practice.css', 'speaking-practice.pdf', 'sources.json', 'README.txt'):
        source = COMPANION_SOURCE / name
        if not source.is_file():
            raise FileNotFoundError(f'Required companion edition is missing: {source}')
        shutil.copy2(source, COMPANION_COPY / name)
    pdf_path = OUT / 'speaking-patterns-fieldbook.pdf'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        # The reading edition is self-contained. Waiting for DOM construction is
        # sufficient for printing and avoids a flaky full-load wait on local
        # file URLs in the bundled Chromium build.
        page.goto(
            (ROOT / 'writeups/speaking-patterns-fieldbook.html').as_uri(),
            wait_until='domcontentloaded', timeout=120_000,
        )
        assert page.locator('.job-chapter').count() == len(JOB_CHAPTERS)
        # Local documents travel in the bundle but cannot be opened as local
        # paths from the PDF. Keep page anchors and public HTTPS source links.
        page.evaluate('''() => {
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.getAttribute('href');
                if (!href.startsWith('#') && !href.startsWith('https://')) a.removeAttribute('href');
            });
        }''')
        page.add_style_tag(content='''@media print {
            nav[aria-label="Book sections"] {display:none}
            .job-chapter {break-inside:auto}
            .chapter p,.book-section p {orphans:3;widows:3}
            .part-heading + .chapter {break-before:auto}
        }''')
        page.pdf(path=str(pdf_path), format='A4', print_background=True,
                 display_header_footer=True, header_template='<span></span>',
                 footer_template='<div style="width:100%;text-align:center;font-size:9px;color:#555">The Speaking Patterns Fieldbook · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                 margin={'top':'20mm','bottom':'20mm','left':'20mm','right':'20mm'})
        browser.close()

    with fitz.open(pdf_path) as document:
        pages = [page.get_text() for page in document]
        # Exclude page-number footers so a page boundary inside one authored
        # paragraph does not make a valid text-preservation check fail.
        content_pages = [page.get_text(clip=fitz.Rect(0, 0, page.rect.width, page.rect.height - 50)) for page in document]
        normalized = norm(' '.join(content_pages))
        for chapter in JOB_CHAPTERS:
            assert norm(chapter['title']) in normalized, chapter['title']
            assert norm(chapter['check']) in normalized, chapter['title']
        for title, _ in INTRODUCTION + WORKED_PRESENTATION + CONCLUSION + COMPANION_GUIDE:
            assert norm(title) in normalized, title
        assert 'All 27 approaches: where they connect' in normalized
        assert '22 broad themes' in normalized
        assert '33 smaller patterns' in normalized
        for theme in core_themes:
            assert norm(theme['title']) in normalized
            assert norm(theme['form']) in normalized
            assert norm(theme['use']) in normalized
        for _, entries in subtheme_groups:
            for item in entries:
                assert norm(item['title']) in normalized
                assert norm(item['when']) in normalized
                assert norm(item['how']) in normalized
        for number, title, fit, pattern_ids, reason in COMPANION_CROSSWALK:
            assert norm(f'{number:02d}. {title} — {fit}') in normalized
            assert norm(reason) in normalized
        for lesson in LESSONS.values():
            assert norm(lesson['title']) in normalized, lesson['title']
            for field in ['principle', 'worked_title', 'before', 'after', 'worked_explanation', 'transfer', 'exercise', 'self_check', 'failure_case']:
                assert norm(lesson[field]) in normalized, (lesson['title'], field)
            for variation in lesson['variations']:
                assert norm(variation) in normalized, (lesson['title'], variation)
        for paragraphs in PUBLIC_SOURCE_READINGS.values():
            for paragraph in paragraphs:
                assert norm(paragraph) in normalized, paragraph
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
        assert expected_video_uris <= pdf_uris, f'Missing PDF video links: {len(expected_video_uris - pdf_uris)}'
        assert 'The revised presentation' in normalized
        assert 'Sources and notes' in normalized
        assert not any(link.get('uri', '').startswith('file:') for page in document for link in page.get_links())
        short_pages = [index + 1 for index, text in enumerate(pages) if len(text.split()) < 40]
        assert not short_pages, f'Inspect underfilled pages: {short_pages}'
        preview_dir = Path(tempfile.mkdtemp(prefix='fieldbook-print-preview-'))
        for index in [0, min(12, len(pages)-1), len(pages)-1]:
            document[index].get_pixmap(matrix=fitz.Matrix(1, 1)).save(preview_dir / f'page-{index+1}.png')
        page_count = len(pages)

    files = [ROOT / 'writeups/speaking-patterns-fieldbook.html',
             ROOT / 'writeups/speaking-patterns-fieldbook.md',
             ROOT / 'writeups/fieldbook-editorial-brief.md',
             ROOT / 'writeups/fieldbook-editorial-handoff.md',
             ROOT / 'writeups/cross-repo-communication-source-map.md',
             ROOT / 'research/cross-repo-communication-source-map.json']
    source_paths = sorted({lesson['source_writeup'] for lesson in LESSONS.values()})
    files += [ROOT / path for path in source_paths]
    files += [COMPANION_COPY / name for name in ('speaking-practice.html', 'speaking-practice.css', 'speaking-practice.pdf', 'sources.json', 'README.txt')]
    manifest = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in files}
    readme = '''# The Speaking Patterns Fieldbook

Unzip the complete folder, then open writeups/speaking-patterns-fieldbook.html
in a browser. It runs offline without an installation or an account. Keep the
writeups folder intact so the linked source analyses remain available.

The PDF is a paginated reading edition. Use the HTML edition for linked source
documents and interactive cards. The Markdown file is the editable manuscript.
This package contains two guides. The fieldbook has seven chapters, 22 main
themes, 18 smaller speaking moves, 15 more ideas to explore, a full sample
presentation and 55 made-up before-and-after examples. It uses 17 selected
transcript analyses from a larger project that has reviewed the full transcripts
of 395 videos in a 480-video inventory; it does not recheck all 395. The companion book
has 27 practice chapters and 11 learning paths. Open the
companion HTML from `writeups/companion/speaking-practice.html`; keep its CSS
file beside it. `writeups/cross-repo-communication-source-map.md` shows which
speech, coaching, storytelling, comedy and polished-talk sources are connected
to which companion chapters. `writeups/companion/sources.json` is the
companion's portable source index. The package does not include audio, video or photographs.

The 55 patterns are ideas noticed in transcript searches. Other reviewers have
not checked them, and no audience study has tested them. A 162-item review set
is ready, but this package contains no reviewer answers. Read
writeups/fieldbook-editorial-handoff.md for details. The speakers and named
organizations do not endorse this book. This package does not claim permission
for other uses of the source material.
'''
    archive = OUT / 'speaking-patterns-fieldbook.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, str(path.relative_to(ROOT)))
        bundle.write(pdf_path, pdf_path.name)
        bundle.writestr('README.md', readme)
        bundle.writestr('manifest.json', json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        for name, digest in manifest.items():
            assert sha256(bundle.read(name)).hexdigest() == digest
    receipt = {'pdf_pages':page_count, 'speaking_job_chapters':len(JOB_CHAPTERS),
               'research_index_entries':55, 'worked_examples':len(LESSONS),
               'broad_themes':len(core_themes),
               'smaller_patterns':sum(len(entries) for _, entries in subtheme_groups),
               'source_video_links':sum(len(links) for links in source_video_links.values()),
               'short_pages_under_40_words':short_pages, 'source_analyses':len(source_paths),
               'bundle_hashes_verified':len(manifest), 'preview_directory':str(preview_dir),
               'status':'editorial_edition_export', 'pdf_sha256':sha256(pdf_path.read_bytes()).hexdigest()}
    (OUT / 'export-check.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
