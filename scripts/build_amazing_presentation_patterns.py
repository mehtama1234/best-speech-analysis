#!/usr/bin/env python3
"""Build a searchable presenter-facing browser for all mined pattern candidates."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "research/exhaustive-pattern-inventory.json"
EVIDENCE = ROOT / "research/all-55-pattern-evidence.json"
OUTPUT = ROOT / "writeups/amazing-presentation-patterns.html"


def load_cards() -> list[dict]:
    inventory = json.loads(INVENTORY.read_text())
    evidence = {
        item["pattern_id"]: item
        for item in json.loads(EVIDENCE.read_text())["patterns"]
    }
    cards = []
    groups = [
        ("core theme", "themes", "theme_id", "episode_hit_count"),
        ("structural subtheme", "relation_patterns", "relation_type", "relation_count"),
        ("additional subtheme", "unmatched_clusters", "cluster_id", "label_hit_count"),
    ]
    for category, collection, id_key, count_key in groups:
        for item in inventory[collection]:
            example = (item.get("examples") or [{}])[0]
            cards.append({
                "id": item[id_key],
                "category": category,
                "form": item.get("candidate_form", ""),
                "video_count": item.get("video_count", 0),
                "source_count": item.get(count_key, 0),
                "example_video": example.get("video_id", ""),
                "example_label": example.get("label") or example.get("claim", "source-linked candidate"),
                "writeup": example.get("writeup", ""),
                "evidence_ids": example.get("evidence_ids", [])[:3],
                "direct_recovered_video_count": evidence[item[id_key]].get("direct_recovered_video_count", 0),
                "alternate_source_video_count": evidence[item[id_key]].get("alternate_source_video_count", 0),
                "external_transcript_video_count": evidence[item[id_key]].get("external_transcript_video_count", 0),
                "direct_recovered_flagged_video_count": evidence[item[id_key]].get("direct_recovered_flagged_video_count", 0),
            })
    return cards


def render(cards: list[dict]) -> str:
    payload = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    categories = sorted({card["category"] for card in cards})
    options = "".join(
        '<option value="' + html.escape(category) + '">' + html.escape(category.title()) + "</option>"
        for category in categories
    )
    template = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Amazing presentation patterns</title>
<style>
:root { --bg:#f5f7fb; --card:#fff; --ink:#172033; --muted:#5e687a; --line:#dce2ee; --accent:#2457d6; --warn:#fff2cf; }
* { box-sizing:border-box; } body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui,sans-serif; }
main { max-width:1120px; margin:auto; padding:30px 18px 70px; } h1 { margin-bottom:8px; }
.muted { color:var(--muted); } .boundary { background:var(--warn); padding:13px 15px; border-radius:9px; }
.controls { position:sticky; top:0; z-index:2; display:flex; gap:10px; flex-wrap:wrap; padding:14px 0; background:rgba(245,247,251,.96); }
input,select { border:1px solid var(--line); border-radius:8px; padding:10px 12px; font:inherit; background:#fff; }
input { flex:1; min-width:250px; } .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(310px,1fr)); gap:14px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:11px; padding:17px; }
.tag { display:inline-block; color:var(--accent); font-size:.8rem; font-weight:700; text-transform:uppercase; letter-spacing:.04em; }
.form { font-size:1.05rem; font-weight:650; margin:10px 0; } .stats { color:var(--muted); font-size:.88rem; }
.use { background:#f1f5ff; padding:10px 12px; border-radius:7px; margin:12px 0; }
details { margin-top:10px; } summary { cursor:pointer; color:var(--accent); } a { color:var(--accent); } code { font-size:.86em; }
.empty { padding:25px 0; color:var(--muted); }
.draft { border:0; border-radius:7px; padding:9px 12px; background:var(--accent); color:#fff; font:inherit; cursor:pointer; }
</style>
</head>
<body><main>
<h1>Amazing presentation patterns</h1>
<p class="muted">55 source-linked candidate patterns across the fixed 480-video inventory: 395 project-generated single-pass full-context transcript reviews (not independent human validation), 71 direct recovered transcript candidates, 11 alternate-source candidates, and 1 external transcript candidate.</p>
<p class="muted"><a href="all-55-pattern-evidence.md">Open the all-55 evidence matrix</a> · <a href="recovered-pattern-candidate-cards.md">Open recovered candidate cards</a> · <a href="recovered-pattern-independent-review.html">Open blinded review</a> · <a href="corpus-coverage-audit.md">Open the coverage audit</a></p>
<p class="boundary">These are drafting structures and discovery candidates. They are not proof of speaker intent, universal effectiveness, or listener outcomes. Adapt the structure to your own evidence, audience and voice.</p>
<div class="controls"><input id="search" type="search" placeholder="Search themes, forms, or source labels…"><select id="category"><option value="">All categories</option>__OPTIONS__</select><input id="topic" type="text" placeholder="Presentation topic"><input id="audience" type="text" placeholder="Audience"><input id="outcome" type="text" placeholder="Desired outcome"></div>
<p id="count" class="muted"></p><section id="cards" class="grid"></section><p id="empty" class="empty" hidden>No patterns match that search.</p>
</main>
<script>
const PATTERNS = __PAYLOAD__;
const cards = document.querySelector("#cards");
const empty = document.querySelector("#empty");
const count = document.querySelector("#count");
const esc = value => String(value || "").replace(/[&<>"']/g, function(char) {
  return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char];
});
function render() {
  const query = document.querySelector("#search").value.toLowerCase().trim();
  const category = document.querySelector("#category").value;
  const shown = PATTERNS.filter(function(item) {
    return (!category || item.category === category) &&
      (!query || JSON.stringify(item).toLowerCase().includes(query));
  });
  count.textContent = shown.length + " of " + PATTERNS.length + " patterns";
  empty.hidden = shown.length !== 0;
  cards.innerHTML = shown.map(function(item) {
    const evidence = (item.evidence_ids || []).map(esc).join(", ");
    const source = item.writeup
      ? "<a href='../" + esc(item.writeup) + "'>" + esc(item.writeup) + "</a>"
      : "source record";
    return "<article class='card'><span class='tag'>" + esc(item.category) + "</span>" +
      "<h2>" + esc(item.id) + "</h2><p class='form'>" + esc(item.form) + "</p>" +
      "<p class='stats'>" + esc(item.video_count) + " canonical videos · " + esc(item.source_count) + " canonical records<br>" +
      esc(item.direct_recovered_video_count) + " direct recovery candidates (" + esc(item.direct_recovered_flagged_video_count) + " flagged) · " +
      esc(item.alternate_source_video_count) + " alternate-source candidates · " + esc(item.external_transcript_video_count) + " external candidates</p>" +
      "<p class='use'><strong>How to use:</strong> Turn each stage of this form into one sentence in your own presentation. Add a concrete example, name the condition or limit, then ask a listener to restate the point.</p>" +
      "<button class='draft' data-pattern='" + esc(item.id) + "'>Download local worksheet</button> " +
      "<details><summary>Open source anchor</summary><p><strong>Video:</strong> <code>" + esc(item.example_video) +
      "</code><br><strong>Corpus label:</strong> " + esc(item.example_label) + "<br><strong>Writeup:</strong> " + source +
      "<br><strong>Evidence:</strong> <code>" + evidence + "</code></p></details></article>";
  }).join("");
}
document.querySelector("#search").addEventListener("input", render);
document.querySelector("#category").addEventListener("change", render);
function downloadWorksheet(id) {
  const item = PATTERNS.find(function(candidate) { return candidate.id === id; });
  if (!item) return;
  const topic = document.querySelector("#topic").value || "Your presentation topic";
  const audience = document.querySelector("#audience").value || "Your audience";
  const outcome = document.querySelector("#outcome").value || "What should the audience understand, decide, or do?";
  const text = "# Presentation worksheet: " + topic + "\\n\\n" +
    "- Audience: " + audience + "\\n- Desired outcome: " + outcome + "\\n" +
    "- Pattern: `" + item.id + "`\\n\\n" +
    "## Candidate form\\n\\n" + item.form + "\\n\\n" +
    "## Draft in your own words\\n\\n" +
    "1. First move:\\n\\n2. Next move:\\n\\n3. Evidence or example:\\n\\n4. Condition, boundary, or non-fit:\\n\\n" +
    "## Listener check\\n\\n- What is the main point?\\n- What changed or became clearer?\\n- What remains uncertain?\\n- Did any part feel pressuring, exclusionary, or hard to access?\\n\\n" +
    "## Revision\\n\\n" +
    "## Source anchor\\n\\n" + item.writeup + " / " + (item.evidence_ids || []).join(", ") + "\\n\\n" +
    "This is a local drafting aid, not evidence that the pattern is universally effective.\\n";
  const blob = new Blob([text], {type: "text/markdown"});
  const link = document.createElement("a"); link.href = URL.createObjectURL(blob);
  link.download = "presentation-" + item.id + ".md"; link.click(); URL.revokeObjectURL(link.href);
}
document.querySelector("#cards").addEventListener("click", function(event) {
  const button = event.target.closest("button[data-pattern]");
  if (button) downloadWorksheet(button.dataset.pattern);
});
render();
</script></body></html>"""
    return template.replace("__OPTIONS__", options).replace("__PAYLOAD__", payload)


if __name__ == "__main__":
    cards = load_cards()
    OUTPUT.write_text(render(cards))
    print("amazing presentation patterns: " + str(len(cards)) + " cards written to " + str(OUTPUT))
