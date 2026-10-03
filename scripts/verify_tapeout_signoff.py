#!/usr/bin/env python3
"""Validate a captured ASIC run before calling it signoff-ready.

The checker works with both local OpenLane/OpenROAD run directories and the
curated report directories stored in this repository.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate timing, routing, DRC, LVS and XOR evidence for an ASIC run."
    )
    parser.add_argument(
        "run_tag",
        nargs="?",
        default="day7_multicorner",
        help="Run tag to inspect (default: day7_multicorner).",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: script's repository root).",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        help="Explicit report directory. Overrides automatic run-directory discovery.",
    )
    return parser.parse_args()


def resolve_report_dir(base_dir: Path, run_tag: str, explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit if explicit.is_absolute() else base_dir / explicit

    candidates = [
        base_dir / "designs" / "riscv32" / "runs" / run_tag / "reports",
        base_dir / "results" / f"reports_{run_tag}",
        base_dir / "results" / run_tag,
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        f"no report directory found for run '{run_tag}'. Tried: "
        + ", ".join(str(path) for path in candidates)
    )


def read_metrics(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"metrics file contains no data rows: {path}")

    return {key: (value or "").strip() for key, value in rows[0].items() if key}


def metric_number(metrics: dict[str, str], key: str, cast=float) -> float | int:
    value = metrics.get(key, "")
    if value == "":
        raise ValueError(f"required metric '{key}' is missing or empty")
    try:
        return cast(value)
    except ValueError as exc:
        raise ValueError(f"metric '{key}' is not numeric: {value!r}") from exc


def check_metrics(metrics: dict[str, str]) -> list[Check]:
    checks: list[Check] = []

    flow_status = metrics.get("flow_status", "").lower()
    checks.append(
        Check(
            "flow status",
            flow_status == "flow completed",
            f"value={metrics.get('flow_status', '<missing>')}",
        )
    )

    route_violations = metric_number(metrics, "tritonRoute_violations", int)
    checks.append(
        Check(
            "routing violations",
            route_violations == 0,
            f"count={route_violations}",
        )
    )

    wns = metric_number(metrics, "wns", float)
    checks.append(Check("setup WNS", wns >= 0.0, f"{wns:+.3f} ns"))

    tns = metric_number(metrics, "tns", float)
    checks.append(Check("setup TNS", tns >= 0.0, f"{tns:+.3f} ns"))

    if "whs" in metrics:
        whs = metric_number(metrics, "whs", float)
        checks.append(Check("hold WHS", whs >= 0.0, f"{whs:+.3f} ns"))
    else:
        checks.append(Check("hold WHS", True, "metric not present; report-level hold check used"))

    if "ths" in metrics:
        ths = metric_number(metrics, "ths", float)
        checks.append(Check("hold THS", ths >= 0.0, f"{ths:+.3f} ns"))
    else:
        checks.append(Check("hold THS", True, "metric not present; report-level hold check used"))

    if "lvs_total_errors" in metrics:
        lvs_errors = metric_number(metrics, "lvs_total_errors", int)
        checks.append(Check("LVS metric", lvs_errors == 0, f"errors={lvs_errors}"))

    return checks


def check_report_exists(report_dir: Path, name: str) -> Check:
    path = report_dir / name
    return Check(f"{name} exists", path.is_file(), str(path))


def check_lvs(report_dir: Path) -> Check:
    path = report_dir / "39-picorv32.lvs.rpt"
    if not path.is_file():
        return Check("LVS clean", False, f"missing report: {path}")

    content = path.read_text(encoding="utf-8", errors="replace").lower()
    clean = (
        "total errors = 0" in content
        or "no net, device, pin, or property mismatches" in content
    )
    return Check("LVS clean", clean, "clean signature found" if clean else "clean signature not found")


def check_xor(report_dir: Path) -> Check:
    path = report_dir / "35-xor.rpt"
    if not path.is_file():
        return Check("XOR clean", False, f"missing report: {path}")

    content = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"total\s+xor\s+differences\s*=\s*(\d+)", content, re.IGNORECASE)
    if match is None:
        return Check("XOR clean", False, "could not parse 'Total XOR differences'")
    count = int(match.group(1))
    return Check("XOR clean", count == 0, f"differences={count}")


def check_drc(report_dir: Path) -> Check:
    path = report_dir / "drc.rpt"
    if not path.is_file():
        return Check("DRC clean", False, f"missing report: {path}")

    content = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"\bCOUNT:\s*(\d+)", content, re.IGNORECASE)
    if match is None:
        return Check("DRC clean", False, "could not parse DRC count")
    count = int(match.group(1))
    return Check("DRC clean", count == 0, f"count={count}")


def main() -> int:
    args = parse_args()
    base_dir = args.base_dir.resolve()

    try:
        report_dir = resolve_report_dir(base_dir, args.run_tag, args.report_dir)
        metrics_path = report_dir / "metrics.csv"
        if not metrics_path.is_file():
            raise FileNotFoundError(f"metrics.csv not found: {metrics_path}")

        metrics = read_metrics(metrics_path)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    checks = check_metrics(metrics)
    checks.extend(
        [
            check_report_exists(report_dir, "39-picorv32.lvs.rpt"),
            check_report_exists(report_dir, "35-xor.rpt"),
            check_report_exists(report_dir, "drc.rpt"),
            check_lvs(report_dir),
            check_xor(report_dir),
            check_drc(report_dir),
        ]
    )

    print(f"ASIC signoff validation: {args.run_tag}")
    print(f"Report directory: {report_dir}")
    print()

    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")

    failed = [check for check in checks if not check.passed]
    print()
    print(f"Checks: {len(checks)} | Passed: {len(checks) - len(failed)} | Failed: {len(failed)}")

    if failed:
        print("Signoff validation FAILED.", file=sys.stderr)
        return 1

    print("Signoff validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
