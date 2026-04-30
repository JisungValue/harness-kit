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

    def run_runtime_script(
        self,
        project_root: Path,
        script_name: str,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(project_root / "scripts" / script_name), *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def init_repo(self, project_root: Path) -> None:
        result = subprocess.run(
            ["git", "init", "-q", str(project_root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_phase_status(self, workspace: Path) -> None:
        workspace.mkdir(parents=True, exist_ok=True)
        (workspace / "phase_status.md").write_text(
            "\n".join(
                [
                    "# Phase Status",
                    "",
                    "## Current State",
                    "",
                    "- Task Status: `active`",
                    "- Current Phase: `Phase 1`",
                    "- Current Gate: `requirements definition`",
                    "- Last Approved Phase: `없음`",
                    "",
                    "## Allowed Write Set",
                    "",
                    "- `$TASK/issue.md`",
                    "- `$TASK/requirements.md`",
                    "- `$TASK/phase_status.md`",
                    "",
                    "## Locked Paths",
                    "",
                    "- `$TASK/plan.md`",
                    "- `docs/project/decisions/*`",
                    "",
                    "## Stale Artifacts",
                    "",
                    "- 없음",
                    "",
                    "## Next Action",
                    "",
                    "- `requirements.md`를 보완한다.",
                    "",
                    "## Cleanup",
                    "",
                    "- Task 종료 전 유지: `yes`",
                    "- Task 종료 후 정리: `Phase 5` close-out 완료 뒤 삭제 가능",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def test_installs_default_vendored_bundle_and_bootstraps_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"

            result = self.run_cli(project_root, "--language", "java")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Generated canonical downstream bundle", result.stdout)
            self.assertIn("Install-time bundle inputs removed from final runtime surface", result.stdout)
            self.assertIn("Install flow completed", result.stdout)

            self.assertTrue((project_root / "AGENTS.md").exists())
            self.assertTrue((project_root / "docs/entrypoint.md").exists())
            self.assertTrue((project_root / "docs/process/harness_guide.md").exists())
            self.assertTrue((project_root / "docs/process/downstream_harness_flow.md").exists())
            self.assertTrue((project_root / "docs/process/common/process_policy.md").exists())
            self.assertTrue(
                (project_root / "docs/process/phases/phase_1_requirement_and_planning/implementation.md").exists()
            )
            self.assertTrue((project_root / "docs/process/common/coding_guidelines_policy.md").exists())
            self.assertFalse((project_root / "docs/process/standard").exists())
            self.assertTrue((project_root / "docs/process/templates/task/issue.md").exists())
            self.assertTrue((project_root / "docs/process/examples/sample-task/issue.md").exists())
            self.assertTrue((project_root / "scripts/validate_overlay_decisions.py").exists())
            self.assertTrue((project_root / "scripts/validate_overlay_consistency.py").exists())
            self.assertTrue((project_root / "scripts/validate_phase_gate.py").exists())
            self.assertFalse((project_root / "vendor/harness-kit").exists())
            self.assertFalse((project_root / "bootstrap").exists())
            self.assertFalse((project_root / "bundle_manifest.json").exists())
            self.assertFalse((project_root / "docs/project_overlay").exists())
            self.assertFalse((project_root / "docs/quickstart.md").exists())
            self.assertFalse((project_root / "scripts/bootstrap_init.py").exists())
            self.assertFalse((project_root / "scripts/adopt_common.py").exists())
            self.assertFalse((project_root / "scripts/adopt_dry_run.py").exists())
            self.assertFalse((project_root / "scripts/adopt_safe_write.py").exists())
            self.assertFalse((project_root / "scripts/check_first_success_docs.py").exists())
            self.assertFalse((project_root / "docs/harness/common/process_policy.md").exists())
            self.assertFalse((project_root / "docs/templates/task/issue.md").exists())
            self.assertIn(
                "docs/process/harness_guide.md",
                (project_root / "docs/entrypoint.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "install-time-only:java_coding_conventions_template.md",
                (project_root / "docs/project/standards/coding_conventions_project.md").read_text(encoding="utf-8"),
            )

            decisions = self.run_runtime_script(
                project_root,
                "validate_overlay_decisions.py",
                ".",
                "--readiness",
                "first-success",
            )
            self.assertEqual(decisions.returncode, 0, decisions.stderr)

            consistency = self.run_runtime_script(
                project_root,
                "validate_overlay_consistency.py",
                ".",
            )
            self.assertEqual(consistency.returncode, 0, consistency.stderr)

            self.init_repo(project_root)
            task_workspace = project_root / "docs/task/greenfield-smoke"
            self.write_phase_status(task_workspace)
            phase_gate = self.run_runtime_script(
                project_root,
                "validate_phase_gate.py",
                "docs/task/greenfield-smoke",
                "--paths",
                "docs/task/greenfield-smoke/issue.md",
                "docs/task/greenfield-smoke/phase_status.md",
            )
            self.assertEqual(phase_gate.returncode, 0, phase_gate.stderr)
            self.assertIn("phase gate validation passed", phase_gate.stdout)

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

            self.assertFalse((project_root / "third_party/harness-kit").exists())
            self.assertTrue((project_root / "scripts/validate_phase_gate.py").exists())
            self.assertIn(
                "docs/process/harness_guide.md",
                (project_root / "docs/entrypoint.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "install-time-only:python_coding_conventions_template.md",
                (project_root / "docs/project/standards/coding_conventions_project.md").read_text(encoding="utf-8"),
            )

            consistency = self.run_runtime_script(
                project_root,
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
            self.assertFalse((project_root / "vendor/harness-kit").exists())
            self.assertTrue((project_root / "scripts/validate_overlay_consistency.py").exists())

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
            self.assertFalse((project_root / "vendor/harness-kit").exists())
            self.assertTrue((project_root / "docs/process/common/process_policy.md").exists())

    def test_existing_legacy_vendor_requires_force_vendor_for_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"
            legacy_policy = project_root / "vendor/harness-kit/docs/harness/common/process_policy.md"
            legacy_policy.parent.mkdir(parents=True, exist_ok=True)
            legacy_policy.write_text("legacy policy\n", encoding="utf-8")

            result = self.run_cli(project_root, "--language", "python")

            self.assertEqual(result.returncode, 1)
            self.assertIn("legacy vendor path already contains files", result.stderr)
            self.assertTrue(legacy_policy.exists())

    def test_force_vendor_refuses_unknown_legacy_vendor_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"
            custom_file = project_root / "vendor/harness-kit/custom.txt"
            custom_file.parent.mkdir(parents=True, exist_ok=True)
            custom_file.write_text("keep me\n", encoding="utf-8")

            result = self.run_cli(project_root, "--language", "python", "--force-vendor")

            self.assertEqual(result.returncode, 1)
            self.assertIn("contains non-bundle paths", result.stderr)
            self.assertTrue(custom_file.exists())

    def test_existing_install_time_residue_fails_before_final_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "recipeForBaby"
            residue = project_root / "docs/project_overlay/README.md"
            residue.parent.mkdir(parents=True, exist_ok=True)
            residue.write_text("stale bundle guide\n", encoding="utf-8")

            result = self.run_cli(project_root, "--language", "python")

            self.assertEqual(result.returncode, 1)
            self.assertIn("install-time only assets remain", result.stderr)
            self.assertIn("docs/project_overlay", result.stderr)
            self.assertFalse((project_root / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
