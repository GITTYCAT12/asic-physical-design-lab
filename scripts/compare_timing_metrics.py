#!/usr/bin/env python3
"""Compare baseline and candidate STA metrics supplied as JSON.

Usage: python scripts/compare_timing_metrics.py baseline.json candidate.json

Optional JSON keys: wns_ns, tns_ns, hold_wns_ns, violating_endpoints.
Slack values are in nanoseconds. This compares supplied values; it does not
parse EDA reports or certify timing signoff.
"""
import json
import math
import sys
from pathlib import Path

METRICS = (
    ("wns_ns", "Setup WNS (ns)"),
    ("tns_ns", "Setup TNS (ns)"),
    ("hold_wns_ns", "Hold WNS (ns)"),
    ("violating_endpoints", "Violating endpoints"),
)


def load_metrics(path):
    """Load recognized metrics and reject malformed or non-finite values."""
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")

    result = {}
    for key, _ in METRICS:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{path}: {key} must be numeric")
        if not math.isfinite(value):
            raise ValueError(f"{path}: {key} must be finite")
        if key == "violating_endpoints" and (value < 0 or not value.is_integer() if isinstance(value, float) else value < 0):
            raise ValueError(f"{path}: violating_endpoints must be a non-negative integer")
        result[key] = value
    return result


def fmt(value):
    return "—" if value is None else f"{value:.4f}"


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {Path(argv[0]).name} baseline.json candidate.json", file=sys.stderr)
        return 2

    try:
        baseline = load_metrics(argv[1])
        candidate = load_metrics(argv[2])
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(f"Baseline:  {argv[1]}")
    print(f"Candidate: {argv[2]}")
    print(f"{'Metric':<28} {'Baseline':>12} {'Candidate':>12} {'Delta':>12}")
    print("-" * 68)

    found = False
    for key, label in METRICS:
        if key not in baseline and key not in candidate:
            continue
        found = True
        old, new = baseline.get(key), candidate.get(key)
        delta = None if old is None or new is None else new - old
        print(f"{label:<28} {fmt(old):>12} {fmt(new):>12} {fmt(delta):>12}")

    if not found:
        print("No recognized metrics found. Expected keys: " + ", ".join(k for k, _ in METRICS))
    print("\nInterpret slack signs using your STA tool's conventions; validate all corners.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
