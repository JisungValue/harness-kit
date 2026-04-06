from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = ROOT / "scripts" / "bootstrap_init.py"
TEMPLATE_MAPPINGS = {
    "docs/project_overlay/project_harness_guide_template.md": "docs/harness_guide.md",
    "docs/project_overlay/architecture_template.md": "docs/standard/architecture.md",
    "docs/project_overlay/implementation_order_template.md": "docs/standard/implementation_order.md",
    "docs/project_overlay/coding_conventions_project_template.md": "docs/standard/coding_conventions_project.md",
    "docs/project_overlay/quality_gate_profile_template.md": "docs/standard/quality_gate_profile.md",
    "docs/project_overlay/testing_profile_template.md": "docs/standard/testing_profile.md",
    "docs/project_overlay/commit_rule_template.md": "docs/standard/commit_rule.md",
}
EXPECTED_DOCS = tuple(TEMPLATE_MAPPINGS.values())
LANGUAGE = "python"
DEFAULT_HARNESS_GUIDE_REFERENCE = "vendor/harness-kit/docs/harness_guide.md"
DEFAULT_BOOTSTRAP_REFERENCE = (
    "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md"
)
FIRST_SUCCESS_COMMAND = (
    "from pathlib import Path; "
    "paths = ['docs/harness_guide.md', 'docs/standard/architecture.md', "
    "'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', "
    "'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', "
    "'docs/standard/commit_rule.md']; "
    "missing = [p for p in paths if not Path(p).exists()]; "
    "print('first success docs are present') if not missing else "
    "(_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
)


