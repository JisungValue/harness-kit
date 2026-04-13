from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bootstrap_init.py"


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
            self.assertTrue((target / "docs/project_entrypoint.md").exists())
            self.assertTrue((target / "docs/decisions/README.md").exists())
            self.assertTrue((target / "docs/standard/architecture.md").exists())
            self.assertTrue((target / "docs/standard/implementation_order.md").exists())
            self.assertTrue((target / "docs/standard/coding_conventions_project.md").exists())
            self.assertTrue((target / "docs/standard/quality_gate_profile.md").exists())
            self.assertTrue((target / "docs/standard/testing_profile.md").exists())
            self.assertTrue((target / "docs/standard/commit_rule.md").exists())

            content = (target / "docs/standard/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("- 현재 프로젝트의 활성 언어/런타임: `python`", content)
            self.assertIn(
                "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                content,
            )

            agent_entrypoint = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Agent Runtime Entry Point", agent_entrypoint)
            self.assertIn("docs/project_entrypoint.md", agent_entrypoint)
            self.assertIn("순서대로 모두 읽고 적용", agent_entrypoint)

            project_entrypoint = (target / "docs/project_entrypoint.md").read_text(encoding="utf-8")
            self.assertIn("# Project Harness Entry Point", project_entrypoint)
            self.assertIn("공통 규칙", project_entrypoint)
            self.assertIn("프로젝트 전용 규칙", project_entrypoint)
            self.assertIn("프로젝트 결정 문서", project_entrypoint)
            self.assertIn("docs/decisions/README.md", project_entrypoint)
            self.assertIn("둘 중 하나만 읽고 멈추지 않는다", project_entrypoint)

            decisions_index = (target / "docs/decisions/README.md").read_text(encoding="utf-8")
            self.assertIn("# Project Decision Index", decisions_index)
            self.assertIn("DEC-###-slug.md", decisions_index)

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
            (docs_dir / "project_entrypoint.md").write_text("existing\n", encoding="utf-8")

            result = self.run_cli(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("bootstrap init failed", result.stderr)
            self.assertIn("docs/project_entrypoint.md", result.stderr)

    def test_force_overwrites_existing_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"

            first_result = self.run_cli(target)
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            guide_path = target / "docs/project_entrypoint.md"
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
            project_entrypoint = (target / "docs/project_entrypoint.md").read_text(encoding="utf-8")
            coding_conventions = (target / "docs/standard/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )

            self.assertIn("third_party/harness-kit/docs/harness_guide.md", project_entrypoint)
            self.assertNotIn("vendor/harness-kit/docs/harness_guide.md", project_entrypoint)
            self.assertIn(
                "third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
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
