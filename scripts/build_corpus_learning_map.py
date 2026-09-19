#!/usr/bin/env python3
"""Build a compact learner entry point from the corpus findings catalog."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/corpus-findings-catalog.json"
OUT = ROOT / "writeups/corpus-learning-map.md"


def clip(text: str, limit: int = 120) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def main() -> int:
    catalog = json.loads(SOURCE.read_text())
    coverage = catalog["coverage"]
    jobs = catalog["job_findings"]
    phrases = sorted(catalog["phrase_forms"], key=lambda x: (-x["video_count"], x["phrase_form"]))
    pairs = catalog["interesting_recurrence_findings"]["top_job_pairs"]
    videos = catalog["video_findings"]

    examples_by_job: dict[str, list[dict]] = {job["job"]: job["examples"] for job in jobs}
    video_by_job: dict[str, list[dict]] = {}
    for row in videos:
        for job in row.get("candidate_jobs", []):
            video_by_job.setdefault(job, []).append(row)

    lines = [
        "# Corpus learning map: start here",
        "",
        "Status: **395-video transcript synthesis with provisional practice hypotheses; not validated best practice**.",
        "",
        f"This is the short route into the full corpus: **{coverage['review_count']} videos**, **{coverage['function_observation_count']} recorded function observations**, **{coverage['relation_observation_count']} structural relations** and **{coverage['phrase_form_count']} exact phrase-form hypotheses**. Heuristic routing currently gives {coverage['videos_with_candidate_practice_job']} videos a provisional practice job; {coverage['videos_without_candidate_practice_job']} remain explicitly unclassified and should be read through their evidence, limits and next test rather than forced into a lesson.",
        "",
        "The catalog records what captions and full-context writeups contain. It does not prove that a phrase works, that a delivery feature caused an effect, or that a speaker's story is factually true.",
        "",
        "## The fastest way to use it",
        "",
        "1. Pick the communication problem, not a famous speaker.",
        "2. Read one exact example and its surrounding context.",
        "3. Rewrite the underlying move in your own words.",
        "4. Add the relevant evidence, condition, consent and limit.",
        "5. Try it in an accessible format and ask one listener to restate it.",
        "6. Keep the useful function, record the non-fit case and revise.",
        "",
        "## The most useful combinations to inspect",
        "",
        "These are same-video inventory combinations, not effectiveness results. The holdout count shows that the combination is not confined to the training split; it is not independent validation.",
        "",
        "| Combination | Videos | Holdout videos | Practical question |",
        "|---|---:|---:|---|",
    ]
    questions = {
        ("closing", "story_or_personal_experience"): "Does the story return to a bounded takeaway rather than end as decoration?",
        ("question", "story_or_personal_experience"): "Does the story answer or sharpen a real question, with an opt-out?",
        ("opening", "closing"): "Does the ending return to the initial orientation with a changed point or limit?",
        ("contrast_or_disagreement", "story_or_personal_experience"): "Does lived detail clarify a change in view without caricaturing the earlier view?",
        ("qualification_or_boundary", "story_or_personal_experience"): "Does the story carry a clear evidence or scope boundary?",
    }
    for pair in pairs[:10]:
        key = (pair["job_a"], pair["job_b"])
        question = questions.get(key, "What does the second move add, and what would count as a non-fit case?")
        lines.append(f"| `{pair['job_a']}` + `{pair['job_b']}` | {pair['shared_video_count']} | {pair['holdout_shared_video_count']} | {question} |")

    lines += ["", "## Exact phrase handles that are worth testing", "", "These are retrieval handles, not scripts. Read the context before adapting them; identical wording can do different jobs.", "", "| Form | Family | Videos | Occurrences | What to test |", "|---|---|---:|---:|---|"]
    phrase_questions = {
        "for example": "Does the case clarify the claim without pretending to prove prevalence?",
        "in other words": "Does the reformulation make the idea usable rather than merely louder?",
        "the point is": "Does the takeaway preserve the unresolved limit?",
        "what matters": "Does the priority follow from the preceding reasoning?",
        "rather than": "Is the contrast fair, or is it a false binary?",
        "i think": "Is the uncertainty attached to a claim and revision condition?",
        "it depends": "Are the actual conditions named?",
        "you can": "Is the listener given a feasible role rather than motivational pressure?",
        "let's": "Who shares the action, authority and cost?",
        "we need to": "Who is responsible, and what support is required?",
    }
    selected = []
    for phrase in phrases:
        if phrase["phrase_form"] in phrase_questions:
            selected.append(phrase)
    for phrase in selected:
        lines.append(f"| `{phrase['phrase_form']}` | `{phrase['family']}` | {phrase['video_count']} | {phrase['occurrence_count']} | {phrase_questions[phrase['phrase_form']]} |")

    lines += ["", "## Job-to-practice index", "", "| Job | Corpus examples | Provisional form | First practice move |", "|---|---:|---|---|"]
    for job in jobs:
        examples = examples_by_job.get(job["job"], [])
        examples_text = ", ".join(f"[{x['video_id']}]({x['source_url']})" for x in examples[:2]) or "none indexed"
        lines.append(f"| `{job['job']}` | {len(examples)} ({examples_text}) | {job['copyable_form']} | {job['practice']} |")

    lines += ["", "## How to inspect one video", "", "Choose any row in the [full corpus findings catalog](corpus-findings-catalog.md). Follow its linked writeup, exact evidence IDs, observed functions, structural relations, boundary cases, limits and next test. If it has no candidate job, that is an explicit research state—not evidence that the talk has no lesson.", "", "For vocal, visual and accessibility practice, use the [delivery learning guide](delivery-learning-guide.md). The current delivery layer is partial: raw media availability, derived proxies and internal frame notes are not independent nonverbal findings.", "", "## Claim ladder", "", "`transcript observation` → `function hypothesis` → `recurrence candidate` → `delivery observation` → `mechanism hypothesis` → `teachability evidence` → `listener outcome`", "", "The current map is strongest at the first two levels and provisional at the next three. Learner and listener tests remain required before calling any move a tested best practice.", ""]
    OUT.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "jobs": len(jobs), "phrases": len(selected), "pairs": min(10, len(pairs))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
