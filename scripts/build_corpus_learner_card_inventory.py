#!/usr/bin/env python3
"""Build a learner-facing card for every transcript-derived function item.

Cards are navigation and practice aids.  They retain the original review
language and exact evidence while borrowing only the provisional form and
limits of the shared communication-job cards.  They never promote a
transcript observation to an effectiveness or best-practice claim.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "research/corpus-lesson-index.json"
TAXONOMY = ROOT / "research/corpus-function-taxonomy.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
JOBS = ROOT / "research/communication-job-cards.json"
JOB_PHRASES = ROOT / "research/job-phrase-candidate-inventory.json"
CORPUS_PHRASES = ROOT / "research/corpus-phrase-form-inventory.json"
DELIVERY_ATLAS = ROOT / "research/delivery-proxy-candidate-atlas.json"
TIMING_ATLAS = ROOT / "research/full-corpus-timing-candidate-atlas.json"
POSE_MOVEMENT = ROOT / "research/pose-movement-analysis.json"
VISUAL_MOVEMENT = ROOT / "research/visual-movement-analysis.json"
OUT = ROOT / "research/corpus-learner-card-inventory.json"
MD = ROOT / "writeups/corpus-learner-card-inventory.md"
HTML = ROOT / "writeups/corpus-learner-card-inventory.html"


def _job_cards() -> dict[str, dict]:
    data = json.loads(JOBS.read_text())
    return {card["canonical_job"]: card for card in data["cards"]}


def _taxonomy_lookup() -> dict[tuple[str, int], dict]:
    data = json.loads(TAXONOMY.read_text())
    lookup = {}
    for entry in data["entries"]:
        for item in entry["functions"]:
            lookup[(entry["review_id"], item["sequence"])] = item
    return lookup


def _phrase_handles(video_id: str, canonical_job: str, segments: list[dict], job_forms: list[dict], corpus_forms: list[dict]) -> list[dict]:
    """Attach exact phrase matches found inside this card's retained evidence."""
    handles = []
    seen = set()
    for form in job_forms:
        if form.get("canonical_job") != canonical_job:
            continue
        phrase = form.get("phrase_form", "")
        if not phrase or not any(example.get("video_id") == video_id for example in form.get("examples", [])):
            continue
        pattern = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)
        for segment in segments:
            if not pattern.search(segment.get("text", "")):
                continue
            key = (phrase, segment.get("evidence_id"))
            if key in seen:
                continue
            seen.add(key)
            handles.append({"phrase_form": phrase, "family": canonical_job, "candidate_kind": form.get("candidate_kind"), "status": form.get("status"), "mechanism_hypothesis": form.get("mechanism_hypothesis"), "evidence_id": segment.get("evidence_id"), "text": segment.get("text"), "source_url": segment.get("source_url"), "retrieval_status": "exact_card_evidence_match_not_validated_best_practice"})
    for form in corpus_forms:
        phrase = form.get("phrase_form", "")
        matched_pattern = form.get("matched_pattern")
        if not matched_pattern:
            continue
        try:
            pattern = re.compile(matched_pattern, re.IGNORECASE)
        except re.error:
            continue
        for segment in segments:
            if not pattern.search(segment.get("text", "")):
                continue
            key = (phrase, segment.get("evidence_id"))
            if key in seen:
                continue
            seen.add(key)
            handles.append({"phrase_form": phrase, "family": form.get("family"), "candidate_kind": "exact_form_inventory", "status": form.get("review_status") or form.get("status"), "mechanism_hypothesis": form.get("mechanism_hypothesis"), "evidence_id": segment.get("evidence_id"), "text": segment.get("text"), "source_url": segment.get("source_url"), "retrieval_status": "exact_card_evidence_match_not_validated_best_practice"})
    handles.sort(key=lambda item: (item["candidate_kind"] != "content_bearing_retrieval_form", item["phrase_form"], item["evidence_id"]))
    return handles[:12]


def _nearest(rows: list[dict], target_time: float | None) -> dict | None:
    if not rows or target_time is None:
        return None
    return min(rows, key=lambda row: abs(float(row.get("time_seconds", row.get("start_seconds", 0))) - target_time))


