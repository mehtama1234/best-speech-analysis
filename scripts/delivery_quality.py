"""Conservative caption-rate screening, not speech alignment or validation."""
import math

MIN_RATE_DURATION_SECONDS = 0.25


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def rate_exclusion_reason(row):
    start, end = row.get("start_seconds"), row.get("end_seconds")
    if not finite_number(start) or not finite_number(end):
        return "missing_or_nonfinite_caption_timing"
    duration = end - start
    if duration <= 0:
        return "nonpositive_caption_duration"
    if duration < MIN_RATE_DURATION_SECONDS:
        return "caption_duration_below_provisional_0.25_second_floor"
    if not finite_number(row.get("words_per_second_proxy")):
        return "missing_or_nonfinite_rate"
    if row["words_per_second_proxy"] < 0:
        return "negative_rate"
    return None


def screened_value(row, metric):
    if metric == "words_per_second_proxy" and rate_exclusion_reason(row):
        return None
    value = row.get(metric)
    return value if finite_number(value) else None
