#!/usr/bin/env python3
"""Build one bounded learner entry point for every reviewed corpus video."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/corpus-learner-card-inventory.json"
OUT = ROOT / "research/corpus-video-learning-itinerary.json"
MD = ROOT / "writeups/corpus-video-learning-itinerary.md"
HTML = ROOT / "writeups/corpus-video-learning-itinerary.html"
JOB_PHRASES = ROOT / "research/job-phrase-candidate-inventory.json"
CORPUS_PHRASES = ROOT / "research/corpus-phrase-form-inventory.json"


def rank_function(card: dict) -> tuple:
    return (
        card.get("canonical_job_status") == "heuristic_mapping",
        bool(card.get("exact_evidence")),
        card.get("canonical_job") not in {"media_or_publisher", "unclassified"},
        len(card.get("observed_move", "")),
    )


def nearest(rows: list[dict], time_seconds: float | None) -> dict | None:
    if not rows or time_seconds is None:
        return None
    return min(rows, key=lambda row: abs(float(row.get("time_seconds", row.get("start_seconds", 0))) - time_seconds))


def delivery_proxy(video_id: str, exact_evidence: list[dict]) -> dict:
    feature_path = ROOT / "data/features" / f"{video_id}.json"
    pose_path = ROOT / "data/pose-features" / f"{video_id}.json"
    if not feature_path.exists():
        return {"status": "not_available_no_local_feature_report", "claim_boundary": "No local audio/visual/pose proxy is available for this video."}
    feature = json.loads(feature_path.read_text())
    target_time = exact_evidence[0].get("start_seconds") if exact_evidence else None
    audio = nearest(feature.get("audio_windows", []), target_time)
    frame = nearest(feature.get("sampled_frames", []), target_time)
    pose = None
    if pose_path.exists():
        pose = nearest(json.loads(pose_path.read_text()).get("frames", []), target_time)
    return {
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


def phrase_handles(video_id: str, canonical_job: str, job_forms: list[dict], corpus_forms: list[dict]) -> list[dict]:
    """Return exact inventory examples attached to this video."""
    handles = []
    seen = set()
    for form in job_forms:
        if form.get("canonical_job") != canonical_job:
            continue
        for example in form.get("examples", []):
            if example.get("video_id") != video_id:
                continue
            key = (form.get("phrase_form"), "job", example.get("evidence_id"))
            if key in seen:
                continue
            seen.add(key)
            handles.append({
                "phrase_form": form.get("phrase_form"), "family": canonical_job,
                "candidate_kind": form.get("candidate_kind"), "status": form.get("status"),
                "mechanism_hypothesis": form.get("mechanism_hypothesis"),
                "evidence_id": example.get("evidence_id"), "text": example.get("text"),
                "source_url": example.get("source_url"),
                "retrieval_status": "exact_inventory_example_not_validated_best_practice",
            })
    for form in corpus_forms:
        for example in form.get("examples", []):
            if example.get("video_id") != video_id:
                continue
            key = (form.get("phrase_form"), "corpus", example.get("evidence_id"))
            if key in seen:
                continue
            seen.add(key)
            handles.append({
                "phrase_form": form.get("phrase_form"), "family": form.get("family"),
                "candidate_kind": "exact_form_inventory",
                "status": form.get("review_status") or form.get("status"),
                "mechanism_hypothesis": form.get("mechanism_hypothesis"),
                "evidence_id": example.get("evidence_id"), "text": example.get("text"),
                "source_url": example.get("source_url"),
                "retrieval_status": "exact_inventory_example_not_validated_best_practice",
            })
    handles.sort(key=lambda item: (item["candidate_kind"] != "content_bearing_retrieval_form", item["phrase_form"], item["evidence_id"]))
    return handles[:8]


def build() -> dict:
    data = json.loads(CARDS.read_text())
    job_phrase_forms = json.loads(JOB_PHRASES.read_text())["forms"]
    corpus_phrase_forms = json.loads(CORPUS_PHRASES.read_text())["forms"]
    by_video = {}
    for card in data["cards"]:
        by_video.setdefault(card["video_id"], []).append(card)
    relations = {}
    for card in data["structural_cards"]:
        relations.setdefault(card["video_id"], []).append(card)
    rows = []
    for video_id in sorted(by_video):
        functions = sorted(by_video[video_id], key=rank_function, reverse=True)
        chosen = functions[0]
        sequence = sorted(relations.get(video_id, []), key=lambda x: bool(x.get("exact_evidence")), reverse=True)
        bridge = sequence[0] if sequence else None
        if chosen["canonical_job"] not in {"unclassified", "media_or_publisher"}:
            learning_track = "canonical_job_lesson"
        elif bridge and bridge.get("relation_type"):
            learning_track = "structural_bridge_lesson"
        else:
            learning_track = "transcript_exploration_lead"
        proxy = delivery_proxy(video_id, chosen["exact_evidence"])
        handles = phrase_handles(video_id, chosen["canonical_job"], job_phrase_forms, corpus_phrase_forms)
        rows.append({
            "video_id": video_id,
            "title": chosen["title"],
            "writeup": chosen.get("writeup"),
            "lesson_card_id": chosen["card_id"],
            "canonical_job": chosen["canonical_job"],
            "learning_track": learning_track,
            "raw_function_label": chosen["raw_function_label"],
            "observed_move": chosen["observed_move"],
            "why_it_might_help": chosen["why_it_might_help"],
            "repeatable_form": chosen["repeatable_form"],
            "practice": chosen["practice"],
            "self_check": chosen["self_check"],
            "exact_evidence": chosen["exact_evidence"],
            "sequence_card_id": bridge["card_id"] if bridge else None,
            "sequence_type": bridge["relation_type"] if bridge else None,
            "sequence_claim": bridge["sequence_claim"] if bridge else None,
            "sequence_evidence": bridge["exact_evidence"] if bridge else [],
            "delivery_proxy": proxy,
            "phrase_handles": handles,
            "phrase_handle_status": "indexed_exact_examples_available" if handles else "no_indexed_phrase_handle_for_selected_video_and_job",
            "limits": chosen["review_limits"],
            "next_test": chosen["next_test"],
            "claim_boundary": "One selected transcript-derived learning entry; selection is a navigation aid, not a best-practice ranking or effectiveness result.",
        })
    report = {
        "schema_version": "1.0",
        "itinerary_id": "corpus-video-learning-itinerary",
        "status": "one_entry_per_reviewed_video_transcript_derived_not_validated",
        "claim_boundary": "This itinerary gives one practical starting lesson for each reviewed video. It does not claim that the selected item is the most important, representative, recurrent, effective or independently verified lesson from that video.",
        "source": "research/corpus-learner-card-inventory.json",
        "video_count": len(rows),
        "entries_with_exact_evidence": sum(bool(row["exact_evidence"]) for row in rows),
        "entries_with_sequence_bridge": sum(bool(row["sequence_card_id"]) for row in rows),
        "entries_with_local_delivery_proxy": sum(row["delivery_proxy"]["status"].startswith("local") for row in rows),
        "entries_with_pose_proxy": sum(bool(row["delivery_proxy"].get("pose_frame")) for row in rows),
        "entries_with_phrase_handles": sum(bool(row["phrase_handles"]) for row in rows),
        "phrase_handle_count": sum(len(row["phrase_handles"]) for row in rows),
        "learning_track_counts": {track: sum(row["learning_track"] == track for row in rows) for track in sorted({row["learning_track"] for row in rows})},
        "entries": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Corpus video-learning itinerary", "", "Status: **one selected starting lesson per reviewed video; transcript-derived and not validated**.", "", report["claim_boundary"], "", f"Entries: **{len(rows)} videos** · exact evidence attached: **{report['entries_with_exact_evidence']}** · sequence bridge attached: **{report['entries_with_sequence_bridge']}** · local delivery proxy attached: **{report['entries_with_local_delivery_proxy']}** · pose proxy attached: **{report['entries_with_pose_proxy']}**.", "", "Use one entry as a short lesson: read the evidence, name the move, inspect any exact phrase handle, adapt the form, practice it in a new situation, then run the self-check. Phrase handles are retrieval candidates, not scripts or proof of effectiveness. Open the linked card inventory for alternate functions and the full writeup for limits. Delivery fields are inspection aids, not recommendations.", "", "## Selected entries", "", "| Video | Job | Selected move | Bridge | Phrase handles |", "|---|---|---|---|---:|"]
    lines.insert(6, f"Phrase handles: **{report['phrase_handle_count']}** across **{report['entries_with_phrase_handles']}** entries. Learning tracks: **{report['learning_track_counts'].get('canonical_job_lesson', 0)}** canonical-job lessons · **{report['learning_track_counts'].get('structural_bridge_lesson', 0)}** structural-bridge lessons · **{report['learning_track_counts'].get('transcript_exploration_lead', 0)}** transcript-exploration leads. These are exact inventory retrieval candidates, not scripts or proof of effectiveness.")
    for row in rows:
        title = row["title"].replace("|", "\\|")
        move = (row["observed_move"] or row["raw_function_label"] or "(no move text)").replace("|", "\\|")[:140]
        lines.append(f"| `{row['video_id']}` {title} | `{row['canonical_job']}` | {move} | `{row['sequence_type'] or 'none'}` | {len(row['phrase_handles'])} |")
    lines += ["", "The [searchable itinerary](corpus-video-learning-itinerary.html) provides the full entry cards and filters.", ""]
    MD.write_text("\n".join(lines))
    articles = []
    for row in rows:
        search = " ".join([row["video_id"], row["title"], row["canonical_job"], row["learning_track"], row["raw_function_label"], row["observed_move"], row["sequence_type"] or ""] + [x["phrase_form"] + " " + x["text"] for x in row["phrase_handles"]]).lower()
        evidence = " ".join(f"<blockquote><code>{html.escape(x['evidence_id'])}</code> {html.escape(x['text'])}</blockquote>" for x in row["exact_evidence"]) or "<p>No exact segment was linked; inspect the full writeup.</p>"
        phrase_items = "".join(f"<li><b><code>{html.escape(x['phrase_form'])}</code></b> · {html.escape(x['family'] or '')} · <code>{html.escape(x['evidence_id'])}</code><br>{html.escape(x['text'])}<br><a href='{html.escape(x['source_url'], quote=True)}'>source</a><br><span class='muted'>{html.escape(x['retrieval_status'])}; {html.escape(x['mechanism_hypothesis'] or '')}</span></li>" for x in row["phrase_handles"])
        phrase_html = f"<h3>Exact phrase handles</h3><p class='muted'>Indexed wording found in this video; reread the context before adapting it.</p><ul>{phrase_items}</ul>" if phrase_items else "<h3>Exact phrase handles</h3><p>No indexed phrase handle for this selected video/job. Do not infer a phrase from the lesson summary.</p>"
        bridge = f"<p><b>Sequence bridge:</b> <code>{html.escape(row['sequence_type'] or '')}</code> {html.escape(row['sequence_claim'] or '')}</p>" if row["sequence_card_id"] else "<p>No sequence bridge was recorded.</p>"
        proxy = row["delivery_proxy"]
        proxy_html = f"<h3>Delivery inspection proxy</h3><p>{html.escape(proxy['status'])}</p><p><b>Audio window:</b> {html.escape(json.dumps(proxy.get('audio_window'), ensure_ascii=False))}</p><p><b>Sampled face/scene frame:</b> {html.escape(json.dumps(proxy.get('sampled_frame'), ensure_ascii=False))}</p><p><b>Pose frame:</b> {html.escape(json.dumps(proxy.get('pose_frame'), ensure_ascii=False))}</p><p class='muted'>{html.escape(proxy['claim_boundary'])}</p>"
        writeup = f"<a href='../{html.escape(row['writeup'])}'>full writeup</a>" if row.get("writeup") else ""
        articles.append(f"<article class='entry' data-search='{html.escape(search, quote=True)}'><h2>{html.escape(row['title'])}</h2><p><code>{html.escape(row['video_id'])}</code> · {writeup}</p><p><b>Track:</b> <code>{html.escape(row['learning_track'])}</code> · <b>Job:</b> <code>{html.escape(row['canonical_job'])}</code> · <b>Original label:</b> {html.escape(row['raw_function_label'])}</p><h3>What to notice</h3><p>{html.escape(row['observed_move'])}</p><h3>Exact evidence</h3>{evidence}{phrase_html}{bridge}{proxy_html}<h3>Try it</h3><p><b>Form:</b> {html.escape(row['repeatable_form'])}</p><p>{html.escape(row['practice'])}</p><h3>Self-check</h3><p>{html.escape(row['self_check'])}</p><details><summary>Limits and next test</summary><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in row['limits'])}</ul><p>{html.escape(row['next_test'])}</p><p>{html.escape(row['claim_boundary'])}</p></details></article>")
    HTML.write_text("""<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Corpus video-learning itinerary</title><style>body{font:15px/1.45 system-ui,sans-serif;max-width:1150px;margin:2rem auto;padding:0 1rem;color:#17202a}input{font:inherit;padding:.7rem;width:min(700px,100%);margin:1rem 0}.notice{background:#fff4ce;border-left:4px solid #b8860b;padding:1rem}.entry{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.entry h2{margin:.1rem 0}.entry h3{margin-bottom:.2rem}blockquote{background:#f4f8fb;border-left:4px solid #39739d;padding:.6rem;margin:.5rem 0}code{overflow-wrap:anywhere}</style><main><h1>Corpus video-learning itinerary</h1><div class='notice'><b>Starting points, not rankings.</b> One transcript-derived learning entry is selected for each reviewed video. Search, read the exact context, adapt the move and keep the stated limits visible.</div><p>395 video entries · exact evidence and practice prompts included.</p><label for='search'>Search by video, title, job, label or wording</label><input id='search' type='search'><p id='count' aria-live='polite'></p><section id='entries'>__ENTRIES__</section></main><script>const entries=[...document.querySelectorAll('.entry')],input=document.querySelector('#search'),count=document.querySelector('#count');function filter(){const q=input.value.toLowerCase();let n=0;entries.forEach(x=>{const ok=!q||x.dataset.search.includes(q);x.hidden=!ok;if(ok)n++});count.textContent=`Showing ${n} of ${entries.length} videos`}input.oninput=filter;filter()</script>""".replace("__ENTRIES__", "\n".join(articles)))
    return report


if __name__ == "__main__":
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": build()["video_count"]}, indent=2))