def _delivery_proxy(video_id: str, segments: list[dict], cache: dict[str, dict]) -> dict:
    if video_id in cache:
        return cache[video_id]
    feature_path = ROOT / "data/features" / f"{video_id}.json"
    pose_path = ROOT / "data/pose-features" / f"{video_id}.json"
    if not feature_path.exists():
        result = {"status": "not_available_no_local_feature_report", "claim_boundary": "No local audio/visual/pose proxy is available for this video."}
        cache[video_id] = result
        return result
    feature = json.loads(feature_path.read_text())
    target_time = segments[0].get("start_seconds") if segments else None
    audio = _nearest(feature.get("audio_windows", []), target_time)
    frame = _nearest(feature.get("sampled_frames", []), target_time)
    pose = None
    if pose_path.exists():
        pose = _nearest(json.loads(pose_path.read_text()).get("frames", []), target_time)
    result = {
        "status": "local_proxy_nearest_sample_not_manual_delivery_review",
        "feature_file": str(feature_path.relative_to(ROOT)),
        "pose_file": str(pose_path.relative_to(ROOT)) if pose_path.exists() else None,
        "target_time_seconds": target_time,
        "audio_offset_seconds": round(float(audio.get("start_seconds") - target_time), 3) if audio and target_time is not None else None,
        "frame_offset_seconds": round(float(frame.get("time_seconds") - target_time), 3) if frame and target_time is not None else None,
        "pose_offset_seconds": round(float(pose.get("time_seconds") - target_time), 3) if pose and target_time is not None else None,
        "audio_window": {key: audio.get(key) for key in ("start_seconds", "end_seconds", "rms_db", "speech_activity_proxy", "pitch_hz_proxy", "pitch_confidence_proxy")} if audio else None,
        "sampled_frame": {key: frame.get(key) for key in ("time_seconds", "face_count", "smile_detector_candidate_count", "mean_luminance", "luminance_std", "face_measurement_status")} if frame else None,
        "pose_frame": {key: pose.get(key) for key in ("time_seconds", "person_detected", "visible_keypoint_count", "visible_wrist_count", "shoulder_width_fraction", "observable_geometry_status")} if pose else None,
        "claim_boundary": "Audio, face/scene and pose fields are local measurement proxies at a nearest sampled interval. They do not establish intentional delivery, emotion, gesture meaning, identity, comprehension or effectiveness.",
    }
    cache[video_id] = result
    return result


def _delivery_candidates(segments: list[dict], delivery_by_evidence: dict[str, list[dict]], timing_by_evidence: dict[str, list[dict]]) -> list[dict]:
    """Return nearby proxy windows for manual delivery inspection."""
    output = []
    evidence_ids = {segment.get("evidence_id") for segment in segments}
    for evidence_id in evidence_ids:
        for item in delivery_by_evidence.get(evidence_id, []):
            output.append({
                "candidate_kind": "delivery_proxy_clip",
                "evidence_id": item.get("evidence_id"), "start_seconds": item.get("start_seconds"), "end_seconds": item.get("end_seconds"),
                "audio_proxy_summary": item.get("audio_proxy_summary"), "nearest_sampled_frame_proxy": item.get("nearest_sampled_frame_proxy"),
                "feature_file": item.get("feature_file"), "status": item.get("candidate_status"),
            })
        for item in timing_by_evidence.get(evidence_id, []):
            output.append({
                "candidate_kind": "timing_density_or_gap",
                "evidence_id": item.get("evidence_id"), "start_seconds": item.get("start_seconds"), "end_seconds": item.get("end_seconds"),
                "candidate_reason": item.get("candidate_reason"), "words_per_second_proxy": item.get("words_per_second_proxy"),
                "transcript_gap_before_seconds": item.get("transcript_gap_before_seconds"), "transcript_gap_after_seconds": item.get("transcript_gap_after_seconds"),
                "mean_rms_db": item.get("mean_rms_db"), "speech_activity_fraction": item.get("speech_activity_fraction"),
                "feature_file": item.get("feature_file"), "status": item.get("status"),
            })
    seen = set()
    unique = []
    for item in output:
        key = (item["candidate_kind"], item.get("evidence_id"))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:6]


