#!/usr/bin/env python3
"""Build provisional practice patterns from reviewed, controlled evidence."""

from __future__ import annotations

import json
from pathlib import Path
from review_evidence import load_annotations, label_supported, label_reason


PRACTICE_GUIDANCE = {
    "contrast_or_disagreement": {
        "title": "Make the comparison explicit",
        "practice": "When correcting or distinguishing ideas, state the contrast directly (for example, expected outcome versus observed outcome) and then supply the replacement claim or evidence.",
        "limit": "This sample combines personal reconsideration, asserted outcomes, reported advice and scene dialogue. Textual contrast does not establish a real interpersonal dispute, successful disagreement handling or truth of the contrasted claims. The selected reviewed sample is not a population precision estimate.",
    },
    "definition": {
        "title": "Define or reframe the key term",
        "practice": "When a term may be ambiguous, give a short meaning, translation, or paraphrase before building the next claim on it.",
        "limit": "A phrase such as 'means' can express personal significance or a causal interpretation rather than a general definition.",
    },
    "example": {
        "title": "Move from the general claim to a concrete case",
        "practice": "After an abstract claim, announce or signal a specific case, statistic, named example, or imagined scene, and connect it back to the claim.",
        "limit": "This sample mixes category lists, asserted cases, numerical comparisons and imagined scenarios. A vivid detail is not automatically an example; an illustration is not factual verification or causal proof. Source allegations and numerical claims are not endorsed.",
    },
    "question": {
        "title": "Use a question to open a response or reflection",
        "practice": "Use a genuine or rhetorical question when it has a clear job—eliciting an answer, setting up a reflection, or framing a problem—and make the answer or transition apparent.",
        "limit": "Interviews, relative clauses, and transcript boundary errors can look like questions to keyword retrieval.",
    },
    "story_or_personal_experience": {
        "title": "Use bounded personal detail",
        "practice": "A short first-person event, setting, action, or quoted line can make an abstract point concrete; mark the transition back to the broader point.",
        "limit": "This sample mixes scene setups, actions, reported dialogue and brief autobiographical memories, not complete story arcs. Isolated counterfactual reactions and historical comparisons are excluded under the experienced-event rubric. Narrated events, quoted claims and emotional descriptions are not independently verified facts or current delivery measurements.",
    },
    "uncertainty_or_qualification": {
        "title": "Qualify predictions and interpretations precisely",
        "practice": "Use explicit qualifiers such as 'I think', 'might', or 'probably' when a claim is a view, prediction, or interpretation rather than an established fact.",
        "limit": "Verbal qualification does not prove internal uncertainty. This sample mixes current-turn views, reported other people's words and unresolved turn attribution; recommendations may remain strong. Voice has not been adjudicated against the wording.",
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
    annotations = load_annotations(root)

    cards = []
    excluded = []
    for label, guidance in PRACTICE_GUIDANCE.items():
        evidence = reviewed["patterns_by_candidate_label"].get(label)
        control = baselines.get(label)
        if not evidence or not control:
            excluded.append({"candidate_label": label, "reasons": ["missing supported evidence or baseline"]})
            continue
        reviewed_count = sum(1 for row in annotations if label in row.get("candidate_labels", []))
        supported_count = sum(1 for row in annotations if label in row.get("candidate_labels", []) and label_supported(row, label))
        support_rate = round(supported_count / reviewed_count, 3) if reviewed_count else None
        reasons = []
        if supported_count < 5:
            reasons.append("fewer than five supported examples")
        if evidence["distinct_video_count"] < 4:
            reasons.append("fewer than four distinct videos")
        if not reviewed_count or supported_count / reviewed_count < 0.7:
            reasons.append("support rate below 0.70")
        if reasons:
            excluded.append({"candidate_label": label, "reviewed_count": reviewed_count,
                             "supported_count": supported_count, "support_rate": support_rate,
                             "distinct_video_count": evidence["distinct_video_count"], "reasons": reasons})
            continue
        counterexamples = [
            {
                "annotation_id": row["annotation_id"],
                "evidence_id": row["evidence_id"],
                "reviewed_speech_function": row.get("reviewed_speech_function"),
                "direct_observation": label_reason(row, label),
            }
            for row in annotations
            if label in row.get("candidate_labels", []) and not label_supported(row, label)
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
            "measurement_scope": {
                "per_metric_example_counts": {key: value["count"] for key, value in evidence["measurement_summary"].items()},
                "baseline_video_count": control["video_count"],
                "baseline_example_count": control["example_count"],
                "baseline_definition": control["comparison"],
                "speaker_recurrence": "not_established; uploaders and videos are not verified distinct speakers",
            },
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
        "delivery_sensitivity_report": "research/disjoint-delivery-comparison.json",
        "excluded_patterns": excluded,
        "patterns": cards,
    }
    output = root / "research/provisional-practice-patterns.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Provisional practice patterns",
        "",
        "Review provenance: legacy reviewer identity is unknown; contextual per-label overrides are assistant transcript-only judgments. See research/contextual-label-reviews.json. These are not independently human-validated findings.",
        "",
        "Delivery robustness is evaluated separately in [the disjoint-reference sensitivity report](disjoint-delivery-comparison.md). A historical rate-direction reversal was traced to a four-millisecond caption artifact; current rate summaries exclude durations below a provisional 0.25-second floor. See [timing diagnosis](timing-artifact-diagnosis.md). Screening does not validate speech timing; do not convert pooled means into instructions to speak faster, slower, louder or at a particular pitch.",
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
            f"Measurement denominators (not the full supported-example count): {card['measurement_scope']['per_metric_example_counts']}. Baseline comparison uses {card['measurement_scope']['baseline_example_count']} examples across {card['measurement_scope']['baseline_video_count']} videos. The baseline includes all usable segments, including target examples; it is not a disjoint or speech-function-matched control.",
            "Video and uploader counts do not establish recurrence across distinct speakers. Review support measures candidate-label agreement, not delivery effectiveness.",
            "",
            "Timestamped examples:",
            "",
        ]
        for example in card["timestamped_examples"]:
            lines.append(f"- [{example['evidence_id']}]({example['url']}): {example.get('text') or '(transcript text unavailable)'}.")
            decision = example.get("contextual_label_decisions", {}).get(card["candidate_label"])
            if decision:
                lines.append(f"  Context: {decision.get('subtype', 'see review reason')}; attribution: {decision.get('view_attribution', 'not separately adjudicated')}. {decision['reason']}")
        lines += [
            "",
            "Counterexamples retained:",
            "",
        ]
        for counterexample in card["counterexamples"]:
            lines.append(f"- `{counterexample['evidence_id']}`: {counterexample['direct_observation']}")
        if not card["counterexamples"]:
            lines.append("No rejected cases in the current reviewed sample; this is not evidence that counterexamples do not exist.")
        lines += [
            "",
            f"Limit: {card['interpretation_limit']}",
            "",
            f"Visual evidence status: {card['visual_evidence_status']}",
            "",
            f"Required next test: {card['required_next_test']}",
            "",
        ]
    lines += ["## Candidates not admitted", "", "Exclusion is retained rather than silently dropping a failed candidate. Existing reviewed examples remain in the delivery report and annotation ledger.", ""]
    for item in excluded:
        lines.append(f"- `{item['candidate_label']}`: {'; '.join(item['reasons'])}; supported/reviewed = {item.get('supported_count', 'n/a')}/{item.get('reviewed_count', 'n/a')}.")
    lines += ["", "This edition evaluates the seven practice-guidance candidates listed by the builder, not every speech-function label in the corpus.", ""]
    (root / "writeups/provisional-practice-patterns.md").write_text("\n".join(lines))
    print(json.dumps({"eligible_patterns": len(cards), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
