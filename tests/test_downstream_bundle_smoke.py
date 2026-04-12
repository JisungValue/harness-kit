from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATE_SCRIPT = ROOT / "scripts" / "generate_downstream_bundle.py"
CANONICAL_BUNDLE_ROOT = ROOT / "dist" / "harness-kit-project-bundle"
LANGUAGE = "python"
DEFAULT_HARNESS_GUIDE_REFERENCE = "vendor/harness-kit/docs/harness_guide.md"
DEFAULT_BOOTSTRAP_REFERENCE = (
    "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md"
)
FIRST_SUCCESS_COMMAND = (
    "from pathlib import Path; "
    "paths = ['docs/project_entrypoint.md', 'docs/standard/architecture.md', "
    "'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', "
    "'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', "
    "'docs/standard/commit_rule.md']; "
    "missing = [p for p in paths if not Path(p).exists()]; "
    "print('first success docs are present') if not missing else "
    "(_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
)


class DownstreamBundleSmokeTest(unittest.TestCase):
    def run_generate_canonical_bundle(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATE_SCRIPT), "--force"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def vendor_generated_bundle(self, workspace_root: Path) -> tuple[Path, Path]:
        generate_result = self.run_generate_canonical_bundle()
        self.assertEqual(generate_result.returncode, 0, generate_result.stderr)
        self.assertTrue(CANONICAL_BUNDLE_ROOT.exists())

        project_root = workspace_root / "consumer-project"
        vendor_root = project_root / "vendor" / "harness-kit"
        vendor_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(CANONICAL_BUNDLE_ROOT, vendor_root)
        return project_root, vendor_root

    def run_bundle_script(
        self,
        project_root: Path,
        script_name: str,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(project_root / "vendor" / "harness-kit" / "scripts" / script_name), *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_first_success_command(self, project_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-c", FIRST_SUCCESS_COMMAND],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_maintainer_assets_absent(self, vendor_root: Path) -> None:
        self.assertFalse((vendor_root / "docs/kit_maintenance").exists())
        self.assertFalse((vendor_root / "scripts/generate_downstream_bundle.py").exists())
        self.assertFalse((vendor_root / "scripts/validate_downstream_bundle.py").exists())
        self.assertFalse((vendor_root / "harness.log").exists())

    def test_generated_bundle_supports_greenfield_bootstrap_and_overlay_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root, vendor_root = self.vendor_generated_bundle(Path(tmp_dir))

            self.assert_maintainer_assets_absent(vendor_root)

            init_result = self.run_bundle_script(
                project_root,
                "bootstrap_init.py",
                ".",
                "--language",
                LANGUAGE,
            )
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            self.assertIn("Created harness bootstrap docs in", init_result.stdout)

            first_success_result = self.run_first_success_command(project_root)
            self.assertEqual(first_success_result.returncode, 0, first_success_result.stderr)
            self.assertIn("first success docs are present", first_success_result.stdout)

            harness_guide = (project_root / "docs/project_entrypoint.md").read_text(encoding="utf-8")
            coding_conventions = (project_root / "docs/standard/coding_conventions_project.md").read_text(
                encoding="utf-8"
            )
            agents = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            gemini = (project_root / "GEMINI.md").read_text(encoding="utf-8")
            self.assertIn(DEFAULT_HARNESS_GUIDE_REFERENCE, harness_guide)
            self.assertIn(DEFAULT_BOOTSTRAP_REFERENCE, coding_conventions)
            self.assertIn("docs/project_entrypoint.md", agents)
            self.assertIn("AGENTS.md", gemini)

            decisions_result = self.run_bundle_script(
                project_root,
                "validate_overlay_decisions.py",
                ".",
                "--readiness",
                "first-success",
            )
            self.assertEqual(decisions_result.returncode, 0, decisions_result.stderr)
            self.assertIn("overlay decision validation passed", decisions_result.stdout)

            consistency_result = self.run_bundle_script(project_root, "validate_overlay_consistency.py", ".")
            self.assertEqual(consistency_result.returncode, 0, consistency_result.stderr)
            self.assertIn("overlay consistency validation passed.", consistency_result.stdout)

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
            existing_harness_guide = project_root / "docs/project_entrypoint.md"
            existing_harness_guide.parent.mkdir(parents=True, exist_ok=True)
            existing_harness_guide.write_text(harness_guide_template, encoding="utf-8")

            adopt_result = self.run_bundle_script(
                project_root,
                "adopt_dry_run.py",
                ".",
                "--language",
                LANGUAGE,
            )
            self.assertEqual(adopt_result.returncode, 0, adopt_result.stderr)
            self.assertIn("write mode: disabled (read-only)", adopt_result.stdout)
            self.assertIn("- missing files: 9", adopt_result.stdout)
            self.assertIn("- differing files: 1", adopt_result.stdout)
            self.assertIn("- conflict candidates: 0", adopt_result.stdout)
            self.assertIn("Differing files (manual review):", adopt_result.stdout)
            self.assertIn(
                "docs/project_entrypoint.md <- docs/project_overlay/project_entrypoint_template.md",
                adopt_result.stdout,
            )

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
            existing_harness_guide = project_root / "docs/project_entrypoint.md"
            existing_harness_guide.parent.mkdir(parents=True, exist_ok=True)
            existing_harness_guide.write_text(harness_guide_template, encoding="utf-8")

            safe_write_result = self.run_bundle_script(
                project_root,
                "adopt_safe_write.py",
                ".",
                "--language",
                LANGUAGE,
            )
            self.assertEqual(safe_write_result.returncode, 0, safe_write_result.stderr)
            self.assertIn("- created files: 9", safe_write_result.stdout)
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


if __name__ == "__main__":
    unittest.main()
