from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_V8_BLOBS = {
    "standards/ticket-specification/v3/standard.md":
        "dfe3c53d732daef276fa3d9d08c69a0597bce95c",
    "profiles/ticket-specification-v3.json":
        "c656c616aeae6427fb7abfc93fc992f161741a85",
    "schemas/ticket-specification-v3.schema.json":
        "1213c83b79dc9adda1947e75983760aca40e0f5b",
    "reference/ai/ticket-authoring-v3.md":
        "0dfac573d61d0fdd37e6eaf7d5cd01e58324dad8",
    "standards/development-workflow/v7/standard.md":
        "d423c36cdc1e703df11e5f30d43ab29e1b4f55e5",
    "profiles/development-workflow-v7.json":
        "b031dcbf718f9634cc6b99948d6b1f0713fc2da9",
    "schemas/development-workflow-v7.schema.json":
        "464cc5100aee7d41d31210ab1c8ee25187dea7b2",
    "reference/ai/development-workflow-v7.md":
        "4f1d06df9e5c0327bc9c0e8b35d0e4dd80630510",
    "standards/web-application-baseline/v1/standard.md":
        "c7805692f65005e9d9cd7d763789a22f7d22e2ce",
    "profiles/web-application-baseline-v1.json":
        "35addb52c8be25903abe5a2b67e7df9261bd3414",
    "schemas/repository-standards-v8.schema.json":
        "260089ff3e1f45043ec673f02f06c9923107fe8e",
    "profiles/repository-standards-compatibility-v7.json":
        "5c1f33e2084ba4c13a9290d9b1b674934120fa1a",
    "reference/repository-standards-v8.single.yml":
        "fcd88d2c6e63b6c5622a2890192b3c415b55364c",
    "reference/repository-standards-v8.web.single.yml":
        "a939007ef43e57be0efe203844a77cdb5a61d8c5",
}


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


class RepositoryContractV9Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (
                ROOT / "schemas" / "repository-standards-v9.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.compatibility_v7 = json.loads(
            (
                ROOT / "profiles" / "repository-standards-compatibility-v7.json"
            ).read_text(encoding="utf-8")
        )
        cls.compatibility_v8 = json.loads(
            (
                ROOT / "profiles" / "repository-standards-compatibility-v8.json"
            ).read_text(encoding="utf-8")
        )
        cls.workflow = json.loads(
            (
                ROOT / "profiles" / "development-workflow-v8.json"
            ).read_text(encoding="utf-8")
        )

    def test_v9_schema_has_exact_core_and_web_pairings(self) -> None:
        self.assertEqual(9, self.schema["properties"]["version"]["const"])
        alternatives = self.schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        for alternative in alternatives:
            properties = alternative["properties"]
            self.assertEqual("v4", properties["ticket-specification"]["const"])
            self.assertEqual("v8", properties["development-workflow"]["const"])
            self.assertEqual("v2", properties["repository-documentation"]["const"])
            self.assertEqual("v1", properties["technology-baseline"]["const"])
            self.assertEqual("v1", properties["contract-first-delivery"]["const"])
        web = alternatives[1]["properties"]
        self.assertEqual("v2", web["web-application-baseline"]["const"])
        self.assertEqual("v1", web["deployment-environments"]["const"])

    def test_v9_references_cover_core_and_web_branching_models(self) -> None:
        expectations = (
            ("repository-standards-v9.single.yml", "single", False),
            ("repository-standards-v9.integration.yml", "integration", False),
            ("repository-standards-v9.web.single.yml", "single", True),
            ("repository-standards-v9.web.integration.yml", "integration", True),
        )
        for name, model, web in expectations:
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("9", values["version"])
                self.assertEqual("v4", values["standards.ticket-specification"])
                self.assertEqual("v8", values["standards.development-workflow"])
                self.assertEqual("v2", values["standards.repository-documentation"])
                self.assertEqual("v1", values["standards.contract-first-delivery"])
                self.assertEqual(model, values["branching.model"])
                if web:
                    self.assertEqual(
                        "v2",
                        values["standards.web-application-baseline"],
                    )
                    self.assertEqual(
                        "v1",
                        values["standards.deployment-environments"],
                    )

    def test_compatibility_v8_preserves_prior_pairings_and_adds_v9(self) -> None:
        prior = self.compatibility_v7["pairings"]
        current = self.compatibility_v8["pairings"]
        self.assertEqual(prior, current[: len(prior)])
        v9 = [item for item in current if item["declaration_schema"] == "v9"]
        self.assertEqual(2, len(v9))
        for pairing in v9:
            self.assertEqual("v4", pairing["ticket_specification"])
            self.assertEqual("v8", pairing["development_workflow"])
            self.assertEqual("v2", pairing["repository_documentation"])
            self.assertEqual("v1", pairing["contract_first_delivery"])
            self.assertEqual("supported", pairing["status"])
        self.assertEqual(
            "fail-closed-until-compatible-enforcement-is-qualified",
            self.compatibility_v8["v9_activation_policy"],
        )

    def test_workflow_v8_exposes_three_logical_contract_gates(self) -> None:
        self.assertEqual(
            [
                "contract-graph",
                "test-contract-qualification",
                "contract-conformance",
            ],
            self.workflow["contract_first"]["logical_gates"],
        )
        self.assertEqual(
            "Status/Ready",
            self.workflow["contract_first"]["freeze"]["status"],
        )
        self.assertTrue(
            self.workflow["contract_first"]["invalidation"]
            ["historical_evidence_preserved"]
        )

    def test_v8_assets_remain_byte_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_V8_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))

    def test_ai_adapters_prohibit_testing_to_implementation(self) -> None:
        ticket = (
            ROOT / "reference" / "ai" / "ticket-authoring-v4.md"
        ).read_text(encoding="utf-8")
        workflow = (
            ROOT / "reference" / "ai" / "development-workflow-v8.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join((ticket + " " + workflow).split())
        self.assertIn("Status/Ready", normalized)
        self.assertIn("controlled negative", normalized)
        self.assertIn("baseline", normalized)
        self.assertIn("tolerance", normalized)
        self.assertIn("requalification", normalized)


if __name__ == "__main__":
    unittest.main()
