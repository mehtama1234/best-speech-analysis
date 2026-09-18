#!/usr/bin/env python3
"""Build a transcript-derived lesson inventory for every completed review.

This is a discovery index, not a validated curriculum.  It exposes the
communication functions, relations, limits and next tests already recorded in
the 395 full-context reviews without silently promoting them to patterns.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def _load_registry(root: Path) -> dict[str, dict]:
    registry: dict[str, dict] = {}
    path = root / "research/segment-registry.jsonl"
    with path.open() as handle:
        for line in handle:
            row = json.loads(line)
            registry.setdefault(row["video_id"], row)
    return registry


def _evidence_set(review: dict) -> set[str]:
    return set(review.get("context_evidence_ids", []))


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    source = json.loads((root / "research/full-context-reviews.json").read_text())
    registry = _load_registry(root)
    entries = []
    function_counts: Counter[str] = Counter()
    relation_counts: Counter[str] = Counter()
    missing_context_ids: list[str] = []

    for review in sorted(source["reviews"], key=lambda item: item["review_id"]):
        video_id = review["video_id"]
        meta = registry.get(video_id, {})
        context_ids = _evidence_set(review)
        functions = []
        for position, item in enumerate(review.get("episode_map", []), start=1):
            evidence_ids = list(item.get("evidence_ids", []))
            missing = [evidence_id for evidence_id in evidence_ids if evidence_id not in context_ids]
            if missing:
                missing_context_ids.extend(missing)
            function = item.get("function", "")
            if function:
                function_counts[function] += 1
            functions.append({
                "sequence": position,
                "function": function,
                "reason": item.get("reason", ""),
                "evidence_ids": evidence_ids,
            })

        relations = []
        for relation in review.get("relations", []):
            relation_type = relation.get("type", "")
            if relation_type:
                relation_counts[relation_type] += 1
            from_ids = list(relation.get("from_evidence_ids", []))
            to_ids = list(relation.get("to_evidence_ids", []))
            missing = [evidence_id for evidence_id in from_ids + to_ids if evidence_id not in context_ids]
            if missing:
                missing_context_ids.extend(missing)
            relations.append({
                "type": relation_type,
                "claim": relation.get("claim", ""),
                "from_evidence_ids": from_ids,
                "to_evidence_ids": to_ids,
            })

        entries.append({
            "review_id": review["review_id"],
            "video_id": video_id,
            "title": meta.get("title") or video_id,
            "channel": meta.get("channel"),
            "video_url": meta.get("video_url"),
            "writeup": review.get("writeup"),
            "modality": review.get("modality"),
            "coverage": review.get("coverage"),
            "lesson_status": "transcript_derived_discovery_not_validated",
            "communication_function_inventory": functions,
            "structural_relation_inventory": relations,
            "boundary_cases": review.get("boundary_cases", []),
            "limits": review.get("limits", []),
            "next_test": review.get("next_test", ""),
        })

    return {
        "schema_version": "1.0",
        "index_id": "corpus-transcript-derived-lesson-inventory",
        "status": "transcript_derived_discovery_index_not_validated",
        "claim_boundary": (
            "This index exposes functions, structural relations, limits and next tests "
            "recorded in full-context transcript reviews. It does not establish recurrence, "
            "delivery effects, teachability, listener outcomes or best-practice status."
        ),
        "source": "research/full-context-reviews.json",
        "review_count": len(entries),
        "entries": entries,
        "summary": {
            "review_count": len(entries),
            "reviews_with_function_inventory": sum(bool(entry["communication_function_inventory"]) for entry in entries),
            "reviews_with_structural_relations": sum(bool(entry["structural_relation_inventory"]) for entry in entries),
            "function_inventory_item_count": sum(len(entry["communication_function_inventory"]) for entry in entries),
            "relation_inventory_item_count": sum(len(entry["structural_relation_inventory"]) for entry in entries),
            "function_counts": dict(function_counts.most_common()),
            "relation_type_counts": dict(relation_counts.most_common()),
            "missing_context_evidence_id_count": len(set(missing_context_ids)),
        },
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/corpus-lesson-index.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    summary = result["summary"]
    lines = [
        "# Corpus transcript-derived lesson inventory",
        "",
        "Status: **discovery index; not validated curriculum**.",
        "",
        "This index exposes the communication functions, structural relations,",
        "limits and next tests recorded in all completed full-context reviews.",
        "It does not establish recurrence, delivery effects, teachability, listener",
        "outcomes or best-practice status.",
        "",
        f"- Reviews indexed: {summary['review_count']}",
        f"- Reviews with function inventories: {summary['reviews_with_function_inventory']}",
        f"- Reviews with structural relations: {summary['reviews_with_structural_relations']}",
        f"- Function inventory items: {summary['function_inventory_item_count']}",
        f"- Relation inventory items: {summary['relation_inventory_item_count']}",
        f"- Missing context evidence IDs: {summary['missing_context_evidence_id_count']}",
        "",
        "Use the [browser](corpus-lesson-index.html) to search by video, title,",
        "function, relation or evidence ID. Open the linked writeup before using",
        "any item as an example or teaching claim.",
        "",
        "## Most common recorded functions",
        "",
    ]
    for label, count in list(summary["function_counts"].items())[:30]:
        lines.append(f"- `{label}` — {count}")
    lines.extend(["", "## Most common recorded structural relations", ""])
    for label, count in list(summary["relation_type_counts"].items())[:30]:
        lines.append(f"- `{label}` — {count}")
    (root / "writeups/corpus-lesson-index.md").write_text("\n".join(lines) + "\n")

    cards = []
    for entry in result["entries"]:
        search_blob = " ".join([
            entry["video_id"], entry["title"] or "", entry["channel"] or "",
            " ".join(item["function"] for item in entry["communication_function_inventory"]),
            " ".join(item["type"] for item in entry["structural_relation_inventory"]),
        ]).lower()
        function_html = "".join(
            f"<li><code>{_escape(item['function'])}</code>: {_escape(item['reason'])} "
            f"<small>{_escape(', '.join(item['evidence_ids']))}</small></li>"
            for item in entry["communication_function_inventory"]
        )
        relation_html = "".join(
            f"<li><code>{_escape(item['type'])}</code>: {_escape(item['claim'])}</li>"
            for item in entry["structural_relation_inventory"]
        )
        limit_html = "".join(f"<li>{_escape(item)}</li>" for item in entry["limits"])
        writeup = entry.get("writeup") or ""
        writeup_link = f"<a href='../{_escape(writeup)}'>full writeup</a>" if writeup else ""
        cards.append(
            f"<article class='entry' data-search='{_escape(search_blob)}'>"
            f"<h2>{_escape(entry['title'])}</h2>"
            f"<p><code>{_escape(entry['video_id'])}</code> · {_escape(entry['review_id'])} · {writeup_link}</p>"
            f"<h3>Recorded communication functions</h3><ol>{function_html or '<li>None recorded</li>'}</ol>"
            f"<h3>Recorded structural relations</h3><ul>{relation_html or '<li>None recorded</li>'}</ul>"
            f"<details><summary>Limits and next test</summary><ul>{limit_html or '<li>None recorded</li>'}</ul>"
            f"<p>{_escape(entry['next_test'])}</p></details></article>"
        )
    html = """<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Corpus lesson inventory</title>
