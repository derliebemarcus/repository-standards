from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_BLOB_SHAS = {
    "profiles/repository-standards-compatibility-v1.json":
        "eb5a74243242aae591061773bfae93cf979e8b34",
    "schemas/repository-standards-v2.schema.json":
        "2759ac6477cf1361e29d7f659f068263d4abf3ad",
    "reference/repository-standards-v2.single.yml":
        "1ca54d7f10e86d417455bfc67e84dd0778eb2108",
    "reference/repository-standards-v2.integration.yml":
        "f075927450078656aa5959de5b7ab7fe34c69252",
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


class WebApplicationAndDeploymentContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.web = load_json("profiles/web-application-baseline-v1.json")
        cls.deployment = load_json("profiles/deployment-environments-v1.json")
        cls.provenance = load_json("schemas/artifact-provenance-v1.schema.json")
        cls.declaration_v3 = load_json(
            "schemas/repository-standards-v3.schema.json"
        )
        cls.compatibility_v2 = load_json(
            "profiles/repository-standards-compatibility-v2.json"
        )

    def test_published_v1_v2_contract_assets_are_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_BLOB_SHAS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(
                    expected_sha,
                    git_blob_sha(ROOT / relative_path),
                )

    def test_required_pages_and_public_provenance_matrix(self) -> None:
        routes = {
            item["route"]
            for item in self.web["required_pages"]
        }
        self.assertEqual(
            {"/impressum", "/datenschutz", "/barrierefreiheit"},
            routes,
        )

        states = self.web["artifact_release_states"]
        self.assertEqual(
            ["commit", "build_number", "build_time"],
            states["non-release"]["public_footer_fields"],
        )
        self.assertEqual(
            ["release_version", "build_number", "build_time"],
            states["release-candidate"]["public_footer_fields"],
        )
        self.assertEqual(
            ["release_version"],
            states["release"]["public_footer_fields"],
        )

    def test_design_and_accessibility_requirements_are_machine_readable(self) -> None:
        design = self.web["design"]
        self.assertTrue(design["same_application_shell"])
        self.assertTrue(design["honor_design_system_decision"])
        self.assertTrue(design["same_accessibility_gates"])
        self.assertFalse(design["standalone_legal_theme_allowed"])

        topics = set(self.web["accessibility_statement"]["required_topics"])
        self.assertIn("conformance-status", topics)
        self.assertIn("known-limitations", topics)
        self.assertIn("feedback-contact", topics)
        self.assertIn("prepared-or-reviewed-date", topics)
        self.assertTrue(self.web["validation"]["blocking"])
        self.assertFalse(self.web["validation"]["legal_compliance_claim"])

    def test_deployment_dimensions_and_branch_mappings_are_independent(self) -> None:
        self.assertEqual(
            [
                "source",
                "artifact-release-state",
                "runtime-environment",
            ],
            self.deployment["dimensions"],
        )
        self.assertEqual(
            {"single": "main", "integration": "develop"},
            self.deployment["branch_to_dev"],
        )
        self.assertFalse(self.deployment["preview"]["canonical_environment"])
        self.assertFalse(
            self.deployment["promotion"]["environment_changes_release_state"]
        )
        self.assertFalse(
            self.deployment["promotion"]["rebuild_application_content"]
        )

    def test_prod_requires_immutable_final_release_artifact(self) -> None:
        prod = self.deployment["environments"]["PROD"]
        self.assertEqual(["release"], prod["accepted_release_states"])
        self.assertTrue(prod["immutable_release_artifact_required"])
        self.assertTrue(
            self.deployment["validation"]["block_unreleased_prod"]
        )
        self.assertTrue(
            self.deployment["validation"]["block_ambiguous_prod_artifact"]
        )

    def test_artifact_provenance_schema_encodes_release_states(self) -> None:
        properties = self.provenance["properties"]
        self.assertEqual(
            ["non-release", "release-candidate", "release"],
            properties["releaseState"]["enum"],
        )
        self.assertEqual(
            "^[0-9a-f]{7,40}$",
            properties["commit"]["pattern"],
        )
        self.assertEqual("date-time", properties["buildTime"]["format"])

        branches = self.provenance["allOf"]
        conditions = {
            branch["if"]["properties"]["releaseState"]["const"]: branch
            for branch in branches
        }
        self.assertIn("non-release", conditions)
        self.assertIn("release-candidate", conditions)
        self.assertIn("release", conditions)
        self.assertIn(
            "releaseVersion",
            conditions["release-candidate"]["then"]["required"],
        )
        self.assertIn(
            "releaseVersion",
            conditions["release"]["then"]["required"],
        )

    def test_declaration_v3_requires_both_new_contracts(self) -> None:
        standards = self.declaration_v3["properties"]["standards"]
        self.assertEqual(
            {
                "ticket-specification",
                "development-workflow",
                "repository-documentation",
                "web-application-baseline",
                "deployment-environments",
            },
            set(standards["required"]),
        )
        properties = standards["properties"]
        self.assertEqual("v1", properties["web-application-baseline"]["const"])
        self.assertEqual("v1", properties["deployment-environments"]["const"])
        self.assertFalse(standards["additionalProperties"])

    def test_compatibility_v2_adds_v3_and_preserves_legacy_sets(self) -> None:
        pairings = {
            item["declaration_schema"]: item
            for item in self.compatibility_v2["pairings"]
        }
        self.assertEqual({"v1", "v2", "v3"}, set(pairings))
        self.assertEqual("v1", pairings["v1"]["ticket_specification"])
        self.assertEqual("v2", pairings["v2"]["ticket_specification"])
        self.assertEqual("v2", pairings["v3"]["ticket_specification"])
        self.assertEqual("v1", pairings["v3"]["web_application_baseline"])
        self.assertEqual("v1", pairings["v3"]["deployment_environments"])
        self.assertEqual(
            "reject",
            self.compatibility_v2["unsupported_pairing_policy"],
        )

    def test_v3_reference_declarations_match_branch_models(self) -> None:
        for filename, model, default_branch in (
            ("repository-standards-v3.single.yml", "single", "main"),
            (
                "repository-standards-v3.integration.yml",
                "integration",
                "develop",
            ),
        ):
            with self.subTest(filename=filename):
                values = declaration_values(ROOT / "reference" / filename)
                self.assertEqual("3", values["version"])
                self.assertEqual(
                    "v1",
                    values["standards.web-application-baseline"],
                )
                self.assertEqual(
                    "v1",
                    values["standards.deployment-environments"],
                )
                self.assertEqual(model, values["branching.model"])
                self.assertEqual(
                    default_branch,
                    values["branching.default_branch"],
                )
                self.assertEqual(
                    "^(main|develop|PR-[0-9]+)$",
                    values["branching.multibranch_filter"],
                )


if __name__ == "__main__":
    unittest.main()
