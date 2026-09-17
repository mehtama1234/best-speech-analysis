"""Known source restrictions, not certification of unrestricted sources."""
import json


def restrictions_by_video(reviews):
    result = {}
    for review in reviews:
        flags = review.get('evidence_restrictions', [])
        if flags:
            result.setdefault(review['video_id'], set()).update(flags)
    return {vid: sorted(flags) for vid, flags in sorted(result.items())}


def load_restrictions(root):
    path = root / 'research/full-context-reviews.json'
    return restrictions_by_video(json.loads(path.read_text())['reviews'])
