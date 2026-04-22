from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATE_SCRIPT = ROOT / "scripts" / "generate_downstream_bundle.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_downstream_bundle.py"


class ValidateDownstreamBundleTest(unittest.TestCase):
    def run_generate(self, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATE_SCRIPT), "--output", str(output)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_validate(self, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT), str(output)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_generated_bundle_passes_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            generate_result = self.run_generate(output)
            self.assertEqual(generate_result.returncode, 0, generate_result.stderr)

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 0, validate_result.stderr)
            self.assertIn("downstream bundle validation passed", validate_result.stdout)

    def test_missing_required_bundle_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)
            (output / "docs/project_overlay/harness_doc_guard_workflow_template.yml").unlink()

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn(
                "missing required bundle file: docs/project_overlay/harness_doc_guard_workflow_template.yml",
                validate_result.stderr,
            )

    def test_unexpected_maintainer_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)
            extra_path = output / "maintainer/docs/release_process.md"
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text("maintainer only\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn(
                "unexpected path outside downstream bundle boundary: maintainer/docs/release_process.md",
                validate_result.stderr,
            )

    def test_manifest_source_patterns_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)

            manifest_path = output / "bundle_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["source_patterns"] = ["docs/examples/**/*.md"]
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn("manifest field mismatch for source_patterns", validate_result.stderr)

    def test_manifest_excluded_patterns_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)

            manifest_path = output / "bundle_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["excluded_patterns"] = ["tests/*"]
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn("manifest field mismatch for excluded_patterns", validate_result.stderr)

    def test_bundle_file_content_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)
            changed_path = output / "scripts/bootstrap_init.py"
            changed_path.write_text("#!/usr/bin/env python3\nprint('drift')\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn("bundle file differs from source-of-truth: scripts/bootstrap_init.py", validate_result.stderr)

    def test_generated_readme_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)
            (output / "README.md").write_text("# stale\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn("generated entry file content drifted: README.md", validate_result.stderr)
            self.assertIn("manifest generated_files entry mismatch for README.md", validate_result.stderr)

    def test_manifest_generated_readme_entry_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            self.assertEqual(self.run_generate(output).returncode, 0)

            manifest_path = output / "bundle_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["generated_files"][0]["sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            validate_result = self.run_validate(output)

            self.assertEqual(validate_result.returncode, 1)
            self.assertIn("manifest generated_files entry mismatch for README.md", validate_result.stderr)


if __name__ == "__main__":
    unittest.main()
