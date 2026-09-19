#!/usr/bin/env python3
"""Build one evidence-linked catalog of the corpus findings and usable lessons."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text())


def clip(text: str, size: int = 280) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= size else text[: size - 1].rstrip() + "…"


def evidence_text(example: dict) -> str:
    return " ".join(s.get("text", "") for s in example.get("exact_segments", []))


def build() -> tuple[dict, str]:
    reviews = load("research/full-context-reviews.json")["reviews"]
    lessons = load("research/corpus-lesson-index.json")["entries"]
    cards = load("research/communication-job-cards.json")["cards"]
    phrases = load("research/corpus-phrase-form-inventory.json")["forms"]
    evidence = load("research/corpus-evidence-bank.json")["records"]

    lesson_by_review = {x["review_id"]: x for x in lessons}
    evidence_by_job: dict[str, list[dict]] = defaultdict(list)
    for row in evidence:
        evidence_by_job[row.get("canonical_job", "unclassified")].append(row)

    rows = []
    for review in reviews:
        lesson = lesson_by_review[review["review_id"]]
        functions = lesson.get("communication_function_inventory", [])
        relations = lesson.get("structural_relation_inventory", [])
        rows.append({
            "review_id": review["review_id"],
            "video_id": review["video_id"],
            "title": lesson.get("title", review["video_id"]),
            "video_url": lesson.get("video_url"),
            "writeup": lesson.get("writeup"),
            "modality": review.get("modality"),
            "coverage": review.get("coverage"),
            "observed_functions": functions,
            "observed_relations": relations,
            "boundary_cases": lesson.get("boundary_cases", review.get("boundary_cases", [])),
            "limits": lesson.get("limits", review.get("limits", [])),
            "next_test": lesson.get("next_test", review.get("next_test")),
            "evidence_ids": review.get("context_evidence_ids", []),
        })

    job_rows = []
    for card in cards:
        job = card["canonical_job"]
        examples = []
        for example in card.get("exact_examples", [])[:3]:
            examples.append({
                "record_id": example.get("record_id"),
                "video_id": example.get("video_id"),
                "title": example.get("title"),
                "source_url": example.get("source_url"),
                "function_label": evidence_by_job.get(job, [{}])[0].get("raw_function_label") if evidence_by_job.get(job) else None,
                "evidence_ids": [s.get("evidence_id") for s in example.get("exact_segments", [])],
                "caption_text": evidence_text(example),
            })
        job_rows.append({
            "job": job,
            "status": card.get("status"),
            "problem": card.get("problem"),
            "mechanism_hypothesis": card.get("mechanism"),
            "copyable_form": card.get("form"),
            "practice": card.get("practice"),
            "self_check": card.get("self_check"),
            "non_fit": card.get("non_fit"),
            "recurrence": card.get("recurrence"),
            "phrase_forms": card.get("phrase_forms", []),
            "examples": examples,
        })

    function_counts = Counter()
    relation_counts = Counter()
    for row in rows:
        function_counts.update(x.get("function", x.get("label", "unlabelled")) for x in row["observed_functions"])
        relation_counts.update(x.get("type", "unlabelled") for x in row["observed_relations"])

    result = {
        "schema_version": "1.0",
        "catalog_id": "corpus-findings-catalog",
        "status": "transcript_derived_findings_with_provisional_practice_hypotheses",
        "claim_boundary": "The per-video rows are actual recorded transcript observations linked to retained evidence and writeups. Copyable forms and mechanism statements are provisional learning hypotheses; they do not establish delivery effects, listener outcomes, teachability or best-practice status.",
        "coverage": {"review_count": len(rows), "function_observation_count": sum(function_counts.values()), "relation_observation_count": sum(relation_counts.values()), "phrase_form_count": len(phrases)},
        "how_to_use": [
            "Start with a job card for a speech task you need tomorrow.",
            "Read its exact caption examples and linked writeups before copying the form.",
            "Use the 395-row index to compare the same move across different talks.",
            "Treat why-it-may-work language as a hypothesis and test it with a listener.",
            "Do not infer nonverbal behavior, effectiveness or factual truth from transcript-only evidence.",
        ],
        "job_findings": job_rows,
        "phrase_forms": phrases,
        "function_counts": function_counts,
        "relation_counts": relation_counts,
        "video_findings": rows,
    }
    result["function_counts"] = dict(function_counts.most_common())
    result["relation_counts"] = dict(relation_counts.most_common())

    lines = [
        "# Corpus findings catalog: what was actually observed and what to use",
        "",
        "Status: **395 transcript-derived findings, with provisional practice hypotheses**.",
        "",
        result["claim_boundary"],
        "",
        f"Coverage: **{len(rows)} videos**, **{result['coverage']['function_observation_count']:,} function observations**, **{result['coverage']['relation_observation_count']:,} structural relations**, and **{len(phrases)} exact phrase-form hypotheses**.",
        "",
        "This is the concrete answer to ‘what did the corpus teach us?’ Each job below gives a usable speech form, the reason it may help, a practice drill, exact retained-caption examples, and a boundary. Each video row then exposes the actual functions, relations, limits and next test recorded during its full-context review.",
        "",
        "## How to use this tomorrow",
        "",
        "1. Pick the job matching the moment: open, explain, disagree, ask, tell a story, repair, or close.",
        "2. Say the copyable form once in your own words; do not imitate the speaker’s identity or accent.",
        "3. Record a 60–120 second attempt, then ask one listener what they understood and where they lost the thread.",
        "4. Keep the move only if it improves clarity without making the claim stronger than the evidence.",
        "",
        "## 18 usable speech jobs, with actual corpus examples",
        "",
    ]
    for job in job_rows:
        lines += [f"### `{job['job']}`", "", f"**What it solves:** {job['problem']}", "", f"**Why it may work:** {job['mechanism_hypothesis']}", "", f"**Copyable form:** {job['copyable_form']}", "", f"**Practice:** {job['practice']}", "", f"**Self-check:** {job['self_check']}", "", f"**Do not force it when:** {job['non_fit']}", ""]
        if job["examples"]:
            lines += ["**Retained-caption examples:**", ""]
            for ex in job["examples"]:
                lines.append(f"- [{ex['video_id']}]({ex['source_url']}) — {clip(ex['caption_text'])} (`{', '.join(ex['evidence_ids'])}`)")
            lines.append("")

    lines += ["## Exact phrase forms: frequency is not effectiveness", "", "These are retrieval signals found in retained captions. They help locate examples; they do not prove that a phrase causes trust, clarity or persuasion.", "", "| Form | Family | Occurrences | Videos | Holdout videos |", "|---|---:|---:|---:|---:|"]
    for p in phrases:
        lines.append(f"| `{p.get('phrase_form', p.get('form', ''))}` | {p.get('family', p.get('candidate_label', ''))} | {p.get('occurrence_count', p.get('occurrences', 0)):,} | {p.get('video_count', 0):,} | {p.get('holdout_video_count', 0):,} |" )

    lines += ["", "## Video-by-video findings (all 395 reviews)", "", "Every row below is a recorded observation, not an invented summary. Open the linked writeup and evidence IDs for the full context.", "", "| # | Video / writeup | Observed functions | Structural relations | Limits / next test |", "|---:|---|---|---|---|"]
    for i, row in enumerate(rows, 1):
        fs = "; ".join(clip(x.get("function", x.get("label", "")), 90) for x in row["observed_functions"][:5]) or "none recorded"
        rs = "; ".join(clip(x.get("type", ""), 70) for x in row["observed_relations"][:4]) or "none recorded"
        lim = clip(" ".join(row["limits"][:2]), 180) if row["limits"] else clip(row.get("next_test") or "see writeup", 180)
        title = clip(row["title"], 90)
        lines.append(f"| {i} | [{title}](../{row['writeup']}) `{row['video_id']}` | {fs} | {rs} | {lim} |")

    lines += ["", "## Aggregate recurrence snapshot", "", "The counts below are inventory counts, not denominators of effective speaking:", "", "### Most frequent recorded function labels", ""]
    lines += [f"- `{k}` — {v}" for k, v in function_counts.most_common(30)]
    lines += ["", "### Most frequent recorded structural relations", ""]
    lines += [f"- `{k}` — {v}" for k, v in relation_counts.most_common(30)]
    lines += ["", "## What is still not established", "", "The corpus has not yet established which moves work best, whether delivery changes the effect, whether learners can perform them, or whether listeners experience better outcomes. Those require independent function/recurrence review, audiovisual delivery review, learner records and locked listener stimulus tests. Keep those claims separate from this catalog.", ""]
    return result, "\n".join(lines)


def main() -> int:
    result, markdown = build()
    (ROOT / "research/corpus-findings-catalog.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "writeups/corpus-findings-catalog.md").write_text(markdown)
    print(json.dumps({"review_count": result["coverage"]["review_count"], "job_count": len(result["job_findings"]), "phrase_count": result["coverage"]["phrase_form_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
