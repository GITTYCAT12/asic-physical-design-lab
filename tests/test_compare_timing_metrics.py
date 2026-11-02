"""Tests for the JSON STA-metrics comparison helper.

Run with: python -m unittest discover -s tests -v
"""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.compare_timing_metrics import load_metrics


class CompareTimingMetricsTests(unittest.TestCase):
    def load_payload(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return load_metrics(path)

    def test_loads_supported_metrics_and_ignores_unrelated_keys(self):
        result = self.load_payload({
            "wns_ns": -0.125,
            "tns_ns": -1.5,
            "hold_wns_ns": 0.02,
            "violating_endpoints": 3,
            "run_tag": "baseline",
        })
        self.assertEqual(result, {
            "wns_ns": -0.125,
            "tns_ns": -1.5,
            "hold_wns_ns": 0.02,
            "violating_endpoints": 3,
        })

    def test_missing_metrics_are_allowed(self):
        self.assertEqual(self.load_payload({"wns_ns": None, "notes": "n/a"}), {})

    def test_rejects_non_object_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.json"
            path.write_text('[1, 2]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must be an object"):
                load_metrics(path)

    def test_rejects_strings_and_booleans(self):
        for value in ("-0.1", True):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "must be numeric"):
                    self.load_payload({"wns_ns": value})

    def test_rejects_non_finite_slack(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "must be finite"):
                    self.load_payload({"wns_ns": value})

    def test_endpoint_count_must_be_non_negative_integer(self):
        for value in (-1, -0.5, 1.5):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "non-negative integer"):
                    self.load_payload({"violating_endpoints": value})

    def test_zero_endpoint_count_is_valid(self):
        self.assertEqual(self.load_payload({"violating_endpoints": 0}), {
            "violating_endpoints": 0,
        })


if __name__ == "__main__":
    unittest.main()
