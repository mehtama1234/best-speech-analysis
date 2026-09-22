"""Select bounded internal counterexample candidates from existing corpus cards.

This is deliberately a screening pass. It does not claim that a candidate
failed, that a form caused an outcome, or that a source is comparable without
further inspection.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/corpus-learner-card-inventory.json"
JOBS = ROOT / "research/communication-job-curriculum-index.json"
OUT = ROOT / "research/autonomous-counterexample-screening.json"
MD = ROOT / "writeups/autonomous-counterexample-screening.md"


def first_evidence(card: dict) -> dict:
    evidence = card.get("exact_evidence") or [{}]

    def evidence_key(item: dict) -> tuple[int, int, str]:
        text = str(item.get("text") or "").strip()
        words = [word for word in text.split() if any(char.isalpha() for char in word)]
        marker_only = text.lower() in {"[music]", "[applause]", "[laughter]"} or len(words) < 4
        return (0 if marker_only else 1, len(words), text)

    item = max(evidence, key=evidence_key)
    return {
        "evidence_id": item.get("evidence_id"),
        "video_id": card.get("video_id"),
        "title": card.get("title"),
        "source_url": item.get("source_url") or card.get("source_url"),
        "transcript_excerpt": item.get("text"),
    }


def card_sort_key(card: dict):
    return (card.get("video_id", ""), card.get("card_id", ""))


def card_quality(card: dict) -> tuple[int, int, str, str]:
    """Rank retrieval candidates without interpreting their speech function."""
    evidence = card.get("exact_evidence") or []
    best_text = max(
        (str(item.get("text") or "") for item in evidence),
        key=lambda text: len(text.split()),
        default="",
    )
    words = [word for word in best_text.split() if any(char.isalpha() for char in word)]
    marker_only = best_text.strip().lower() in {"[music]", "[applause]", "[laughter]"}
    lexical_score = 0 if marker_only or len(words) < 4 else 1
    return (-lexical_score, -len(words), card.get("video_id", ""), card.get("card_id", ""))


def build() -> dict:
    cards_payload = json.loads(CARDS.read_text(encoding="utf-8"))
    jobs_payload = json.loads(JOBS.read_text(encoding="utf-8"))
    cards = cards_payload["cards"]
    by_job = defaultdict(list)
    phrase_to_cards = defaultdict(list)
    for card in cards:
        job = card.get("canonical_job")
        if job and job not in {"unclassified", "media_or_publisher"}:
            by_job[job].append(card)
        for handle in card.get("phrase_handles", []):
            phrase_to_cards[handle.get("phrase_form")].append(card)
    for group in by_job.values():
        group.sort(key=card_quality)
    for group in phrase_to_cards.values():
        group.sort(key=card_sort_key)

    items = []
    for lesson in jobs_payload["lessons"]:
        job = lesson["canonical_job"]
        group = by_job[job]
        used_card_ids: set[str] = set()
        used_video_ids: set[str] = set()

        def pick(pool: list[dict]) -> dict:
            """Prefer a new card and source video for each type within a job."""
            for card in pool:
                if card.get("card_id") not in used_card_ids and card.get("video_id") not in used_video_ids:
                    used_card_ids.add(card.get("card_id"))
                    used_video_ids.add(card.get("video_id"))
                    return card
            for card in pool:
                if card.get("card_id") not in used_card_ids:
                    used_card_ids.add(card.get("card_id"))
                    used_video_ids.add(card.get("video_id"))
                    return card
            card = pool[0]
            used_card_ids.add(card.get("card_id"))
            used_video_ids.add(card.get("video_id"))
            return card
        # Deterministic, conservative candidate selection. These are not
        # promoted to the original review workbook, which remains a separate
        # review instrument.
        no_phrase = [card for card in group if not card.get("phrase_handles")]
        risky = [
            card for card in group
            if any(word in (" ".join(card.get("review_limits", []))).lower() for word in ("privacy", "consent", "safety", "trauma", "access"))
        ]
        weak = [card for card in group if card.get("non_fit") or card.get("next_test")]
        confounded = [card for card in group if card.get("delivery_proxy", {}).get("status") in {"no_local_media", "proxy_only", "local_proxy_nearest_sample_not_manual_delivery_review"}]
        phrase_card = None
        for card in group:
            handles = card.get("phrase_handles", [])
            if handles and phrase_to_cards.get(handles[0].get("phrase_form")):
                others = [x for x in phrase_to_cards[handles[0]["phrase_form"]] if x.get("canonical_job") != job]
                if others:
                    phrase_card = (card, others[0], handles[0]["phrase_form"])
                    break
        selections = [
            ("absent_but_speech_works", pick(no_phrase or group), "Same provisional job has a transcript card without an indexed phrase handle; this tests whether the phrase is necessary or merely a retrieval aid."),
            ("present_but_limit_visible", pick(weak or group), "The card carries an explicit non-fit or next-test boundary; this tests whether the proposed form needs a condition."),
            ("alternate_function_or_phrase", pick(([phrase_card[0]] + group) if phrase_card else (group[1:] or group)), "A repeated phrase or nearby form may serve another function; context prevents treating wording as a universal technique."),
            ("setting_or_delivery_confound", pick(confounded or group), "The available delivery layer is proxy-only or missing/manual-review pending; this blocks a delivery interpretation."),
            ("safety_accessibility_screen", pick(risky or group), "The source or job may involve privacy, consent, vulnerability or access concerns; the candidate requires bounded adaptation rather than imitation."),
        ]
        for counter_type, card, rationale in selections:
            evidence = first_evidence(card)
            items.append({
                "screening_item_id": f"autonomous-counterexample:{job}:{counter_type}",
                "canonical_job": job,
                "counterexample_type": counter_type,
                "status": "internal_screening_candidate_not_validated",
                "candidate": evidence,
                "source_card_id": card.get("card_id"),
                "observed_move": card.get("observed_move"),
                "rationale": rationale,
                "internal_decision": "retain_for_limit_review",
                "claim_boundary": "This is an internally selected candidate for a limit or alternate explanation. It does not establish failure, ineffectiveness, causality, speaker intent or generalization.",
            })
    report = {
        "schema_version": "1.0",
        "screening_id": "autonomous-counterexample-screening",
        "status": "internal_candidate_screening_complete_not_validation",
        "item_count": len(items),
        "job_count": len(jobs_payload["lessons"]),
        "items_per_job": 5,
        "unique_source_videos_per_job": 5,
        "claim_boundary": "The project agent selected bounded candidates from existing transcript cards for internal adversarial review. Candidates are not independent or confirmed counterexamples and do not establish effectiveness or failure.",
        "selection_method": "Deterministic use of absent phrase handles, explicit non-fit/next-test fields, proxy/missing delivery status, cross-job phrase reuse and safety/accessibility limit text.",
        "items": items,
    }
    return report


def render(report: dict) -> str:
    lines = [
        "# Autonomous counterexample screening",
        "",
        "Status: **internal candidate screening complete; not validated counterexample evidence**.",
        "",
        report["claim_boundary"],
        "",
        f"The screening retains **{report['item_count']} candidates** across **{report['job_count']} jobs** (**{report['items_per_job']} per job, from {report['unique_source_videos_per_job']} distinct source videos per job**). The original counterexample workbook remains blank because this screening does not silently impersonate a separate reviewer.",
        "",
        "| Job | Type | Evidence | Internal reason to retain |",
        "|---|---|---|---|",
    ]
    for item in report["items"]:
        ev = item["candidate"].get("evidence_id") or "no aligned evidence"
        lines.append(f"| `{item['canonical_job']}` | `{item['counterexample_type']}` | `{ev}` | {item['rationale']} |")
    lines += [
        "",
        "## How to use this list",
        "",
        "Read the full surrounding transcript and any available source media before turning a candidate into a lesson boundary. Preserve `no_defensible_candidate_found` when the evidence does not support a comparison. Do not describe any row as a failure or proof that a pattern does not work.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD.write_text(render(report), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "markdown": str(MD.relative_to(ROOT)), "item_count": report["item_count"], "job_count": report["job_count"]}, indent=2))
