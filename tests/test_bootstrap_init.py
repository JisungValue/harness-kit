from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bootstrap" / "scripts" / "bootstrap_init.py"
FINAL_RUNTIME_EXAMPLES = (
    "docs/process/examples/project-decisions/DEC-001-authorization-validation-location.md",
    "docs/process/examples/sample-lightweight-task/issue.md",
    "docs/process/examples/sample-lightweight-task/plan.md",
    "docs/process/examples/sample-lightweight-task/validation_report.md",
)
EXCLUDED_FINAL_RUNTIME_EXAMPLES = (
    "docs/process/examples/bootstrap-first-success/validation_report.md",
    "docs/process/examples/bootstrap-first-success/overlay_completion_validation_report.md",
    "docs/process/examples/sample-task/issue.md",
    "docs/process/examples/sample-task/requirements.md",
    "docs/process/examples/sample-task/plan.md",
    "docs/process/examples/sample-task/phase_status.md",
    "docs/process/examples/sample-task/implementation_notes.md",
    "docs/process/examples/sample-task/validation_report.md",
    "docs/process/examples/sample-task/coding_conventions_project_example.md",
    "docs/process/examples/sample-lightweight-task/requirements.md",
    "docs/process/examples/sample-lightweight-task/phase_status.md",
    "docs/process/examples/sample-lightweight-task/implementation_notes.md",
)


