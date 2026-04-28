from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_SCRIPT = ROOT / "downstream" / "scripts" / "validate_phase_gate.py"


class ValidatePhaseGateTest(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        result = subprocess.run(
            ["git", "init", "-q", str(root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_phase_status(
        self,
        workspace: Path,
        *,
        stale_line: str = "- 없음",
        allowed_write_set: list[str] | None = None,
        locked_paths: list[str] | None = None,
    ) -> None:
        workspace.mkdir(parents=True, exist_ok=True)
        allowed_entries = allowed_write_set or [
            "$TASK/issue.md",
            "$TASK/requirements.md",
            "$TASK/implementation_notes.md",
            "$TASK/phase_status.md",
        ]
        locked_entries = locked_paths or [
            "$TASK/plan.md",
            "$TASK/validation_report.md",
            "docs/decisions/*",
        ]
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
                    *[f"- `{entry}`" for entry in allowed_entries],
                    "",
                    "## Locked Paths",
                    "",
                    *[f"- `{entry}`" for entry in locked_entries],
                    "",
                    "## Stale Artifacts",
                    "",
                    stale_line,
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

    def run_validator(self, workspace: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR_SCRIPT), str(workspace), *extra_args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_passes_when_candidate_paths_match_allowed_write_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)

            result = self.run_validator(
                workspace,
                "--paths",
                "docs/task/1_sample_task/requirements.md",
                "docs/task/1_sample_task/phase_status.md",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("phase gate validation passed", result.stdout)

    def test_fails_on_locked_path_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)

            result = self.run_validator(
                workspace,
                "--paths",
                "docs/task/1_sample_task/plan.md",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("locked path violation", result.stderr)

    def test_fails_on_outside_allowed_write_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)

            result = self.run_validator(
                workspace,
                "--paths",
                "src/app.py",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("outside allowed write set", result.stderr)

    def test_fails_when_stale_artifact_is_not_locked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace, stale_line="- `$TASK/requirements.md`")

            result = self.run_validator(
                workspace,
                "--paths",
                "docs/task/1_sample_task/phase_status.md",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("stale artifact must also be locked", result.stderr)

    def test_uses_git_status_when_paths_are_not_supplied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)
            (workspace / "requirements.md").write_text("# Requirements\n", encoding="utf-8")

            result = self.run_validator(workspace)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("docs/task/1_sample_task/requirements.md", result.stdout)

    def test_default_git_scope_ignores_unrelated_dirty_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)
            (workspace / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            src_dir = repo_root / "src"
            src_dir.mkdir()
            (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

            result = self.run_validator(workspace)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("docs/task/1_sample_task/requirements.md", result.stdout)
            self.assertNotIn("src/app.py", result.stdout)

    def test_default_git_scope_validates_task_relevant_paths_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(
                workspace,
                allowed_write_set=[
                    "$TASK/issue.md",
                    "$TASK/requirements.md",
                    "$TASK/implementation_notes.md",
                    "$TASK/phase_status.md",
                    "src/app.py",
                ],
            )
            src_dir = repo_root / "src"
            src_dir.mkdir()
            (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")
            tools_dir = repo_root / "tools"
            tools_dir.mkdir()
            (tools_dir / "dev.py").write_text("print('dev')\n", encoding="utf-8")

            result = self.run_validator(workspace)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("src/app.py", result.stdout)
            self.assertNotIn("tools/dev.py", result.stdout)

    def test_repo_git_scope_still_reports_unrelated_dirty_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            workspace = repo_root / "docs/task/1_sample_task"
            self.write_phase_status(workspace)
            (workspace / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            src_dir = repo_root / "src"
            src_dir.mkdir()
            (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

            result = self.run_validator(workspace, "--git-scope", "repo")

            self.assertEqual(result.returncode, 1)
            self.assertIn("outside allowed write set: src/app.py", result.stderr)


if __name__ == "__main__":
    unittest.main()
