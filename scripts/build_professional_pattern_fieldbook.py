#!/usr/bin/env python3
"""Build the polished presenter-facing Speaking Patterns Fieldbook."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from fieldbook_editorial_lessons import LESSONS, READING_ROUTES
from fieldbook_book_sections import INTRODUCTION, WORKED_PRESENTATION, CONCLUSION, COMPANION_GUIDE
from fieldbook_core_chapters import JOB_CHAPTERS
from fieldbook_public_source_readings import PUBLIC_SOURCE_READINGS
from fieldbook_companion_crosswalk import COMPANION_CROSSWALK

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "research/presentation-pattern-playbook.json"
OUTPUT = ROOT / "writeups/speaking-patterns-fieldbook.html"
CORE_THEMES_SOURCE = ROOT / "writeups/amazing-presentation-patterns.md"

# The broad theme names are editorial headings; these IDs point readers to
# the matching detailed entries in the 55-pattern index.
CORE_THEME_PATTERN_IDS = {
    1: "orientation_and_roadmap",
    2: "story_memory_and_scene",
    3: "contrast_and_reversal",
    4: "analogy_metaphor_and_callback",
    5: "future_hope_and_action",
    6: "audience_invitation_and_next_turn",
    7: "scale_shift",
    8: "qualification_and_boundary",
    9: "credit_and_collective_agency",
    10: "choice_and_responsibility",
    11: "metrics_and_revaluation",
    12: "question_and_reframe",
    13: "objection_and_response",
    14: "identity_status_and_belonging",
    15: "value_and_moral_frame",
    16: "definition_and_explanation",
    17: "risk_safety_and_limit",
    18: "cause_and_mechanism",
    19: "institution_system_and_policy",
    20: "repair_and_self_correction",
    21: "grief_loss_and_continuation",
    22: "humor_rapport_and_self_undercut",
}

CORE_THEME_PLAIN_TITLES = {
    1: "Start with context before details",
    2: "Use one specific story to explain an idea",
    3: "Show what changed",
    4: "Use an analogy carefully",
    5: "Turn hope into a specific next step",
    6: "Invite a clear response without pressure",
    7: "Connect one person's experience to the bigger picture",
    8: "State your point and its limits",
    9: "Name everyone's contribution",
    10: "Say who is responsible for what",
    11: "Choose a measure that reflects what matters",
    12: "Answer the question behind the question",
    13: "State the other side's concern fairly",
    14: "Explain what your experience can—and cannot—show",
    15: "Separate facts from values",
    16: "Define it, give an example, say where it stops",
    17: "Name the risk before asking people to trust you",
    18: "Explain how it may work; do not call that proof",
    19: "Connect a personal story to the rules around it",
    20: "Correct yourself clearly",
    21: "Acknowledge loss and name what continues",
    22: "Use brief humor, then return to the point",
}

CORE_THEME_PLAIN_FORMS = {
    1: "Set the scene → say why it matters → show where you are going.",
    2: "Tell one specific moment → explain what it shows → say what it cannot prove.",
    3: "Say what you thought → what changed → what you think now → what still holds.",
    4: "Give a comparison → say what matches → say where it stops matching.",
    5: "Say what you hope for → name one doable step → say what help or limits matter.",
    6: "Ask for a clear response → make it easy to answer → make it okay to decline.",
    7: "Start with one person's experience → explain the larger rule or system → connect them.",
    8: "Make your point → say when it applies and where it does not.",
    9: "Name the work people did → say what it led to → name the support behind it.",
    10: "Name who decides → what help is available → who is still responsible.",
    11: "Name the usual measure → what it misses → a measure that better fits the decision.",
    12: "Repeat the question → explain the decision underneath it → answer with any needed condition.",
    13: "State the concern fairly → answer it → say what remains uncertain.",
    14: "Explain how your background affects your view → connect it to the point → do not treat it as proof.",
    15: "State what happened → name the value judgment → explain the decision it leads to.",
    16: "Define the term → give an example → say where the example no longer fits.",
    17: "Name what could go wrong → say how it could be reduced → say who must act.",
    18: "State the point → explain how it might work → say what evidence is still needed.",
    19: "Describe one person's experience → explain the rule or pressure behind it → show which choices remain.",
    20: "Point out the mistake → correct it plainly → continue.",
    21: "Name the loss → do not pretend it is resolved → say what care or work continues.",
    22: "Use a brief, self-aware joke → reconnect with the room → return to the main point.",
}

STRUCTURAL_PATTERN_IDS = [
    "premise_correction", "scope_repair", "analogy_transfer", "evidence_gap",
    "expectation_reversal", "register_shift", "audience_shift", "credit_redirection",
    "hands_off", "reciprocal_learning", "self_undercut", "despair_to_hope",
    "metric_revaluation", "moral_to_memorial", "optional_support",
    "question_redefinition", "sorrow_and_continuation", "story_to_thesis",
]

ADDITIONAL_PATTERN_IDS = [
    "purpose_attention_example", "recognition_to_specific_credit",
    "unfinished_work_to_commitment", "familiarity_to_scope", "unity_across_scale",
    "authority_to_service", "difficulty_to_capability",
    "invitation_to_low_barrier_entry", "access_obstacle_to_support",
    "emotion_to_composure", "selection_and_incentive", "failure_to_reframe",
    "authenticity_vs_performance", "craft_process_over_outcome",
    "technical_explanation_and_interruption",
]


def read_core_themes(catalog):
    text = CORE_THEMES_SOURCE.read_text()
    match = re.search(
        r"^## The 22 core themes\s*$(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("Could not find the 22 core themes in the source writeup")
    blocks = re.findall(
        r"^### (\d+)\. (.+?)\s*\n\n\*\*Form:\*\* (.*?)\s*\n"
        r"\*\*Found in:\*\* (\d+) videos\.\s*\n\n(.*?)(?=\n### |\Z)",
        match.group(1),
        flags=re.MULTILINE | re.DOTALL,
    )
    if len(blocks) != 22 or set(CORE_THEME_PATTERN_IDS) != set(range(1, 23)):
        raise ValueError(f"Expected 22 broad themes; found {len(blocks)}")
    cards = {card["pattern_id"]: card for card in catalog}
    themes = []
    for raw_number, title, form, raw_count, use in blocks:
        number, count = int(raw_number), int(raw_count)
        pattern_id = CORE_THEME_PATTERN_IDS[number]
        card = cards.get(pattern_id)
        if not card or card.get("category") != "core_theme":
            raise ValueError(f"Theme {number} does not point to a core pattern: {pattern_id}")
        if card.get("canonical_video_count") != count:
            raise ValueError(f"Theme {number} count does not match {pattern_id}")
        themes.append({
            "number": number,
            "title": CORE_THEME_PLAIN_TITLES[number],
            "source_title": title.strip(),
            "form": CORE_THEME_PLAIN_FORMS[number],
            "count": count,
            "use": re.sub(r"\s+", " ", use).strip(),
            "pattern_id": pattern_id,
            "pattern_title": LESSONS[pattern_id]["title"],
        })
    return themes


def read_subtheme_tables(catalog):
    text = CORE_THEMES_SOURCE.read_text()
    cards = {card["pattern_id"]: card for card in catalog}
    groups = [
        ("The 18 high-value structural subthemes", STRUCTURAL_PATTERN_IDS, "structural_subtheme", 3),
        ("Fifteen additional subthemes", ADDITIONAL_PATTERN_IDS, "additional_subtheme", 2),
    ]
    result = []
    for heading, pattern_ids, category, column_count in groups:
        section = re.search(
            rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if not section:
            raise ValueError(f"Could not find subtheme table: {heading}")
        rows = []
        for line in section.group(1).splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != column_count or all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            if cells[0].lower() == "subtheme":
                continue
            rows.append(cells)
        if len(rows) != len(pattern_ids):
            raise ValueError(f"{heading}: expected {len(pattern_ids)} rows, found {len(rows)}")
        entries = []
        for cells, pattern_id in zip(rows, pattern_ids):
            card = cards.get(pattern_id)
            if not card or card.get("category") != category:
                raise ValueError(f"Subtheme row does not match the expected category: {pattern_id}")
            entries.append({
                "source_label": cells[0],
                "use": cells[1],
                "sequence": cells[2] if column_count == 3 else "",
                "pattern_id": pattern_id,
                "title": LESSONS[pattern_id]["title"],
                "when": LESSONS[pattern_id]["problem"],
                "how": LESSONS[pattern_id]["transfer"],
            })
        result.append((heading, entries))
    return result


def read_video_passage_links():
    """Link each cited caption range to its saved YouTube start time.

    These are navigation aids, not confirmation that the caption timing or
    transcript text matches the recording.
    """
    transcripts = {}
    writeup_video_ids = {}
    links_by_pattern = {}
    for pattern_id, lesson in LESSONS.items():
        writeup = lesson["source_writeup"]
        if writeup not in writeup_video_ids:
            text = (ROOT / writeup).read_text()[:1800]
            matches = re.findall(r"`([A-Za-z0-9_-]{11})`", text)
            video_ids = [
                video_id for video_id in matches
                if (ROOT / "data/transcripts" / f"{video_id}.json").is_file()
            ]
            if not video_ids:
                raise ValueError(f"No saved transcript found for source analysis {writeup}")
            writeup_video_ids[writeup] = video_ids[0]
        video_id = writeup_video_ids[writeup]
        if video_id not in transcripts:
            transcripts[video_id] = json.loads(
                (ROOT / "data/transcripts" / f"{video_id}.json").read_text()
            )["transcript"]
        transcript = transcripts[video_id]
        ranges = re.findall(r"(\d+)\s*[–-]\s*(\d+)", lesson["source_passages"])
        if not ranges:
            raise ValueError(f"No caption ranges listed for {pattern_id}")
        anchors = []
        for first, last in ranges:
            start, end = int(first), int(last)
            if start > end or end >= len(transcript):
                raise ValueError(f"Caption range outside transcript for {pattern_id}: {first}–{last}")
            start_ms = transcript[start].get("startMs")
            if start_ms is None:
                raise ValueError(f"Caption {start} has no saved start time for {pattern_id}")
            seconds = int(start_ms) // 1000
            minutes, remainder = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            time_label = f"{hours}:{minutes:02d}:{remainder:02d}" if hours else f"{minutes}:{remainder:02d}"
            anchors.append({
                "caption_range": f"{start}–{end}",
                "time": time_label,
                "url": f"https://www.youtube.com/watch?v={video_id}&t={seconds}s",
            })
        links_by_pattern[pattern_id] = anchors
    return links_by_pattern


def video_links_html(links):
    return " · ".join(
        f'<a href="{html.escape(link["url"], quote=True)}">'
        f'{html.escape(link["time"])} (captions {html.escape(link["caption_range"])})</a>'
        for link in links
    )


FEATURED = {
    "story_memory_and_scene": {
        "kicker": "Make an idea visible",
        "principle": "A short scene can make an abstract point easier to picture. It cannot prove the point by itself. Explain what the moment illustrates and what it does not show.",
        "example_title": "Jeff Bezos: from childhood detail to a decision principle",
        "example": "Bezos describes estimating years of life supposedly lost to smoking while travelling with his grandparents. He expects praise for being clever; his grandmother cries instead. His grandfather distinguishes kindness from cleverness. Later, the speaker uses the difference between gifts and choices to explain a new way to judge his action. See the lesson for passage references and a practice example.",
        "source": "2u2Sd9MeFUc",
        "writeup": "writeups/full-context-address-72.md",
        "use": "Use when a difficult idea needs a human-scale entry point. Give the audience one moment they can picture, then explain the point in plain language.",
        "nonfit": "Do not use a vivid personal story as proof of a general rule, and do not disclose someone else's private experience merely to create emotional force.",
        "practice": "Tell a 45-second scene with a clear time, place and action. Add one sentence beginning ‘This illustrates…’ and one beginning ‘It does not establish…’."
    },
    "contrast_and_reversal": {
        "kicker": "Make change legible",
        "principle": "Contrast lets the audience see a change rather than merely hear that one occurred. Treat the earlier frame fairly, show the turn, then state what remains true across both sides.",
        "example_title": "Mindy Kaling: when a checklist meets reality",
        "example": "Kaling contrasts a completed college checklist with an adult timetable that largely did not unfold as expected. Her parenthood account names support from family and friends, and she still allows that structured ambition can motivate. The point permits revising a plan while preserving its useful purpose. Read the worked lesson above for the passage references and an application.",
        "source": "5mXFlne4JB8",
        "writeup": "writeups/full-context-address-71.md",
        "use": "Use for a changed plan, a lesson learned, a disagreement or a decision that looks different after new evidence.",
        "nonfit": "Do not manufacture a dramatic ‘before’ position or caricature the people who held it. A contrast that requires a false enemy weakens the point.",
        "practice": "Write: ‘I initially thought ____. Then ____ happened. Now I think ____. What remains true is ____.’"
    },
    "question_and_reframe": {
        "kicker": "Answer the question underneath",
        "principle": "A reframe is useful when the literal question hides the decision the audience actually needs to make. Acknowledge the surface question first; then explain the distinction that makes a better answer possible.",
        "example_title": "Taylor Swift: moving from the literal answer to the deeper idea",
        "example": "In the reviewed interview, an answer shifts the frame from the mechanics of music and lyrics toward the idea or feeling underneath them. The transferable move is not evasion; it is showing why the first frame is incomplete before answering the more useful question.",
        "source": "l2ojUrbq8EM",
        "writeup": "writeups/full-context-interview-27.md",
        "use": "Use in a Q&A, proposal defense or difficult conversation when the audience's wording points at a real concern but not the decision itself.",
        "nonfit": "Do not use reframing to dodge a legitimate objection, avoid a direct answer or make the audience feel foolish for asking plainly.",
        "practice": "Say: ‘The direct question is ____. The distinction that matters here is ____. With that distinction, my answer is ____.’"
    },
    "qualification_and_boundary": {
        "kicker": "Be precise without disappearing",
        "principle": "Qualification protects a clear claim from being stretched beyond its evidence. State the useful point first, attach the condition to the right part of it, and say what would change your mind.",
        "example_title": "A calendar claim narrowed to its actual condition",
        "example": "The transcript review shows a broad statement narrowed by its timing. Precise wording helps listeners understand how far the claim reaches.",
        "source": "kTw_KyXcHIc",
        "writeup": "writeups/full-context-address-73.md",
        "use": "Use when your evidence is partial, your recommendation has a boundary, or the audience may mistake a hypothesis for a guarantee.",
        "nonfit": "Do not bury every sentence under caveats. A qualification should make the claim more usable, not dissolve it into fog.",
        "practice": "State one claim, one condition and one revision trigger: ‘I believe ____, when ____. I would revisit it if ____. ’"
    },
    "scale_shift": {
        "kicker": "Connect the person to the system",
        "principle": "A scale shift shows how an individual experience relates to an institution, incentive or shared responsibility. The bridge must be spoken; otherwise the audience is left to confuse one person's story with proof about a whole system.",
        "example_title": "From an individual moment to a wider responsibility",
        "example": "Some speakers move from one person's experience to a wider responsibility. Make that step clear: ‘Here is what happened to one person. Here is the rule or condition around it. Here is the choice available to us.’",
        "source": "vPDQOB7pRRM",
        "writeup": "writeups/full-context-historical-01.md",
        "use": "Use when a talk must connect lived experience to policy, culture, organizational design or shared action.",
        "nonfit": "Do not turn one story into a population claim, or use system language to erase the person's agency and particularity.",
        "practice": "Draft three sentences: one about the person, one about the surrounding condition, and one about the responsible next choice."
    },
    "audience_invitation_and_next_turn": {
        "kicker": "Give the audience a safe next move",
        "principle": "Participation becomes usable when the next turn is specific, answerable and safe to decline. The invitation should clarify the role, not pressure people into performing enthusiasm.",
        "example_title": "An invitation that makes participation concrete",
        "example": "The reviewed speeches include invitations to answer a question or take part in shared work. Say what response you want, explain the first step and make clear when people can decline.",
        "source": "fHAOWLhrxhQ",
        "writeup": "writeups/full-context-scene-11.md",
        "use": "Use at the end of a proposal, after a difficult explanation, or whenever the audience needs to know exactly how to participate.",
        "nonfit": "Do not confuse applause, public disclosure or immediate agreement with understanding. Offer typed, private, asynchronous or no-response paths where appropriate.",
        "practice": "Replace ‘Any thoughts?’ with one concrete question, a response format and a safe way to pass."
    },
    "analogy_metaphor_and_callback": {
        "kicker": "Give the idea a handle—and a return",
        "principle": "An analogy makes a relation clear. A callback gives an earlier image new meaning later. Both require a stopping point: say what transfers, what does not and why the return matters now.",
        "example_title": "A remembered image that changes meaning later",
        "example": "Some speakers return to an earlier phrase or image after explaining the subject. Introduce the image, explain one link to your point and return to it with a changed meaning. An image can help explain an idea, but it is not proof.",
        "source": "vPDQOB7pRRM",
        "writeup": "writeups/full-context-historical-01.md",
        "use": "Use to give a technical idea a memorable structure or to make a long presentation feel architecturally coherent.",
        "nonfit": "Do not let a vivid analogy smuggle in a conclusion, erase important differences or become a decorative callback with no new work to do.",
        "practice": "Write an image, the single relation it carries, the sentence where it stops, and the later line that gives it a new job."
    },
    "humor_rapport_and_self_undercut": {
        "kicker": "Lower distance, then return to substance",
        "principle": "Lightness can make a room more reachable when it is brief, self-aware and followed by a clear substantive point. The move is about the relationship with the room, not about winning attention at someone else's expense.",
        "example_title": "Self-including humor before a difficult point",
        "example": "Some speakers include themselves in a joke before making a serious point. The review does not show how listeners responded. If you try this, avoid making someone else the target and move back to the subject quickly.",
        "source": "5mXFlne4JB8",
        "writeup": "writeups/full-context-address-71.md",
        "use": "Use to acknowledge shared awkwardness, reset attention or soften a transition before a serious point.",
        "nonfit": "Do not use humor to dodge responsibility, expose someone sharing private details or make a group pay for your joke.",
        "practice": "Write one line that includes your own stake or limitation, then follow it immediately with the point the audience came to hear."
    }
}


def main() -> int:
    catalog = json.loads(PLAYBOOK.read_text())["cards"]
    core_themes = read_core_themes(catalog)
    subtheme_groups = read_subtheme_tables(catalog)
    source_video_links = read_video_passage_links()
    job_for_pattern = {
        pattern_id: chapter
        for chapter in JOB_CHAPTERS
        for pattern_id in chapter["pattern_ids"]
    }
    catalog_ids = {card["pattern_id"] for card in catalog}
    if len(job_for_pattern) != len(LESSONS) or set(job_for_pattern) != catalog_ids:
        raise ValueError("core-job chapters must map every research pattern exactly once")
    if set(PUBLIC_SOURCE_READINGS) != catalog_ids:
        raise ValueError("every pattern must have a plain-language source summary")

    items = []
    for card in catalog:
        key = card["pattern_id"]
        lesson = LESSONS[key]
        job = job_for_pattern[key]
        items.append({
            "pattern_id": key,
            "title": lesson["title"],
            "category": card["category"],
            "job_id": job["id"],
            "job_title": job["title"],
            "candidate_form": lesson["principle"],
            "use_when": lesson["problem"],
            "how_to_use": lesson["transfer"],
            "worked_title": lesson["worked_title"],
            "before": lesson["before"],
            "after": lesson["after"],
            "worked_explanation": lesson["worked_explanation"],
            "variations": lesson["variations"],
            "exercise": lesson["exercise"],
            "practice_check": lesson["self_check"],
            "safety_boundary": lesson["failure_case"],
            "source_label": lesson["source_title"],
            "source_example": PUBLIC_SOURCE_READINGS[key],
            "source_writeup": lesson["source_writeup"],
            "source_passages": lesson["source_passages"],
            "source_video_links": source_video_links[key],
            "retrieved_video_count": card.get("canonical_video_count", 0),
            "status": "transcript candidate; not independently reviewed",
        })
    payload = {
        "items": items,
        "claim_boundary": "The 55 labels are transcript-retrieval candidates. They have not been independently reviewed or tested with audiences.",
    }
    # Script elements contain raw text; HTML entities would corrupt the data.
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    document = render(data)
    e = html.escape
    chapters = '<section class="chapters" id="core-jobs"><h2>Seven common presentation problems</h2><p>Start with the problem your talk needs to solve. Each chapter explains one, reads a real transcript example, says what that example cannot tell us, and gives you an exercise.</p><p><a href="speaking-patterns-fieldbook.md">Read the manuscript</a> · <a href="#pattern-catalog">Browse the 55 speaking patterns</a> · <a href="cross-repo-communication-source-map.md">See all speech, humor and communication sources</a> · <a href="fieldbook-editorial-brief.md">How this book was prepared</a></p><nav aria-label="Presentation problems" id="job-contents"><ol>'
    chapters += "".join(f'<li><a href="#job-{e(chapter["id"])}">{e(chapter["title"])}</a></li>' for chapter in JOB_CHAPTERS)
    chapters += "</ol></nav>"
    for chapter in JOB_CHAPTERS:
        chapters += (
            f'<article class="chapter job-chapter" id="job-{e(chapter["id"])}">'
            f'<p class="eyebrow">Speaking job</p><h2>{e(chapter["title"])}</h2>'
            f'<p class="job-question"><strong>Ask:</strong> {e(chapter["question"])}</p>'
            f'<h3>Main point</h3><p>{e(chapter["principle"])}</p>'
            f'<h3>A way to do it</h3><ol>{"".join("<li>" + e(step) + "</li>" for step in chapter["method"])}</ol>'
        )
        for example_key in chapter["example_keys"]:
            lesson = LESSONS[example_key]
            source_paragraphs = "".join(f'<p>{e(paragraph)}</p>' for paragraph in PUBLIC_SOURCE_READINGS[example_key])
            video_links = video_links_html(source_video_links[example_key])
            chapters += (
                f'<section class="source-case"><h3>{e(lesson["source_title"])}</h3>'
            f'<p class="source-note">Summary in the editors’ words; not the speaker’s exact words.</p>'
                f'{source_paragraphs}<p class="source-note"><a href="../{e(lesson["source_writeup"], quote=True)}">Read the full source analysis</a>. {e(lesson["source_passages"])}</p>'
                f'<p class="source-note">Watch at saved caption start times: {video_links}. The recording was not checked here to confirm the captions or timing.</p></section>'
            )
        chapters += (
            f'<h3>What this example does not show</h3><p>{e(chapter["boundary"])}</p>'
            f'<h3>An invented failure case</h3><p class="source-note">This situation is made up for practice; it is not a finding from the videos.</p><p>{e(chapter["failure_case"])}</p>'
            f'<h3>Try it</h3><p>{e(chapter["exercise"])}</p>'
            f'<h3>Check your draft</h3><p>{e(chapter["check"])}</p>'
            f'<p class="pattern-links"><strong>Related patterns:</strong> '
            + ", ".join(f'<a href="#pattern-{e(key)}">{e(LESSONS[key]["title"])}</a>' for key in chapter["pattern_ids"])
            + "</p></article>"
        )
    chapters += "</section>"
    def render_paragraph(text):
        link_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+|#[A-Za-z0-9_-]+|[A-Za-z0-9._/-]+\.(?:html|pdf|zip)(?:#[A-Za-z0-9_-]+)?)\)')
        pieces = []
        cursor = 0
        for match in link_pattern.finditer(text):
            pieces.append(html.escape(text[cursor:match.start()]))
            label, url = match.groups()
            relation = ' rel="noopener noreferrer"' if url.startswith('https://') else ''
            pieces.append(f'<a href="{html.escape(url, quote=True)}"{relation}>{html.escape(label)}</a>')
            cursor = match.end()
        pieces.append(html.escape(text[cursor:]))
        return ''.join(pieces)

    def book_section(section_id, heading, sections):
        return (f'<section class="book-section" id="{section_id}"><h2>{html.escape(heading)}</h2>' +
                ''.join('<h3>' + html.escape(title) + '</h3>' + ''.join('<p>' + render_paragraph(p) + '</p>' for p in paragraphs) for title, paragraphs in sections) + '</section>')
    chapters = book_section('reading-guide', 'How to use the fieldbook', INTRODUCTION) + chapters
    theme_html = (
        '<section class="theme-overview" id="core-themes"><h2>22 broad themes</h2>'
        '<p>These are the 22 main themes in the larger pattern writeup. Each link opens its related detailed entry in the 55-pattern index. '
        'The counts mean a transcript search found a match in that many videos; the matches have not all been checked.</p>'
    )
    manuscript_themes = [
        '## 22 broad themes',
        'These are the 22 main themes in the larger pattern writeup. Each link opens its related detailed entry in the 55-pattern index. The counts mean a transcript search found a match in that many videos; the matches have not all been checked.',
    ]
    for theme in core_themes:
        anchor = f"pattern-{theme['pattern_id']}"
        theme_html += (
            f'<article class="theme-item"><h3>{theme["number"]}. {e(theme["title"])}</h3>'
            f'<p><strong>In simple terms:</strong> {e(theme["form"])}</p>'
            f'<p><strong>Search matches:</strong> {theme["count"]} videos.</p>'
            f'<p>{e(theme["use"])}</p>'
            f'<p><a href="#{e(anchor)}">Related detailed pattern: {e(theme["pattern_title"])}</a></p></article>'
        )
        manuscript_themes.extend([
            f"### {theme['number']}. {theme['title']}",
            f"**In simple terms:** {theme['form']}",
            f"**Search matches:** {theme['count']} videos. These matches have not all been checked.",
            theme["use"],
            f"Related detailed pattern: [{theme['pattern_title']}](#{anchor}).",
        ])
    theme_html += (
        '<p>The other 33 entries in the index are 18 structure patterns and 15 other patterns. '
        'They can support more than one broad theme, so this guide does not force each one under a single heading.</p></section>'
    )
    manuscript_themes.append(
        'The other 33 entries in the index are 18 structure patterns and 15 other patterns. They can support more than one broad theme, so this guide does not force each one under a single heading.'
    )
    chapters += theme_html
    subtheme_html = (
        '<section class="theme-overview subtheme-overview" id="subthemes">'
        '<h2>33 smaller patterns</h2>'
        '<p>The first 18 are smaller speaking moves that can fit inside a larger theme. '
        'The next 15 are additional ideas worth exploring. Each links to a full entry with a made-up example, a practice task and limits. '
        'These are not assigned to just one of the 22 themes because they can serve more than one.</p>'
    )
    manuscript_subthemes = [
        '## 33 smaller patterns',
        'The first 18 are smaller speaking moves that can fit inside a larger theme. The next 15 are additional ideas worth exploring. Each links to a full entry with a made-up example, a practice task and limits. These are not assigned to just one of the 22 themes because they can serve more than one.',
    ]
    for heading, entries in subtheme_groups:
        plain_heading = '18 smaller moves that fit inside a talk' if len(entries) == 18 else '15 more ideas to explore'
        subtheme_html += f'<div class="subtheme-group"><h3>{e(plain_heading)}</h3>'
        manuscript_subthemes.append('### ' + plain_heading)
        for item in entries:
            anchor = f"pattern-{item['pattern_id']}"
            subtheme_html += (
                f'<article class="theme-item"><h4>{e(item["title"])}</h4>'
                f'<p><strong>Try this when:</strong> {e(item["when"])}</p>'
                f'<p><strong>How to use it:</strong> {e(item["how"])}</p>'
                f'<p><a href="#{e(anchor)}">See its made-up example, practice task and limits</a></p></article>'
            )
            manuscript_subthemes.extend([
                f'#### {item["title"]}',
                '**Try this when:** ' + item["when"],
                '**How to use it:** ' + item["how"],
                f'[See its made-up example, practice task and limits](#{anchor}).',
            ])
        subtheme_html += '</div>'
    subtheme_html += '</section>'
    chapters += subtheme_html
    index_html = '<section class="print-index" id="print-pattern-index"><h2>55 speaking patterns to try</h2><p>These names describe patterns noticed while searching transcripts. The counts show how many videos had a search match; no one has checked every match. Each pattern has a made-up before-and-after example to show one possible use. Those practice examples are not from the videos.</p>'
    manuscript_index = ['## 55 speaking patterns to try', 'These names describe possible patterns noticed while searching transcripts. Counts show how many videos had a search match; they are not counts of checked examples. Each pattern has a made-up before-and-after example. Use the linked chapter and source note to see what the idea means and what the transcript can show.']
    for chapter in JOB_CHAPTERS:
        index_html += f'<h3>{e(chapter["title"])}</h3><ul>'
        manuscript_index.append('### ' + chapter["title"])
        for key in chapter["pattern_ids"]:
            lesson = LESSONS[key]
            card = next(row for row in catalog if row["pattern_id"] == key)
            count = card.get("canonical_video_count", 0)
            index_html += (
                f'<li id="print-pattern-{e(key)}"><strong>{e(lesson["title"])}</strong> '
                f'<p><strong>Main point:</strong> {e(lesson["principle"])}</p>'
                f'<p><strong>When it may help:</strong> {e(lesson["problem"])}</p>'
                f'<p><strong>How to try it:</strong> {e(lesson["transfer"])}</p>'
                f'<div class="source-example"><p><strong>Source example — {e(lesson["source_title"])}</strong></p>'
                '<p>Summary of the linked transcript analysis.</p>'
                + ''.join(f'<p>{e(paragraph)}</p>' for paragraph in PUBLIC_SOURCE_READINGS[key])
                + '</div>'
                f'<p><strong>Invented practice example — {e(lesson["worked_title"])}.</strong></p>'
                f'<p><strong>Before:</strong> {e(lesson["before"])}</p>'
                f'<p><strong>After:</strong> {e(lesson["after"])}</p>'
                f'<p><strong>Why this change may help:</strong> {e(lesson["worked_explanation"])}</p>'
                f'<p><strong>Ways to adapt it:</strong></p><ul>{"".join("<li>" + e(variation) + "</li>" for variation in lesson["variations"])}</ul>'
                f'<p><strong>Try it:</strong> {e(lesson["exercise"])}</p>'
                f'<p><strong>Check:</strong> {e(lesson["self_check"])}</p>'
                f'<div class="pattern-source-tail"><p><strong>Limit:</strong> {e(lesson["failure_case"])}</p>'
                f'<p class="source-note">Search returned records in {count} videos; not independently confirmed. '
                f'<a href="../{e(lesson["source_writeup"], quote=True)}">Source note</a>; {e(lesson["source_passages"])}</p>'
                f'<p class="source-note">Video at saved caption start times: {video_links_html(source_video_links[key])}. Timing has not been checked against the recording.</p></div></li>'
            )
            manuscript_index.extend([
                f'<a id="pattern-{key}"></a>\n#### {lesson["title"]}',
                f'**Main point:** {lesson["principle"]}',
                f'**When it may help:** {lesson["problem"]}',
                f'**How to try it:** {lesson["transfer"]}',
                f'**Source example — {lesson["source_title"]}**',
                'Summary of the linked transcript analysis.',
                *PUBLIC_SOURCE_READINGS[key],
                f'**Invented practice example — {lesson["worked_title"]}**',
                f'**Before:** {lesson["before"]}',
                f'**After:** {lesson["after"]}',
                f'**Why this change may help:** {lesson["worked_explanation"]}',
                '**Ways to adapt it:**',
                '\n'.join(f'{index}. {variation}' for index, variation in enumerate(lesson["variations"], 1)),
                f'**Try it:** {lesson["exercise"]}',
                f'**Check:** {lesson["self_check"]}',
                f'**Limit:** {lesson["failure_case"]}',
                f'**Search matches:** {count} videos. No one has checked every match.',
                f'[Source analysis]({Path(lesson["source_writeup"]).name}) — {lesson["source_passages"]}',
                'Video links use the saved start time for each cited caption range; the recording was not checked here: '
                + ', '.join(f'[{link["time"]}]({link["url"]})' for link in source_video_links[key]) + '.',
            ])
        index_html += '</ul>'
    index_html += '</section>'
    chapters += index_html
    chapters += book_section('worked-presentation', 'Put the pieces together: a full example', WORKED_PRESENTATION)
    chapters += book_section('closing-note', 'Your next draft', CONCLUSION)
    chapters += book_section('companion-guides', 'How this book connects to Charisma on Command', COMPANION_GUIDE)
    crosswalk_intro = ('Each entry is an editor’s comparison. “Close fit” means both guides address much the same speaking problem. '
                       '“Related, but different” means they overlap but should not be treated as the same lesson. '
                       '“Not covered here” means the 55 patterns do not directly address that approach.')
    crosswalk_sections = []
    for number, title, fit, pattern_ids, reason in COMPANION_CROSSWALK:
        related = ', '.join(
            f'[{LESSONS[pattern_id]["title"]}](#pattern-{pattern_id})' for pattern_id in pattern_ids
        ) or 'No direct match in the 55 patterns.'
        companion_chapter = f'[{number:02d}. {title}](companion/speaking-practice.html#chapter-{number:02d})'
        crosswalk_sections.append((f'{number:02d}. {title} — {fit}', [
            reason,
            'Companion chapter: ' + companion_chapter,
            'Related patterns: ' + related,
        ]))
    chapters += book_section('companion-crosswalk', 'All 27 approaches: where they connect', [("How to read this list", [crosswalk_intro]), *crosswalk_sections])
    source_paths = sorted({lesson['source_writeup'] for lesson in LESSONS.values()})
    source_notes = [
        'Source readings summarize local transcript analyses in the editors’ words. They are not verified quotations or recordings of the original events. Each analysis describes what is known and what is missing. Using one source in several lessons does not count as several independent examples.',
        'Scripted film scenes are treated as constructed dialogue. The historical composite is treated as a composite text, not a verified original voice. Real-address and interview accounts remain attributed reports; this book does not verify every biographical, institutional or outcome claim.',
        'No source audio, video, photographs, song lyrics or full speech texts are reproduced in this fieldbook. Speaker names identify the analyzed material and do not imply endorsement. The practice scripts and explanations are original teaching material. This attribution note is not a claim of publication-rights clearance.',
    ]
    source_entries = []
    for source_path in source_paths:
        title = (ROOT / source_path).read_text().splitlines()[0].removeprefix('# ')
        kind = ('Scripted fiction' if 'scene-' in source_path else
                'Historical composite text' if 'historical-' in source_path else
                'Interview transcript analysis' if 'interview-' in source_path else
                'Address transcript analysis')
        source_entries.append((source_path, title, kind))
    chapters += book_section('source-notes', 'Sources and notes', [('How to read the source references', source_notes)])
    chapters += '<ul class="source-index">' + ''.join(f'<li><a href="../{html.escape(path)}">{html.escape(title)}</a><br><span class="source-note">{kind}</span></li>' for path, title, kind in source_entries) + '</ul>'
    document = document.replace("__FIELD_BOOK_CONTENT__", chapters)
    document = document.replace("Read the <a href='external-review-launch-manifest.md'>validation boundary</a> for the independent evidence still required.", "Read the <a href='#source-notes'>source and attribution notes</a> for the limits of these readings.")
    document = document.replace("<section class='catalog'>", "<section class='catalog' id='pattern-catalog'>")
    document = document.replace('</style>', '''
.chapter{max-width:780px;margin:48px auto 72px;font-size:1.08rem}
header .nav{flex-wrap:wrap}.grid{grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr))}.case-grid{grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))}
@media(max-width:760px){.part-heading h2{font-size:1.5rem;overflow-wrap:anywhere}}
.source-index{max-width:780px;margin:0 auto 60px}.source-index li{margin-bottom:16px;break-inside:avoid}
@media print{body{background:#fff!important}.footer-note{display:none}.reading-route,.pattern-source-tail{break-inside:avoid}.source-example>p:first-child,.source-example>p:nth-child(2){break-after:avoid}.chapter p,.book-section p{orphans:3;widows:3}.part-heading + .chapter{break-before:auto}}
.part-heading{margin:64px 0 24px;padding:28px;color:#fff;background:#17324d}.part-heading h2{font-size:2rem;margin:0 0 12px}.part-heading p{max-width:760px;margin:0}
@media print{header.part-heading{display:block!important;background:none;color:#192126;border-bottom:1px solid #aaa;break-before:page;break-after:avoid}}
.book-section{max-width:780px;margin:48px auto 72px;font-size:1.08rem}.book-section h2{font-size:2.4rem;line-height:1.2}.book-section h3{margin-top:32px;font-size:1.5rem}@media print{.book-section{break-before:page;font-size:11pt}.book-section h2,.book-section h3{break-after:avoid}}
.job-chapter{border-top:3px solid var(--coral);padding-top:28px}.job-chapter h2{font-size:2.4rem;line-height:1.15}.job-chapter h3{font-size:1.45rem;margin-top:32px}.source-case{border-left:4px solid var(--blue);padding:2px 20px;margin:26px 0}.job-question,.index-note{background:#fff5dc;padding:16px 20px}.pattern-links{font-size:.92rem;color:var(--muted)}.print-index{display:none}.print-index li{margin:0 0 22px}.print-index li p{margin:4px 0}
.theme-overview{max-width:780px;margin:48px auto 72px}.theme-overview .theme-item{border-top:1px solid var(--line);padding:12px 0 20px;break-inside:avoid}.theme-overview .theme-item h3{margin:16px 0 8px;font-size:1.4rem}.theme-overview .theme-item p{margin:8px 0}
.subtheme-overview .subtheme-group{margin:38px 0}.subtheme-overview .subtheme-group>h3{font-size:1.8rem}.subtheme-overview .theme-item h4{font-family:Georgia,'Times New Roman',serif;font-size:1.25rem;margin:12px 0}.subtheme-overview .theme-item p{font-size:.98rem}
@media print{.print-index{display:block!important;break-before:page;max-width:780px;margin:0 auto;font-size:9.5pt}.catalog{display:none!important}.job-chapter{break-before:page}.core-chapters{display:block}.chapters>nav{display:block}.chapters>nav ol{columns:2;column-gap:32px;margin:20px 0 0;padding-left:24px}.chapters>nav li{break-inside:avoid;margin:0 0 10px}.chapters>nav a{text-decoration:none}}
.chapter h3{font-size:2.2rem;line-height:1.2}.chapter h4{margin:30px 0 10px;font-size:1.2rem}
.chapter h5{font-size:1rem;margin:0}.source-note{font-size:.88rem;color:#52616a}
.chapter-return{font-size:.9rem}#lesson-contents{display:grid;grid-template-columns:1fr 1fr;gap:24px}.reading-route{border-top:2px solid #d66b4e;padding:12px 0}.reading-route h3{font-size:1.5rem;margin:4px 0}.reading-route p{font-size:.95rem}#lesson-contents li{break-inside:avoid;margin-bottom:10px}a:focus-visible,button:focus-visible{outline:3px solid #d66b4e;outline-offset:4px}
.before-after{display:grid;grid-template-columns:1fr 1fr;gap:20px;background:#edf2f4;padding:22px}
dialog{max-width:760px;width:calc(100% - 32px);max-height:85vh;overflow:auto;border:1px solid #cfcac1;border-radius:8px;padding:24px}
dialog::backdrop{background:#17324d99}dialog h2{font-size:1.8rem}dialog button{font:inherit;padding:8px 16px}
@media(max-width:760px){.before-after{grid-template-columns:1fr}.chapter h3{font-size:1.7rem}#lesson-contents{grid-template-columns:1fr}}
@media print{header,.featured,.catalog,dialog,.chapter-return{display:none!important}.hero{background:none!important;color:#192126;padding:0}.hero p{color:#192126;font-size:11pt;line-height:1.4;margin:4px 0}.hero h1{font-size:36pt;margin:8px 0 12px}.facts{display:none!important}.wrap{max-width:none;padding:0}.chapter{break-before:page;margin:0;max-width:none;font-size:11pt}.chapter h3{font-size:24pt}.chapter h4,.chapter h5{break-after:avoid}.before-after{display:block;background:none;border:1px solid #aaa}.before-after>div+div{margin-top:14px}.source-note{font-size:9pt}.intro{display:block;margin-bottom:8px}a{color:inherit}main{padding:0}@page{margin:20mm}}
</style>''')
    document = document.replace("<script id='fieldbook-data'", '<dialog id="move-dialog" aria-labelledby="move-title"><button id="close-move" type="button">Close</button><div id="move-content"></div></dialog><script id=\'fieldbook-data\'')
    OUTPUT.write_text(document)
    manuscript = [
        '# The Speaking Patterns Fieldbook',
        '## A practical guide to speaking clearly',
            'Seven chapters address common speaking problems. The index groups 55 ideas into 22 main themes, 18 smaller speaking moves and 15 more ideas to explore. Each entry links to its example and practice task. These are ideas to try, not proven rules.',
        'The examples in this book come from 17 selected transcript analyses. The larger project has reviewed the full transcripts of 395 of the 480 videos in its inventory. This book does not recheck all 395. Other reviewers have not checked these readings, and no audience study has tested the advice. Source examples summarize transcripts; they are not exact quotations. Caption numbers mark text order, not video time.',
    ]
    for title, paragraphs in INTRODUCTION:
        manuscript.extend(['## ' + title, *paragraphs])
    manuscript.append('## Seven speaking jobs')
    for chapter in JOB_CHAPTERS:
        manuscript.extend([
            '### ' + chapter["title"],
            '**Ask:** ' + chapter["question"],
            '#### Main point', chapter["principle"],
            '#### A way to do it', '\n'.join(f'{index}. {step}' for index, step in enumerate(chapter["method"], 1)),
        ])
        for example_key in chapter["example_keys"]:
            lesson = LESSONS[example_key]
            manuscript.extend([
                '#### ' + lesson["source_title"],
                'Paraphrase of the linked transcript analysis; not a quotation.',
                *PUBLIC_SOURCE_READINGS[example_key],
                f'[Read the source analysis]({Path(lesson["source_writeup"]).name}). {lesson["source_passages"]}',
            ])
        manuscript.extend([
            '#### What this example does not show', chapter["boundary"],
            '#### Invented failure case', 'This situation is made up for practice; it is not a finding from the videos.', chapter["failure_case"],
            '#### Try it', chapter["exercise"],
            '#### Check your draft', chapter["check"],
            '**Related patterns:** ' + ', '.join(LESSONS[key]['title'] for key in chapter["pattern_ids"]),
        ])
    manuscript.extend(manuscript_themes)
    manuscript.extend(manuscript_subthemes)
    manuscript.extend(manuscript_index)
    for heading, sections in [('Put the pieces together: a complete presentation', WORKED_PRESENTATION), ('Your next draft', CONCLUSION), ('How this book connects to Charisma on Command', COMPANION_GUIDE)]:
        manuscript.append('## ' + heading)
        for title, paragraphs in sections:
            manuscript.extend(['### ' + title, *paragraphs])
    manuscript.extend(['## All 27 approaches: where they connect', crosswalk_intro])
    for number, title, fit, pattern_ids, reason in COMPANION_CROSSWALK:
        manuscript.extend([
            f'### {number:02d}. {title} — {fit}',
            reason,
            f'Companion chapter: [{number:02d}. {title}](companion/speaking-practice.html#chapter-{number:02d})',
            'Related patterns: ' + (', '.join(
                LESSONS[pattern_id]["title"] for pattern_id in pattern_ids
            ) or 'No direct match in the 55 patterns.'),
        ])
    manuscript.extend(['## Sources and notes', *source_notes,
                       '\n'.join(f'- [{title}]({Path(path).name}) — {kind}.' for path, title, kind in source_entries)])
    OUTPUT.with_suffix('.md').write_text('\n\n'.join(manuscript) + '\n')
    print(f"professional fieldbook: {len(JOB_CHAPTERS)} job chapters, {len(items)} research index entries")
    return 0


def render(data: str) -> str:
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<meta name='description' content='Seven presentation chapters, 22 main themes, 33 smaller speaking moves, examples and exercises.'>
<title>The Speaking Patterns Fieldbook</title><style>
:root{{--ink:#192126;--muted:#657078;--paper:#fbfaf7;--card:#fff;--line:#e4e0d8;--navy:#17324d;--coral:#d66b4e;--gold:#d9a441;--blue:#2c668d}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,sans-serif}}a{{color:var(--blue)}}.serif,h1,h2,h3{{font-family:Georgia,'Times New Roman',serif;letter-spacing:-.02em}}.wrap{{max-width:1180px;margin:auto;padding:0 24px}}header{{background:var(--navy);color:#fff;padding:22px 0;border-bottom:5px solid var(--coral)}}header .nav{{display:flex;justify-content:space-between;gap:20px;align-items:center}}header a{{color:#fff;text-decoration:none;font-weight:700}}.eyebrow,.tag{{color:var(--gold);text-transform:uppercase;letter-spacing:.12em;font-size:.74rem;font-weight:800}}.hero{{padding:78px 0 65px;background:linear-gradient(135deg,#17324d 0%,#254f69 58%,#d66b4e 160%);color:#fff}}.hero h1{{font-size:clamp(2.8rem,7vw,6.6rem);line-height:.98;max-width:900px;margin:16px 0 25px}}.hero p{{font-size:1.2rem;max-width:720px;color:#e8eef0}}.hero .facts{{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}}.fact{{border:1px solid #ffffff45;background:#ffffff12;border-radius:99px;padding:8px 15px}}main{{padding:45px 0 90px}}.intro{{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:start;margin-bottom:55px}}.intro h2{{font-size:2.4rem;margin-top:0}}.note{{background:#fff5dc;border-left:5px solid var(--gold);padding:19px 22px;border-radius:4px}}.featured{{margin:40px 0 68px}}.featured h2,.catalog h2{{font-size:2.5rem}}.case-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}.case{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--coral);padding:24px;border-radius:5px;box-shadow:0 7px 20px #17324d0b}}.case h3{{font-size:1.45rem;margin:9px 0}}.case .principle{{font-size:1.03rem}}.case details{{margin-top:14px}}summary{{cursor:pointer;color:var(--blue);font-weight:750}}.case .label{{color:var(--coral);font-weight:800;font-size:.78rem;text-transform:uppercase;letter-spacing:.07em}}.controls{{position:sticky;top:0;z-index:3;background:#fbfaf7ee;backdrop-filter:blur(10px);padding:15px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:flex;gap:10px;flex-wrap:wrap}}input,select{{font:inherit;padding:11px 13px;border:1px solid #cfcac1;border-radius:4px;background:#fff}}#search{{flex:1;min-width:250px}}.catalog-head{{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-top:20px}}.catalog-head p{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:15px}}.card{{background:#fff;border:1px solid var(--line);border-radius:5px;padding:20px;min-height:245px;display:flex;flex-direction:column}}.card h3{{font-size:1.25rem;margin:7px 0}}.card .form{{color:var(--blue);font-weight:650}}.card .use{{color:var(--muted);font-size:.93rem}}.card button{{margin-top:auto;align-self:start;border:0;background:var(--navy);color:#fff;padding:9px 12px;border-radius:4px;cursor:pointer;font:inherit}}.card[hidden]{{display:none}}.footer-note{{margin-top:55px;border-top:1px solid var(--line);padding-top:22px;color:var(--muted);font-size:.9rem}}@media(max-width:760px){{.intro{{grid-template-columns:1fr}}.hero{{padding-top:55px}}.catalog-head{{display:block}}}}
</style><style>@media(max-width:760px){{.hero h1{{overflow-wrap:anywhere}}}}</style></head><body id='top'><header><div class='wrap nav'><a href='#top'>Clear speaking, in practice</a><span>The Speaking Patterns Fieldbook</span></div></header>
<section class='hero'><div class='wrap'><div class='eyebrow'>A practical guide to clearer presentations</div><h1>Plan a clearer presentation.</h1><p>Use these seven chapters to explain ideas, tell useful stories, answer hard questions and make clear requests. The index groups 55 ideas into 22 main themes and 33 smaller patterns. Examples come from 17 selected transcript analyses. The wider project has full transcript reviews of 395 of its 480 videos, but this book does not repeat that review. No outside reviewer or listener study has tested these ideas.</p><div class='facts'><span class='fact'>7 practical chapters</span><span class='fact'>22 main themes</span><span class='fact'>33 smaller patterns</span><span class='fact'>17 source analyses</span></div></div></section>
<main><div class='wrap'><section class='intro'><div><h2>Try the move in your own words.</h2><p>Use this book to make your point clearer, explain an unfamiliar idea, answer a hard question or give your audience a useful next step.</p><p>The examples show possible choices, not a style to copy. Use facts you can support and language that sounds like you.</p></div><div class='note'><b>How to use this book</b><ol><li>Name what you want your audience to understand or do.</li><li>Choose one of the seven chapters that fits that job.</li><li>Read the source example and its limits.</li><li>Try the idea with your own facts, then check what a listener understood.</li></ol></div></section>
<section class='core-chapters'><div id='core-chapters-container'>__FIELD_BOOK_CONTENT__</div></section>
<section class='catalog' id='pattern-catalog'><div class='eyebrow'>Pattern list</div><div class='catalog-head'><h2>55 speaking patterns—not 55 proven rules</h2><p id='count'></p></div><p class='index-note'>These are possible patterns noticed in transcript searches. The counts are search matches, not checked examples. Open an entry for a plain-language explanation, a made-up before-and-after example, a practice task and source notes.</p><div class='controls'><input id='search' type='search' placeholder='Search patterns, examples or presentation problems'><select id='category'><option value=''>All patterns</option><option value='core_theme'>Main themes</option><option value='structural_subtheme'>Structure patterns</option><option value='additional_subtheme'>Other patterns</option></select></div><div id='cards' class='grid'></div></section><p class='footer-note'>Other reviewers have not checked this advice, and we have not tested it with audiences. A pattern appearing often in search results does not show that it caused a response or will work in every setting. Read <a href='fieldbook-editorial-handoff.md'>what still needs review</a> for details.</p></div></main>
<script id='fieldbook-data' type='application/json'>{data}</script><script>
const model=JSON.parse(document.getElementById('fieldbook-data').textContent),cards=document.getElementById('cards'),count=document.getElementById('count'),search=document.getElementById('search'),category=document.getElementById('category');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
const categoryName=v=>({{core_theme:'Main theme',structural_subtheme:'Structure pattern',additional_subtheme:'Other pattern'}}[v]||'Pattern');
function renderCards(){{const q=search.value.toLowerCase().trim(),g=category.value,rows=model.items.filter(x=>(!g||x.category===g)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));count.textContent=rows.length+' of '+model.items.length+' labels';cards.innerHTML=rows.map(x=>'<article class="card" id="pattern-'+esc(x.pattern_id)+'"><div class="tag">'+esc(categoryName(x.category))+'</div><h3>'+esc(x.title)+'</h3><p class="form">'+esc(x.candidate_form)+'</p><p class="use"><a href="#job-'+esc(x.job_id)+'">Chapter: '+esc(x.job_title)+'</a></p><p class="source-note">The search returned matches in '+x.retrieved_video_count+' videos. Reviewers have not checked these matches.</p><button data-id="'+esc(x.pattern_id)+'">Open details</button></article>').join('')}}
const dialog=document.getElementById('move-dialog');
cards.addEventListener('click',event=>{{
  const button=event.target.closest('button[data-id]');if(!button)return;
  const item=model.items.find(x=>x.pattern_id===button.dataset.id);if(!item)return;
  document.getElementById('move-content').innerHTML='<h2 id="move-title">'+esc(item.title)+'</h2><p><strong>In plain language:</strong> '+esc(item.candidate_form)+'</p><p><strong>Chapter:</strong> <a href="#job-'+esc(item.job_id)+'">'+esc(item.job_title)+'</a></p><h3>When it may help</h3><p>'+esc(item.use_when)+'</p><h3>How to try it</h3><p>'+esc(item.how_to_use)+'</p><h3>Practice example—made up for this book</h3><p><strong>'+esc(item.worked_title)+'</strong></p><h4>Before</h4><blockquote>'+esc(item.before)+'</blockquote><h4>After</h4><blockquote>'+esc(item.after)+'</blockquote><p><strong>Why this change may help:</strong> '+esc(item.worked_explanation)+'</p><h3>Ways to adapt it</h3><ul>'+item.variations.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul><h3>Try it yourself</h3><p>'+esc(item.exercise)+'</p><h3>Check your draft</h3><p>'+esc(item.practice_check)+'</p><h3>Limit</h3><p>'+esc(item.safety_boundary)+'</p><h3>Search result—not a confirmed example</h3><p>The search returned matches in '+item.retrieved_video_count+' videos. Reviewers have not checked these matches.</p><h3>Source passage</h3><p>'+esc(item.source_label)+'</p><p><a href="../'+esc(item.source_writeup)+'">Read the source analysis</a></p><p>'+esc(item.source_passages)+'</p><h3>Watch the cited passages</h3><ul>'+item.source_video_links.map(link=>'<li><a href="'+esc(link.url)+'">'+esc(link.time)+' (captions '+esc(link.caption_range)+')</a></li>').join('')+'</ul><p>The links use saved caption times; the recording was not checked here to confirm the captions or timing.</p>';
  const practiceHeading=Array.from(document.querySelectorAll('#move-content h3')).find(h=>h.textContent==='Practice example—made up for this book');
  practiceHeading.insertAdjacentHTML('beforebegin','<section class="source-example"><h3>Source example</h3><p><strong>'+esc(item.source_label)+'</strong></p><p>Summary of the linked transcript analysis.</p>'+item.source_example.map(paragraph=>'<p>'+esc(paragraph)+'</p>').join('')+'</section>');
  dialog.showModal();
}});
document.getElementById('close-move').onclick=()=>dialog.close();
search.setAttribute('aria-label','Search the 55 speaking patterns');category.setAttribute('aria-label','Filter speaking patterns by type');
search.oninput=renderCards;category.onchange=renderCards;renderCards();</script></body></html>"""


if __name__ == "__main__":
    raise SystemExit(main())
