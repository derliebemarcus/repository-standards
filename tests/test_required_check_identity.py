from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_BLOBS = {
    "standards/development-workflow/v5/standard.md":
        "4d84f0ec8d07d13e48b41e2de8a4edbb7b2787a0",
    "profiles/development-workflow-v5.json":
        "d2c90a3b12533a68b1fc1663abc942129d111cfb",
    "schemas/development-workflow-v5.schema.json":
        "747f49a7bcdde15706025b94d9ada778227993dc",
    "reference/ai/development-workflow-v5.md":
        "457b504699786189ef285705cd2e30b424f0a94c",
    "schemas/repository-standards-v6.schema.json":
        "93be6e041a9be193544b1d33bd6aec666b93ecc8",
    "profiles/repository-standards-compatibility-v5.json":
        "41412cc736149621c179bf41b53e16305d2aa16c",
}


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def declaration_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        if raw_line == raw_line.lstrip() and raw_line.endswith(":"):
            section = raw_line[:-1]
            continue
        key, separator, value = raw_line.strip().partition(":")
        if not separator:
            continue
        normalized = value.strip().strip('"')
        values[f"{section}.{key}" if section else key] = normalized
    return values


class RequiredCheckIdentityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = load_json("profiles/development-workflow-v6.json")
        cls.workflow_v5 = load_json("profiles/development-workflow-v5.json")
        cls.workflow_schema = load_json("schemas/development-workflow-v6.schema.json")
        cls.repository_schema = load_json("schemas/repository-standards-v7.schema.json")
        cls.compatibility = load_json(
            "profiles/repository-standards-compatibility-v6.json"
        )
        cls.compatibility_v5 = load_json(
            "profiles/repository-standards-compatibility-v5.json"
        )

    def test_v6_preserves_v5_behavior_except_required_check_contract(self) -> None:
        for key in (
            "branch_naming",
            "pull_request_naming",
            "pre_write_validation",
            "exemptions",
            "post_write_validation",
            "branching",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.workflow_v5[key], self.workflow[key])

        self.assertEqual("6.0.0", self.workflow["version"])
        self.assertEqual("v7", self.workflow["requires"]["declaration_schema"])
        self.assertEqual("v3", self.workflow["requires"]["ticket_specification"])
        self.assertIn("required_checks", self.workflow)

    def test_forgejo_gitea_event_is_part_of_concrete_identity(self) -> None:
        checks = self.workflow["required_checks"]
        forgejo = checks["providers"]["forgejo_gitea"]
        self.assertEqual("logical-gate-with-provider-adapter", checks["identity_model"])
        self.assertEqual("<workflow> / <job> (<event>)", forgejo["context_format"])
        self.assertTrue(forgejo["event_part_of_identity"])
        self.assertTrue(forgejo["event_change_requires_identity_migration"])
        self.assertTrue(forgejo["workflow_and_branch_protection_migrate_together"])
        self.assertTrue(forgejo["bounded_pattern_matching_allowed"])

    def test_github_mapping_does_not_invent_forgejo_event_suffix(self) -> None:
        github = self.workflow["required_checks"]["providers"]["github"]
        self.assertEqual("<job>", github["normal_context_format"])
        self.assertEqual(
            "<job> / <reusable-job>", github["reusable_context_format"]
        )
        self.assertFalse(github["event_part_of_identity"])
        self.assertFalse(github["workflow_name_part_of_identity"])
        self.assertFalse(github["matrix_part_of_identity"])

    def test_pull_request_target_has_explicit_untrusted_code_boundary(self) -> None:
        target = self.workflow["required_checks"]["events"]["pull_request_target"]
        self.assertTrue(target["base_branch_context"])
        self.assertTrue(target["privileged_context"])
        self.assertFalse(target["untrusted_pr_code_execution_allowed"])
        self.assertEqual(
            ["policy", "metadata", "repository-governance"],
            target["recommended_uses"],
        )

    def test_stale_unproducible_required_context_fails_closed(self) -> None:
        checks = self.workflow["required_checks"]
        migration = checks["migration"]
        self.assertTrue(checks["configured_context_must_be_producible"])
        self.assertTrue(checks["fail_closed"])
        self.assertTrue(migration["verify_new_identity_is_produced"])
        self.assertTrue(migration["update_workflow_and_protection_consistently"])
        self.assertTrue(migration["reject_stale_unproducible_required_context"])
        self.assertTrue(migration["must_not_weaken_logical_gate"])
        self.assertTrue(migration["rollback_evidence_required_until_qualified"])

    def test_workflow_schema_pins_required_check_contract(self) -> None:
        required = set(self.workflow_schema["required"])
        self.assertIn("required_checks", required)
        required_checks = self.workflow_schema["properties"]["required_checks"]
        self.assertEqual(self.workflow["required_checks"], required_checks["const"])

    def test_declaration_v7_supports_core_and_web_variants(self) -> None:
        self.assertEqual(7, self.repository_schema["properties"]["version"]["const"])
        alternatives = self.repository_schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        for alternative in alternatives:
            properties = alternative["properties"]
            self.assertEqual("v3", properties["ticket-specification"]["const"])
            self.assertEqual("v6", properties["development-workflow"]["const"])
            self.assertEqual("v1", properties["repository-documentation"]["const"])
            self.assertEqual("v1", properties["technology-baseline"]["const"])
        self.assertNotIn("web-application-baseline", alternatives[0]["properties"])
        self.assertEqual(
            "v1",
            alternatives[1]["properties"]["web-application-baseline"]["const"],
        )
        self.assertEqual(
            "v1",
            alternatives[1]["properties"]["deployment-environments"]["const"],
        )

    def test_compatibility_v6_preserves_v5_and_adds_exact_v7_pairings(self) -> None:
        previous = self.compatibility_v5["pairings"]
        current = self.compatibility["pairings"]
        self.assertEqual(previous, current[: len(previous)])
        v7 = [item for item in current if item["declaration_schema"] == "v7"]
        self.assertEqual(2, len(v7))
        for pairing in v7:
            self.assertEqual("v3", pairing["ticket_specification"])
            self.assertEqual("v6", pairing["development_workflow"])
            self.assertEqual("v1", pairing["repository_documentation"])
            self.assertEqual("v1", pairing["technology_baseline"])
            self.assertEqual("supported", pairing["status"])
        self.assertEqual("reject", self.compatibility["unsupported_pairing_policy"])

    def test_v7_reference_declarations_are_consistent(self) -> None:
        expectations = (
            ("repository-standards-v7.single.yml", "single", False),
            ("repository-standards-v7.integration.yml", "integration", False),
            ("repository-standards-v7.web.single.yml", "single", True),
            ("repository-standards-v7.web.integration.yml", "integration", True),
        )
        for name, model, web in expectations:
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("7", values["version"])
                self.assertEqual("v3", values["standards.ticket-specification"])
                self.assertEqual("v6", values["standards.development-workflow"])
                self.assertEqual("v1", values["standards.repository-documentation"])
                self.assertEqual("v1", values["standards.technology-baseline"])
                self.assertEqual(model, values["branching.model"])
                if web:
                    self.assertEqual(
                        "v1", values["standards.web-application-baseline"]
                    )
                    self.assertEqual(
                        "v1", values["standards.deployment-environments"]
                    )

    def test_v6_generated_ai_adapter_is_current(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "render_development_workflow_assets_v6.py"),
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_previously_published_v5_v6_assets_are_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))


if __name__ == "__main__":
    unittest.main()
