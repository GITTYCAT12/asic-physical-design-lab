"""Tests for malformed and valid experiment-status manifests."""

import tempfile
import unittest
from pathlib import Path

from scripts import validate_repo


class ValidateRepoManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_root = validate_repo.ROOT
        validate_repo.ROOT = Path(self.temp_dir.name)
        (validate_repo.ROOT / "results").mkdir()

    def tearDown(self):
        validate_repo.ROOT = self.original_root
        self.temp_dir.cleanup()

    def write_manifest(self, content):
        path = validate_repo.ROOT / "results/experiment_status.csv"
        path.write_text(content, encoding="utf-8")

    def test_rejects_record_with_missing_trailing_values(self):
        self.write_manifest(
            "experiment,status,artifact,notes\n"
            "baseline,captured\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("line 2", errors[0])
        self.assertIn("missing value(s)", errors[0])

    def test_rejects_record_with_extra_csv_fields(self):
        self.write_manifest(
            "experiment,status,artifact,notes\n"
            "baseline,captured,baseline.csv,reference,unexpected\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("line 2", errors[0])
        self.assertIn("extra CSV field", errors[0])

    def test_rejects_missing_required_header(self):
        self.write_manifest(
            "experiment,status,artifact\n"
            "baseline,captured,baseline.csv\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("missing columns", errors[0])
        self.assertIn("notes", errors[0])

    def test_rejects_duplicate_header(self):
        self.write_manifest(
            "experiment,status,artifact,notes,notes\n"
            "baseline,captured,baseline.csv,reference,duplicate\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate columns", errors[0])

    def test_rejects_artifact_path_traversal(self):
        (validate_repo.ROOT / "README.md").write_text("outside results", encoding="utf-8")
        self.write_manifest(
            "experiment,status,artifact,notes\n"
            "baseline,captured,../README.md,reference\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("must stay within results", errors[0])

    def test_rejects_absolute_artifact_path(self):
        outside = validate_repo.ROOT / "outside.csv"
        outside.write_text("metric,value\nwns,-0.1\n", encoding="utf-8")
        self.write_manifest(
            "experiment,status,artifact,notes\n"
            f"baseline,captured,{outside},reference\n"
        )

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(len(errors), 1)
        self.assertIn("must stay within results", errors[0])

    def test_accepts_a_well_formed_captured_record(self):
        self.write_manifest(
            "experiment,status,artifact,notes\n"
            "baseline,captured,baseline.csv,reference run\n"
        )
        artifact = validate_repo.ROOT / "results/baseline.csv"
        artifact.write_text("metric,value\nwns,-0.12\n", encoding="utf-8")

        errors = validate_repo.validate_status_manifest()

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
