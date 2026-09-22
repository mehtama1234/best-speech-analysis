"""Build an internal, non-independent audit of the corpus learning system."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research/autonomous-curriculum-audit.json"
OUT_MD = ROOT / "writeups/autonomous-curriculum-audit.md"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def nonempty(value) -> bool:
    return value not in (None, "", [], {})


def build() -> dict:
    curriculum = load("research/communication-job-curriculum-index.json")
    delivery = load("research/communication-job-delivery-sampling.json")
    counters = load("research/communication-job-counterexample-workbook.json")
    cards = load("research/corpus-learner-card-inventory.json")
    itinerary = load("research/corpus-video-learning-itinerary.json")
    media = load("research/full-corpus-media-coverage.json")
    phrases = load("research/corpus-phrase-form-inventory.json")
    internal_delivery = load("research/communication-job-delivery-internal-observations.json")
    counter_screening = load("research/autonomous-counterexample-screening.json")

    delivery_by_job = {}
    for item in delivery["items"]:
        delivery_by_job.setdefault(item["canonical_job"], []).append(item)
    counter_by_job = {}
    for item in counters["items"]:
        counter_by_job.setdefault(item["canonical_job"], []).append(item)

    jobs = []
    for lesson in curriculum["lessons"]:
        job = lesson["canonical_job"]
        delivery_items = delivery_by_job.get(job, [])
        counter_items = counter_by_job.get(job, [])
        delivery_completed = sum(
            all(nonempty(item["review"].get(field)) for field in (
                "transcript_alignment",
                "vocal_timing_observation",
                "audio_measurement_and_limit",
                "visual_observation",
                "setting_editing_music_observation",
                "speaker_event_identity",
                "missingness_or_accessibility_note",
            ))
            for item in delivery_items
        )
        counter_completed = sum(
            all(nonempty(item["review"].get(field)) for field in (
                "evidence_status",
                "function_decision",
                "identity_status",
                "context_note",
                "alternative_explanation",
                "safety_or_accessibility_note",
            ))
            for item in counter_items
        )
        jobs.append(
            {
                "canonical_job": job,
                "pattern_id": lesson["pattern_id"],
                "lesson_status": lesson["status"],
                "exact_example_count": len(lesson["exact_examples"]),
                "phrase_form_count": len(lesson["phrase_forms"]),
                "phrase_form_coverage_status": lesson["phrase_form_coverage_status"],
                "delivery_queue_count": len(delivery_items),
                "delivery_completed_count": delivery_completed,
                "counterexample_queue_count": len(counter_items),
                "counterexample_completed_count": counter_completed,
                "learner_status": lesson["learner"].get("status"),
                "listener_status": lesson["listener"].get("status"),
                "internal_readiness": "lesson_and_transcript_evidence_present",
            }
        )

    delivery_review_count = sum(x["delivery_completed_count"] for x in jobs)
    counter_review_count = sum(x["counterexample_completed_count"] for x in jobs)
    report = {
        "schema_version": "1.0",
        "audit_id": "autonomous-curriculum-audit",
        "status": "internal_reconciliation_checkpoint_not_promotion_validation",
        "claim_boundary": (
            "This audit reconciles local transcript, queue, media-availability and "
            "curriculum artifacts. It is performed by the project agent and does "
            "not establish independent review, speaker intent, learner teachability, "
            "listener outcomes or communication effectiveness."
        ),
        "coverage": {
            "fixed_corpus_videos": itinerary["video_count"],
            "full_context_reviews": cards["summary"]["review_count"],
            "function_cards": cards["summary"]["card_count"],
            "structural_cards": cards["summary"]["structural_card_count"],
            "exact_phrase_forms": phrases["form_count"],
            "communication_jobs": curriculum["lesson_count"],
            "videos_with_canonical_job_lesson": itinerary["learning_track_counts"].get("canonical_job_lesson", 0),
            "videos_with_structural_bridge": itinerary["learning_track_counts"].get("structural_bridge_lesson", 0),
            "videos_with_exploration_lead": itinerary["learning_track_counts"].get("transcript_exploration_lead", 0),
            "unclassified_cards": cards["summary"]["unclassified_cards"],
            "raw_media_present": media["counts"]["raw_audio_video_present"],
        },
        "review_queues": {
            "delivery_items": delivery["item_count"],
            "delivery_items_internally_completed": delivery_review_count,
            "delivery_items_with_bounded_internal_observation": internal_delivery["item_count"],
            "delivery_items_with_manual_vocal_review": 0,
            "counterexample_items": counters["item_count"],
            "counterexample_items_internally_completed": counter_review_count,
            "counterexample_screening_candidates": counter_screening["item_count"],
        },
        "jobs": jobs,
        "remaining_autonomous_work": [
            "Add manual listening and full-sequence edit review to the 36 bounded delivery observations; current frame/proxy observations remain limited.",
            "Read and adjudicate the 90 internally screened counterexample candidates; preserve no-defensible-candidate outcomes.",
            "Reconcile the 157 exploration-track videos and unclassified cards into bounded lesson leads or explicit no-fit records.",
            "Run adversarial consistency checks across exact evidence, phrase forms, lesson claims, delivery limits and safety boundaries.",
        ],
        "deliberately_not_claimed": [
            "independent human agreement",
            "universal best practice",
            "speaker intent",
            "learner improvement",
            "listener comprehension or persuasion",
        ],
        "sources": [
            "research/communication-job-curriculum-index.json",
            "research/communication-job-delivery-sampling.json",
            "research/communication-job-counterexample-workbook.json",
            "research/corpus-learner-card-inventory.json",
            "research/corpus-video-learning-itinerary.json",
            "research/full-corpus-media-coverage.json",
            "research/corpus-phrase-form-inventory.json",
        ],
    }
    return report


def markdown(report: dict) -> str:
    c = report["coverage"]
    q = report["review_queues"]
    lines = [
        "# Autonomous curriculum audit",
        "",
        "Status: **internal reconciliation checkpoint; not independent validation or promotion evidence**.",
        "",
        report["claim_boundary"],
        "",
        f"The fixed corpus has **{c['fixed_corpus_videos']} videos**, **{c['full_context_reviews']} full-context reviews**, **{c['function_cards']} function cards**, **{c['structural_cards']} structural cards**, **{c['exact_phrase_forms']} exact phrase forms** and **{c['communication_jobs']} communication-job lessons**.",
        "",
        "## Coverage snapshot",
        "",
        "| Layer | Count | Interpretation |",
        "|---|---:|---|",
        f"| Canonical-job video lessons | {c['videos_with_canonical_job_lesson']} | Transcript-derived job lesson selected |",
        f"| Structural-bridge video lessons | {c['videos_with_structural_bridge']} | Sequence or relation lesson selected |",
        f"| Exploration leads | {c['videos_with_exploration_lead']} | Evidence exists; canonical job remains bounded or unresolved |",
        f"| Unclassified learner cards | {c['unclassified_cards']} | Do not turn into recommendations without a clearer function |",
        f"| Raw local audio/video available | {c['raw_media_present']} | Availability only; not delivery review |",
        "",
        "## Review queues",
        "",
        f"- Delivery queue: **{q['delivery_items']}** items; bounded internal observations: **{q['delivery_items_with_bounded_internal_observation']}**; manual vocal review: **{q['delivery_items_with_manual_vocal_review']}**.",
        f"- Counterexample queue: **{q['counterexample_items']}** blank review slots; autonomous screening candidates: **{q['counterexample_screening_candidates']}**; confirmed review slots: **{q['counterexample_items_internally_completed']}**.",
        "- Blank or incomplete fields remain visible rather than being treated as negative findings.",
        "",
        "## Job-by-job reconciliation",
        "",
        "| Job | Examples | Forms | Delivery done | Counters done | Learner | Listener |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for job in report["jobs"]:
        lines.append(
            f"| `{job['canonical_job']}` | {job['exact_example_count']} | {job['phrase_form_count']} | {job['delivery_completed_count']}/{job['delivery_queue_count']} | {job['counterexample_completed_count']}/{job['counterexample_queue_count']} | `{job['learner_status']}` | `{job['listener_status']}` |"
        )
    lines += [
        "",
        "## Remaining autonomous work",
        "",
    ]
    lines.extend(f"- {item}" for item in report["remaining_autonomous_work"])
    lines += [
        "",
        "## Deliberately not claimed",
        "",
    ]
    lines.extend(f"- {item}" for item in report["deliberately_not_claimed"])
    lines += [
        "",
        "The source lesson browser and [stakeholder tutorial](stakeholder-tutorial.md) are learning surfaces. This audit is the internal control document for advancing them without silently converting hypotheses into facts.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"json": str(OUT_JSON), "markdown": str(OUT_MD), "jobs": len(report["jobs"]), "delivery_completed": report["review_queues"]["delivery_items_internally_completed"], "counterexample_completed": report["review_queues"]["counterexample_items_internally_completed"]}, indent=2))
