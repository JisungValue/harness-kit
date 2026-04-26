from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = ROOT / "bootstrap" / "scripts" / "bootstrap_init.py"
ADOPT_SCRIPT = ROOT / "bootstrap" / "scripts" / "adopt_dry_run.py"


class AdoptDryRunTest(unittest.TestCase):
    def bootstrap_project(self, target: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(BOOTSTRAP_SCRIPT), str(target), "--language", "python"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_adopt_dry_run(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ADOPT_SCRIPT), str(target), "--language", "python"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fresh_bootstrap_reports_all_targets_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- missing files: 0", result.stdout)
            self.assertIn("- existing but unchanged targets: 11", result.stdout)
            self.assertIn("- differing files: 0", result.stdout)
            self.assertIn("- conflict candidates: 0", result.stdout)

    def test_missing_files_are_reported_safe_to_create(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "docs/standard/testing_profile.md").unlink()

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- missing files: 1", result.stdout)
            self.assertIn("Missing files (safe to create):", result.stdout)
            self.assertIn("docs/standard/testing_profile.md", result.stdout)

    def test_localized_existing_file_is_reported_as_differing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace(
                "vendor/harness-kit/docs/harness_guide.md",
                "third_party/harness-kit/docs/harness_guide.md",
                1,
            )
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- differing files: 1", result.stdout)
            self.assertIn("Differing files (manual review):", result.stdout)
            self.assertIn("docs/project_entrypoint.md", result.stdout)

    def test_unrelated_file_at_target_path_is_reported_as_conflict_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            commit_rule_path = target / "docs/standard/commit_rule.md"
            commit_rule_path.write_text("# Totally Different Doc\n", encoding="utf-8")

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- conflict candidates: 1", result.stdout)
            self.assertIn("Conflict candidates (manual decision required):", result.stdout)
            self.assertIn("primary heading differs", result.stdout)

    def test_directory_target_is_reported_as_conflict_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            conflict_path = target / "docs/standard/quality_gate_profile.md"
            conflict_path.unlink()
            conflict_path.mkdir()

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- conflict candidates: 1", result.stdout)
            self.assertIn("destination path is a directory", result.stdout)

    def test_parent_path_conflict_is_not_reported_safe_to_create(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            target.mkdir(parents=True)
            (target / "docs").write_text("not a directory\n", encoding="utf-8")

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- missing files: 3", result.stdout)
            self.assertIn("- conflict candidates: 8", result.stdout)
            self.assertIn("parent path is not a directory", result.stdout)

    def test_legacy_project_entrypoint_is_reported_as_migration_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            legacy_path = target / "docs/harness_guide.md"
            (target / "docs/project_entrypoint.md").replace(legacy_path)

            agents_path = target / "AGENTS.md"
            agents_text = agents_path.read_text(encoding="utf-8")
            agents_text = agents_text.replace("docs/project_entrypoint.md", "docs/harness_guide.md", 1)
            agents_path.write_text(agents_text, encoding="utf-8")

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- legacy entrypoint migration candidates: 1", result.stdout)
            self.assertIn("Legacy entrypoint migration candidates:", result.stdout)
            self.assertIn("docs/harness_guide.md -> docs/project_entrypoint.md", result.stdout)
            self.assertNotIn("Missing files (safe to create):\n- docs/project_entrypoint.md", result.stdout)

    def test_stale_legacy_entrypoint_leftover_is_reported_as_blocked_migration_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            legacy_path = target / "docs/harness_guide.md"
            legacy_path.write_text(
                (target / "docs/project_entrypoint.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = self.run_adopt_dry_run(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- legacy entrypoint migration candidates: 1", result.stdout)
            self.assertIn("retire the stale legacy file manually", result.stdout)


if __name__ == "__main__":
    unittest.main()
