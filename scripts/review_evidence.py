"""Resolve label-specific assistant reviews without rewriting legacy judgments."""
import hashlib
import json


def context_digest(rows):
    payload = [{key: row[key] for key in
                ("evidence_id", "start_seconds", "end_seconds", "text")}
               for row in rows]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load_annotations(root):
    rows = [json.loads(line) for line in
            (root / "research/annotation-ledger.jsonl").read_text().splitlines() if line.strip()]
    path = root / "research/contextual-label-reviews.json"
    reviews = json.loads(path.read_text())["reviews"] if path.exists() else []
    originals = {row["annotation_id"]: row for row in rows}
    needed = {eid for review in reviews for eid in review["context_evidence_ids"]}
    context = {}
    if needed:
        with (root / "research/segment-registry.jsonl").open() as source:
            for line in source:
                item = json.loads(line)
                if item["evidence_id"] in needed:
                    context[item["evidence_id"]] = item
    seen = set()
    for review in reviews:
        original = originals[review["annotation_id"]]
        assert review["evidence_id"] == original["evidence_id"], "Review target mismatch"
        assert review["evidence_id"] in review["context_evidence_ids"], "Target outside context"
        assert review["reviewer_type"] == "assistant", "Unsupported reviewer provenance"
        assert review["modality"] == "transcript_only", "Unsupported review modality"
        assert context_digest([context[eid] for eid in review["context_evidence_ids"]]) == review["context_sha256"], "Stale review context"
        decisions = review["label_decisions"]
        assert set(decisions) == set(original["candidate_labels"]), "Incomplete per-label review"
        assert original["annotation_id"] not in seen, "Duplicate contextual review"
        seen.add(original["annotation_id"])
        for decision in decisions.values():
            assert type(decision["supported"]) is bool and decision["reason"], "Invalid decision"
        original["label_decisions"] = decisions
        original["contextual_review_id"] = review["review_id"]
    return rows


def label_supported(row, label):
    if "label_decisions" in row:
        return row["label_decisions"][label]["supported"]
    return row.get("candidate_label_supported") is True


def supported_labels(row):
    return [label for label in row.get("candidate_labels", []) if label_supported(row, label)]


def label_reason(row, label):
    return row.get("label_decisions", {}).get(label, {}).get("reason", row.get("direct_observation"))
