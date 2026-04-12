from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = ROOT / "scripts" / "bootstrap_init.py"
ADOPT_SAFE_WRITE_SCRIPT = ROOT / "scripts" / "adopt_safe_write.py"


class AdoptSafeWriteTest(unittest.TestCase):
    def bootstrap_project(self, target: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(BOOTSTRAP_SCRIPT), str(target), "--language", "python"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_adopt_safe_write(self, target: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ADOPT_SAFE_WRITE_SCRIPT), str(target), "--language", "python", *extra_args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_safe_write_creates_missing_files_only_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "docs/standard/testing_profile.md").unlink()

            result = self.run_adopt_safe_write(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- created files: 1", result.stdout)
            self.assertIn("- forced overwrites: 0", result.stdout)
            self.assertTrue((target / "docs/standard/testing_profile.md").exists())

    def test_safe_write_does_not_overwrite_differing_file_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8").replace(
                "vendor/harness-kit/docs/harness_guide.md",
                "third_party/harness-kit/docs/harness_guide.md",
                1,
            )
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_adopt_safe_write(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- forced overwrites: 0", result.stdout)
            self.assertIn("- remaining differing files: 1", result.stdout)
            self.assertIn("third_party/harness-kit/docs/harness_guide.md", guide_path.read_text(encoding="utf-8"))

    def test_safe_write_force_overwrites_selected_differing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            guide_path = target / "docs/project_entrypoint.md"
            guide_path.write_text("# Project Harness Entry Point\n\nlocalized\n", encoding="utf-8")

            result = self.run_adopt_safe_write(target, "--force-overwrite", "docs/project_entrypoint.md")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- forced overwrites: 1", result.stdout)
            self.assertIn("- remaining differing files: 0", result.stdout)
            self.assertIn("vendor/harness-kit/docs/harness_guide.md", guide_path.read_text(encoding="utf-8"))

    def test_safe_write_rejects_force_overwrite_for_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "docs/standard/testing_profile.md").unlink()

            result = self.run_adopt_safe_write(target, "--force-overwrite", "docs/standard/testing_profile.md")

            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid force-overwrite target", result.stderr)

    def test_safe_write_rejects_force_overwrite_for_unchanged_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_adopt_safe_write(target, "--force-overwrite", "docs/standard/testing_profile.md")

            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid force-overwrite target", result.stderr)

    def test_safe_write_rejects_force_overwrite_for_directory_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            conflict_path = target / "docs/standard/quality_gate_profile.md"
            conflict_path.unlink()
            conflict_path.mkdir()

            result = self.run_adopt_safe_write(target, "--force-overwrite", "docs/standard/quality_gate_profile.md")

            self.assertEqual(result.returncode, 1)
            self.assertIn("force-overwrite blocked by target path shape conflict", result.stderr)

    def test_safe_write_rejects_force_overwrite_when_target_root_is_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "not-a-project"
            target.write_text("not a directory\n", encoding="utf-8")

            result = self.run_adopt_safe_write(target, "--force-overwrite", "docs/project_entrypoint.md")

            self.assertEqual(result.returncode, 1)
            self.assertIn("force-overwrite blocked by target path shape conflict", result.stderr)

    def test_safe_write_can_refresh_unchanged_targets_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_adopt_safe_write(target, "--update-unchanged")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("- refreshed unchanged targets: 10", result.stdout)
            self.assertIn("- remaining unchanged targets: 10", result.stdout)


if __name__ == "__main__":
    unittest.main()
