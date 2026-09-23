#!/usr/bin/env python3
"""Build one honest source map for the speech and humor repositories."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS_ROOT = ROOT.parent / "speaking-humor-and-communication-concepts-research"
ATLAS_STATUS = ATLAS_ROOT / "analysis/source-corpus-status.json"
ATLAS_JOBS = ATLAS_ROOT / "analysis/source-to-job-crosswalk.json"
ATLAS_WAVE2 = ATLAS_ROOT / "analysis/wave-2-unified-candidate-crosswalk.json"
ATLAS_COMPANION_SOURCES = ATLAS_ROOT / "deliverables/speaking-practice/sources.json"
ATLAS_COMPANION_CHAPTERS = ATLAS_ROOT / "writeups/speaking-practice"
LOCAL_WAVE2 = ROOT / "research/wave-2-unified-candidate-crosswalk.json"
OUTPUT_JSON = ROOT / "research/cross-repo-communication-source-map.json"
OUTPUT_MD = ROOT / "writeups/cross-repo-communication-source-map.md"


def load(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def corpus_id(source: dict) -> str:
    status = source["status"]
    if status.startswith("ingested-as-"):
        return status.removeprefix("ingested-as-")
    return source["slug"]


def transcript_summary(corpus: str) -> dict:
    path = ATLAS_ROOT / "raw-material/youtube/transcripts" / corpus / "summary.json"
    if not path.is_file():
        return {"videos": 0, "available_transcripts": 0, "total_words": 0}
    return load(path)


def source_kind(category: str) -> str:
    return {
        "framework": "coaching and drills",
        "social": "social communication coaching",
        "storytelling": "storytelling coaching",
        "difficult-conversations": "conflict coaching",
        "conversation": "conversation coaching",
        "workplace": "workplace communication coaching",
        "examples": "speech examples and coaching",
        "humor": "humor coaching",
        "humor-storytelling": "stand-up storytelling",
        "humor-exemplars": "stand-up examples",
        "polished-talks": "polished public talks",
    }.get(category, category.replace("-", " "))


def companion_source_key(name: str) -> str:
    """Use the guide's channel labels, including its two name-order variants."""
    aliases = {
        "Communication Coach Alexander Lyon Videos": "Alexander Lyon Communication Coach",
    }
    return aliases.get(name, name.removesuffix(" Videos"))


def companion_chapters() -> dict[str, list[dict]]:
    """Return published guide chapters grouped by the source named in its trail."""
    sources = load(ATLAS_COMPANION_SOURCES)["sources"]
    titles = {}
    for path in ATLAS_COMPANION_CHAPTERS.glob("*.md"):
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.match(r"# (\d+) — (.+)", first_line)
        if match:
            titles[match.group(1)] = match.group(2)
    grouped: dict[str, list[str]] = {}
    for row in sources:
        grouped.setdefault(row["channel"], []).extend(row["chapters"])
    return {
        channel: [
            {
                "number": number,
                "title": titles[number],
                "href": f"companion/speaking-practice.html#chapter-{number}",
            }
            for number in sorted(set(numbers), key=int)
        ]
        for channel, numbers in grouped.items()
    }


def plain_best_for(corpus: str, fallback: str) -> str:
    known = {
        "ali-siddiq-wave-2": "long stories, escalation, callbacks, and point of view",
        "dry-bar-comedy-wave-2-starter": "premise, payoff, performer contrast, and audience awareness",
        "ted-wave-2-starter": "clear openings, explanations, story-to-point transitions, and endings",
        "stand-up-studios-wave-3-starter": "future humor comparison after more transcripts are available",
    }
    return known.get(corpus, fallback)


def integration_state(source: dict, corpus: str, candidate_counts: Counter, chapters: list[dict]) -> str:
    status = source["status"]
    if "insufficient-transcript" in status:
        return "Not included: too little transcript material."
    if candidate_counts[corpus]:
        return f"Shown as {candidate_counts[corpus]} provisional expansion candidates."
    if corpus.endswith("wave-1"):
        return (
            "Used directly in the companion guide."
            if chapters else
            "Available in the atlas; no published companion chapter yet."
        )
    return "In the source map only; no candidate has been promoted."


