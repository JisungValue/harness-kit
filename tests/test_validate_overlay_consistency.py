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
    def bootstrap_project(self, target: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(BOOTSTRAP_SCRIPT), str(target), "--language", "python"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

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

            guide_path = target / "docs/harness_guide.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace("- `docs/standard/testing_profile.md`\n", "", 1)
            guide_path.write_text(guide_text, encoding="utf-8")

            result = self.run_checker(target)

            self.assertEqual(result.returncode, 1)
            self.assertIn("필수 standard 문서 참조가 누락", result.stderr)

    def test_self_referencing_common_harness_guide_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sample-project"
            self.bootstrap_project(target)

            guide_path = target / "docs/harness_guide.md"
            guide_text = guide_path.read_text(encoding="utf-8")
            guide_text = guide_text.replace(
                "vendor/harness-kit/docs/harness_guide.md",
                "docs/harness_guide.md",
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


if __name__ == "__main__":
    unittest.main()
