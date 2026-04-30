from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATE_SCRIPT = ROOT / "maintainer" / "scripts" / "generate_downstream_bundle.py"
BOOTSTRAP_SCRIPT = ROOT / "bootstrap" / "scripts" / "bootstrap_init.py"
CANONICAL_BUNDLE_ROOT = ROOT / "dist" / "harness-kit-project-bundle"
DEFAULT_HARNESS_GUIDE_REFERENCE = "docs/process/harness_guide.md"
FIRST_SUCCESS_SCRIPT = "check_first_success_docs.py"
DEFAULT_VENDOR_RELATIVE_PATH = Path("vendor/harness-kit")


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location("bootstrap_init", BOOTSTRAP_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load bootstrap_init module")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LANGUAGE_BOOTSTRAP_REFERENCES = load_bootstrap_module().LANGUAGE_BOOTSTRAP_PATHS


class DownstreamBundleSmokeTest(unittest.TestCase):
    def run_generate_canonical_bundle(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATE_SCRIPT), "--force"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def vendor_generated_bundle(
        self,
        workspace_root: Path,
        project_name: str = "consumer-project",
        vendor_relative_path: Path = DEFAULT_VENDOR_RELATIVE_PATH,
    ) -> tuple[Path, Path]:
        generate_result = self.run_generate_canonical_bundle()
        self.assertEqual(generate_result.returncode, 0, generate_result.stderr)
        self.assertTrue(CANONICAL_BUNDLE_ROOT.exists())

        project_root = workspace_root / project_name
        vendor_root = project_root / vendor_relative_path
        vendor_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(CANONICAL_BUNDLE_ROOT, vendor_root)
        return project_root, vendor_root

    def run_bundle_script(
        self,
        project_root: Path,
        script_name: str,
        *args: str,
        vendor_relative_path: Path = DEFAULT_VENDOR_RELATIVE_PATH,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(project_root / vendor_relative_path / "scripts" / script_name), *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_first_success_command(
        self,
        project_root: Path,
        vendor_relative_path: Path = DEFAULT_VENDOR_RELATIVE_PATH,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_bundle_script(project_root, FIRST_SUCCESS_SCRIPT, ".", vendor_relative_path=vendor_relative_path)

    def assert_maintainer_assets_absent(self, vendor_root: Path) -> None:
        self.assertFalse((vendor_root / "docs/kit_maintenance").exists())
        self.assertFalse((vendor_root / "scripts/generate_downstream_bundle.py").exists())
        self.assertFalse((vendor_root / "scripts/validate_downstream_bundle.py").exists())
        self.assertFalse((vendor_root / "harness.log").exists())

    def assert_greenfield_bundle_language_flow(
        self,
        workspace_root: Path,
        language: str,
        bootstrap_reference: str,
        vendor_relative_path: Path = DEFAULT_VENDOR_RELATIVE_PATH,
        vendor_path_arg: str | None = None,
    ) -> None:
        project_root, vendor_root = self.vendor_generated_bundle(
            workspace_root,
            f"consumer-project-{language}-{vendor_relative_path.name}",
            vendor_relative_path=vendor_relative_path,
        )

        self.assert_maintainer_assets_absent(vendor_root)
        workflow_template = vendor_root / "docs/project_overlay/harness_doc_guard_workflow_template.yml"
        self.assertTrue(workflow_template.exists())
        self.assertIn("@<pin-tag-or-sha>", workflow_template.read_text(encoding="utf-8"))

        init_args = [".", "--language", language]
        if vendor_path_arg is not None:
            init_args.extend(["--vendor-path", vendor_path_arg])
        init_result = self.run_bundle_script(
            project_root,
            "bootstrap_init.py",
            *init_args,
            vendor_relative_path=vendor_relative_path,
        )
        self.assertEqual(init_result.returncode, 0, init_result.stderr)
        self.assertIn("Created harness bootstrap docs in", init_result.stdout)
        self.assertIn(
            "docs/entrypoint.md <- docs/project_overlay/project_entrypoint_template.md",
            init_result.stdout,
        )

        first_success_result = self.run_first_success_command(project_root, vendor_relative_path=vendor_relative_path)
        self.assertEqual(first_success_result.returncode, 0, first_success_result.stderr)
        self.assertIn("first success docs are present", first_success_result.stdout)

        harness_guide = (project_root / "docs/entrypoint.md").read_text(encoding="utf-8")
        decisions_index = (project_root / "docs/project/decisions/README.md").read_text(encoding="utf-8")
        coding_conventions = (project_root / "docs/project/standards/coding_conventions_project.md").read_text(
            encoding="utf-8"
        )
        agents = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        gemini = (project_root / "GEMINI.md").read_text(encoding="utf-8")
        self.assertIn(DEFAULT_HARNESS_GUIDE_REFERENCE, harness_guide)
        self.assertIn(bootstrap_reference, coding_conventions)
        self.assertIn("docs/entrypoint.md", agents)
        self.assertIn("순서대로 모두 읽고 적용", agents)
        self.assertIn("둘 중 하나만 읽고 멈추지 않는다", harness_guide)
        self.assertIn("docs/project/decisions/README.md", harness_guide)
        self.assertIn("DEC-###-slug.md", decisions_index)
        self.assertIn("AGENTS.md", gemini)
        self.assertIn("연결된 문서 체인도 끝까지 따라간다", gemini)

        decisions_result = self.run_bundle_script(
            project_root,
            "validate_overlay_decisions.py",
            ".",
            "--readiness",
            "first-success",
            vendor_relative_path=vendor_relative_path,
        )
        self.assertEqual(decisions_result.returncode, 0, decisions_result.stderr)
        self.assertIn("overlay decision validation passed", decisions_result.stdout)

        consistency_result = self.run_bundle_script(
            project_root,
            "validate_overlay_consistency.py",
            ".",
            vendor_relative_path=vendor_relative_path,
        )
        self.assertEqual(consistency_result.returncode, 0, consistency_result.stderr)
        self.assertIn("overlay consistency validation passed.", consistency_result.stdout)

    def test_generated_bundle_supports_greenfield_bootstrap_and_overlay_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir)
            for language, bootstrap_reference in LANGUAGE_BOOTSTRAP_REFERENCES.items():
                self.assert_greenfield_bundle_language_flow(workspace_root, language, bootstrap_reference)

    def test_generated_bundle_supports_greenfield_bootstrap_with_localized_vendor_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_root = Path(tmp_dir)
            self.assert_greenfield_bundle_language_flow(
                workspace_root,
                "python",
                "third_party/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
                vendor_relative_path=Path("third_party/harness-kit"),
                vendor_path_arg="third_party/harness-kit",
            )

    def test_generated_bundle_supports_brownfield_adopt_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root, vendor_root = self.vendor_generated_bundle(Path(tmp_dir))

            self.assert_maintainer_assets_absent(vendor_root)

            harness_guide_template = (vendor_root / "docs/project_overlay/project_entrypoint_template.md").read_text(
                encoding="utf-8"
            )
            harness_guide_template = harness_guide_template.replace(
                DEFAULT_HARNESS_GUIDE_REFERENCE,
                "third_party/harness-kit/docs/harness_guide.md",
                1,
            )
            existing_harness_guide = project_root / "docs/entrypoint.md"
            existing_harness_guide.parent.mkdir(parents=True, exist_ok=True)
            existing_harness_guide.write_text(harness_guide_template, encoding="utf-8")

            adopt_result = self.run_bundle_script(
                project_root,
                "adopt_dry_run.py",
                ".",
                "--language",
                "python",
            )
            self.assertEqual(adopt_result.returncode, 0, adopt_result.stderr)
            self.assertIn("write mode: disabled (read-only)", adopt_result.stdout)
            self.assertIn("- missing files: 43", adopt_result.stdout)
            self.assertIn("- differing files: 1", adopt_result.stdout)
            self.assertIn("- conflict candidates: 0", adopt_result.stdout)
            self.assertIn("Differing files (manual review):", adopt_result.stdout)
            self.assertIn(
                "docs/entrypoint.md <- docs/project_overlay/project_entrypoint_template.md",
                adopt_result.stdout,
            )

    def test_generated_bundle_supports_incremental_consistency_mode_for_partial_brownfield_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root, vendor_root = self.vendor_generated_bundle(Path(tmp_dir))

            self.assert_maintainer_assets_absent(vendor_root)

            harness_guide_template = (vendor_root / "docs/project_overlay/project_entrypoint_template.md").read_text(
                encoding="utf-8"
            )
            existing_harness_guide = project_root / "docs/entrypoint.md"
            existing_harness_guide.parent.mkdir(parents=True, exist_ok=True)
            existing_harness_guide.write_text(harness_guide_template, encoding="utf-8")

            third_party_guide = project_root / DEFAULT_HARNESS_GUIDE_REFERENCE
            third_party_guide.parent.mkdir(parents=True, exist_ok=True)
            third_party_guide.write_text("# Harness Core Guide\n", encoding="utf-8")
            downstream_flow = project_root / "docs/process/downstream_harness_flow.md"
            downstream_flow.write_text("# Downstream Harness Flow\n", encoding="utf-8")

            incremental_result = self.run_bundle_script(
                project_root,
                "validate_overlay_consistency.py",
                ".",
                "--mode",
                "incremental",
            )
            self.assertEqual(incremental_result.returncode, 0, incremental_result.stderr)
            self.assertIn("overlay consistency validation passed for mode 'incremental'.", incremental_result.stdout)
            self.assertIn("Still missing overlay docs allowed in incremental mode:", incremental_result.stdout)
            self.assertIn("docs/project/decisions/README.md", incremental_result.stdout)
            self.assertIn("Still missing runtime instruction entrypoints allowed in incremental mode:", incremental_result.stdout)
            self.assertIn("AGENTS.md", incremental_result.stdout)

    def test_generated_bundle_supports_brownfield_safe_write_for_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root, vendor_root = self.vendor_generated_bundle(Path(tmp_dir))

            self.assert_maintainer_assets_absent(vendor_root)

            harness_guide_template = (vendor_root / "docs/project_overlay/project_entrypoint_template.md").read_text(
                encoding="utf-8"
            )
            harness_guide_template = harness_guide_template.replace(
                DEFAULT_HARNESS_GUIDE_REFERENCE,
                "third_party/harness-kit/docs/harness_guide.md",
                1,
            )
            existing_harness_guide = project_root / "docs/entrypoint.md"
            existing_harness_guide.parent.mkdir(parents=True, exist_ok=True)
            existing_harness_guide.write_text(harness_guide_template, encoding="utf-8")

            safe_write_result = self.run_bundle_script(
                project_root,
                "adopt_safe_write.py",
                ".",
                "--language",
                "python",
            )
            self.assertEqual(safe_write_result.returncode, 0, safe_write_result.stderr)
            self.assertIn("- created files: 43", safe_write_result.stdout)
            self.assertIn("- remaining missing files: 0", safe_write_result.stdout)
            self.assertIn("- remaining differing files: 1", safe_write_result.stdout)

            first_success_result = self.run_first_success_command(project_root)
            self.assertEqual(first_success_result.returncode, 0, first_success_result.stderr)
            self.assertIn("first success docs are present", first_success_result.stdout)

            decisions_result = self.run_bundle_script(
                project_root,
                "validate_overlay_decisions.py",
                ".",
                "--readiness",
                "first-success",
            )
            self.assertEqual(decisions_result.returncode, 0, decisions_result.stderr)

    def test_generated_bundle_supports_legacy_entrypoint_migration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root, vendor_root = self.vendor_generated_bundle(Path(tmp_dir))

            self.assert_maintainer_assets_absent(vendor_root)

            legacy_template = (vendor_root / "docs/project_overlay/project_entrypoint_template.md").read_text(
                encoding="utf-8"
            )
            legacy_path = project_root / "docs/harness_guide.md"
            legacy_path.parent.mkdir(parents=True, exist_ok=True)
            legacy_path.write_text(legacy_template, encoding="utf-8")

            agents_template = (vendor_root / "docs/project_overlay/agent_entrypoint_template.md").read_text(
                encoding="utf-8"
            )
            agents_template = agents_template.replace("docs/entrypoint.md", "docs/harness_guide.md", 1)
            (project_root / "AGENTS.md").write_text(agents_template, encoding="utf-8")

            dry_run_result = self.run_bundle_script(
                project_root,
                "adopt_dry_run.py",
                ".",
                "--language",
                "python",
            )
            self.assertEqual(dry_run_result.returncode, 0, dry_run_result.stderr)
            self.assertIn("- legacy entrypoint migration candidates: 1", dry_run_result.stdout)

            migrate_result = self.run_bundle_script(
                project_root,
                "adopt_safe_write.py",
                ".",
                "--language",
                "python",
                "--migrate-legacy-entrypoint",
            )
            self.assertEqual(migrate_result.returncode, 0, migrate_result.stderr)
            self.assertIn("- migrated legacy entrypoints: 1", migrate_result.stdout)
            self.assertFalse(legacy_path.exists())
            self.assertTrue((project_root / "docs/entrypoint.md").exists())

            consistency_result = self.run_bundle_script(project_root, "validate_overlay_consistency.py", ".")
            self.assertEqual(consistency_result.returncode, 0, consistency_result.stderr)
            self.assertIn("overlay consistency validation passed.", consistency_result.stdout)


if __name__ == "__main__":
    unittest.main()
