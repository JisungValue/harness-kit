from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_downstream_bundle.py"


def load_bundle_module():
    spec = importlib.util.spec_from_file_location("generate_downstream_bundle", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load generate_downstream_bundle module")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class GenerateDownstreamBundleTest(unittest.TestCase):
    def make_dist_temp_dir(self) -> tempfile.TemporaryDirectory[str]:
        dist_root = ROOT / "dist"
        dist_root.mkdir(exist_ok=True)
        return tempfile.TemporaryDirectory(dir=dist_root)

    def run_cli(self, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *extra_args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_generates_bundle_with_manifest_and_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"

            result = self.run_cli("--output", str(output))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Generated downstream bundle", result.stdout)
            self.assertTrue((output / "README.md").exists())
            self.assertTrue((output / "bundle_manifest.json").exists())
            self.assertTrue((output / "docs/harness_guide.md").exists())
            self.assertTrue((output / "docs/downstream_harness_flow.md").exists())
            self.assertTrue((output / "docs/version_support.md").exists())
            self.assertTrue((output / "docs/examples/sample-task/issue.md").exists())
            self.assertTrue((output / "bootstrap/README.md").exists())
            self.assertTrue((output / "docs/project_overlay/harness_doc_guard_workflow_template.yml").exists())
            self.assertTrue((output / "scripts/adopt_common.py").exists())
            self.assertTrue((output / "scripts/adopt_dry_run.py").exists())
            self.assertTrue((output / "scripts/adopt_safe_write.py").exists())
            self.assertTrue((output / "scripts/check_first_success_docs.py").exists())
            self.assertTrue((output / "scripts/validate_phase_gate.py").exists())

            self.assertFalse((output / "maintainer/docs/release_process.md").exists())
            self.assertFalse((output / "scripts/check_harness_docs.py").exists())
            self.assertFalse((output / "scripts/install_downstream_bundle.py").exists())
            self.assertFalse((output / "tests/test_bootstrap_init.py").exists())
            self.assertFalse((output / "harness.log").exists())

            bundle_readme = (output / "README.md").read_text(encoding="utf-8")
            self.assertIn("# Harness Kit Project Bundle", bundle_readme)
            self.assertNotIn("maintainer/docs/downstream_bundle_boundary.md", bundle_readme)
            self.assertIn("- `.git*`", bundle_readme)

            manifest = json.loads((output / "bundle_manifest.json").read_text(encoding="utf-8"))
            copied_paths = [entry["path"] for entry in manifest["copied_files"]]
            self.assertEqual(copied_paths, sorted(copied_paths))
            self.assertIn("docs/quickstart.md", copied_paths)
            self.assertIn("docs/downstream_harness_flow.md", copied_paths)
            self.assertIn("docs/version_support.md", copied_paths)
            self.assertIn("docs/project_overlay/harness_doc_guard_workflow_template.yml", copied_paths)
            self.assertIn("scripts/bootstrap_init.py", copied_paths)
            self.assertIn("scripts/validate_phase_gate.py", copied_paths)
            self.assertEqual(manifest["artifact_format"], "directory")
            self.assertEqual(
                manifest["boundary_document"],
                "maintainer/docs/downstream_bundle_boundary.md",
            )
            self.assertIn("bootstrap/**/*", manifest["source_patterns"])
            self.assertIn("docs/examples/**/*.md", manifest["source_patterns"])
            self.assertIn("docs/project_overlay/harness_doc_guard_workflow_template.yml", manifest["source_patterns"])
            self.assertIn("maintainer/docs/*", manifest["excluded_patterns"])
            self.assertEqual(manifest["generated_files"][0]["path"], "README.md")

    def test_bundle_patterns_are_read_from_boundary_document(self) -> None:
        module = load_bundle_module()
        synthetic_boundary = "\n".join(
            [
                "### 1) Downstream 필수 자산",
                "- `scripts/bootstrap_init.py`",
                "### 2) Downstream 선택 자산",
                "- `docs/examples/**/*.md`",
                "### 3) Maintainer 전용 자산",
                "- `scripts/validate_downstream_bundle.py`",
            ]
        )

        with mock.patch.object(module, "read_boundary_document", return_value=synthetic_boundary):
            self.assertEqual(
                module.extract_bundle_patterns(),
                ["scripts/bootstrap_init.py", "docs/examples/**/*.md"],
            )

            bundle_files = module.build_bundle_files()
            bundle_paths = [bundle_file.relative_path.as_posix() for bundle_file in bundle_files]

        self.assertIn("scripts/bootstrap_init.py", bundle_paths)
        self.assertNotIn("docs/project_entrypoint.md", bundle_paths)
        self.assertTrue(
            all(path == "scripts/bootstrap_init.py" or path.startswith("docs/examples/") for path in bundle_paths)
        )

    def test_bundle_readme_exclusions_are_read_from_boundary_document(self) -> None:
        module = load_bundle_module()
        synthetic_boundary = "\n".join(
            [
                "### 1) Downstream 필수 자산",
                "- `scripts/bootstrap_init.py`",
                "### 2) Downstream 선택 자산",
                "- `docs/examples/**/*.md`",
                "### 3) Maintainer 전용 자산",
                "- `scripts/check_harness_docs.py`",
                "- `scripts/validate_downstream_bundle.py`",
            ]
        )

        with mock.patch.object(module, "read_boundary_document", return_value=synthetic_boundary):
            readme_text = module.bundle_readme_text([])

        self.assertIn("- `scripts/check_harness_docs.py`", readme_text)
        self.assertIn("- `scripts/validate_downstream_bundle.py`", readme_text)

    def test_maintainer_only_patterns_override_included_paths(self) -> None:
        module = load_bundle_module()
        synthetic_boundary = "\n".join(
            [
                "### 1) Downstream 필수 자산",
                "- `scripts/bootstrap_init.py`",
                "- `docs/examples/**/*.md`",
                "### 2) Downstream 선택 자산",
                "- `docs/examples/**/*.md`",
                "### 3) Maintainer 전용 자산",
                "- `scripts/bootstrap_init.py`",
            ]
        )

        with mock.patch.object(module, "read_boundary_document", return_value=synthetic_boundary):
            bundle_files = module.build_bundle_files()
            bundle_paths = [bundle_file.relative_path.as_posix() for bundle_file in bundle_files]

        self.assertNotIn("scripts/bootstrap_init.py", bundle_paths)
        self.assertTrue(all(path.startswith("docs/examples/") for path in bundle_paths))

    def test_manifest_is_deterministic_across_output_locations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            first_output = Path(tmp_dir) / "bundle-a"
            second_output = Path(tmp_dir) / "bundle-b"

            first_result = self.run_cli("--output", str(first_output))
            second_result = self.run_cli("--output", str(second_output))

            self.assertEqual(first_result.returncode, 0, first_result.stderr)
            self.assertEqual(second_result.returncode, 0, second_result.stderr)

            first_manifest = (first_output / "bundle_manifest.json").read_text(encoding="utf-8")
            second_manifest = (second_output / "bundle_manifest.json").read_text(encoding="utf-8")
            self.assertEqual(first_manifest, second_manifest)

    def test_fails_when_output_directory_is_not_empty_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            output.mkdir()
            (output / "old.txt").write_text("stale\n", encoding="utf-8")

            result = self.run_cli("--output", str(output))

            self.assertEqual(result.returncode, 1)
            self.assertIn("already contains files", result.stderr)

    def test_force_replaces_existing_bundle_directory(self) -> None:
        with self.make_dist_temp_dir() as tmp_dir:
            output = Path(tmp_dir) / "bundle"

            first_result = self.run_cli("--output", str(output))
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "bundle_manifest.json").exists())

    def test_force_allows_stale_previous_bundle_paths_listed_in_manifest(self) -> None:
        with self.make_dist_temp_dir() as tmp_dir:
            output = Path(tmp_dir) / "bundle"

            first_result = self.run_cli("--output", str(output))
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            stale_path = output / "docs/project_overlay/project_harness_guide_template.md"
            stale_path.parent.mkdir(parents=True, exist_ok=True)
            stale_path.write_text("stale previous bundle file\n", encoding="utf-8")

            manifest_path = output / "bundle_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["copied_files"].append(
                {
                    "path": "docs/project_overlay/project_harness_guide_template.md",
                    "sha256": "0" * 64,
                    "size_bytes": stale_path.stat().st_size,
                }
            )
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale_path.exists())

    def test_force_rejects_non_bundle_directory(self) -> None:
        with self.make_dist_temp_dir() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            output.mkdir()
            (output / "old.txt").write_text("stale\n", encoding="utf-8")

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 1)
            self.assertIn("contains non-bundle paths", result.stderr)

    def test_force_rejects_output_outside_dist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 1)
            self.assertIn("can only replace bundle output directories under dist/", result.stderr)

    def test_force_rejects_non_empty_output_outside_dist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "bundle"

            first_result = self.run_cli("--output", str(output))
            self.assertEqual(first_result.returncode, 0, first_result.stderr)

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 1)
            self.assertIn("can only replace bundle output directories under dist/", result.stderr)

    def test_force_rejects_spoofed_manifest_directory(self) -> None:
        with self.make_dist_temp_dir() as tmp_dir:
            output = Path(tmp_dir) / "bundle"
            output.mkdir()
            (output / "bundle_manifest.json").write_text(
                '{"boundary_document": "maintainer/docs/downstream_bundle_boundary.md", "entry_readme": "README.md", "manifest_path": "bundle_manifest.json"}\n',
                encoding="utf-8",
            )
            (output / "old.txt").write_text("stale\n", encoding="utf-8")

            result = self.run_cli("--output", str(output), "--force")

            self.assertEqual(result.returncode, 1)
            self.assertIn("contains non-bundle paths", result.stderr)

    def test_rejects_repository_root_as_output(self) -> None:
        result = self.run_cli("--output", str(ROOT))

        self.assertEqual(result.returncode, 1)
        self.assertIn("repository root", result.stderr)


if __name__ == "__main__":
    unittest.main()
