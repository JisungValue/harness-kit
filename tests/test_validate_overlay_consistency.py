from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = ROOT / "scripts" / "bootstrap_init.py"
CONSISTENCY_SCRIPT = ROOT / "scripts" / "validate_overlay_consistency.py"


class ValidateOverlayConsistencyTest(unittest.TestCase):
    def create_reference_files(
        self,
        target: Path,
        harness_guide_reference: str = "vendor/harness-kit/docs/harness_guide.md",
        bootstrap_reference: str = "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
    ) -> None:
        harness_guide_path = target / harness_guide_reference
        harness_guide_path.parent.mkdir(parents=True, exist_ok=True)
        harness_guide_path.write_text("# Harness Core Guide\n", encoding="utf-8")

        bootstrap_path = target / bootstrap_reference
        bootstrap_path.parent.mkdir(parents=True, exist_ok=True)
        bootstrap_path.write_text("# Python Coding Conventions\n", encoding="utf-8")

    def bootstrap_project(self, target: Path) -> None:
        self.bootstrap_project_with_vendor_path(target)

    def bootstrap_project_with_vendor_path(
        self,
        target: Path,
        vendor_path: str = "vendor/harness-kit",
    ) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(BOOTSTRAP_SCRIPT),
                str(target),
                "--language",
                "python",
                "--vendor-path",
                vendor_path,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.create_reference_files(
            target,
            harness_guide_reference=f"{vendor_path}/docs/harness_guide.md",
            bootstrap_reference=f"{vendor_path}/bootstrap/language_conventions/python_coding_conventions_template.md",
        )

    def run_checker(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CONSISTENCY_SCRIPT), str(target)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fresh_bootstrap_passes_consistency_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay consistency validation passed", result.stdout)

    def test_missing_project_doc_link_in_harness_guide_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace("- `docs/standard/testing_profile.md`\n", "", 1)
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("필수 standard 문서 참조가 누락", result.stderr)

    def test_missing_agents_entrypoint_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "AGENTS.md").unlink()

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("필수 runtime instruction entrypoint가 없습니다: AGENTS.md", result.stderr)

    def test_missing_decisions_index_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)
            (target / "docs/decisions/README.md").unlink()

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("필수 overlay 문서가 없습니다: docs/decisions/README.md", result.stderr)

    def test_gemini_adapter_without_agents_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            gemini_path = target / "GEMINI.md"
            gemini_text = gemini_path.read_text(encoding="utf-8")
            gemini_text = gemini_text.replace("- `AGENTS.md`\n", "- `docs/project_entrypoint.md`\n", 1)
            gemini_path.write_text(gemini_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("GEMINI.md: `AGENTS.md`를 공통 진입점으로 연결하지 않습니다.", result.stderr)

    def test_agents_without_traversal_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            agents_path = target / "AGENTS.md"
            agents_text = agents_path.read_text(encoding="utf-8")
            agents_text = agents_text.replace(
                "## 실행 계약\n\n- 이 파일에 연결된 문서는 순서대로 모두 읽고 적용한 뒤에만 다음 작업으로 넘어간다.\n- `docs/project_entrypoint.md`를 열었으면 그 문서의 `공통 규칙`, `프로젝트 전용 규칙`에 연결된 문서까지 끝까지 이어서 읽고 적용한다.\n- 링크만 확인하고 중간 문서에서 멈추지 않는다.\n\n",
                "",
                1,
            )
            agents_path.write_text(agents_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("AGENTS.md: Missing section: ## 실행 계약", result.stderr)

    def test_project_entrypoint_without_traversal_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace(
                "## 실행 계약\n\n- 이 문서에 들어온 runtime 또는 작업자는 `공통 규칙`, `프로젝트 전용 규칙`에 적힌 문서를 순서대로 모두 읽고 적용한 뒤에만 구현 또는 판단을 진행한다.\n- vendored core guide는 공통 규칙 기준을 주고, `docs/standard/*` 문서는 프로젝트 전용 기준을 주므로 둘 중 하나만 읽고 멈추지 않는다.\n\n",
                "",
                1,
            )
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("docs/project_entrypoint.md: Missing section: ## 실행 계약", result.stderr)

    def test_project_entrypoint_without_decisions_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace("## 프로젝트 결정 문서\n\n- `docs/decisions/README.md`\n\n- 현재 작업이 중요한 정책, 예외 처리 규칙, 책임 배치, 운영 결정을 건드리면 이 문서에서 관련 decision을 찾아 함께 읽고 갱신한다.\n", "", 1)
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("docs/project_entrypoint.md: Missing section: ## 프로젝트 결정 문서", result.stderr)

    def test_decisions_index_missing_listed_decision_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            decisions_index_path = target / "docs/decisions/README.md"
            decisions_text = decisions_index_path.read_text(encoding="utf-8")
            decisions_text = decisions_text.replace(
                "- 아직 active decision 없음. 새 decision을 추가하면 여기에 기록한다.",
                "- `docs/decisions/DEC-001-authorization-validation-location.md`",
                1,
            )
            decisions_index_path.write_text(decisions_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("index에 적힌 decision 문서가 실제 프로젝트에 없습니다", result.stderr)

    def test_self_referencing_common_harness_guide_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace(
                "vendor/harness-kit/docs/harness_guide.md",
                "docs/project_entrypoint.md",
                1,
            )
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("공통 harness guide 경로가 없습니다", result.stderr)

    def test_unlocalized_bootstrap_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/standard/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- bootstrap 출처 또는 기준 언어 문서: `vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md`",
                "- bootstrap 출처 또는 기준 언어 문서: `bootstrap/language_conventions/python_coding_conventions_template.md`",
                1,
            )
            coding_text = coding_text.replace(
                "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                "bootstrap/language_conventions/python_coding_conventions_template.md",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("repo-local path로 남아 있습니다", result.stderr)

    def test_missing_localized_common_harness_guide_path_fails(self) -> None:
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

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("vendored harness guide 경로가 실제 프로젝트에서 존재하지 않습니다", result.stderr)
            self.assertIn("third_party/harness-kit/docs/harness_guide.md", result.stderr)

    def test_existing_localized_common_harness_guide_path_passes(self) -> None:
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
            self.create_reference_files(target, harness_guide_reference="third_party/harness-kit/docs/harness_guide.md")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay consistency validation passed", result.stdout)

    def test_mixed_valid_and_stale_common_harness_guide_paths_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/project_entrypoint.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace(
                "- `vendor/harness-kit/docs/harness_guide.md`\n",
                "- `vendor/harness-kit/docs/harness_guide.md`\n- `third_party/harness-kit/docs/harness_guide.md`\n",
                1,
            )
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("stale vendored harness guide 경로가 남아 있습니다", result.stderr)
            self.assertIn("third_party/harness-kit/docs/harness_guide.md", result.stderr)

    def test_missing_localized_bootstrap_reference_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/standard/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- bootstrap 출처 또는 기준 언어 문서: `vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md`",
                "- bootstrap 출처 또는 기준 언어 문서: `third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md`",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("bootstrap 기준 문서 경로가 실제 프로젝트에서 존재하지 않습니다", result.stderr)
            self.assertIn("third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md", result.stderr)

    def test_existing_localized_bootstrap_reference_path_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            coding_path = target / "docs/standard/coding_conventions_project.md"
            coding_text = coding_path.read_text(encoding="utf-8")
            coding_text = coding_text.replace(
                "- bootstrap 출처 또는 기준 언어 문서: `vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md`",
                "- bootstrap 출처 또는 기준 언어 문서: `third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md`",
                1,
            )
            coding_path.write_text(coding_text, encoding="utf-8")
            self.create_reference_files(
                target,
                bootstrap_reference="third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
            )

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay consistency validation passed", result.stdout)

    def test_bootstrap_with_vendor_path_passes_without_manual_localization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project_with_vendor_path(target, vendor_path="third_party/harness-kit")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("overlay consistency validation passed", result.stdout)

    def test_missing_quality_gate_boundary_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            quality_gate_path = target / "docs/standard/quality_gate_profile.md"
            quality_gate_text = quality_gate_path.read_text(encoding="utf-8")
            quality_gate_text = quality_gate_text.replace(
                "- 세부 테스트 범위와 환경은 `testing_profile.md`를 참조한다.\n",
                "",
                1,
            )
            quality_gate_path.write_text(quality_gate_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("testing_profile.md로 세부 기준을 연결하지 않습니다", result.stderr)

    def test_missing_implementation_order_reference_to_architecture_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            order_path = target / "docs/standard/implementation_order.md"
            order_text = order_path.read_text(encoding="utf-8")
            order_text = order_text.replace("architecture.md", "layer_structure.md", 1)
            order_path.write_text(order_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("architecture.md 참조가 없어", result.stderr)

    def test_missing_commit_rule_gate_term_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            commit_rule_path = target / "docs/standard/commit_rule.md"
            commit_rule_text = commit_rule_path.read_text(encoding="utf-8")
            commit_rule_text = commit_rule_text.replace(
                "- 현재 커밋 범위에서 필수 테스트가 통과하는가\n",
                "",
                1,
            )
            commit_rule_path.write_text(commit_rule_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("`test` 기준이 없습니다", result.stderr)

    def test_legacy_project_local_entrypoint_leftover_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            legacy_path = target / "docs/harness_guide.md"
            legacy_path.write_text(
                (target / "docs/project_entrypoint.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("legacy project-local entrypoint가 남아 있습니다", result.stderr)


if __name__ == "__main__":
    unittest.main()