<style>
body{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}
input{width:100%;box-sizing:border-box;padding:.7rem;font:inherit;margin:1rem 0 1.5rem}
.notice{background:#fff4ce;padding:1rem;border-left:4px solid #b8860b}
.entry{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}
small{display:block;color:#53606c;margin-top:.35rem} code{overflow-wrap:anywhere}
h2{margin:.1rem 0}.entry h3{margin-bottom:.25rem} li{margin:.35rem 0}
</style>
<main><h1>Corpus transcript-derived lesson inventory</h1>
<div class="notice"><strong>Discovery only.</strong> These are transcript-review
observations and interpretations, not validated patterns, delivery findings,
learning evidence or listener outcomes.</div>
<p>395 completed full-context reviews. Search by title, video ID, function,
relation type or evidence ID.</p>
<label for="search">Search the inventory</label>
<input id="search" type="search" placeholder="e.g. contrast, repair, video ID, evidence ID">
<p id="count" aria-live="polite"></p><section id="entries">
""" + "\n".join(cards) + """</section></main>
<script>
const input=document.querySelector('#search'), cards=[...document.querySelectorAll('.entry')], count=document.querySelector('#count');
function filter(){const q=input.value.trim().toLowerCase();let n=0;cards.forEach(c=>{const show=!q||c.dataset.search.includes(q);c.hidden=!show;if(show)n++});count.textContent=`Showing ${n} of ${cards.length} reviews`;}
input.addEventListener('input',filter);filter();
</script>
"""
    (root / "writeups/corpus-lesson-index.html").write_text(html)
    return result


def _escape(value: str) -> str:
    import html
    return html.escape(str(value), quote=True)


if __name__ == "__main__":
    output = write_outputs()
    print(json.dumps(output["summary"], indent=2))
