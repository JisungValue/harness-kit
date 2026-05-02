from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "maintainer" / "scripts" / "check_harness_docs.py"


def load_check_harness_docs_module():
    spec = importlib.util.spec_from_file_location("check_harness_docs", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load check_harness_docs module")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckHarnessDocsTest(unittest.TestCase):
    def test_project_standard_template_guardrails_pass_for_current_templates(self) -> None:
        module = load_check_harness_docs_module()
        errors: list[str] = []

        module.check_project_standard_template_guardrails(errors)

        self.assertEqual(errors, [])

    def test_project_standard_template_guardrails_fail_when_core_phrase_is_missing(self) -> None:
        module = load_check_harness_docs_module()
        original_read_text = module.read_text

        def fake_read_text(rel_path: str) -> str:
            text = original_read_text(rel_path)
            if rel_path == "bootstrap/docs/project_overlay/architecture_template.md":
                return text.replace(
                    "기획서만 보고 구체 클래스명/파일명/패키지명/모듈명을 추측하지 않는다",
                    "",
                    1,
                )
            return text

        errors: list[str] = []
        with mock.patch.object(module, "read_text", side_effect=fake_read_text):
            module.check_project_standard_template_guardrails(errors)

        self.assertTrue(
            any("기획서만 보고 구체 클래스명/파일명/패키지명/모듈명을 추측하지 않는다" in error for error in errors),
            errors,
        )

    def test_project_standard_template_guardrails_fail_when_implementation_order_phrase_is_missing(self) -> None:
        module = load_check_harness_docs_module()
        original_read_text = module.read_text

        def fake_read_text(rel_path: str) -> str:
            text = original_read_text(rel_path)
            if rel_path == "bootstrap/docs/project_overlay/implementation_order_template.md":
                return text.replace(
                    "class/file 단위 구현 순서가 아니라 layer/boundary 단위 기본 구현 순서",
                    "",
                    1,
                )
            return text

        errors: list[str] = []
        with mock.patch.object(module, "read_text", side_effect=fake_read_text):
            module.check_project_standard_template_guardrails(errors)

        self.assertTrue(
            any("class/file 단위 구현 순서가 아니라 layer/boundary 단위 기본 구현 순서" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
