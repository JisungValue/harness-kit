from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "maintainer" / "scripts" / "install_downstream_bundle.py"


class InstallDownstreamBundleTest(unittest.TestCase):
    def run_cli(self, target: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(target), *extra_args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_vendored_script(
        self,
        project_root: Path,
        vendor_relative_path: Path,
        script_name: str,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(project_root / vendor_relative_path / "scripts" / script_name), *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_installs_default_vendored_bundle_and_bootstraps_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"

            result = self.run_cli(project_root, "--language", "java")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Generated canonical downstream bundle", result.stdout)
            self.assertIn("Vendored downstream bundle into", result.stdout)
            self.assertIn("Install flow completed", result.stdout)

            vendor_root = project_root / "vendor/harness-kit"
            self.assertTrue((vendor_root / "bundle_manifest.json").exists())
            self.assertTrue((vendor_root / "downstream/scripts/validate_phase_gate.py").exists())
            self.assertTrue((project_root / "AGENTS.md").exists())
            self.assertTrue((project_root / "docs/entrypoint.md").exists())
            self.assertTrue((project_root / "docs/process/harness_guide.md").exists())
            self.assertTrue((project_root / "docs/process/downstream_harness_flow.md").exists())
            self.assertTrue((project_root / "docs/process/common/process_policy.md").exists())
            self.assertTrue(
                (project_root / "docs/process/phases/phase_1_requirement_and_planning/implementation.md").exists()
            )
            self.assertTrue((project_root / "docs/process/standard/coding_guidelines_core.md").exists())
            self.assertTrue((project_root / "docs/process/templates/task/issue.md").exists())
            self.assertTrue((project_root / "docs/process/examples/sample-task/issue.md").exists())
            self.assertFalse((project_root / "docs/harness/common/process_policy.md").exists())
            self.assertFalse((project_root / "docs/templates/task/issue.md").exists())
            self.assertIn(
                "docs/process/harness_guide.md",
                (project_root / "docs/entrypoint.md").read_text(encoding="utf-8"),
            )

            first_success = self.run_vendored_script(
                project_root,
                Path("vendor/harness-kit"),
                "check_first_success_docs.py",
                ".",
            )
            self.assertEqual(first_success.returncode, 0, first_success.stderr)
            self.assertIn("first success docs are present", first_success.stdout)

            consistency = self.run_vendored_script(
                project_root,
                Path("vendor/harness-kit"),
                "validate_overlay_consistency.py",
                ".",
            )
            self.assertEqual(consistency.returncode, 0, consistency.stderr)

    def test_installs_localized_vendor_path_and_bootstraps_with_localized_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"

            result = self.run_cli(
                project_root,
                "--language",
                "python",
                "--vendor-path",
                "third_party/harness-kit",
            )

            self.assertEqual(result.returncode, 0, result.stderr)

            vendor_root = project_root / "third_party/harness-kit"
            self.assertTrue((vendor_root / "bundle_manifest.json").exists())
            self.assertTrue((vendor_root / "downstream/scripts/validate_phase_gate.py").exists())
            self.assertIn(
                "docs/process/harness_guide.md",
                (project_root / "docs/entrypoint.md").read_text(encoding="utf-8"),
            )

            consistency = self.run_vendored_script(
                project_root,
                Path("third_party/harness-kit"),
                "validate_overlay_consistency.py",
                ".",
            )
            self.assertEqual(consistency.returncode, 0, consistency.stderr)

    def test_rejects_vendor_path_inside_docs_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"

            result = self.run_cli(
                project_root,
                "--language",
                "java",
                "--vendor-path",
                "docs/harness-kit",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("vendor path must stay outside downstream project docs/", result.stderr)
            self.assertFalse((project_root / "docs/harness-kit").exists())

    def test_requires_force_bootstrap_when_generated_docs_already_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"
            existing_path = project_root / "docs/entrypoint.md"
            existing_path.parent.mkdir(parents=True, exist_ok=True)
            existing_path.write_text("stale\n", encoding="utf-8")

            result = self.run_cli(project_root, "--language", "java")

            self.assertEqual(result.returncode, 1)
            self.assertIn("target files already exist", result.stderr)
            self.assertIn("--force-bootstrap", result.stderr)
            self.assertFalse((project_root / "vendor/harness-kit").exists())

    def test_force_vendor_and_force_bootstrap_allow_reinstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"

            first_result = self.run_cli(project_root, "--language", "java")
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            second_result = self.run_cli(
                project_root,
                "--language",
                "java",
                "--force-vendor",
                "--force-bootstrap",
            )

            self.assertEqual(second_result.returncode, 0, second_result.stderr)
            self.assertIn("Install flow completed", second_result.stdout)
            self.assertTrue((project_root / "vendor/harness-kit/bundle_manifest.json").exists())

    def test_force_vendor_replaces_legacy_process_doc_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"
            legacy_policy = project_root / "vendor/harness-kit/docs/harness/common/process_policy.md"
            legacy_template = project_root / "vendor/harness-kit/docs/templates/task/issue.md"
            legacy_policy.parent.mkdir(parents=True, exist_ok=True)
            legacy_template.parent.mkdir(parents=True, exist_ok=True)
            legacy_policy.write_text("legacy policy\n", encoding="utf-8")
            legacy_template.write_text("legacy template\n", encoding="utf-8")

            result = self.run_cli(project_root, "--language", "python", "--force-vendor")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(legacy_policy.exists())
            self.assertFalse(legacy_template.exists())
            self.assertTrue((project_root / "vendor/harness-kit/docs/process/common/process_policy.md").exists())
            self.assertTrue((project_root / "docs/process/common/process_policy.md").exists())


if __name__ == "__main__":
    unittest.main()
