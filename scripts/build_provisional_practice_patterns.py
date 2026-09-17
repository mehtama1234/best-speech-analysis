#!/usr/bin/env python3
"""Build provisional practice patterns from reviewed, controlled evidence."""

from __future__ import annotations

import json
from pathlib import Path


PRACTICE_GUIDANCE = {
    "contrast_or_disagreement": {
        "title": "Make the comparison explicit",
        "practice": "When correcting or distinguishing ideas, state the contrast directly (for example, expected outcome versus observed outcome) and then supply the replacement claim or evidence.",
        "limit": "Contrast markers can describe a personal turning point or rhetorical framing rather than an interpersonal disagreement.",
    },
    "definition": {
        "title": "Define or reframe the key term",
        "practice": "When a term may be ambiguous, give a short meaning, translation, or paraphrase before building the next claim on it.",
        "limit": "A phrase such as 'means' can express personal significance or a causal interpretation rather than a general definition.",
    },
    "example": {
        "title": "Move from the general claim to a concrete case",
        "practice": "After an abstract claim, announce or signal a specific case, statistic, named example, or imagined scene, and connect it back to the claim.",
        "limit": "A vivid story detail is not automatically an example used to support a general argument.",
    },
    "question": {
        "title": "Use a question to open a response or reflection",
        "practice": "Use a genuine or rhetorical question when it has a clear job—eliciting an answer, setting up a reflection, or framing a problem—and make the answer or transition apparent.",
        "limit": "Interviews, relative clauses, and transcript boundary errors can look like questions to keyword retrieval.",
    },
    "story_or_personal_experience": {
        "title": "Use bounded personal detail",
        "practice": "A short first-person event, setting, action, or quoted line can make an abstract point concrete; mark the transition back to the broader point.",
        "limit": "Historical explanation, hypothetical scenarios, and isolated personal details may not form a complete story.",
    },
    "uncertainty_or_qualification": {
        "title": "Qualify predictions and interpretations precisely",
        "practice": "Use explicit qualifiers such as 'I think', 'might', or 'probably' when a claim is a view, prediction, or interpretation rather than an established fact.",
        "limit": "Verbal qualification does not prove a speaker's internal uncertainty, and voice may reinforce or contradict the wording.",
    },
    "conclusion_or_summary": {
        "title": "Mark the takeaway",
        "practice": "Use a clear summary or conclusion marker when compressing a preceding explanation, story, or comparison into the point the audience should retain.",
        "limit": "A transition word such as 'therefore' can introduce a consequence without closing the speech.",
    },
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    reviewed = json.loads((root / "research/reviewed-delivery-patterns.json").read_text())
    baselines = json.loads((root / "research/reviewed-delivery-baselines.json").read_text())["patterns"]
    annotations = [
        json.loads(line)
        for line in (root / "research/annotation-ledger.jsonl").read_text().splitlines()
        if line.strip()
    ]

    cards = []
    for label, guidance in PRACTICE_GUIDANCE.items():
        evidence = reviewed["patterns_by_candidate_label"].get(label)
        control = baselines.get(label)
        if not evidence or not control:
            continue
        reviewed_count = sum(1 for row in annotations if label in row.get("candidate_labels", []))
        supported_count = sum(1 for row in annotations if label in row.get("candidate_labels", []) and row.get("candidate_label_supported") is True)
        support_rate = round(supported_count / reviewed_count, 3) if reviewed_count else None
        if supported_count < 5 or evidence["distinct_video_count"] < 4 or support_rate is None or support_rate < 0.7:
            continue
        counterexamples = [
            {
                "annotation_id": row["annotation_id"],
                "evidence_id": row["evidence_id"],
                "reviewed_speech_function": row.get("reviewed_speech_function"),
                "direct_observation": row.get("direct_observation"),
            }
            for row in annotations
            if label in row.get("candidate_labels", []) and row.get("candidate_label_supported") is False
        ]
        cards.append({
            "pattern_id": f"provisional-{label}",
            "candidate_label": label,
            "title": guidance["title"],
            "status": "provisional_practice_hypothesis",
            "eligibility": {
                "reviewed_count": reviewed_count,
                "supported_count": supported_count,
                "support_rate": support_rate,
                "distinct_video_count": evidence["distinct_video_count"],
                "distinct_uploader_count": evidence["distinct_uploader_count"],
                "minimum_supported_examples": 5,
                "minimum_distinct_videos": 4,
            },
            "direct_measurement_summary": evidence["measurement_summary"],
            "same_video_baseline_summary": control["metric_deltas"],
            "timestamped_examples": evidence["examples"][:5],
            "counterexamples": counterexamples,
            "practice_implication": guidance["practice"],
            "interpretation_limit": guidance["limit"],
            "visual_evidence_status": "Pose and face measurements exist for the broader pilot, but these pattern cards do not claim manually verified visual alignment.",
            "required_next_test": "Review more examples across speakers and formats, inspect the video frames/audio, and compare with matched speech-function controls before calling this a general best practice.",
        })

    report = {
        "schema_version": "0.1",
        "policy": "Provisional practice hypotheses require at least five supported reviewed examples, four distinct videos, and a support rate of at least 0.70. They are not universal findings or effectiveness claims.",
        "candidate_label_count": len(PRACTICE_GUIDANCE),
        "eligible_pattern_count": len(cards),
        "patterns": cards,
    }
    output = root / "research/provisional-practice-patterns.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Provisional practice patterns",
        "",
        "These are practice hypotheses, not universal speech rules. A card is admitted only when at least five reviewed examples support the candidate label, those examples span at least four videos, and the reviewed support rate is at least 0.70. The delivery values are measured summaries and same-video exploratory deltas; they do not establish causation, persuasion, comprehension, or internal state.",
        "",
        f"Eligible provisional patterns: **{len(cards)}** of **{len(PRACTICE_GUIDANCE)}** candidate labels.",
        "",
    ]
    for card in cards:
        eligibility = card["eligibility"]
        baseline = card["same_video_baseline_summary"]
        lines += [
            f"## {card['title']}",
            "",
            f"Candidate label: `{card['candidate_label']}`  ",
            f"Evidence: {eligibility['supported_count']} supported examples across {eligibility['distinct_video_count']} videos and {eligibility['distinct_uploader_count']} uploaders; reviewed support rate {eligibility['support_rate']}.",
            "",
            f"Practice hypothesis: {card['practice_implication']}",
            "",
            f"Direct measurement summary: RMS mean {card['direct_measurement_summary']['mean_rms_db']['mean']}; pitch proxy mean {card['direct_measurement_summary']['mean_pitch_hz_proxy']['mean']}; words/second proxy mean {card['direct_measurement_summary']['words_per_second_proxy']['mean']}; transcript gap-before mean {card['direct_measurement_summary']['transcript_gap_before_seconds']['mean']} seconds.",
            f"Same-video exploratory deltas: RMS {baseline['mean_rms_db']['mean_delta']} dB; pitch proxy {baseline['mean_pitch_hz_proxy']['mean_delta']} Hz; words/second {baseline['words_per_second_proxy']['mean_delta']}.",
            "",
            "Timestamped examples:",
            "",
        ]
        for example in card["timestamped_examples"]:
            lines.append(f"- [{example['evidence_id']}]({example['url']}): {example.get('text') or '(transcript text unavailable)'}.")
        lines += [
            "",
            "Counterexamples retained:",
            "",
        ]
        for counterexample in card["counterexamples"]:
            lines.append(f"- `{counterexample['evidence_id']}`: {counterexample['direct_observation']}")
        lines += [
            "",
            f"Limit: {card['interpretation_limit']}",
            "",
            f"Visual evidence status: {card['visual_evidence_status']}",
            "",
            f"Required next test: {card['required_next_test']}",
            "",
        ]
    (root / "writeups/provisional-practice-patterns.md").write_text("\n".join(lines))
    print(json.dumps({"eligible_patterns": len(cards), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
