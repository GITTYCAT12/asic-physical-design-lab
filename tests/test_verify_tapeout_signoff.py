"""Regression tests for fail-closed ASIC signoff metric handling."""

import unittest

from scripts.verify_tapeout_signoff import check_metrics, metric_number


BASE_METRICS = {
    "flow_status": "flow completed",
    "tritonRoute_violations": "0",
    "wns": "0.025",
    "tns": "0.0",
}


class SignoffMetricTests(unittest.TestCase):
    def test_missing_hold_metrics_remain_unverified(self):
        checks = {check.name: check for check in check_metrics(BASE_METRICS)}

        self.assertFalse(checks["hold WHS"].passed)
        self.assertFalse(checks["hold THS"].passed)
        self.assertIn("unverified", checks["hold WHS"].detail)
        self.assertIn("unverified", checks["hold THS"].detail)

    def test_finite_zero_hold_metrics_can_pass(self):
        metrics = BASE_METRICS | {"whs": "0.0", "ths": "0.0"}
        checks = {check.name: check for check in check_metrics(metrics)}

        self.assertTrue(checks["hold WHS"].passed)
        self.assertTrue(checks["hold THS"].passed)

    def test_negative_setup_slack_is_a_real_failure(self):
        metrics = BASE_METRICS | {"wns": "-0.1", "tns": "-0.3", "whs": "0", "ths": "0"}
        checks = {check.name: check for check in check_metrics(metrics)}

        self.assertFalse(checks["setup WNS"].passed)
        self.assertFalse(checks["setup TNS"].passed)

    def test_non_finite_metrics_are_rejected(self):
        for value in ("nan", "inf", "-inf", "1e999"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "must be finite"):
                    metric_number({"wns": value}, "wns")


if __name__ == "__main__":
    unittest.main()
