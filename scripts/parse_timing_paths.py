#!/usr/bin/env python3
"""Parse OpenSTA-style timing reports into a compact, reusable summary."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


_STARTPOINT = re.compile(r"^\s*Startpoint:\s*(?P<value>\S+)", re.IGNORECASE | re.MULTILINE)
_ENDPOINT = re.compile(r"^\s*Endpoint:\s*(?P<value>\S+)", re.IGNORECASE | re.MULTILINE)
_SLACK = re.compile(
    r"^\s*slack\s*\([^)]*\)\s*(?P<value>-?\d+(?:\.\d+)?)",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(frozen=True)
class TimingPath:
    """Minimal timing-path record that is stable across report formatting changes."""

    index: int
    startpoint: str
    endpoint: str
    slack_ns: float

    @property
    def status(self) -> str:
        return "VIOLATION" if self.slack_ns < 0 else "OK"


def parse_timing_report(text: str) -> list[TimingPath]:
    """Extract timing paths from an OpenSTA-style report.

    A path is formed from a Startpoint block, its first Endpoint line, and
    the first slack value found in that block. Blocks without all three
    fields are skipped rather than producing misleading zero-valued data.
    """

    starts = list(_STARTPOINT.finditer(text))
    paths: list[TimingPath] = []

    for position, match in enumerate(starts, start=1):
        block_end = starts[position].start() if position < len(starts) else len(text)
        block = text[match.start() : block_end]

        endpoint_match = _ENDPOINT.search(block)
        slack_match = _SLACK.search(block)
        if endpoint_match is None or slack_match is None:
            continue

        paths.append(
            TimingPath(
                index=len(paths) + 1,
                startpoint=match.group("value"),
                endpoint=endpoint_match.group("value"),
                slack_ns=float(slack_match.group("value")),
            )
        )

    return paths


def write_csv(paths: list[TimingPath], output: Path) -> None:
    """Write parsed timing paths as a stable CSV artifact."""

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "startpoint", "endpoint", "slack_ns", "status"])
        for path in paths:
            writer.writerow(
                [
                    path.index,
                    path.startpoint,
                    path.endpoint,
                    f"{path.slack_ns:.3f}",
                    path.status,
                ]
            )


def print_summary(paths: list[TimingPath], limit: int) -> None:
    """Print a human-readable timing summary."""

    selected = paths if limit == 0 else paths[:limit]

    print("Path | Startpoint | Endpoint | Slack (ns) | Status")
    print("-" * 78)
    for path in selected:
        print(
            f"{path.index:>4} | {path.startpoint} | {path.endpoint} | "
            f"{path.slack_ns:+.3f} | {path.status}"
        )

    violations = sum(path.slack_ns < 0 for path in paths)
    worst = min((path.slack_ns for path in paths), default=float("nan"))

    print()
    print(f"Total parsed paths : {len(paths)}")
    print(f"Violations         : {violations}")
    if paths:
        print(f"Worst slack (ns)   : {worst:+.3f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse OpenSTA timing paths and optionally write CSV output."
    )
    parser.add_argument("report", help="Path to the OpenSTA timing report.")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum paths to print; use 0 to print all paths (default: 10).",
    )
    parser.add_argument(
        "--violations-only",
        action="store_true",
        help="Print only paths with negative slack.",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Optional output CSV containing the parsed paths.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.limit < 0:
        parser.error("--limit must be >= 0")

    report_path = Path(args.report)
    if not report_path.is_file():
        print(f"Error: timing report '{report_path}' not found.", file=sys.stderr)
        return 2

    text = report_path.read_text(encoding="utf-8", errors="replace")
    paths = parse_timing_report(text)
    if not paths:
        print(
            "Error: no complete timing paths were found "
            "(expected Startpoint / Endpoint / slack fields).",
            file=sys.stderr,
        )
        return 1

    if args.violations_only:
        paths_to_print = [path for path in paths if path.slack_ns < 0]
    else:
        paths_to_print = paths

    print_summary(paths_to_print, args.limit)

    if args.csv is not None:
        write_csv(paths_to_print, args.csv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