def main() -> int:
    status = load(ATLAS_STATUS)
    jobs = load(ATLAS_JOBS)
    atlas_wave2 = load(ATLAS_WAVE2)
    guide_chapters_by_channel = companion_chapters()
    local_wave2 = load(LOCAL_WAVE2)
    local_wave2_content = {key: value for key, value in local_wave2.items() if key != "local_snapshot"}
    if atlas_wave2 != local_wave2_content:
        raise ValueError("Local wave-2 snapshot does not match the humor repository crosswalk")

    jobs_by_corpus = {row["corpus_id"]: row for row in jobs["rows"]}
    candidate_counts = Counter(row["source"] for row in atlas_wave2["rows"])
    sources = []
    for source in status["sources"]:
        corpus = corpus_id(source)
        summary = transcript_summary(corpus)
        source_jobs = jobs_by_corpus.get(corpus, {})
        guide_chapters = guide_chapters_by_channel.get(companion_source_key(source["title"]), [])
        sources.append({
            "corpus_id": corpus,
            "source": source["title"],
            "kind": source_kind(source["category"]),
            "channel_videos_seen": source["videos_captured"],
            "starter_videos": summary["videos"],
            "transcripts_available": summary["available_transcripts"],
            "transcript_words": summary["total_words"],
            "jobs": source_jobs.get("jobs", source.get("recommended_strategy", "")),
            "best_for": plain_best_for(
                corpus, source_jobs.get("novelty_target", source["recommended_strategy"])
            ),
            "source_status": source["status"],
            "integration_state": integration_state(source, corpus, candidate_counts, guide_chapters),
            "provisional_candidate_count": candidate_counts[corpus],
            "companion_chapters": guide_chapters,
        })

    fixed = {
        "corpus_id": "fixed-speech-corpus",
        "source": "Best Speech Analysis fixed corpus",
        "kind": "addresses, interviews, memorials, and scripted scenes",
        "channel_videos_seen": 480,
        "starter_videos": 395,
        "transcripts_available": 395,
        "transcript_words": None,
        "jobs": ["seven presentation problems and 55 detailed pattern entries"],
        "best_for": "the main fieldbook and full-context source readings",
        "source_status": "fixed inventory; 395 full-context transcript reviews",
        "integration_state": "The fieldbook's main evidence layer.",
        "provisional_candidate_count": 55,
        "companion_chapters": [],
    }
    rows = [fixed, *sources]
    summary = {
        "fixed_corpus_inventory_videos": fixed["channel_videos_seen"],
        "fixed_corpus_full_context_reviews": fixed["transcripts_available"],
        "external_source_corpora": len(sources),
        "external_channel_inventory_videos": sum(row["channel_videos_seen"] for row in sources),
        "external_starter_videos": sum(row["starter_videos"] for row in sources),
        "external_transcripts_available": sum(row["transcripts_available"] for row in sources),
        "external_provisional_candidates": sum(candidate_counts.values()),
        "core_companion_corpora": sum(row["corpus_id"].endswith("wave-1") for row in sources),
        "core_corpora_with_published_companion_chapters": sum(bool(row["companion_chapters"]) for row in sources),
        "usable_expansion_corpora": sum(row["provisional_candidate_count"] > 0 for row in sources),
        "deferred_corpora": sum("Not included" in row["integration_state"] for row in sources),
    }
    payload = {
        "schema_version": "1.0",
        "purpose": "One navigation map for the fixed speech corpus and the separate speaking, humor, and communication atlas.",
        "claim_boundary": "A transcript count shows what text is available, not that a source has been independently reviewed, that a pattern recurs, or that advice works. Comedy, coaching, and polished talks stay separate from the fixed speech corpus.",
        "summary": summary,
        "sources": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# One map of the speech, humor, and communication sources",
        "",
        "This page joins two repositories without pretending they are one study.",
        "",
        "- **Fixed speech corpus:** 480 videos in the inventory; 395 have full-context transcript reviews. This is the main evidence layer for the fieldbook.",
        f"- **Communication and humor atlas:** {summary['external_source_corpora']} source corpora; {summary['external_transcripts_available']} available starter transcripts. These sources supply coaching, storytelling, humor, and polished-talk comparisons.",
        f"- **Expansion candidates:** {summary['external_provisional_candidates']} rows from Ali Siddiq, Dry Bar Comedy, and TED. They are visible as candidates, not added to the 55 fixed-corpus patterns.",
        "",
        "## How to read this map",
        "",
        "Do not add the two video counts together and call them one corpus. A coaching video teaches advice. A comedy set is a performance. A TED talk is a polished public talk. A source in the fixed corpus is a transcript review. Each can help with practice, but they answer different questions.",
        "",
        "| Source | Kind of material | Videos seen | Starter transcripts | Best used for | Published guide trail | Where it appears now |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        best_for = row["best_for"]
        if isinstance(best_for, list):
            best_for = "; ".join(best_for)
        guide_trail = "; ".join(
            f"[{chapter['number']}. {chapter['title']}]({chapter['href']})"
            for chapter in row["companion_chapters"]
        ) or "—"
        lines.append(
            f"| {row['source']} | {row['kind']} | {row['channel_videos_seen']} | "
            f"{row['transcripts_available']}/{row['starter_videos']} | {best_for} | {guide_trail} | {row['integration_state']} |"
        )
    lines += [
        "",
        "## What is already connected",
        "",
        f"The [Speaking Patterns Fieldbook](speaking-patterns-fieldbook.html) uses the fixed speech corpus for its 55 entries. The published companion guide has direct source trails for {summary['core_corpora_with_published_companion_chapters']} of the ten core communication-and-humor corpora; the table links every one of those chapters. The [unified pattern synthesis](unified-pattern-synthesis.md) also shows the 19 provisional Ali Siddiq, Dry Bar Comedy, and TED rows.",
        "",
        "## What is not yet connected",
        "",
        "The ten core channels are not merged into the fieldbook's 55-pattern count. The expansion rows have not had the independent context, transfer, learner, or listener checks needed for promotion. Stand-Up Studios has only one usable transcript out of a 22-video starter slice, so it is not a usable pattern source yet.",
        "",
        "## What to borrow from each kind of source",
        "",
        "- **Fixed speech corpus:** wording, structure, and limits from a full transcript review. It is the best place to start when drafting a presentation.",
        "- **Coaching channels:** drills and ways to practise. A coach's recommendation is not proof that the recommendation works for everyone.",
        "- **Comedy:** story shape, detail, contrast, timing, callback, and recovery. Do not copy teasing, stereotypes, conflict, or crowd treatment into a workplace or public presentation.",
        "- **TED and Toastmasters:** a comparison point for a prepared public talk. A polished performance does not prove that the same structure will work for a different topic or audience.",
        "",
        "## Where to start",
        "",
        "- **You are writing a talk:** start with the fieldbook. Use Toastmasters or TED only to compare a prepared opening, explanation, or ending.",
        "- **You need to tell a story:** start with the fieldbook's story chapter. Matthew Dicks can help you choose and shape the event; Ali Siddiq and Dry Bar can help you notice detail, escalation, and callback. Keep the comedy material as a structural example, not language to copy.",
        "- **You need to handle a difficult conversation:** start with Jefferson Fisher, Chad Littlefield, and the Charisma on Command companion chapters. Then write the exact question, limit, or next step in your own words.",
        "- **You need a clear workplace answer:** start with Alexander Lyon and Think Fast Talk Smart. Use the fieldbook to check whether your answer names the decision, the facts, and what remains unknown.",
        "- **You need to sound less rehearsed:** use Ultraspeaking and Vinh Giang for practice drills. Do not mistake a drill for evidence that a delivery style suits every audience.",
        "- **You want lightness or humor:** start with Andrew Tarvin's workplace-focused material. Use the comedy sources for structure and timing, then remove anything that depends on ridicule or private information.",
        "",
        "## The practical route",
        "",
        "Use the fieldbook when you are drafting a presentation. Use the companion guide when you need a drill for a specific situation. Use comedy only for structure, story detail, timing, callback, or recovery—not as a model for how to treat a coworker or audience member. Read the original source and its limits before borrowing any move.",
        "",
        "## Claim boundary",
        "",
        payload["claim_boundary"],
        "",
    ]
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)} and {OUTPUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