def _movement_candidates(video_id: str, segments: list[dict], pose_summaries: dict[str, dict], visual_summaries: dict[str, dict]) -> list[dict]:
    target = segments[0].get("start_seconds") if segments else None
    pose = pose_summaries.get(video_id, {})
    pairs = pose.get("pairs", [])
    ranked = sorted(pairs, key=lambda pair: abs(float(pair.get("midpoint_seconds", 0)) - float(target or 0)))
    output = []
    for pair in ranked[:3]:
        output.append({
            "candidate_kind": "pose_geometry_movement_pair",
            "start_time_seconds": pair.get("start_time_seconds"), "end_time_seconds": pair.get("end_time_seconds"), "midpoint_seconds": pair.get("midpoint_seconds"),
            "offset_from_card_seconds": round(float(pair.get("midpoint_seconds", 0)) - float(target), 3) if target is not None else None,
            "mean_keypoint_displacement": pair.get("mean_keypoint_displacement"), "mean_wrist_displacement": pair.get("mean_wrist_displacement"), "mean_shoulder_displacement": pair.get("mean_shoulder_displacement"),
            "keypoint_count": pair.get("keypoint_count"),
            "status": "mediapipe_pose_landmark_geometry_only_requires_manual_video_review",
        })
    visual = visual_summaries.get(video_id)
    if visual:
        output.append({
            "candidate_kind": "visual_summary_context",
            "sampled_frame_count": visual.get("sampled_frame_count"), "face_observable_frames": visual.get("face_observable_frames"), "face_present_frames": visual.get("face_present_frames"), "movement_pairs": visual.get("movement_pairs"),
            "status": "face_scene_summary_requires_manual_video_review_no_expression_or_intent_inference",
        })
    return output


