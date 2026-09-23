import importlib.util
import html
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EDITORIAL = load_module("fieldbook_lessons", "fieldbook_editorial_lessons.py")
CORE = load_module("fieldbook_core", "fieldbook_core_chapters.py")
PUBLIC_READINGS = load_module("fieldbook_public_readings", "fieldbook_public_source_readings.py")
CROSSWALK = load_module("fieldbook_crosswalk", "fieldbook_companion_crosswalk.py").COMPANION_CROSSWALK
FIELD_BOOK_BUILDER = load_module("fieldbook_builder", "build_professional_pattern_fieldbook.py")


class ProfessionalPatternFieldbookTest(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / "writeups/speaking-patterns-fieldbook.html").read_text()
        self.manuscript = (ROOT / "writeups/speaking-patterns-fieldbook.md").read_text()
        self.catalog = json.loads((ROOT / "research/presentation-pattern-playbook.json").read_text())

    def test_seven_chapters_and_all_55_research_labels_are_present(self):
        self.assertEqual(len(CORE.JOB_CHAPTERS), 7)
        self.assertEqual(self.catalog["card_count"], 55)
        self.assertIn("Seven common presentation problems", self.page)
        self.assertIn("55 speaking patterns—not 55 proven rules", self.page)
        self.assertIn('href="cross-repo-communication-source-map.md"', self.page)
        self.assertIn("55 speaking patterns to try", self.manuscript)
        payload = self.index_payload()
        for chapter in CORE.JOB_CHAPTERS:
            self.assertIn(f'id="job-{chapter["id"]}"', self.page)
            self.assertIn(chapter["title"], self.manuscript)
        for card in self.catalog["cards"]:
            self.assertIn(card["pattern_id"], {item["pattern_id"] for item in payload["items"]})

    def test_job_map_covers_every_catalog_entry_once(self):
        mapped = [pattern_id for chapter in CORE.JOB_CHAPTERS for pattern_id in chapter["pattern_ids"]]
        catalog_ids = {card["pattern_id"] for card in self.catalog["cards"]}
        self.assertEqual(len(mapped), len(set(mapped)))
        self.assertEqual(set(mapped), catalog_ids)

    def test_plain_language_theme_overview_links_all_22_main_patterns(self):
        themes = FIELD_BOOK_BUILDER.read_core_themes(self.catalog["cards"])
        self.assertEqual(len(themes), 22)
        self.assertIn('id="core-themes"', self.page)
        self.assertIn("## 22 broad themes", self.manuscript)
        self.assertIn("These matches have not all been checked.", self.manuscript)
        self.assertIn("18 structure patterns and 15 other patterns", self.manuscript)
        for theme in themes:
            with self.subTest(theme=theme["number"]):
                self.assertIn(html.escape(theme["title"]), self.page)
                self.assertIn(theme["title"], self.manuscript)
                self.assertIn(f'href="#pattern-{theme["pattern_id"]}"', self.page)
                self.assertIn(f'[{theme["pattern_title"]}](#pattern-{theme["pattern_id"]})', self.manuscript)
                self.assertIn(f'<a id="pattern-{theme["pattern_id"]}"></a>', self.manuscript)
                self.assertIn(theme["form"], self.manuscript)

    def test_both_subtheme_groups_link_to_full_practice_entries(self):
        groups = FIELD_BOOK_BUILDER.read_subtheme_tables(self.catalog["cards"])
        self.assertEqual([len(entries) for _, entries in groups], [18, 15])
        self.assertIn('id="subthemes"', self.page)
        self.assertIn("## 33 smaller patterns", self.manuscript)
        for _, entries in groups:
            for item in entries:
                with self.subTest(pattern=item["pattern_id"]):
                    self.assertIn(item["title"], self.page)
                    self.assertIn(item["title"], self.manuscript)
                    self.assertIn(f'href="#pattern-{item["pattern_id"]}"', self.page)
                    self.assertIn(f'[See its made-up example, practice task and limits](#pattern-{item["pattern_id"]})', self.manuscript)
                    self.assertIn(f'<a id="pattern-{item["pattern_id"]}"></a>', self.manuscript)

    def test_each_chapter_has_plain_guidance_a_source_and_a_limit(self):
        for chapter in CORE.JOB_CHAPTERS:
            with self.subTest(chapter=chapter["id"]):
                for field in ["question", "principle", "method", "example_keys", "boundary", "failure_case", "exercise", "check"]:
                    self.assertTrue(chapter[field])
                self.assertTrue(chapter["example_keys"])
                for key in chapter["example_keys"]:
                    lesson = EDITORIAL.LESSONS[key]
                    self.assertTrue((ROOT / lesson["source_writeup"]).is_file())
                    self.assertGreaterEqual(len(PUBLIC_READINGS.PUBLIC_SOURCE_READINGS[key]), 2)
                    self.assertIn("caption", lesson["source_passages"].lower())
                    self.assertIn(lesson["source_title"], self.manuscript)
                    for paragraph in PUBLIC_READINGS.PUBLIC_SOURCE_READINGS[key]:
                        self.assertIn(paragraph, self.manuscript)
                    self.assertIn(lesson["source_passages"], self.manuscript)
                self.assertIn(chapter["boundary"], self.manuscript)

    def test_practice_instructions_use_short_sentences(self):
        fields = ["principle", "transfer", "exercise", "self_check", "worked_explanation"]
        for pattern_id, lesson in EDITORIAL.LESSONS.items():
            for field in fields:
                for sentence in re.split(r"(?<=[.!?])(?:['’\"])?\s+", lesson[field]):
                    words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", sentence)
                    with self.subTest(pattern=pattern_id, field=field, sentence=sentence):
                        self.assertLessEqual(len(words), 31)

    def test_selected_caption_references_fit_the_saved_transcripts(self):
        checked_sources = set()
        for key, lesson in EDITORIAL.LESSONS.items():
            with self.subTest(pattern=key):
                source_path = ROOT / lesson["source_writeup"]
                source_text = source_path.read_text()
                video_ids = re.findall(r"`([A-Za-z0-9_-]{11})`", source_text[:1800])
                video_ids = [video_id for video_id in video_ids if (ROOT / "data/transcripts" / f"{video_id}.json").is_file()]
                self.assertTrue(video_ids, lesson["source_writeup"])
                video_id = video_ids[0]
                transcript = json.loads((ROOT / "data/transcripts" / f"{video_id}.json").read_text())["transcript"]
                cited_ranges = re.findall(r"(\d+)\s*[–-]\s*(\d+)", lesson["source_passages"])
                self.assertTrue(cited_ranges, key)
                for start, end in cited_ranges:
                    self.assertGreaterEqual(int(start), 0)
                    self.assertLess(int(start), len(transcript), (key, start, len(transcript)))
                    self.assertLess(int(end), len(transcript), (key, end, len(transcript)))
                checked_sources.add(video_id)
        self.assertEqual(len(EDITORIAL.LESSONS), 55)
        self.assertEqual(len(checked_sources), 17)

    def test_source_video_links_open_at_the_saved_start_of_each_cited_caption_range(self):
        payload_items = {item["pattern_id"]: item for item in self.index_payload()["items"]}
        video_links = FIELD_BOOK_BUILDER.read_video_passage_links()
        self.assertEqual(set(video_links), set(EDITORIAL.LESSONS))
        for key, lesson in EDITORIAL.LESSONS.items():
            with self.subTest(pattern=key):
                ranges = re.findall(r"(\d+)\s*[–-]\s*(\d+)", lesson["source_passages"])
                links = video_links[key]
                self.assertEqual(len(links), len(ranges))
                self.assertEqual(payload_items[key]["source_video_links"], links)
                writeup = (ROOT / lesson["source_writeup"]).read_text()[:1800]
                video_ids = [
                    video_id for video_id in re.findall(r"`([A-Za-z0-9_-]{11})`", writeup)
                    if (ROOT / "data/transcripts" / f"{video_id}.json").is_file()
                ]
                transcript = json.loads((ROOT / "data/transcripts" / f"{video_ids[0]}.json").read_text())["transcript"]
                for (start, end), link in zip(ranges, links):
                    seconds = int(transcript[int(start)]["startMs"]) // 1000
                    self.assertEqual(link["caption_range"], f"{start}–{end}")
                    self.assertTrue(link["url"].endswith(f"&t={seconds}s"))
                    self.assertIn(html.escape(link["url"], quote=True), self.page)
                    self.assertIn(f'[{link["time"]}]({link["url"]})', self.manuscript)
        self.assertIn("recording was not checked here", self.manuscript)

    def test_example_and_claim_boundaries_are_clear(self):
        for text in ["not the speaker's exact words", "ideas to try, not proven rules", "Other reviewers have not checked", "no audience study has tested the advice", "This full example is invented for practice."]:
            self.assertIn(text, self.manuscript)
        self.assertNotIn("55 lessons in this book", self.manuscript)
        self.assertNotIn("reviewing 395 speeches and interviews", self.page)
        self.assertIn("395 of its 480 videos", self.page)
        self.assertIn("does not repeat that review", self.page)
        self.assertIn("does not recheck all 395", self.manuscript)

    def test_full_practice_presentation_and_source_notes_are_in_both_formats(self):
        for section_id in ["reading-guide", "worked-presentation", "closing-note", "companion-guides", "companion-crosswalk", "source-notes"]:
            self.assertIn(f'id="{section_id}"', self.page)
        for phrase in ["The first draft", "The revised presentation", "Why these choices belong together", "Prepare for the question that could change the decision", "16 transcripts", "all 27 approaches", "Sources and notes"]:
            self.assertIn(phrase, self.page)
            self.assertIn(phrase, self.manuscript)

    def test_companion_source_links_are_direct_and_time_anchored(self):
        for video_id, seconds in [("zUBDMZNayj4", "t=114s"), ("BfUEDvrD1Y4", "t=123s"), ("_2tXNCxg8hs", "t=98s"), ("Tg_yavuXU6g", "t=505s")]:
            url = f"https://www.youtube.com/watch?v={video_id}&{seconds}"
            self.assertIn(url.replace("&", "&amp;"), self.page)
            self.assertIn(url, self.manuscript)

    def test_editorial_crosswalk_covers_all_27_approaches_without_inventing_matches(self):
        self.assertEqual(len(CROSSWALK), 27)
        self.assertEqual([row[0] for row in CROSSWALK], list(range(1, 28)))
        valid_ids = set(EDITORIAL.LESSONS)
        allowed_fits = {"Close fit", "Related, but different", "Not covered here"}
        for number, title, fit, pattern_ids, reason in CROSSWALK:
            with self.subTest(approach=number):
                self.assertTrue(title)
                self.assertIn(fit, allowed_fits)
                self.assertTrue(reason)
                self.assertTrue(set(pattern_ids) <= valid_ids)
                self.assertIn(f"{number:02d}. {title} — {fit}", self.page)
                self.assertIn(f"{number:02d}. {title} — {fit}", self.manuscript)
                self.assertIn(reason, self.manuscript)
                chapter_link = f'companion/speaking-practice.html#chapter-{number:02d}'
                self.assertIn(chapter_link, self.page)
                self.assertIn(chapter_link, self.manuscript)
                for pattern_id in pattern_ids:
                    self.assertIn(f'href="#pattern-{pattern_id}"', self.page)
                    self.assertIn(EDITORIAL.LESSONS[pattern_id]["title"], self.manuscript)
        self.assertEqual([row[0] for row in CROSSWALK if row[3] == []], [2, 10, 21])

    def test_research_index_names_sources_and_discloses_search_count_limit(self):
        payload = self.index_payload()
        self.assertEqual(len(payload["items"]), 55)
        self.assertEqual(set(PUBLIC_READINGS.PUBLIC_SOURCE_READINGS), set(EDITORIAL.LESSONS))
        self.assertIn("not been independently reviewed", payload["claim_boundary"])
        for item in payload["items"]:
            lesson = EDITORIAL.LESSONS[item["pattern_id"]]
            self.assertEqual(item["candidate_form"], lesson["principle"])
            self.assertEqual(item["source_example"], PUBLIC_READINGS.PUBLIC_SOURCE_READINGS[item["pattern_id"]])
            entry = self.manuscript.split(f'<a id="pattern-{item["pattern_id"]}"></a>', 1)[1].split('<a id="pattern-', 1)[0]
            for paragraph in item["source_example"]:
                self.assertIn(paragraph, entry)
                self.assertIn(html.escape(paragraph), self.page)
            self.assertLess(entry.index('**Source example'), entry.index('**Invented practice example'))
            self.assertNotEqual(item["candidate_form"], item["use_when"])
            self.assertIn('**Main point:** ' + lesson["principle"], self.manuscript)
            self.assertIn('<strong>Main point:</strong> ' + html.escape(lesson["principle"]), self.page)
            self.assertIn(item["source_passages"], self.manuscript)
            self.assertTrue((ROOT / item["source_writeup"]).is_file())
            self.assertEqual(item["status"], "transcript candidate; not independently reviewed")
            for field in ["how_to_use", "worked_title", "before", "after", "worked_explanation", "exercise", "practice_check", "safety_boundary"]:
                self.assertTrue(item[field], (item["pattern_id"], field))
                self.assertIn(item[field], self.manuscript, (item["pattern_id"], field))
            self.assertEqual(len(item["variations"]), 3)
            for variation in item["variations"]:
                self.assertIn(variation, self.manuscript)

    def index_payload(self):
        marker = "<script id='fieldbook-data' type='application/json'>"
        return json.loads(self.page.split(marker, 1)[1].split("</script>", 1)[0])


if __name__ == "__main__":
    unittest.main()
