#!/usr/bin/env python3
"""Build a corpus-wide speaker/event identity and duplication review queue."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/full-reading-queue.json"
REGISTRY = ROOT / "data/metadata/video-registry.jsonl"
OUT_JSON = ROOT / "research/corpus-identity-review-workbook.json"
OUT_MD = ROOT / "writeups/corpus-identity-review-workbook.md"
OUT_HTML = ROOT / "writeups/corpus-identity-review-workbook.html"
OUT_REQUEST = ROOT / "writeups/corpus-identity-review-request.md"


def norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(title or "").lower()).strip()


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    registry = {}
    for line in REGISTRY.read_text().splitlines():
        row = json.loads(line)
        registry[row["video_id"]] = row
    title_groups = defaultdict(list)
    for row in registry.values():
        title_groups[norm_title(row.get("title", ""))].append(row["video_id"])
    items = []
    for row in queue["videos"]:
        meta = registry.get(row["video_id"], {})
        same_title = sorted(v for v in title_groups.get(norm_title(row["title"]), []) if v != row["video_id"])
        items.append({
            "review_item_id": f"identity:{row['video_id']}",
            "video_id": row["video_id"],
            "queue_order": row["order"],
            "title": row["title"],
            "source_url": meta.get("url", f"https://www.youtube.com/watch?v={row['video_id']}"),
            "channel": meta.get("channel"),
            "channel_id": meta.get("channel_id"),
            "uploader_id": meta.get("uploader_id"),
            "duration_seconds": meta.get("duration_seconds"),
            "availability": meta.get("availability"),
            "playlist_memberships": meta.get("playlist_memberships", []),
            "transcript_reviewed": row["has_full_context_analytic_review"],
            "potential_same_title_video_ids": same_title,
            "review": {
                "speaker_identity": None,
                "event_identity": None,
                "upload_event_match": None,
                "duplicate_or_compilation_status": None,
                "source_provenance_status": None,
                "reviewer_code": None,
                "rationale_or_uncertainty": None,
            },
        })
    workbook = {
        "schema_version": "1.0",
        "workbook_id": "corpus-identity-review-workbook",
        "status": "metadata_preflight_independent_review_pending",
        "source_queue": "research/full-reading-queue.json",
        "source_registry": "data/metadata/video-registry.jsonl",
        "item_count": len(items),
        "registry_row_count": len(registry),
        "potential_same_title_group_count": sum(bool(item["potential_same_title_video_ids"]) for item in items),
        "claim_boundary": "This workbook records source metadata and requests independent verification of speaker, event, upload correspondence and duplication status. Registry metadata and title matches are leads, not proof. It does not establish communication effectiveness, speaker intent, delivery meaning or recurrence across independent events.",
        "independence_requirement": "Reviewer must not be the person who created the transcript corpus, labels or identity candidate groups.",
        "decision_vocabulary": {
            "speaker_identity": ["verified", "not_verified", "unclear", "multiple_or_overlapping_speakers"],
            "event_identity": ["verified_distinct_event", "same_event_as_other_upload", "compilation_or_clip", "unclear"],
            "upload_event_match": ["confirmed", "mismatch", "not_checked", "unclear"],
            "duplicate_or_compilation_status": ["distinct_for_counting", "duplicate_exclude", "compilation_exclude_or_bound", "unclear"],
            "source_provenance_status": ["official_or_primary", "reputable_secondary", "edited_repost", "unknown", "restricted"],
        },
        "reviewer": {"name": None, "role": None, "date": None, "conflict_statement": None},
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(workbook, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Corpus identity and duplication review workbook", "", "Status: **metadata preflight; independent review pending**.", "", workbook["claim_boundary"], "", f"Reviewed queue items: **{len(items)}** · registry rows: **{len(registry)}** · possible same-title leads: **{workbook['potential_same_title_group_count']}**.", "", "| # | Video | Title | Channel | Duration | Possible same-title IDs | Review |", "|---:|---|---|---|---:|---:|---|"]
    for n, item in enumerate(items, 1):
        lines.append(f"| {n} | `{item['video_id']}` | {item['title'].replace('|', '\\|')} | {item['channel'] or ''} | {item['duration_seconds'] or ''} | {len(item['potential_same_title_video_ids'])} | pending |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    fieldsets = []
    vocab = workbook["decision_vocabulary"]
    for n, item in enumerate(items, 1):
        selects = "".join(f'<label>{html.escape(key)}<select required name="item_{n}_{key}"><option value="">Choose</option>{"".join(f"<option>{html.escape(value)}</option>" for value in values)}</select></label>' for key, values in vocab.items())
        duplicate = ", ".join(item["potential_same_title_video_ids"]) or "none detected"
        fieldsets.append(f'<fieldset><legend>{n}. {html.escape(item["video_id"])} · {html.escape(item["title"])}</legend><p><a href="{html.escape(item["source_url"], quote=True)}" target="_blank" rel="noopener">source</a> · channel: {html.escape(str(item["channel"]))} · duration: {html.escape(str(item["duration_seconds"]))}s<br>Possible same-title IDs: {html.escape(duplicate)}</p>{selects}<label>Reviewer code<input required name="item_{n}_reviewer_code"></label><label>Rationale or uncertainty<textarea required name="item_{n}_rationale_or_uncertainty" rows="2"></textarea></label></fieldset>')
    OUT_HTML.write_text(f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Corpus identity review</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem}}fieldset{{margin:1rem 0;padding:1rem;border:1px solid #9aa7b2;border-radius:.5rem}}label{{display:block;margin:.4rem 0}}textarea{{width:100%;box-sizing:border-box}}.notice{{background:#fff6d6;padding:.8rem}}</style><h1>Corpus identity and duplication review</h1><div class="notice">{html.escape(workbook["claim_boundary"])}</div><form id="review"><fieldset><legend>Reviewer identity</legend><label>Name/code<input required name="reviewer_name"></label><label>Role<input required name="reviewer_role"></label><label>Date<input required type="date" name="review_date"></label><label>Modality<textarea required name="review_modality" rows="2"></textarea></label><label>Conflict statement<textarea required name="conflict_statement" rows="2"></textarea></label><label><input required type="checkbox" name="independent_attestation"> I am independent of corpus construction and candidate grouping.</label></fieldset>{''.join(fieldsets)}<button type="button" id="download">Download review JSON</button></form><script>document.querySelector('#download').onclick=()=>{{const f=document.querySelector('#review');if(!f.reportValidity())return;const r={{}};for(const e of f.elements)if(e.name)r[e.name]=e.type==='checkbox'?e.checked:e.value;const blob=new Blob([JSON.stringify({{schema_version:'1.0',record_type:'corpus_identity_independent_review',workbook_id:'corpus-identity-review-workbook',claim_boundary:'Identity and duplication review only; not recurrence or effectiveness evidence.',responses:r}},null,2)+'\\n'],{{type:'application/json'}}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='corpus-identity-independent-review.json';a.click();URL.revokeObjectURL(u)}};</script>''')
    OUT_REQUEST.write_text("""# Corpus identity and duplication review request\n\nReview all 395 full-context queue items independently. Use registry metadata only as a lead. Verify speaker identity, event identity, upload/event correspondence and duplicate/compilation status; preserve `unclear` and `not_checked` decisions. Do not count title matches as proof of independent recurrence.\n\n- Workbook: `research/corpus-identity-review-workbook.json`\n- Browser form: `writeups/corpus-identity-review-workbook.html`\n- Validator: `scripts/validate_corpus_identity_review.py`\n\nThis review does not establish delivery effectiveness, speaker intent, audience outcomes or universal best practice.\n""")
    print(f"wrote corpus identity workbook ({len(items)} items; {workbook['potential_same_title_group_count']} same-title leads)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
