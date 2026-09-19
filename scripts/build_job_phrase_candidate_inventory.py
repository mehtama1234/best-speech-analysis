#!/usr/bin/env python3
"""Mine bounded multi-word phrase candidates from the full evidence bank."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "research/corpus-evidence-bank.json"
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
OUT = ROOT / "research/job-phrase-candidate-inventory.json"
MD = ROOT / "writeups/job-phrase-candidate-inventory.md"

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "for", "from", "has", "have", "he", "her", "his", "i", "if", "in", "is", "it", "its", "me", "my", "not", "of", "on", "or", "our", "that", "the", "their", "them", "there", "they", "this", "to", "was", "we", "were", "what", "when", "where", "which", "who", "will", "with", "you", "your",
}
JOBS = {
    "opening", "closing", "question", "answer_or_response", "story_or_personal_experience", "example_or_case", "contrast_or_disagreement", "correction_or_reframe", "repair_or_self_correction", "qualification_or_boundary", "definition_or_explanation", "transition_or_structure", "callback_or_repetition", "humor_or_rapport", "credit_or_acknowledgment", "call_to_action_or_audience_role", "persuasion_or_advocacy", "reflection_or_value_frame",
}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z'’-]*", text.lower())


def event_split(video_id: str, atlas: dict) -> str:
    return next((row.get("event_split", "unassigned") for row in atlas.get("videos", []) if row.get("video_id") == video_id), "unassigned")


def main() -> int:
    bank = json.loads(BANK.read_text())
    atlas = json.loads(ATLAS.read_text())
    forms: dict[str, dict[tuple[str, ...], dict]] = defaultdict(dict)
    for record in bank["records"]:
        job = record.get("canonical_job")
        if job not in JOBS:
            continue
        video_id = record["video_id"]
        split = event_split(video_id, atlas)
        for segment in record.get("segments", []):
            words = tokens(segment.get("text", ""))
            for size in (2, 3, 4):
                for start in range(max(0, len(words) - size + 1)):
                    gram = tuple(words[start:start + size])
                    content = sum(word not in STOPWORDS and len(word) > 2 for word in gram)
                    if content < 1 or content / size < 0.5:
                        continue
                    item = forms[job].setdefault(gram, {"occurrence_count": 0, "videos": set(), "train": set(), "holdout": set(), "examples": []})
                    item["occurrence_count"] += 1
                    item["videos"].add(video_id)
                    if split == "train": item["train"].add(video_id)
                    if split == "holdout": item["holdout"].add(video_id)
                    if video_id not in {example["video_id"] for example in item["examples"]} and len(item["examples"]) < 3:
                        item["examples"].append({"video_id": video_id, "evidence_id": segment["evidence_id"], "text": segment.get("text", ""), "source_url": record.get("source_url")})

    output_forms = []
    for job, candidates in sorted(forms.items()):
        eligible = [(gram, item) for gram, item in candidates.items() if len(item["videos"]) >= 4]
        eligible.sort(key=lambda pair: (-len(pair[1]["videos"]), -pair[1]["occurrence_count"], pair[0]))
        for gram, item in eligible[:12]:
            output_forms.append({
                "canonical_job": job,
                "phrase_form": " ".join(gram),
                "occurrence_count": item["occurrence_count"],
                "video_count": len(item["videos"]),
                "train_video_count": len(item["train"]),
                "holdout_video_count": len(item["holdout"]),
                "examples": item["examples"],
                "status": "heuristic_multiword_form_requires_context_and_independent_review",
                "mechanism_hypothesis": "This repeated form may help perform the surrounding communication job; the phrase alone does not establish function, intent, delivery or effectiveness.",
            })
    by_job = Counter(row["canonical_job"] for row in output_forms)
    report = {
        "schema_version": "1.0",
        "inventory_id": "job-phrase-candidate-inventory",
        "status": "heuristic_multiword_phrase_candidates_not_validated",
        "source": "research/corpus-evidence-bank.json",
        "claim_boundary": "Forms are exact contiguous n-grams from retained caption segments grouped by provisional canonical job. Counts describe transcript recurrence across the local corpus; they do not establish speaker intent, independent event recurrence, delivery meaning, effectiveness or listener outcomes.",
        "selection_rule": "2–4 word n-grams with at least one content word, appearing in at least four videos; top 12 per provisional job by distinct-video count then occurrence count.",
        "job_count": len(JOBS),
        "form_count": len(output_forms),
        "forms_per_job": dict(by_job),
        "forms": output_forms,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Job phrase candidate inventory", "", "Status: **heuristic multi-word phrase candidates; not validated**.", "", report["claim_boundary"], "", f"Candidate forms: **{len(output_forms)}** across **{len(JOBS)}** provisional jobs. Selection: {report['selection_rule']}", "", "| Job | Candidate form | Videos | Train | Holdout | Occurrences | Example |", "|---|---|---:|---:|---:|---:|---|"]
    for row in output_forms:
        example = row["examples"][0] if row["examples"] else {}
        lines.append(f"| `{row['canonical_job']}` | `{row['phrase_form']}` | {row['video_count']} | {row['train_video_count']} | {row['holdout_video_count']} | {row['occurrence_count']} | [{example.get('evidence_id', '')}]({example.get('source_url', '')}) |")
    lines += ["", "## How to use", "", "Read the full surrounding caption context before adapting a form. Write the intended meaning in your own words, then add the evidence boundary, condition, consent or next-turn path required by the job. Treat the form as a retrieval handle, not a script.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "job_count": len(JOBS), "form_count": len(output_forms), "forms_per_job": dict(by_job)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
