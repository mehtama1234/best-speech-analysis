#!/usr/bin/env python3
"""Build a bounded delivery-observation queue for all 18 communication jobs."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "research/corpus-evidence-bank.json"
CARDS = ROOT / "research/communication-job-cards.json"
COVERAGE = ROOT / "research/multimodal-coverage-audit.json"
OUT_JSON = ROOT / "research/communication-job-delivery-sampling.json"
OUT_MD = ROOT / "writeups/communication-job-delivery-sampling.md"
OUT_HTML = ROOT / "writeups/communication-job-delivery-sampling.html"
MARKER = re.compile(r"^\s*\[[^\]]+\]\s*$")

REVIEW_FIELDS = (
    "transcript_alignment",
    "vocal_timing_observation",
    "audio_measurement_and_limit",
    "visual_observation",
    "setting_editing_music_observation",
    "speaker_event_identity",
    "missingness_or_accessibility_note",
    "reviewer_code",
)


def lexical_words(record: dict) -> int:
    return sum(len(re.findall(r"[A-Za-zÀ-ÿ]+", s.get("text", ""))) for s in record.get("segments", [])[:3] if not MARKER.match(s.get("text", "")))


def main() -> int:
    bank = json.loads(BANK.read_text())
    cards = json.loads(CARDS.read_text())["cards"]
    coverage = json.loads(COVERAGE.read_text())
    media = {item["video_id"]: item for item in coverage["videos"]}
    by_job = defaultdict(list)
    for record in bank["records"]:
        if record["canonical_job"] in {card["canonical_job"] for card in cards} and record.get("segments"):
            info = media.get(record["video_id"], {})
            raw = info.get("media_state") == "raw_audio_video_present"
            by_job[record["canonical_job"]].append((0 if raw else 1, -lexical_words(record), record["video_id"], record, info))
    items = []
    for card in cards:
        job = card["canonical_job"]
        selected = []
        seen = set()
        for _raw_rank, _word_rank, video_id, record, info in sorted(by_job[job], key=lambda row: (row[0], row[1], row[2])):
            if video_id in seen:
                continue
            seen.add(video_id)
            segments = record["segments"][:3]
            selected.append({
                "sample_id": f"delivery:{job}:{len(selected)+1:02d}",
                "card_id": card["card_id"],
                "canonical_job": job,
                "evidence_id": segments[0]["evidence_id"],
                "video_id": video_id,
                "title": record["title"],
                "start_seconds": segments[0]["start_seconds"],
                "end_seconds": segments[-1]["end_seconds"],
                "source_url": record["source_url"],
                "transcript_excerpt": " ".join(s["text"] for s in segments),
                "transcript_segment_ids": [s["evidence_id"] for s in segments],
                "raw_media_state": info.get("media_state", "not_in_selected_media_audit"),
                "video_file": (info.get("video_files") or [None])[0],
                "audio_file": (info.get("audio_files") or [None])[0],
                "feature_file": (info.get("feature_files") or [None])[0],
                "selection_note": "ranked for raw audio/video when available, then lexical transcript context; this is a sampling queue, not an observation",
                "review": {
                    "transcript_alignment": None,
                    "vocal_timing_observation": None,
                    "audio_measurement_and_limit": None,
                    "visual_observation": None,
                    "setting_editing_music_observation": None,
                    "speaker_event_identity": None,
                    "missingness_or_accessibility_note": None,
                    "reviewer_code": None,
                },
            })
            if len(selected) == 2:
                break
        items.extend(selected)
    workbook = {
        "schema_version": "1.0",
        "sampling_id": "communication-job-delivery-sampling",
        "status": "queue_built_manual_observation_pending",
        "source_evidence_bank": "research/corpus-evidence-bank.json",
        "source_media_audit": "research/multimodal-coverage-audit.json",
        "job_count": len(cards),
        "target_samples_per_job": 2,
        "item_count": len(items),
        "claim_boundary": "This is a stratified queue for manual delivery and setting observation. It does not itself contain vocal, nonverbal, editing, room, speaker-intent or effectiveness findings. Derived features are proxies and raw-media absence remains visible.",
        "review_schema": {
            "record_type": "communication_job_delivery_sampling_review",
            "required_session_fields": ["reviewer_name", "reviewer_role", "review_date", "review_modality", "conflict_statement"],
            "required_item_fields": list(REVIEW_FIELDS),
            "transcript_alignment_values": ["aligned", "partially_aligned", "not_aligned", "indeterminate"],
            "independence_note": "A reviewer code and conflict statement are required; an export is not independent merely because those fields are present.",
        },
        "coverage_summary": {"raw_audio_video_items": sum(i["raw_media_state"] == "raw_audio_video_present" for i in items), "derived_or_other_items": sum(i["raw_media_state"] != "raw_audio_video_present" for i in items), "manual_observations_completed": 0},
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job delivery sampling queue", "", "Status: **queue built; manual observation pending**.", "", workbook["claim_boundary"], "", f"Jobs: **{len(cards)}** · target: **2 samples/job** · queued: **{len(items)}** · raw audio/video: **{workbook['coverage_summary']['raw_audio_video_items']}**.", "", "| Job | Sample | Video | Media state | Transcript window | Manual review |", "|---|---:|---|---|---|---|"]
    for item in items:
        lines.append(f"| `{item['canonical_job']}` | {item['sample_id'][-2:]} | `{item['video_id']}` | `{item['raw_media_state']}` | `{item['start_seconds']}`–`{item['end_seconds']}s` | pending |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fieldsets = []
    for n, item in enumerate(items, 1):
        fieldsets.append(f'''<fieldset><legend>{n}. {html.escape(item['canonical_job'])} · {html.escape(item['video_id'])}</legend><p><b>{html.escape(item['evidence_id'])}</b> · {item['start_seconds']}–{item['end_seconds']}s · <a href="{html.escape(item['source_url'], quote=True)}" target="_blank" rel="noopener">source</a><br>{html.escape(item['transcript_excerpt'])}<br><small>Media: {html.escape(item['raw_media_state'])}; feature: {html.escape(str(item['feature_file']))}</small></p><label>Transcript alignment<select required name="item_{n}_transcript_alignment"><option value="">Choose</option><option>aligned</option><option>partially_aligned</option><option>not_aligned</option><option>indeterminate</option></select></label><label>Vocal/timing observation<textarea required name="item_{n}_vocal_timing_observation" rows="2"></textarea></label><label>Audio measurement and limit<textarea required name="item_{n}_audio_measurement_and_limit" rows="2"></textarea></label><label>Visual observation<textarea required name="item_{n}_visual_observation" rows="2"></textarea></label><label>Setting/editing/music observation<textarea required name="item_{n}_setting_editing_music_observation" rows="2"></textarea></label><label>Speaker/event identity<textarea required name="item_{n}_speaker_event_identity" rows="2"></textarea></label><label>Missingness/accessibility note<textarea required name="item_{n}_missingness_or_accessibility_note" rows="2"></textarea></label><label>Reviewer code<input required name="item_{n}_reviewer_code"></label></fieldset>''')
    OUT_HTML.write_text(f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication-job delivery sampling</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.5rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style><h1>Communication-job delivery sampling</h1><div class="notice">{html.escape(workbook["claim_boundary"])}</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<textarea required name="review_modality" rows="2"></textarea></label><label>Independence/conflict statement<textarea required name="conflict_statement" rows="2"></textarea></label></fieldset>{''.join(fieldsets)}<button type="button" id="download">Download observations JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'communication_job_delivery_sampling_review',sampling_id:'communication-job-delivery-sampling',claim_boundary:'Manual delivery observation only; not effectiveness evidence.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='communication-job-delivery-observations.json';a.click();URL.revokeObjectURL(u)}};</script>''')
    print(f"wrote delivery sampling queue ({len(items)} items; {workbook['coverage_summary']['raw_audio_video_items']} raw audio/video)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
