from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "ticket-specification-v1.json"
TEMPLATES = (
    "epic.md",
    "story.md",
    "bug.md",
    "security.md",
    "documentation.md",
    "testing.md",
)


class TicketSpecificationTest(unittest.TestCase):
    def load_json(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profile_defaults_and_cardinality(self) -> None:
        profile = self.load_json(PROFILE)
        defaults = profile["defaults"]
        categories = profile["label_categories"]

        self.assertEqual("marcus", defaults["assignee"])
        self.assertEqual("Priority/Low", defaults["priority"])
        self.assertEqual("Status/Backlog", defaults["status"])
        self.assertEqual(1, categories["kind"]["minimum"])
        self.assertEqual(1, categories["kind"]["maximum"])
        self.assertEqual(1, categories["priority"]["maximum"])
        self.assertEqual(1, categories["status"]["maximum"])
        self.assertEqual(1, categories["area"]["minimum"])
        self.assertIsNone(categories["area"]["maximum"])
        self.assertEqual([1, 2, 3, 5, 8, 13], categories["estimate"]["values"])

    def test_profile_ticket_families(self) -> None:
        profile = self.load_json(PROFILE)
        families = profile["families"]

        self.assertEqual(["Kind/Epic"], families["epic"])
        self.assertIn("Kind/Feature", families["story"])
        self.assertIn("Kind/Refactoring", families["story"])
        self.assertIn("Kind/Maintenance", families["story"])
        self.assertIn("Kind/Research", families["story"])
        self.assertEqual(["Kind/Bug"], families["bug"])
        self.assertEqual("Blocked by", profile["relations"]["direct_dependency_heading"])
        self.assertTrue(profile["relations"]["include_closed_tickets"])

    def test_ticket_schema_contains_ready_and_research_conditions(self) -> None:
        schema = self.load_json(
            ROOT / "schemas" / "ticket-specification-v1.schema.json"
        )
        self.assertGreaterEqual(len(schema["allOf"]), 3)
        self.assertIn("Kind/Epic", schema["properties"]["kind"]["enum"])
        self.assertEqual(
            "Priority/Low",
            schema["properties"]["priority"]["default"],
        )

    def test_repository_schema_contains_both_branching_models(self) -> None:
        schema = self.load_json(
            ROOT / "schemas" / "repository-standards-v1.schema.json"
        )
        models = schema["properties"]["branching"]["oneOf"]
        self.assertEqual("single", models[0]["properties"]["model"]["const"])
        self.assertEqual("integration", models[1]["properties"]["model"]["const"])
        self.assertEqual(
            "^(main|develop|PR-[0-9]+)$",
            models[1]["properties"]["multibranch_filter"]["const"],
        )

    def test_workflow_v2_contract(self) -> None:
        text = (
            ROOT
            / "standards"
            / "development-workflow"
            / "v2"
            / "standard.md"
        ).read_text(encoding="utf-8")

        normalized = " ".join(text.split())
        self.assertIn("Does this repository use a `develop` branch?", normalized)
        self.assertIn("^(main|develop|PR-[0-9]+)$", normalized)
        self.assertIn(
            "Regular ticket branches MUST be created from `develop`",
            normalized,
        )
        self.assertIn(
            "Regular ticket pull requests MUST target `develop`",
            normalized,
        )
        self.assertIn(
            "MUST be created manually and merged manually",
            normalized,
        )
        self.assertIn(
            "`main` and `develop` MUST use equivalent protection",
            normalized,
        )
        self.assertIn("MUST then be reintegrated into `develop`", normalized)
        self.assertIn("Builds of `main` MUST be triggered manually", normalized)

    def test_generated_assets_match_committed_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            completed = subprocess.run(
                [
                    sys.executable,
                    "tools/render_ticket_assets.py",
                    "--root",
                    str(ROOT),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                0,
                completed.returncode,
                completed.stdout + completed.stderr,
            )

            for name in TEMPLATES:
                expected = ROOT / "reference" / "issue-templates" / name
                actual = output / "reference" / "issue-templates" / name
                self.assertEqual(
                    expected.read_text(encoding="utf-8"),
                    actual.read_text(encoding="utf-8"),
                )

            expected_ai = ROOT / "reference" / "ai" / "ticket-authoring-v1.md"
            actual_ai = output / "reference" / "ai" / "ticket-authoring-v1.md"
            self.assertEqual(
                expected_ai.read_text(encoding="utf-8"),
                actual_ai.read_text(encoding="utf-8"),
            )

    def test_templates_preserve_common_and_dependency_sections(self) -> None:
        required = (
            "## Context",
            "## Goal",
            "## Scope",
            "### In scope",
            "### Out of scope",
            "### Affected components",
            "## Relations",
            "### Blocked by",
            "## Validation",
            "## Impact assessment",
            "## Estimate",
        )
        for name in TEMPLATES:
            text = (
                ROOT / "reference" / "issue-templates" / name
            ).read_text(encoding="utf-8")
            for heading in required:
                self.assertIn(heading, text, f"{heading} missing from {name}")

    def test_ai_adapter_requires_released_policy_loading(self) -> None:
        text = (
            ROOT / "reference" / "ai" / "ticket-authoring-v1.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        self.assertIn("MUST load the matching adapter", normalized)
        self.assertIn("MUST NOT reconstruct rules from memory", normalized)
        self.assertIn("workboard_forgejo_issue_dependency_sync", normalized)


if __name__ == "__main__":
    unittest.main()