def build() -> dict:
    index = json.loads(INDEX.read_text())
    evidence = {}
    for record in json.loads(EVIDENCE.read_text())["records"]:
        for segment in record.get("segments", []):
            evidence[segment["evidence_id"]] = {
                "text": segment.get("text", ""),
                "start_seconds": segment.get("start_seconds"),
                "end_seconds": segment.get("end_seconds"),
                "source_url": record.get("source_url"),
            }
    taxonomy = _taxonomy_lookup()
    jobs = _job_cards()
    job_phrase_forms = json.loads(JOB_PHRASES.read_text())["forms"]
    corpus_phrase_forms = json.loads(CORPUS_PHRASES.read_text())["forms"]
    delivery_cache = {}
    delivery_by_evidence = {}
    for item in json.loads(DELIVERY_ATLAS.read_text()).get("candidates", []):
        delivery_by_evidence.setdefault(item.get("evidence_id"), []).append(item)
    timing_by_evidence = {}
    for item in json.loads(TIMING_ATLAS.read_text()).get("items", []):
        timing_by_evidence.setdefault(item.get("evidence_id"), []).append(item)
    pose_summaries = json.loads(POSE_MOVEMENT.read_text()).get("video_summary", {})
    visual_summaries = json.loads(VISUAL_MOVEMENT.read_text()).get("video_summary", {})
    cards = []
    relation_cards = []
    job_counts = Counter()
    unclassified = 0
    boundary_items = 0
    for entry in index["entries"]:
        for item in entry["communication_function_inventory"]:
            mapped = taxonomy.get((entry["review_id"], item["sequence"]), {})
            job = mapped.get("canonical_job", "unclassified")
            template = jobs.get(job)
            if job == "unclassified":
                unclassified += 1
            elif job == "media_or_publisher":
                boundary_items += 1
            else:
                job_counts[job] += 1
            segments = []
            for evidence_id in item.get("evidence_ids", [])[:5]:
                row = evidence.get(evidence_id, {})
                segments.append({
                    "evidence_id": evidence_id,
                    "text": row.get("text", ""),
                    "start_seconds": row.get("start_seconds"),
                    "end_seconds": row.get("end_seconds"),
                    "source_url": row.get("source_url"),
                })
            if template:
                form = template["form"]
                mechanism = template["mechanism"]
                practice = template["practice"]
                self_check = template["self_check"]
                non_fit = template["non_fit"]
            else:
                form = "Inspect the complete context first; do not imitate this label without a clearer function decision."
                mechanism = "No shared-job mechanism is assigned until the original function label is reviewed."
                practice = "Rewrite the observed move in plain language, then test whether a listener can identify its purpose."
                self_check = "Can you describe what the speaker is doing without relying on the label alone?"
                non_fit = "Do not turn an unclassified episode into a recommendation."
            phrase_handles = _phrase_handles(entry["video_id"], job, segments, job_phrase_forms, corpus_phrase_forms)
            cards.append({
                "card_id": f"{entry['review_id']}:{item['sequence']}",
                "review_id": entry["review_id"],
                "video_id": entry["video_id"],
                "title": entry["title"],
                "writeup": entry.get("writeup"),
                "canonical_job": job,
                "canonical_job_status": (
                    "heuristic_mapping" if job not in {"unclassified", "media_or_publisher"}
                    else "non_speech_boundary" if job == "media_or_publisher"
                    else "unclassified_pending_review"
                ),
                "raw_function_label": item.get("function", ""),
                "observed_move": item.get("reason", ""),
                "why_it_might_help": mechanism,
                "repeatable_form": form,
                "practice": practice,
                "self_check": self_check,
                "non_fit": non_fit,
                "exact_evidence": segments,
                "phrase_handles": phrase_handles,
                "phrase_handle_status": "indexed_exact_card_evidence_matches" if phrase_handles else "no_indexed_phrase_match_in_card_evidence",
                "delivery_proxy": _delivery_proxy(entry["video_id"], segments, delivery_cache),
                "delivery_candidates": _delivery_candidates(segments, delivery_by_evidence, timing_by_evidence),
                "movement_candidates": _movement_candidates(entry["video_id"], segments, pose_summaries, visual_summaries),
                "review_limits": entry.get("limits", []),
                "next_test": entry.get("next_test", ""),
                "claim_boundary": "Transcript-derived discovery and practice hypothesis only; not independently reviewed, delivery-validated, learner-validated or listener-outcome evidence.",
            })
        for relation_number, relation in enumerate(entry["structural_relation_inventory"], start=1):
            from_ids = relation.get("from_evidence_ids", [])[:3]
            to_ids = relation.get("to_evidence_ids", [])[:3]
            evidence_ids = list(dict.fromkeys(from_ids + to_ids))
            segments = []
            for evidence_id in evidence_ids:
                row = evidence.get(evidence_id, {})
                segments.append({
                    "evidence_id": evidence_id,
                    "text": row.get("text", ""),
                    "start_seconds": row.get("start_seconds"),
                    "end_seconds": row.get("end_seconds"),
                    "source_url": row.get("source_url"),
                })
            relation_cards.append({
                "card_id": f"{entry['review_id']}:relation:{relation_number}",
                "review_id": entry["review_id"],
                "video_id": entry["video_id"],
                "title": entry["title"],
                "writeup": entry.get("writeup"),
                "card_type": "structural_sequence",
                "relation_type": relation.get("type", ""),
                "sequence_claim": relation.get("claim", ""),
                "from_evidence_ids": from_ids,
                "to_evidence_ids": to_ids,
                "exact_evidence": segments,
                "phrase_handles": _phrase_handles(entry["video_id"], "", segments, [], corpus_phrase_forms),
                "delivery_proxy": _delivery_proxy(entry["video_id"], segments, delivery_cache),
                "delivery_candidates": _delivery_candidates(segments, delivery_by_evidence, timing_by_evidence),
                "movement_candidates": _movement_candidates(entry["video_id"], segments, pose_summaries, visual_summaries),
                "why_it_might_help": "Hypothesis: making the bridge between these two moves explicit may reduce the listener's need to infer why the talk changed direction.",
                "repeatable_approach": "Complete the first move, name the relationship, then make the second move; do not assume the audience will supply the bridge.",
                "practice": "Give a 30–60 second explanation using the same move-to-move relationship with a new topic. Ask a listener to name the bridge.",
                "self_check": "Can a listener state what changed and why the second move followed the first?",
                "non_fit": "Do not force a sequence onto a talk whose source context, speaker turns or editing make the relationship uncertain.",
                "review_limits": entry.get("limits", []),
                "next_test": entry.get("next_test", ""),
                "claim_boundary": "Transcript-derived structural relation and practice hypothesis only; not independently reviewed, delivery-validated, learner-validated or listener-outcome evidence.",
            })
    report = {
        "schema_version": "1.0",
        "inventory_id": "corpus-learner-card-inventory",
        "status": "transcript_derived_practice_navigation_not_validated",
        "claim_boundary": "Every card is a way to learn from and inspect a recorded transcript review. It does not establish that the move works, that the speaker intended the inferred function, or that the form should be used universally.",
        "source_artifacts": [str(INDEX.relative_to(ROOT)), str(TAXONOMY.relative_to(ROOT)), str(EVIDENCE.relative_to(ROOT)), str(JOBS.relative_to(ROOT))],
        "summary": {
            "review_count": len(index["entries"]),
            "card_count": len(cards),
            "structural_card_count": len(relation_cards),
            "total_card_count": len(cards) + len(relation_cards),
            "cards_with_exact_evidence": sum(bool(card["exact_evidence"]) for card in cards),
            "structural_cards_with_exact_evidence": sum(bool(card["exact_evidence"]) for card in relation_cards),
            "cards_with_phrase_handles": sum(bool(card["phrase_handles"]) for card in cards),
            "sequence_cards_with_phrase_handles": sum(bool(card["phrase_handles"]) for card in relation_cards),
            "phrase_handle_count": sum(len(card["phrase_handles"]) for card in cards + relation_cards),
            "cards_with_local_delivery_proxy": sum(card["delivery_proxy"]["status"].startswith("local") for card in cards + relation_cards),
            "cards_with_pose_proxy": sum(bool(card["delivery_proxy"].get("pose_frame")) for card in cards + relation_cards),
            "cards_with_delivery_candidates": sum(bool(card["delivery_candidates"]) for card in cards + relation_cards),
            "delivery_candidate_count": sum(len(card["delivery_candidates"]) for card in cards + relation_cards),
            "cards_with_movement_candidates": sum(bool(card["movement_candidates"]) for card in cards + relation_cards),
            "movement_candidate_count": sum(len(card["movement_candidates"]) for card in cards + relation_cards),
            "cards_with_shared_job_template": sum(job_counts.values()),
            "non_speech_or_publisher_boundary_cards": boundary_items,
            "unclassified_cards": unclassified,
            "canonical_job_counts": dict(job_counts.most_common()),
        },
        "cards": cards,
        "structural_cards": relation_cards,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    summary = report["summary"]
    MD.write_text("\n".join([
        "# Corpus learner-card inventory", "",
        "Status: **transcript-derived practice navigation; not validated curriculum**.", "",
        report["claim_boundary"], "",
        f"This inventory contains **{summary['card_count']} function cards** and **{summary['structural_card_count']} sequence cards** from **{summary['review_count']} full-context reviews**. "
        f"Each card preserves the original function label and reason, up to five exact caption segments, a provisional shared-job form where available, a drill, self-check, non-fit warning, limits and next test.", "",
        f"Function cards with exact evidence: **{summary['cards_with_exact_evidence']}** · sequence cards with exact evidence: **{summary['structural_cards_with_exact_evidence']}** of {summary['structural_card_count']} · cards with phrase handles: **{summary['cards_with_phrase_handles']}** · sequence cards with phrase handles: **{summary['sequence_cards_with_phrase_handles']}** · phrase handles: **{summary['phrase_handle_count']}** · cards with local delivery proxies: **{summary['cards_with_local_delivery_proxy']}** · cards with pose proxies: **{summary['cards_with_pose_proxy']}** · cards with delivery candidates: **{summary['cards_with_delivery_candidates']}** (**{summary['delivery_candidate_count']}** windows) · cards with a shared speech-job template: **{summary['cards_with_shared_job_template']}** · publisher/media boundary cards: **{summary['non_speech_or_publisher_boundary_cards']}** · unclassified and requiring review: **{summary['unclassified_cards']}**.", "",
        "Use the [searchable inventory](corpus-learner-card-inventory.html) to filter by video, raw label, canonical job, relation type or wording. Use the linked full writeup and source context before treating a card as a lesson.", "",
        "## How to use one card", "",
        "1. Read the exact evidence and the surrounding writeup.",
        "2. State the communication problem in your own words.",
        "3. Try the repeatable form in a low-stakes example.",
        "4. Run the self-check and note where the form does not fit.",
        "5. Keep delivery, audience effect and factual claims separate until they are independently checked.", "",
        "## Canonical-job distribution", "",
        "| Job | Cards |", "|---|---:|",
        *[f"| `{job}` | {count} |" for job, count in summary["canonical_job_counts"].items()], "",
        "The [JSON inventory](../research/corpus-learner-card-inventory.json) retains every card and its provenance.", "",
    ]) + "\n")
    articles = []
    all_cards = cards + relation_cards
    for card in all_cards:
        is_relation = card.get("card_type") == "structural_sequence"
        search = " ".join([
            card["title"], card["video_id"], card.get("canonical_job", ""),
            card.get("raw_function_label", ""), card.get("observed_move", ""),
            card.get("relation_type", ""), card.get("sequence_claim", ""),
        ] + [x["phrase_form"] + " " + x["text"] for x in card.get("phrase_handles", [])]).lower()
        evidence_html = " ".join(
            f"<blockquote><code>{html.escape(row['evidence_id'])}</code> {html.escape(row['text'])}</blockquote>"
            for row in card["exact_evidence"]
        ) or "<p>No exact segment was linked; inspect the full writeup.</p>"
        writeup = f"<a href='../{html.escape(card['writeup'])}'>full writeup</a>" if card.get("writeup") else ""
        phrase_items = "".join(f"<li><b><code>{html.escape(x['phrase_form'])}</code></b> · {html.escape(x['family'] or '')} · <code>{html.escape(x['evidence_id'])}</code><br>{html.escape(x['text'])}<br><span class='muted'>{html.escape(x['retrieval_status'])}; {html.escape(x['mechanism_hypothesis'] or '')}</span></li>" for x in card.get("phrase_handles", []))
        phrase_html = f"<h3>Exact phrase handles</h3><ul>{phrase_items}</ul>" if phrase_items else "<h3>Exact phrase handles</h3><p class='muted'>No indexed phrase match in this card's retained evidence.</p>"
        proxy = card["delivery_proxy"]
        proxy_html = f"<h3>Delivery inspection proxy</h3><p>{html.escape(proxy['status'])}</p><p><b>Audio:</b> {html.escape(json.dumps(proxy.get('audio_window'), ensure_ascii=False))}</p><p><b>Face/scene:</b> {html.escape(json.dumps(proxy.get('sampled_frame'), ensure_ascii=False))}</p><p><b>Pose:</b> {html.escape(json.dumps(proxy.get('pose_frame'), ensure_ascii=False))}</p><p class='muted'>{html.escape(proxy['claim_boundary'])}</p>"
        candidate_items = "".join(f"<li><b>{html.escape(x['candidate_kind'])}</b> · <code>{html.escape(x.get('evidence_id') or '')}</code> · {html.escape(str(x.get('start_seconds')))}–{html.escape(str(x.get('end_seconds')))}s<br>{html.escape(x.get('candidate_reason') or x.get('status') or '')}</li>" for x in card.get("delivery_candidates", []))
        candidates_html = f"<h3>Nearby delivery candidates</h3><p class='muted'>These windows are routing aids for manual listening/viewing, not interpreted nonverbal findings.</p><ul>{candidate_items}</ul>" if candidate_items else "<h3>Nearby delivery candidates</h3><p class='muted'>No indexed timing or delivery candidate matched this card's retained evidence.</p>"
        movement_items = "".join(f"<li><b>{html.escape(x['candidate_kind'])}</b> · {html.escape(str(x.get('midpoint_seconds', x.get('movement_pairs', ''))))}<br>{html.escape(x.get('status') or '')}</li>" for x in card.get("movement_candidates", []))
        movement_html = f"<h3>Movement inspection candidates</h3><ul>{movement_items}</ul>" if movement_items else "<h3>Movement inspection candidates</h3><p class='muted'>No pose/visual movement summary is available for this card's video.</p>"
        if is_relation:
            heading = f"<p><b>Sequence:</b> <code>{html.escape(card['relation_type'])}</code></p><h3>Sequence claim</h3><p>{html.escape(card['sequence_claim'])}</p>"
            form_heading = "Repeatable approach"
            form = card["repeatable_approach"]
            label = "Structural sequence"
        else:
            heading = f"<p><b>Job:</b> <code>{html.escape(card['canonical_job'])}</code> · <b>Original label:</b> {html.escape(card['raw_function_label'])}</p><h3>Observed move</h3><p>{html.escape(card['observed_move'])}</p>"
            form_heading = "Repeatable form"
            form = card["repeatable_form"]
            label = "Function"
        articles.append(
            f"<article id='card-{html.escape(card['card_id'], quote=True)}' class='card' data-card-id='{html.escape(card['card_id'], quote=True)}' data-video-id='{html.escape(card['video_id'], quote=True)}' data-title='{html.escape(card['title'], quote=True)}' data-job='{html.escape(card.get('canonical_job', ''), quote=True)}' data-source-evidence='{html.escape(','.join(x.get('evidence_id', '') for x in card.get('exact_evidence', [])), quote=True)}' data-search='{html.escape(search, quote=True)}' data-relation='{html.escape(card.get('relation_type', ''), quote=True)}' data-kind='{html.escape(card.get('card_type', 'function'), quote=True)}'>"
            f"<h2>{html.escape(card['title'])}</h2><p><code>{html.escape(card['card_id'])}</code> · {writeup}</p>"
            f"<p><b>Card type:</b> {label}</p>{heading}<h3>Exact evidence</h3>{evidence_html}{phrase_html}{proxy_html}{candidates_html}{movement_html}"
            f"<h3>Why it might help</h3><p>{html.escape(card['why_it_might_help'])}</p>"
            f"<h3>{form_heading}</h3><p>{html.escape(form)}</p>"
            f"<h3>Practice</h3><p>{html.escape(card['practice'])}</p>"
            f"<details><summary>Self-check, non-fit and limits</summary><p><b>Self-check:</b> {html.escape(card['self_check'])}</p><p><b>Non-fit:</b> {html.escape(card['non_fit'])}</p><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in card['review_limits'])}</ul><p>{html.escape(card['claim_boundary'])}</p></details></article>"
        )
    jobs_select = "".join(f"<option>{html.escape(job)}</option>" for job in sorted({c['canonical_job'] for c in cards}))
    relation_select = "".join(f"<option>{html.escape(kind)}</option>" for kind in sorted({c['relation_type'] for c in relation_cards}))
    page = """<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Corpus learner-card inventory</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input,select,button{font:inherit;padding:.6rem;margin:.3rem .5rem .8rem 0}input{width:min(620px,100%)}button{cursor:pointer;background:#173f5f;color:white;border:0;border-radius:4px}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.card{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.card.selected{border:3px solid #d1495b;box-shadow:0 0 0 4px #fbe4e7}.card h2{margin:.1rem 0}.card h3{margin-bottom:.2rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem;margin:.5rem 0}code{overflow-wrap:anywhere}.muted{color:#5c6872}</style><main><h1>Corpus learner-card inventory</h1><div class='notice'><b>Practice navigation, not proof.</b> These cards expose transcript-derived observations from all reviewed videos. “Why it might help” is a hypothesis; exact wording remains retained caption text; delivery and listener effects are not established.</div><p class='muted'>395 reviews · 4,016 function cards + 2,800 sequence cards. Search, inspect the full context, then practice with the limits visible.</p><button id='study' type='button'>Start a practice card</button> <button id='next' type='button'>Next visible card</button><span id='study-status' class='muted'></span><br><label>Job <select id='job'><option value=''>All jobs</option>__JOBS__</select></label><label>Sequence type <select id='relation'><option value=''>All sequences</option>__RELATIONS__</select></label><label>Search <input id='search' type='search' placeholder='title, video ID, original label, relation or wording'></label><p id='count' aria-live='polite'></p><section id='cards'>__CARDS__</section></main><script>const cards=[...document.querySelectorAll('.card')],search=document.querySelector('#search'),job=document.querySelector('#job'),relation=document.querySelector('#relation'),count=document.querySelector('#count'),studyStatus=document.querySelector('#study-status');let selected=-1;function filter(){const q=search.value.toLowerCase(),j=job.value,r=relation.value;let n=0;cards.forEach(c=>{const ok=(!j||c.dataset.job===j)&&(!r||c.dataset.relation===r)&&(!q||c.dataset.search.includes(q));c.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${cards.length} cards`}function visible(){return cards.filter(c=>!c.hidden)}function choose(offset){const pool=visible();if(!pool.length){studyStatus.textContent=' No cards match the current filters.';return}selected=(selected+offset+pool.length)%pool.length;cards.forEach(c=>c.classList.remove('selected'));const card=pool[selected];card.classList.add('selected');card.scrollIntoView({behavior:'smooth',block:'start'});studyStatus.textContent=' Practice the highlighted card, then use its self-check and non-fit notes.'}search.oninput=()=>{selected=-1;filter()};job.onchange=()=>{selected=-1;filter()};relation.onchange=()=>{selected=-1;filter()};document.querySelector('#study').onclick=()=>choose(Math.floor(Math.random()*Math.max(1,visible().length)));document.querySelector('#next').onclick=()=>choose(1);filter()</script>"""
    practice_html = "<section style='background:#eef7f0;border-left:4px solid #4c956c;padding:1rem;margin:1rem 0'><b>Local practice log</b><p class='muted'>Select a card, adapt it in your own words, and record what happened. Do not include sensitive personal information. This export is a learning record, not proof of effectiveness.</p><label>Delivery mode <select id='practice-mode'><option>spoken</option><option>typed</option><option>captioned</option><option>asynchronous</option><option>AAC-supported</option></select></label><label>My adapted wording<textarea id='practice-wording' placeholder='Write your own version of the move'></textarea></label><label>Listener restatement or response<textarea id='listener-restatement' placeholder='What did the listener say they understood?'></textarea></label><label>What was unclear, unsafe or did not fit?<textarea id='practice-nonfit' placeholder='Record uncertainty, burden, access issue or non-fit'></textarea></label><label>Revision for next attempt<textarea id='practice-revision' placeholder='What will you change?'></textarea></label><button id='save-practice' type='button'>Save current practice</button> <button id='download-practice' type='button'>Download practice log</button><span id='practice-status' class='muted'></span></section>"
    page = page.replace("<span id='study-status' class='muted'></span><br>", "<span id='study-status' class='muted'></span>" + practice_html + "<br>")
    practice_js = ";const practiceLog=[];function currentCard(){return document.querySelector('.card.selected')}function field(id){return document.querySelector('#'+id).value.trim()}function clearPractice(){['practice-wording','listener-restatement','practice-nonfit','practice-revision'].forEach(id=>document.querySelector('#'+id).value='')}document.querySelector('#save-practice').onclick=()=>{const c=currentCard();if(!c){document.querySelector('#practice-status').textContent=' Select a practice card first.';return}practiceLog.push({record_type:'local_learner_practice',schema_version:'1.0',created_at:new Date().toISOString(),card_id:c.dataset.cardId,video_id:c.dataset.videoId,title:c.dataset.title,canonical_job:c.dataset.job,source_evidence_ids:c.dataset.sourceEvidence.split(',').filter(Boolean),delivery_mode:document.querySelector('#practice-mode').value,adapted_wording:field('practice-wording'),listener_restatement:field('listener-restatement'),non_fit_or_safety_note:field('practice-nonfit'),revision:field('practice-revision'),claim_boundary:'Learner practice record; not independent validation or proof of listener effectiveness.'});document.querySelector('#practice-status').textContent=' Saved '+practiceLog.length+' practice record(s).';clearPractice()};document.querySelector('#download-practice').onclick=()=>{if(!practiceLog.length){document.querySelector('#practice-status').textContent=' Save a practice record first.';return}const blob=new Blob([JSON.stringify({schema_version:'1.0',record_type:'local_learner_practice_log',claim_boundary:'Learner practice records are not independent validation or proof of effectiveness.',records:practiceLog},null,2)+'\\n'],{type:'application/json'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='corpus-learner-practice-log.json';a.click();URL.revokeObjectURL(u)}"
    page = page.replace("</script>", practice_js + "</script>", 1)
    HTML.write_text(page.replace("__JOBS__", jobs_select).replace("__RELATIONS__", relation_select).replace("__CARDS__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    print(json.dumps(build()["summary"], indent=2))