class BootstrapInitCliTest(unittest.TestCase):
    def run_cli(self, target: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(target), "--language", "python", *extra_args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_creates_required_project_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / "GEMINI.md").exists())
            self.assertTrue((target / "docs/entrypoint.md").exists())
            self.assertTrue((target / "docs/project/decisions/README.md").exists())
            self.assertTrue((target / "docs/project/standards/architecture.md").exists())
            self.assertTrue((target / "docs/project/standards/implementation_order.md").exists())
            self.assertTrue((target / "docs/project/standards/coding_conventions_project.md").exists())
            self.assertTrue((target / "docs/project/standards/quality_gate_profile.md").exists())
            self.assertTrue((target / "docs/project/standards/testing_profile.md").exists())
            self.assertTrue((target / "docs/project/standards/commit_rule.md").exists())
            self.assertTrue((target / "docs/process/harness_guide.md").exists())
            self.assertTrue((target / "docs/process/downstream_harness_flow.md").exists())
            self.assertTrue((target / "docs/process/common/process_policy.md").exists())
            self.assertTrue((target / "docs/process/phases/phase_1_requirement_and_planning/implementation.md").exists())
            self.assertTrue((target / "docs/process/common/coding_guidelines_policy.md").exists())
            self.assertFalse((target / "docs/process/standard").exists())
            self.assertTrue((target / "docs/process/templates/task/issue.md").exists())
            for relative_path in FINAL_RUNTIME_EXAMPLES:
                self.assertTrue((target / relative_path).exists(), relative_path)
            for relative_path in EXCLUDED_FINAL_RUNTIME_EXAMPLES:
                self.assertFalse((target / relative_path).exists(), relative_path)

            content = (target / "docs/project/standards/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("- 현재 프로젝트의 활성 언어/런타임: `python`", content)
            self.assertIn(
                "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                content,
            )

            agent_entrypoint = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Agent Runtime Entry Point", agent_entrypoint)
            self.assertIn("docs/entrypoint.md", agent_entrypoint)
            self.assertIn("순서대로 모두 읽고 적용", agent_entrypoint)

            project_entrypoint = (target / "docs/entrypoint.md").read_text(encoding="utf-8")
            self.assertIn("# Project Harness Entry Point", project_entrypoint)
            self.assertIn("공통 규칙", project_entrypoint)
            self.assertIn("프로젝트 전용 규칙", project_entrypoint)
            self.assertIn("프로젝트 결정 문서", project_entrypoint)
            self.assertIn("docs/process/harness_guide.md", project_entrypoint)
            self.assertIn("docs/process/downstream_harness_flow.md", project_entrypoint)
            self.assertIn("docs/project/decisions/README.md", project_entrypoint)
            self.assertIn("둘 중 하나만 읽고 멈추지 않는다", project_entrypoint)

            decisions_index = (target / "docs/project/decisions/README.md").read_text(encoding="utf-8")
            self.assertIn("# Project Decision Index", decisions_index)
            self.assertIn("DEC-###-slug.md", decisions_index)

            process_guide = (target / "docs/process/harness_guide.md").read_text(encoding="utf-8")
            self.assertIn("docs/process/common/process_policy.md", process_guide)
            self.assertIn("docs/process/common/coding_guidelines_policy.md", process_guide)
            self.assertNotIn("docs/process/standard", process_guide)
            self.assertNotIn("docs/harness/common/process_policy.md", process_guide)

            claude_entrypoint = (target / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("# Claude Adapter Entry Point", claude_entrypoint)
            self.assertIn("AGENTS.md", claude_entrypoint)
            self.assertIn("연결된 문서 체인도 끝까지 따라간다", claude_entrypoint)

            gemini_entrypoint = (target / "GEMINI.md").read_text(encoding="utf-8")
            self.assertIn("# Gemini Adapter Entry Point", gemini_entrypoint)
            self.assertIn("AGENTS.md", gemini_entrypoint)
            self.assertIn("연결된 문서 체인도 끝까지 따라간다", gemini_entrypoint)

    def test_fails_fast_when_generated_file_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            target.mkdir(parents=True)
            docs_dir = target / "docs"
            docs_dir.mkdir()
            (docs_dir / "entrypoint.md").write_text("existing\n", encoding="utf-8")

            result = self.run_cli(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("bootstrap init failed", result.stderr)
            self.assertIn("docs/entrypoint.md", result.stderr)

    def test_force_overwrites_existing_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            first_result = self.run_cli(target)
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            guide_path = target / "docs/entrypoint.md"
            guide_path.write_text("changed\n", encoding="utf-8")

            second_result = self.run_cli(target, "--force")

            self.assertEqual(second_result.returncode, 0, second_result.stderr)
            self.assertIn("Overwrote harness bootstrap docs", second_result.stdout)
            self.assertNotEqual(guide_path.read_text(encoding="utf-8"), "changed\n")

    def test_fails_when_parent_path_is_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            docs_path = target / "docs"
            target.mkdir(parents=True)
            docs_path.write_text("not a directory\n", encoding="utf-8")

            result = self.run_cli(target, "--force")

            self.assertEqual(result.returncode, 1)
            self.assertIn("not writable as a bootstrap tree", result.stderr)
            self.assertIn(str(docs_path), result.stderr)

    def test_localizes_generated_references_for_non_default_vendor_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target, "--vendor-path", "third_party/harness-kit")

            self.assertEqual(result.returncode, 0, result.stderr)
            project_entrypoint = (target / "docs/entrypoint.md").read_text(encoding="utf-8")
            coding_conventions = (target / "docs/project/standards/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )

            self.assertIn("docs/process/harness_guide.md", project_entrypoint)
            self.assertIn("docs/process/downstream_harness_flow.md", project_entrypoint)
            self.assertNotIn("third_party/harness-kit/docs/harness_guide.md", project_entrypoint)
            self.assertNotIn("vendor/harness-kit/docs/harness_guide.md", project_entrypoint)
            self.assertIn(
                "third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                coding_conventions,
            )

    def test_can_record_install_time_only_language_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target, "--language-reference-mode", "install-time-note")

            self.assertEqual(result.returncode, 0, result.stderr)
            coding_conventions = (target / "docs/project/standards/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )

            self.assertIn(
                "install-time-only:python_coding_conventions_template.md",
                coding_conventions,
            )
            self.assertNotIn(
                "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                coding_conventions,
            )

    def test_rejects_absolute_vendor_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target, "--vendor-path", "/opt/harness-kit")

            self.assertEqual(result.returncode, 1)
            self.assertIn("vendor path must be project-root relative", result.stderr)

    def test_rejects_windows_absolute_vendor_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target, "--vendor-path", r"C:\harness-kit")

            self.assertEqual(result.returncode, 1)
            self.assertIn("vendor path must be project-root relative", result.stderr)

    def test_rejects_windows_drive_relative_vendor_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            result = self.run_cli(target, "--vendor-path", r"C:harness-kit")

            self.assertEqual(result.returncode, 1)
            self.assertIn("vendor path must be project-root relative", result.stderr)


if __name__ == "__main__":
    unittest.main()
