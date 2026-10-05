#!/usr/bin/env python3
"""Compare two OpenLane metrics.csv files and report implementation deltas."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


METRICS = {
    "wns": ("wns", "higher is better"),
    "tns": ("tns", "higher is better"),
    "critical_path_ns": ("critical_path_ns", "lower is better"),
    "DIEAREA_mm^2": ("DIEAREA_mm^2", "lower is better"),
    "wire_length": ("wire_length", "lower is better"),
    "vias": ("vias", "lower is better"),
    "Final_Util": ("Final_Util", "lower is better"),
    "tritonRoute_violations": ("tritonRoute_violations", "lower is better"),
    "Magic_violations": ("Magic_violations", "lower is better"),
    "pin_antenna_violations": ("pin_antenna_violations", "lower is better"),
    "net_antenna_violations": ("net_antenna_violations", "lower is better"),
    "lvs_total_errors": ("lvs_total_errors", "lower is better"),
}


def read_metrics(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{path}: no metric row found")
    return rows[0]


def numeric(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "")
    if value in (None, "", "-1"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def verdict(delta: float, direction: str) -> str:
    if abs(delta) < 1e-12:
        return "UNCHANGED"
    improved = delta > 0 if direction == "higher is better" else delta < 0
    return "IMPROVED" if improved else "REGRESSED"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two OpenLane metrics.csv files."
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--metrics",
        nargs="*",
        choices=sorted(METRICS),
        default=sorted(METRICS),
        help="Metrics to compare; defaults to the complete curated set.",
    )
    args = parser.parse_args()

    try:
        baseline = read_metrics(args.baseline)
        candidate = read_metrics(args.candidate)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print("Metric | Baseline | Candidate | Delta | Assessment")
    print("-" * 82)

    comparable = 0
    regressions = 0
    improvements = 0

    for name in args.metrics:
        key, direction = METRICS[name]
        before = numeric(baseline, key)
        after = numeric(candidate, key)
        if before is None or after is None:
            print(f"{name} | unavailable | unavailable | - | SKIPPED")
            continue

        delta = after - before
        result = verdict(delta, direction)
        comparable += 1
        improvements += result == "IMPROVED"
        regressions += result == "REGRESSED"
        print(f"{name} | {before:.4f} | {after:.4f} | {delta:+.4f} | {result}")

    print()
    print(f"Comparable metrics : {comparable}")
    print(f"Improvements       : {improvements}")
    print(f"Regressions        : {regressions}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())