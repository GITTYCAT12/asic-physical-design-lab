"""Unit tests for OpenSTA timing-report parsing and CSV output.

Run with: python -m unittest discover -s tests -v
"""

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.parse_timing_paths import parse_timing_report, write_csv


SAMPLE_REPORT = """Startpoint: top/u_reg0/Q
Endpoint: top/u_reg1/D
slack (VIOLATED) -0.125

Startpoint: top/u_reg2/Q
Endpoint: top/u_reg3/D
slack (MET) 0.250
"""


class ParseTimingPathsTests(unittest.TestCase):
    def test_parses_multiple_paths_and_classifies_slack(self):
        paths = parse_timing_report(SAMPLE_REPORT)

        self.assertEqual(len(paths), 2)
        self.assertEqual(
            (paths[0].index, paths[0].startpoint, paths[0].endpoint),
            (1, "top/u_reg0/Q", "top/u_reg1/D"),
        )
        self.assertAlmostEqual(paths[0].slack_ns, -0.125)
        self.assertEqual(paths[0].status, "VIOLATION")
        self.assertAlmostEqual(paths[1].slack_ns, 0.250)
        self.assertEqual(paths[1].status, "OK")

    def test_skips_incomplete_blocks_without_gaps_in_path_indices(self):
        report = """Startpoint: top/incomplete/Q
Endpoint: top/no_slack/D

Startpoint: top/complete/Q
Endpoint: top/complete/D
slack (MET) 0.000
"""
        paths = parse_timing_report(report)

        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0].index, 1)
        self.assertEqual(paths[0].startpoint, "top/complete/Q")
        self.assertEqual(paths[0].slack_ns, 0.0)
        self.assertEqual(paths[0].status, "OK")

    def test_returns_empty_list_when_report_has_no_complete_paths(self):
        self.assertEqual(parse_timing_report("No timing paths found.\n"), [])

    def test_write_csv_creates_parent_and_emits_stable_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "timing" / "paths.csv"
            paths = parse_timing_report(SAMPLE_REPORT)

            write_csv(paths, output)

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))

        self.assertEqual(
            rows[0], ["path", "startpoint", "endpoint", "slack_ns", "status"]
        )
        self.assertEqual(rows[1], ["1", "top/u_reg0/Q", "top/u_reg1/D", "-0.125", "VIOLATION"])
        self.assertEqual(rows[2], ["2", "top/u_reg2/Q", "top/u_reg3/D", "0.250", "OK"])


if __name__ == "__main__":
    unittest.main()
