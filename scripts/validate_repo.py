#!/usr/bin/env python3
"""Validate the lightweight, source-controlled parts of the ASIC lab."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    ".gitignore",
    "configs/config.json",
    "designs/riscv32/config.json",
    "constraints/clocks.sdc",
    "rtl/picorv32.v",
    "scripts/parse_timing_paths.py",
    "results/experiment_status.csv",
]

REQUIRED_DIRS = ["rtl", "configs", "constraints", "designs", "scripts", "results"]
STATUS_VALUES = {"captured", "placeholder"}


def fail(message: str) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)


def validate_paths() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in REQUIRED_DIRS:
        if not (ROOT / relative).is_dir():
            errors.append(f"missing required directory: {relative}")
    return errors


def validate_json() -> list[str]:
    errors: list[str] = []
    for relative in ("configs/config.json", "designs/riscv32/config.json"):
        path = ROOT / relative
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {relative}: {exc}")
    return errors


def read_status_rows() -> list[dict[str, str]]:
    path = ROOT / "results/experiment_status.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    expected = {"experiment", "status", "artifact", "notes"}
    actual = set(rows[0]) if rows else set()
    missing = expected - actual
    if missing:
        raise ValueError(f"status manifest missing columns: {sorted(missing)}")

    return rows


def validate_status_manifest() -> list[str]:
    errors: list[str] = []
    try:
        rows = read_status_rows()
    except (OSError, ValueError, csv.Error) as exc:
        return [f"cannot read results/experiment_status.csv: {exc}"]

    seen: set[str] = set()

    for row in rows:
        name = row["experiment"].strip()
        status = row["status"].strip()
        artifact = row["artifact"].strip()

        if not name:
            errors.append("status manifest contains an empty experiment name")
            continue
        if name in seen:
            errors.append(f"duplicate experiment in status manifest: {name}")
        seen.add(name)

        if status not in STATUS_VALUES:
            errors.append(f"{name}: unsupported status '{status}'")

        artifact_path = ROOT / "results" / artifact
        if not artifact_path.is_file():
            errors.append(f"{name}: artifact does not exist: results/{artifact}")
            continue

        if artifact_path.suffix.lower() != ".csv":
            continue

        try:
            with artifact_path.open(newline="", encoding="utf-8") as handle:
                csv_rows = list(csv.reader(handle))
        except (OSError, csv.Error) as exc:
            errors.append(f"{name}: cannot read {artifact}: {exc}")
            continue

        if not csv_rows or not any(cell.strip() for cell in csv_rows[0]):
            errors.append(f"{name}: CSV has no header: results/{artifact}")
            continue

        data_rows = [row for row in csv_rows[1:] if any(cell.strip() for cell in row)]
        if status == "captured" and not data_rows:
            errors.append(f"{name}: marked captured but artifact contains no data rows")
        if status == "placeholder" and data_rows:
            errors.append(f"{name}: marked placeholder but artifact contains data rows")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_paths())
    if not any("configs/config.json" in error or "designs/riscv32/config.json" in error for error in errors):
        errors.extend(validate_json())
    if not any("results/experiment_status.csv" in error for error in errors):
        errors.extend(validate_status_manifest())

    if errors:
        for error in errors:
            fail(error)
        print(f"Validation failed with {len(errors)} issue(s).", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    print("Source-controlled structure, JSON configuration, and experiment-status manifest are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
