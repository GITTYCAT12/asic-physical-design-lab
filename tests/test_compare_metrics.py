"""Unit tests for the PPA metric comparison helper.

Run with: python -m unittest discover -s tests -v
"""
import tempfile
import unittest
from pathlib import Path

from scripts.compare_metrics import numeric, read_metrics, verdict


class CompareMetricsTests(unittest.TestCase):
    def test_numeric_parses_valid_value(self):
        self.assertEqual(numeric({"wns": "-0.125"}, "wns"), -0.125)

    def test_numeric_skips_missing_and_sentinel_values(self):
        self.assertIsNone(numeric({"wns": ""}, "wns"))
        self.assertIsNone(numeric({"wns": "-1"}, "wns"))
        self.assertIsNone(numeric({}, "wns"))

    def test_verdict_respects_metric_direction(self):
        self.assertEqual(verdict(0.2, "higher is better"), "IMPROVED")
        self.assertEqual(verdict(-0.2, "higher is better"), "REGRESSED")
        self.assertEqual(verdict(-2.0, "lower is better"), "IMPROVED")
        self.assertEqual(verdict(2.0, "lower is better"), "REGRESSED")
        self.assertEqual(verdict(0.0, "lower is better"), "UNCHANGED")

    def test_read_metrics_uses_first_csv_row(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.csv"
            path.write_text("wns,tns\n-0.1,-1.2\n0.0,0.0\n", encoding="utf-8")
            self.assertEqual(read_metrics(path), {"wns": "-0.1", "tns": "-1.2"})

    def test_read_metrics_rejects_empty_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.csv"
            path.write_text("wns,tns\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_metrics(path)


if __name__ == "__main__":
    unittest.main()
