#!/usr/bin/env python3
"""Build a small label-blinded launch packet spanning every recovered pattern."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/recovered-pattern-candidate-cards.json"
OUT = ROOT / "research/recovered-pattern-priority-review.json"
KEY = ROOT / "research/recovered-pattern-priority-review-key.json"
MD = ROOT / "writeups/recovered-pattern-priority-review.md"


def blind_id(card_id: str) -> str:
    return "priority-blind-" + hashlib.sha256(card_id.encode()).hexdigest()[:14]


def select(cards: list[dict]) -> list[dict]:
    if not cards:
        return []

    # Preserve the existing per-pattern scope: up to three cards, each from a
    # different catalog video. Global source constraints prevent popular videos
    # from being mistaken for independent replications across many patterns.
    ordered = sorted(cards, key=lambda card: card["card_id"])
    grouped = defaultdict(list)
    for index, card in enumerate(ordered):
        grouped[card["pattern_id"]].append(index)
    quotas = {
        pattern_id: min(3, len({ordered[index]["video_id"] for index in indices}))
        for pattern_id, indices in grouped.items()
    }
    item_count = sum(quotas.values())
    source_limit = 3
    source_ids = sorted({card.get("candidate_video_id") or card["video_id"] for card in ordered})
    source_variable = {source_id: len(ordered) + index for index, source_id in enumerate(source_ids)}
    variable_count = len(ordered) + len(source_ids)

    by_pattern = defaultdict(list)
    by_linked_source = defaultdict(list)
    by_catalog_source = defaultdict(list)
    by_pattern_source = defaultdict(list)
    def linked_source(card):
        return card.get("candidate_video_id") or card["video_id"]

    for index, card in enumerate(ordered):
        by_pattern[card["pattern_id"]].append(index)
        by_linked_source[linked_source(card)].append(index)
        by_catalog_source[card["video_id"]].append(index)
        by_pattern_source[(card["pattern_id"], linked_source(card))].append(index)

    constraints = []
    lower_bounds = []
    upper_bounds = []

    def add_constraint(indices, values, lower, upper):
        constraints.append((indices, values))
        lower_bounds.append(lower)
        upper_bounds.append(upper)

    for pattern_id, indices in sorted(by_pattern.items()):
        add_constraint(indices, [1] * len(indices), quotas[pattern_id], quotas[pattern_id])
    for source_id, indices in sorted(by_linked_source.items()):
        add_constraint(indices, [1] * len(indices), -np.inf, source_limit)
        used = source_variable[source_id]
        add_constraint(indices + [used], [1] * len(indices) + [-source_limit], -np.inf, 0)
        add_constraint(indices + [used], [-1] * len(indices) + [1], -np.inf, 0)
    for indices in by_catalog_source.values():
        add_constraint(indices, [1] * len(indices), -np.inf, source_limit)
    for indices in by_pattern_source.values():
        add_constraint(indices, [1] * len(indices), -np.inf, 1)

    row_indices = []
    column_indices = []
    coefficients = []
    for row, (indices, values) in enumerate(constraints):
        row_indices.extend([row] * len(indices))
        column_indices.extend(indices)
        coefficients.extend(values)
    matrix = coo_matrix(
        (coefficients, (row_indices, column_indices)),
        shape=(len(constraints), variable_count),
    ).tocsr()

    # Lexicographically maximize distinct linked source videos, then minimize
    # existing structural quality flags, with card ID as a stable final tie-break.
    maximum_flag_cost = sum(
        sorted((len(card.get("quality_flags", [])) for card in ordered), reverse=True)[:item_count]
    )
    source_reward = maximum_flag_cost + 1
    objective = np.zeros(variable_count)
    for index, card in enumerate(ordered):
        objective[index] = len(card.get("quality_flags", [])) + index * 1e-9
    for index in source_variable.values():
        objective[index] = -source_reward

    result = milp(
        objective,
        integrality=np.ones(variable_count),
        bounds=Bounds(np.zeros(variable_count), np.ones(variable_count)),
        constraints=LinearConstraint(matrix, lower_bounds, upper_bounds),
        options={"time_limit": 60},
    )
    if not result.success or result.x is None:
        raise RuntimeError(f"could not build source-diverse review batch: {result.message}")

    selected = [card for index, card in enumerate(ordered) if result.x[index] > 0.5]
    selected_by_pattern = Counter(card["pattern_id"] for card in selected)
    selected_by_source = Counter(linked_source(card) for card in selected)
    selected_by_catalog = Counter(card["video_id"] for card in selected)
    if selected_by_pattern != Counter(quotas):
        raise RuntimeError("review batch does not preserve the per-pattern item quotas")
    if max(selected_by_source.values(), default=0) > source_limit:
        raise RuntimeError("review batch exceeds the linked-source reuse limit")
    if max(selected_by_catalog.values(), default=0) > source_limit:
        raise RuntimeError("review batch exceeds the original catalog-source reuse limit")
    return selected


def main() -> int:
    source = json.loads(CARDS.read_text())
    cards = select(source["cards"])
    items = []
    key_items = []
    for card in cards:
        bid = blind_id(card["card_id"])
        items.append({
            "blind_item_id": bid,
            # Give reviewers the claim they must inspect, while withholding the
            # internal pattern name, category and card ID. A decision without
            # the proposed move would have no defined target.
            "proposed_move": card["candidate_form"],
            "video_id": card["video_id"],
            "candidate_video_id": card.get("candidate_video_id"),
            "original_source_url": (
                f"https://www.youtube.com/watch?v={card['video_id']}"
                if card.get("candidate_video_id") and card["candidate_video_id"] != card["video_id"]
                else None
            ),
            "title": card.get("title"),
            "evidence_layer": card["evidence_layer"],
            "source_url": f"https://www.youtube.com/watch?v={card['candidate_video_id'] or card['video_id']}",
            "evidence": card["evidence"],
            "review_prompt": "Compare the excerpt with the proposed move above. Decide whether it shows that move, does something else, or cannot be judged from the available context. Check the source, surrounding context and caption quality.",
        })
        key_items.append({
            "blind_item_id": bid,
            "card_id": card["card_id"],
            "pattern_id": card["pattern_id"],
            "category": card["category"],
            "candidate_form": card["candidate_form"],
            "quality_flags": card.get("quality_flags", []),
            "quality_disposition": card.get("quality_disposition"),
        })
    items.sort(key=lambda item: item["blind_item_id"])
    key_items.sort(key=lambda item: item["blind_item_id"])
    pattern_ids = sorted({item["pattern_id"] for item in key_items})
    linked_source_counts = Counter(item["source_url"].rsplit("=", 1)[-1] for item in items)
    catalog_source_counts = Counter(item["video_id"] for item in items)
    candidate_linked_sources = {
        card.get("candidate_video_id") or card["video_id"]
        for card in source["cards"]
    }
    candidate_catalog_sources = {card["video_id"] for card in source["cards"]}
    layer_counts = Counter(item["evidence_layer"] for item in items)
    selection_rule = (
        "Preserve up to three distinct catalog videos per pattern. Globally maximize distinct linked source videos, "
        "cap reuse at three items per linked source and per original catalog video, then prefer fewer structural "
        "quality flags. Source reuse remains clustered evidence, not independent replication."
    )
    packet = {
        "schema_version": "1.0",
        "review_packet_id": "recovered-pattern-priority-review",
        "status": "priority_launch_packet_no_human_records",
        "claim_boundary": "This is a bounded label-blinded review launch packet. It does not establish semantic accuracy, recurrence, delivery meaning, learner transfer, listener outcomes or effectiveness.",
        "selection_rule": selection_rule,
        "pattern_count": len(pattern_ids),
        "item_count": len(items),
        "source_coverage": {
            "candidate_linked_source_count": len(candidate_linked_sources),
            "selected_linked_source_count": len(linked_source_counts),
            "maximum_items_per_linked_source": max(linked_source_counts.values()),
            "candidate_catalog_video_count": len(candidate_catalog_sources),
            "selected_catalog_video_count": len(catalog_source_counts),
            "maximum_items_per_catalog_video": max(catalog_source_counts.values()),
            "selected_evidence_layer_counts": dict(sorted(layer_counts.items())),
        },
        "promotion_eligible": False,
        "items": items,
    }
    key = {
        "schema_version": "1.0",
        "status": "internal_priority_key_do_not_send_with_packet",
        "claim_boundary": "Internal mapping only; it is not independent evidence.",
        "items": key_items,
    }
    OUT.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    KEY.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Recovered-pattern priority review packet",
        "",
        "Status: **priority launch packet; no human records received**.",
        "",
        packet["claim_boundary"],
        "",
        f"Patterns covered: **{len(pattern_ids)} / 55** · blinded items: **{len(items)}** · distinct linked sources: **{len(linked_source_counts)} / {len(candidate_linked_sources)}** · maximum reuse per linked source: **{max(linked_source_counts.values())}**.",
        "",
        packet["selection_rule"] + " The selection uses the full available linked-source pool but still contains up to three examples per source; do not treat all 162 items as independent video-level replications. The one external-transcript source is represented only within that same cap, so the packet does not reproduce the candidate pool's evidence-layer proportions.",
        "",
        "## Files",
        "",
        "- Packet to send: `research/recovered-pattern-priority-review.json`",
        "- Internal key: `research/recovered-pattern-priority-review-key.json` (do not send)",
        "- Exhaustive packet: `research/recovered-pattern-independent-review-workbook.json`",
        "- Browser surface: `writeups/recovered-pattern-priority-review.html`",
        "- Export validator: `scripts/validate_recovered_pattern_priority_review_export.py`",
        "- Two-review comparison: `scripts/compare_recovered_pattern_priority_reviews.py`",
        "- Disagreement packet builder: `scripts/build_recovered_pattern_priority_adjudication.py`",
        "",
        "## Reviewer instructions",
        "",
        "The packet shows a short description of the proposed move so you know what to check. It hides the internal pattern name, category and card ID. Review every item independently; do not look at the internal key or another reviewer's decisions. The reviewer must not be the analyst who created the candidate cards or key. For each excerpt, say what the speaker is doing, give another plausible reading, note relevant context, flag source/accessibility concerns and record uncertainty. Choose 'not enough context' or 'unclear' when needed; do not force a positive answer.",
        "",
        "Return the downloaded JSON export unchanged. If an item cannot be reviewed, leave it missing rather than guessing; partial exports are accepted and the validator and comparator preserve missing decisions and notes. Do not include or request the internal key. The validator checks export shape only; it does not verify reviewer independence or the truth of any decision. Obtain two genuinely independent returns before comparing them. Preserve disagreements and route them to the adjudication packet; neither agreement nor adjudication establishes recurrence, delivery meaning, teachability, listener outcomes or effectiveness.",
        "",
        "A returned review can support or reject a retrieval candidate; it cannot prove recurrence, delivery meaning, teachability or effectiveness.",
    ]) + "\n")
    print(json.dumps({"pattern_count": len(pattern_ids), "item_count": len(items), "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
