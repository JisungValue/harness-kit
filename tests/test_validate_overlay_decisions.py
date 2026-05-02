from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = ROOT / "bootstrap" / "scripts" / "bootstrap_init.py"
VALIDATOR_SCRIPT = ROOT / "bootstrap" / "scripts" / "validate_overlay_decisions.py"


class ValidateOverlayDecisionsTest(unittest.TestCase):
    def bootstrap_project(self, target: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(BOOTSTRAP_SCRIPT), str(target), "--language", "python"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_validator(self, target: Path, readiness: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR_SCRIPT), str(target), "--readiness", readiness],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fresh_bootstrap_passes_first_success_with_allowed_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay decision validation passed", result.stdout)
            self.assertIn("Allowed unresolved markers", result.stdout)
            self.assertIn("docs/project/standards/quality_gate_profile.md", result.stdout)
            self.assertIn("docs/project/standards/commit_rule.md", result.stdout)

    def test_fresh_bootstrap_fails_phase2_due_to_unresolved_overlay_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_validator(target, "phase2")

            self.assertEqual(result.returncode, 1)
            self.assertIn("overlay decision validation failed", result.stderr)
            self.assertIn("docs/project/standards/coding_conventions_project.md", result.stderr)
            self.assertIn("docs/project/standards/quality_gate_profile.md", result.stderr)
            self.assertIn("Still allowed after the blocking items above are fixed", result.stderr)
            self.assertIn("docs/project/standards/commit_rule.md", result.stderr)

    def test_todo_marker_is_always_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            architecture_path = target / "docs/project/standards/architecture.md"
            architecture_path.write_text(
                architecture_path.read_text(encoding="utf-8") + "\nTODO: fill me\n",
                encoding="utf-8",
            )

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("TODO", result.stderr)
            self.assertIn("docs/project/standards/architecture.md", result.stderr)

    def test_todo_marker_on_ignored_placeholder_example_line_is_still_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            architecture_path = target / "docs/project/standards/architecture.md"
            architecture_text = architecture_path.read_text(encoding="utf-8")
            architecture_text = architecture_text.replace(
                "- `레이어/책임: [프로젝트 결정 필요]`",
                "- `레이어/책임: [프로젝트 결정 필요]` TODO",
                1,
            )
            architecture_path.write_text(architecture_text, encoding="utf-8")

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("TODO", result.stderr)
            self.assertIn("docs/project/standards/architecture.md", result.stderr)

    def test_missing_required_doc_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "docs/project/standards/testing_profile.md").unlink()

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("Missing required overlay docs", result.stderr)
            self.assertIn("docs/project/standards/testing_profile.md", result.stderr)

    def test_directory_path_shape_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            entrypoint_path = target / "docs/entrypoint.md"
            entrypoint_path.unlink()
            entrypoint_path.mkdir()

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("Required overlay docs with invalid path shapes", result.stderr)
            self.assertIn("docs/entrypoint.md", result.stderr)
            self.assertIn("expected a file but found a directory", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_non_file_path_shape_fails_without_traceback(self) -> None:
        if not hasattr(os, "mkfifo"):
            self.skipTest("mkfifo unavailable")

        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            entrypoint_path = target / "docs/entrypoint.md"
            entrypoint_path.unlink()
            os.mkfifo(entrypoint_path)

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("Required overlay docs with invalid path shapes", result.stderr)
            self.assertIn("docs/entrypoint.md", result.stderr)
            self.assertIn("expected a file but found a non-file path", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_phase2_passes_after_required_decisions_are_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/project/standards/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- 현재 프로젝트에서 우선 적용하는 핵심 규칙 범주: `[naming / modeling / error handling / concurrency / collections / testing / interop 등]`",
                "- 현재 프로젝트에서 우선 적용하는 핵심 규칙 범주: `naming / modeling / error handling`",
                1,
            )
            coding_text = coding_text.replace(
                "- 현재 프로젝트의 주요 금지 패턴: `[프로젝트 결정 필요]`",
                "- 현재 프로젝트의 주요 금지 패턴: `raw external error propagation`",
                1,
            )
            coding_text = coding_text.replace(
                "- 현재 Phase 2에서 미해결로 둘 수 없는 언어별 결정 항목: `[프로젝트 결정 필요]`",
                "- 현재 Phase 2에서 미해결로 둘 수 없는 언어별 결정 항목: `error handling style, async boundary`",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            quality_gate_path = target / "docs/project/standards/quality_gate_profile.md"
            quality_gate_text = quality_gate_path.read_text(encoding="utf-8")
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run ruff check .`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "formatter failure blocks commit", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run ruff check .`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "Phase 2 종료 전", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "linter failure blocks commit", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run mypy .`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "Phase 2 종료 전", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "type failure blocks commit", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run pytest`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "Phase 2 종료 전", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "test failure blocks commit", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run import-linter`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "CI 전용", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "architecture rule failure blocks merge", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "`poetry run pytest tests/perf`", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "CI 전용", 1)
            quality_gate_text = quality_gate_text.replace("[프로젝트 결정 필요]", "performance regression blocks release", 1)
            quality_gate_path.write_text(quality_gate_text, encoding="utf-8")

            result = self.run_validator(target, "phase2")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay decision validation passed", result.stdout)

    def test_first_success_requires_canonical_resolved_language_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/project/standards/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- 현재 프로젝트의 활성 언어/런타임: `python`",
                "- 활성 언어: `[프로젝트 결정 필요]`",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("required-field", result.stderr)
            self.assertIn("Resolve these required canonical fields first", result.stderr)
            self.assertIn("- 활성 언어: `[프로젝트 결정 필요]`", result.stderr)
            self.assertRegex(result.stderr, r"docs/project/standards/coding_conventions_project\.md:\d+")
            self.assertIn("next: Replace the canonical active runtime line with a resolved value.", result.stderr)

    def test_first_success_fails_if_unresolved_canonical_field_is_left_and_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/project/standards/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- 현재 프로젝트의 활성 언어/런타임: `python`",
                "- 현재 프로젝트의 활성 언어/런타임: `[프로젝트 결정 필요]`\n"
                "- 현재 프로젝트의 활성 언어/런타임: `python`",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("- 현재 프로젝트의 활성 언어/런타임: `[프로젝트 결정 필요]`", result.stderr)
            self.assertNotIn("docs/project/standards/coding_conventions_project.md:24 [프로젝트 결정 필요]", result.stderr)

    def test_same_line_todo_is_not_suppressed_by_required_field_dedup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/project/standards/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- 현재 프로젝트의 활성 언어/런타임: `python`",
                "- 현재 프로젝트의 활성 언어/런타임: `[프로젝트 결정 필요]` TODO",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("required-field", result.stderr)
            self.assertIn("TODO", result.stderr)
            self.assertIn("docs/project/standards/coding_conventions_project.md:24 TODO", result.stderr)

    def test_decisions_index_placeholder_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            decisions_path = target / "docs/project/decisions/README.md"
            decisions_text = decisions_path.read_text(encoding="utf-8")
            decisions_text = decisions_text.replace(
                "- 아직 active decision 없음. 새 decision을 추가하면 여기에 기록한다.",
                "- [프로젝트 결정 필요] current decisions 분류 기준을 확정한다.",
                1,
            )
            decisions_path.write_text(decisions_text, encoding="utf-8")

            result = self.run_validator(target, "first-success")

            self.assertEqual(result.returncode, 1)
            self.assertIn("docs/project/decisions/README.md", result.stderr)
            self.assertIn("[프로젝트 결정 필요]", result.stderr)


if __name__ == "__main__":
    unittest.main()
