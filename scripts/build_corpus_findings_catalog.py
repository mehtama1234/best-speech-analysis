#!/usr/bin/env python3
"""Build one evidence-linked catalog of the corpus findings and usable lessons."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# Conservative discovery routing from explicitly named structural relations.
# These alternate routes are not semantic adjudications or validated labels.
STRUCTURAL_JOB_MAP = {
    "closes": {"closing"}, "releases": {"closing"},
    "returns": {"callback_or_repetition", "closing"},
    "reuses": {"callback_or_repetition"}, "reconnects": {"callback_or_repetition"},
    "reframes": {"correction_or_reframe"}, "redirects": {"correction_or_reframe"},
    "replaces": {"correction_or_reframe"}, "contradicts": {"contrast_or_disagreement"},
    "contrasts": {"contrast_or_disagreement"}, "grounds": {"example_or_case"},
    "concretizes": {"example_or_case"}, "humanizes": {"story_or_personal_experience"},
    "operationalizes": {"call_to_action_or_audience_role"},
    "commits": {"call_to_action_or_audience_role"},
    "promises": {"call_to_action_or_audience_role"}, "invites": {"question"},
    "explains": {"definition_or_explanation"}, "defines": {"definition_or_explanation"},
    "demystifies": {"definition_or_explanation"}, "translates": {"definition_or_explanation"},
    "questions": {"question"}, "answers": {"answer_or_response"}, "opens": {"opening"},
    "organizes": {"transition_or_structure"}, "prepares": {"transition_or_structure"},
    "bridges": {"transition_or_structure"}, "bounds": {"qualification_or_boundary"},
    "constrains": {"qualification_or_boundary"}, "calibrates": {"qualification_or_boundary"},
    "connects": {"transition_or_structure"}, "widens": {"reflection_or_value_frame"},
    "frames": {"reflection_or_value_frame"}, "makes_visible": {"definition_or_explanation"},
    "systematizes": {"definition_or_explanation"}, "teaches": {"definition_or_explanation"},
}


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
    taxonomy = load("research/corpus-function-taxonomy.json")["entries"]
    phrases = load("research/corpus-phrase-form-inventory.json")["forms"]
    evidence = load("research/corpus-evidence-bank.json")["records"]
    delivery = load("research/communication-job-delivery-internal-observations.json")["items"]
    comparison = load("research/communication-job-cross-comparison.json")

    lesson_by_review = {x["review_id"]: x for x in lessons}
    taxonomy_by_review = {x["review_id"]: x for x in taxonomy}
    card_by_job = {x["canonical_job"]: x for x in cards}
    evidence_by_job: dict[str, list[dict]] = defaultdict(list)
    for row in evidence:
        evidence_by_job[row.get("canonical_job", "unclassified")].append(row)

    rows = []
    for review in reviews:
        lesson = lesson_by_review[review["review_id"]]
        taxonomy_entry = taxonomy_by_review.get(review["review_id"], {})
        candidate_jobs = sorted({
            x.get("canonical_job")
            for x in taxonomy_entry.get("functions", [])
            if x.get("canonical_job") and x.get("canonical_job") != "unclassified"
        })
        functions = lesson.get("communication_function_inventory", [])
        relations = lesson.get("structural_relation_inventory", [])
        structural_route_types = sorted({
            relation.get("type")
            for relation in relations
            if relation.get("type") in STRUCTURAL_JOB_MAP
        })
        structural_candidate_jobs = sorted({
            job
            for relation_type in structural_route_types
            for job in STRUCTURAL_JOB_MAP[relation_type]
        }) if not candidate_jobs else []
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
            "candidate_jobs": candidate_jobs,
            "candidate_job_forms": {
                job: card_by_job[job].get("form")
                for job in candidate_jobs
                if job in card_by_job
            },
            "structural_candidate_jobs": structural_candidate_jobs,
            "structural_candidate_job_forms": {
                job: card_by_job[job].get("form")
                for job in structural_candidate_jobs
                if job in card_by_job
            },
            "structural_route_types": structural_route_types,
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
        function_counts.update(x.get("function") or x.get("label") or "unlabelled" for x in row["observed_functions"])
        relation_counts.update(x.get("type") or "unlabelled" for x in row["observed_relations"])

    result = {
        "schema_version": "1.0",
        "catalog_id": "corpus-findings-catalog",
        "status": "transcript_derived_findings_with_provisional_practice_hypotheses",
        "claim_boundary": "The per-video rows are actual recorded transcript observations linked to retained evidence and writeups. Candidate jobs and practice forms are heuristic routing aids; copyable forms and mechanism statements are provisional learning hypotheses and do not establish delivery effects, listener outcomes, teachability or best-practice status.",
        "coverage": {
            "review_count": len(rows),
            "function_observation_count": sum(function_counts.values()),
            "relation_observation_count": sum(relation_counts.values()),
            "phrase_form_count": len(phrases),
            "videos_with_candidate_practice_job": sum(bool(row["candidate_job_forms"]) for row in rows),
            "videos_without_candidate_practice_job": sum(not row["candidate_job_forms"] for row in rows),
            "videos_with_structural_candidate_practice_job": sum(bool(row["structural_candidate_job_forms"]) for row in rows),
            "videos_without_any_candidate_practice_job": sum(
                not row["candidate_job_forms"] and not row["structural_candidate_job_forms"]
                for row in rows
            ),
        },
        "how_to_use": [
            "Start with a job card for a speech task you need tomorrow.",
            "Read its exact caption examples and linked writeups before copying the form.",
            "Use the 395-row index to compare the same move across different talks.",
            "Treat why-it-may-work language as a hypothesis and test it with a listener.",
            "Do not infer nonverbal behavior, effectiveness or factual truth from transcript-only evidence.",
        ],
        "job_findings": job_rows,
        "phrase_forms": phrases,
        "delivery_observations": [
            {
                "sample_id": x.get("sample_id"),
                "job": x.get("canonical_job"),
                "video_id": x.get("video_id"),
                "source_url": x.get("source_url"),
                "sampled_midpoint_seconds": x.get("sampled_midpoint_seconds"),
                "transcript_alignment": x.get("transcript_alignment"),
                "visual_observation": x.get("visual_observation"),
                "setting_editing_music_observation": x.get("setting_editing_music_observation"),
                "vocal_timing_observation": x.get("vocal_timing_observation"),
                "audio_measurements": x.get("audio_measurements"),
                "nearest_sampled_frame_measurement": x.get("nearest_sampled_frame_measurement"),
                "limits": x.get("missingness_or_accessibility_note"),
                "independence": x.get("independence"),
            }
            for x in delivery
        ],
        "function_counts": function_counts,
        "relation_counts": relation_counts,
        "interesting_recurrence_findings": {
            "status": "same_video_inventory_patterns_not_effectiveness_results",
            "top_job_pairs": sorted(
                [
                    {
                        "job_a": x.get("left_job"),
                        "job_b": x.get("right_job"),
                        "shared_video_count": x.get("shared_video_count", 0),
                        "holdout_shared_video_count": x.get("shared_holdout_video_count", 0),
                    }
                    for x in comparison.get("pair_rows", [])
                ],
                key=lambda x: (-x["shared_video_count"], x["job_a"], x["job_b"]),
            )[:20],
            "interpretation": "These pairs identify combinations worth reading and testing. Same-video co-occurrence does not show that one move causes another, that the pair is effective, or that either move was independently classified.",
        },
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
        f"Coverage: **{len(rows)} videos**, **{result['coverage']['function_observation_count']:,} function observations**, **{result['coverage']['relation_observation_count']:,} structural relations**, and **{len(phrases)} exact phrase-form hypotheses**. Existing heuristic taxonomy routes **{result['coverage']['videos_with_candidate_practice_job']} videos** to one or more practice cards; a separate named-relation route adds **{result['coverage']['videos_with_structural_candidate_practice_job']} candidate routes**; **{result['coverage']['videos_without_any_candidate_practice_job']} remain without either route**.",
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

    lines += ["", "## Actual delivery observations currently available", "", f"There are **{len(delivery)} bounded internal audiovisual observations**, two per communication job. These are useful inspection evidence, not validated nonverbal or vocal best practices. Manual listening, continuous gesture/gaze review, speaker identity, audience response and independent review remain open.", "", "| Job | Video / time | What was visible | Vocal/audio status | Measurement boundary |", "|---|---|---|---|---|"]
    for x in delivery:
        m = x.get("audio_measurements") or {}
        metrics = ", ".join(f"{k}={v}" for k, v in list(m.items())[:3]) or "not available"
        lines.append(f"| `{x.get('canonical_job')}` | [{x.get('video_id')} @ {x.get('sampled_midpoint_seconds')}s]({x.get('source_url')}) | {clip(x.get('visual_observation', ''), 190)} | {clip(x.get('vocal_timing_observation', ''), 150)} | {clip(metrics, 160)}; {clip(x.get('missingness_or_accessibility_note', ''), 150)} |")

    findings = result["interesting_recurrence_findings"]
    lines += ["", "## Most interesting cross-talk combinations", "", "These are the highest same-video job co-occurrences in the comparison inventory. They are reading targets and practice hypotheses, not causal or effectiveness findings.", "", "| Job A | Job B | Shared videos | Shared holdout videos |", "|---|---|---:|---:|"]
    for x in findings["top_job_pairs"]:
        lines.append(f"| `{x['job_a']}` | `{x['job_b']}` | {x['shared_video_count']} | {x['holdout_shared_video_count']} |")

    lines += ["", "## Video-by-video findings (all 395 reviews)", "", "Every row below is a recorded observation, not an invented summary. Candidate jobs are heuristic routes into the 18 practice cards; structural candidates are a separate conservative route derived only from named relation types and still require review. Rows with neither route remain explicitly unclassified. Open the linked writeup and evidence IDs for the full context.", "", "| # | Video / writeup | Candidate practice jobs | Structural candidate route | Observed functions | Structural relations | Limits / next test |", "|---:|---|---|---|---|---|---|"]
    for i, row in enumerate(rows, 1):
        fs = "; ".join(
            clip(x.get("function") or x.get("label") or ("unlabelled: " + x.get("reason") if x.get("reason") else "unlabelled"), 120)
            for x in row["observed_functions"][:5]
        ) or "none recorded"
        rs = "; ".join(
            clip(x.get("type") or ("unlabelled: " + x.get("claim") if x.get("claim") else "unlabelled"), 100)
            for x in row["observed_relations"][:4]
        ) or "none recorded"
        jobs = "; ".join(f"`{job}`" for job in row.get("candidate_jobs", []) if job in card_by_job) or "none"
        structural_jobs = "; ".join(f"`{job}`" for job in row.get("structural_candidate_jobs", []) if job in card_by_job) or "none"
        lim = clip(" ".join(row["limits"][:2]), 180) if row["limits"] else clip(row.get("next_test") or "see writeup", 180)
        title = clip(row["title"], 90)
        lines.append(f"| {i} | [{title}](../{row['writeup']}) `{row['video_id']}` | {jobs} | {structural_jobs} | {fs} | {rs} | {lim} |")

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