class BootstrapEndToEndTest(unittest.TestCase):
    def assert_expected_docs_exist(self, project_root: Path) -> None:
        missing = [path for path in EXPECTED_DOCS if not (project_root / path).exists()]
        self.assertEqual(missing, [], f"Missing docs: {missing}")

    def assert_first_success_signals(
        self,
        project_root: Path,
        harness_guide_reference: str,
        bootstrap_reference: str,
    ) -> None:
        harness_guide = (project_root / "docs/harness_guide.md").read_text(encoding="utf-8")
        coding_conventions = (
            project_root / "docs/standard/coding_conventions_project.md"
        ).read_text(encoding="utf-8")

        self.assertIn(harness_guide_reference, harness_guide)
        for project_doc_path in (
            "docs/standard/architecture.md",
            "docs/standard/implementation_order.md",
            "docs/standard/coding_conventions_project.md",
            "docs/standard/quality_gate_profile.md",
            "docs/standard/testing_profile.md",
            "docs/standard/commit_rule.md",
        ):
            self.assertIn(project_doc_path, harness_guide)

        self.assertIn(f"- 현재 프로젝트의 활성 언어/런타임: `{LANGUAGE}`", coding_conventions)
        self.assertIn(bootstrap_reference, coding_conventions)
        self.assertIn(
            "- 현재 프로젝트에서 우선 적용하는 핵심 규칙 범주:",
            coding_conventions,
        )

        quality_gate_profile = (
            project_root / "docs/standard/quality_gate_profile.md"
        ).read_text(encoding="utf-8")
        commit_rule = (project_root / "docs/standard/commit_rule.md").read_text(
            encoding="utf-8"
        )

        for relative_path in (
            "docs/standard/quality_gate_profile.md",
            "docs/standard/testing_profile.md",
            "docs/standard/commit_rule.md",
        ):
            self.assertGreater(
                len((project_root / relative_path).read_text(encoding="utf-8").strip()),
                0,
                f"Expected non-empty file: {relative_path}",
            )

        self.assertIn("[프로젝트 결정 필요]", quality_gate_profile)
        self.assertIn("[팀 결정 필요]", commit_rule)

    def localize_manual_path(
        self,
        project_root: Path,
        harness_guide_reference: str,
        bootstrap_reference: str,
    ) -> None:
        harness_guide_path = project_root / "docs/harness_guide.md"
        harness_guide_content = harness_guide_path.read_text(encoding="utf-8")
        harness_guide_content = harness_guide_content.replace(
            DEFAULT_HARNESS_GUIDE_REFERENCE,
            harness_guide_reference,
            1,
        )
        harness_guide_path.write_text(harness_guide_content, encoding="utf-8")

        coding_conventions_path = project_root / "docs/standard/coding_conventions_project.md"
        content = coding_conventions_path.read_text(encoding="utf-8")
        content = content.replace(
            "- 언어별 convention 초안이 필요하면 `bootstrap/language_conventions/`에서 해당 언어 템플릿을 골라 이 문서에 병합한다.",
            f"- 언어별 convention 초안이 필요하면 `{bootstrap_reference.rsplit('/', 1)[0]}/`에서 해당 언어 템플릿을 골라 이 문서에 병합한다.",
            1,
        )
        content = content.replace(
            "- bootstrap 템플릿을 복사했다면 어떤 언어 템플릿을 기준으로 병합했는지 적는다.",
            "- bootstrap 템플릿을 복사했다면 어떤 언어 템플릿을 기준으로 병합했는지 적는다.\n"
            f"- 수동 경로 예시 기준 문서는 `{bootstrap_reference}`다.",
            1,
        )
        content = content.replace(
            "- 현재 프로젝트의 활성 언어/런타임: `[프로젝트 결정 필요]`",
            f"- 현재 프로젝트의 활성 언어/런타임: `{LANGUAGE}`",
            1,
        )
        content = content.replace(
            "- bootstrap 출처 또는 기준 언어 문서: `[프로젝트 결정 필요]`",
            f"- bootstrap 출처 또는 기준 언어 문서: `{bootstrap_reference}`",
            1,
        )

        language_template_path = ROOT / "bootstrap/language_conventions/python_coding_conventions_template.md"
        language_template_excerpt = "\n".join(
            language_template_path.read_text(encoding="utf-8").splitlines()[:20]
        )
        content += (
            "\n\n## 수동 병합 예시\n\n"
            f"- 아래 내용은 `{bootstrap_reference}`에서 가져온 발췌본이다.\n\n"
            f"```md\n{language_template_excerpt}\n```\n"
        )
        coding_conventions_path.write_text(content, encoding="utf-8")

    def run_first_success_command(self, project_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-c", FIRST_SUCCESS_COMMAND],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_init_cli_matches_first_success_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "bootstrap-cli-project"

            init_result = subprocess.run(
                [sys.executable, str(BOOTSTRAP_SCRIPT), str(project_root), "--language", "python"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            self.assertIn("Created harness bootstrap docs in", init_result.stdout)
            self.assertIn(
                "docs/harness_guide.md <- docs/project_overlay/project_harness_guide_template.md",
                init_result.stdout,
            )
            self.assertIn(
                "docs/standard/coding_conventions_project.md <- docs/project_overlay/coding_conventions_project_template.md",
                init_result.stdout,
            )
            self.assert_expected_docs_exist(project_root)
            self.assert_first_success_signals(
                project_root,
                DEFAULT_HARNESS_GUIDE_REFERENCE,
                DEFAULT_BOOTSTRAP_REFERENCE,
            )

            verify_result = self.run_first_success_command(project_root)

            self.assertEqual(verify_result.returncode, 0, verify_result.stderr)
            self.assertIn("first success docs are present", verify_result.stdout)

    def test_manual_template_copy_reaches_same_minimum_doc_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "bootstrap-manual-project"
            harness_guide_reference = "third_party/harness-kit/docs/harness_guide.md"
            bootstrap_reference = (
                "third_party/harness-kit/bootstrap/language_conventions/"
                "python_coding_conventions_template.md"
            )
            project_root.mkdir(parents=True)

            for source_rel, destination_rel in TEMPLATE_MAPPINGS.items():
                destination = project_root / destination_rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / source_rel, destination)

            self.localize_manual_path(
                project_root,
                harness_guide_reference,
                bootstrap_reference,
            )

            self.assert_expected_docs_exist(project_root)
            self.assert_first_success_signals(
                project_root,
                harness_guide_reference,
                bootstrap_reference,
            )

            verify_result = self.run_first_success_command(project_root)

            self.assertEqual(verify_result.returncode, 0, verify_result.stderr)
            self.assertIn("first success docs are present", verify_result.stdout)


if __name__ == "__main__":
    unittest.main()
