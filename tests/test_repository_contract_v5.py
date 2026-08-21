from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_BLOBS = {
    "standards/development-workflow/v4/standard.md":
        "9fe544bc476543702bc4145fd33b8ac4568a8a37",
    "profiles/development-workflow-v4.json":
        "190e32a76dcee12e0fcbe22ffd8f44393f1a56a9",
    "schemas/development-workflow-v4.schema.json":
        "6c237aa28ed62747651a36aa81b177be1db690e1",
    "reference/ai/development-workflow-v4.md":
        "a7115036bf9a03ba8135ebbfe0d1d193f3197969",
    "schemas/repository-standards-v4.schema.json":
        "30171324e3a66fc53cb0cd9e1d7a277a5c04acef",
    "reference/repository-standards-v4.single.yml":
        "1823297a445ee3ca0a2e5fa1481c8ed5f76bc9c3",
    "reference/repository-standards-v4.integration.yml":
        "eb12ce961b1a1a4602967fa1a043efec44f42dd3",
    "reference/repository-standards-v4.web.single.yml":
        "ab378567fd9558ecf9e3300b8a31519993bf3824",
    "reference/repository-standards-v4.web.integration.yml":
        "085c8bc13fb91e488f137d0208a3c330ad1bf630",
    "profiles/repository-standards-compatibility-v3.json":
        "229dc6f7618f5597e4662c56d5f28347abaaa48a",
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


class RepositoryContractV5Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = json.loads(
            (ROOT / "profiles" / "development-workflow-v5.json").read_text(
                encoding="utf-8"
            )
        )
        cls.workflow_schema = json.loads(
            (ROOT / "schemas" / "development-workflow-v5.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.repository_schema = json.loads(
            (ROOT / "schemas" / "repository-standards-v5.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.compatibility = json.loads(
            (
                ROOT
                / "profiles"
                / "repository-standards-compatibility-v4.json"
            ).read_text(encoding="utf-8")
        )

    def test_v5_workflow_couples_to_ticket_v3_and_declaration_v5(self) -> None:
        self.assertEqual("5.0.0", self.workflow["version"])
        self.assertEqual("v5", self.workflow["requires"]["declaration_schema"])
        self.assertEqual("v3", self.workflow["requires"]["ticket_specification"])
        self.assertEqual(
            "profiles/ticket-specification-v3.json#/branch_prefixes",
            self.workflow["branch_naming"]["prefix_source"],
        )
        schema_text = json.dumps(self.workflow_schema, sort_keys=True)
        self.assertIn('"const": "v5"', schema_text)
        self.assertIn('"const": "v3"', schema_text)

    def test_v5_preserves_v4_workflow_behavior_except_version_coupling(self) -> None:
        v4 = json.loads(
            (ROOT / "profiles" / "development-workflow-v4.json").read_text(
                encoding="utf-8"
            )
        )
        for key in (
            "pull_request_naming",
            "pre_write_validation",
            "exemptions",
            "post_write_validation",
            "branching",
        ):
            with self.subTest(key=key):
                self.assertEqual(v4[key], self.workflow[key])
        v4_branch = dict(v4["branch_naming"])
        v5_branch = dict(self.workflow["branch_naming"])
        v4_branch.pop("prefix_source")
        v5_branch.pop("prefix_source")
        self.assertEqual(v4_branch, v5_branch)

    def test_declaration_v5_supports_core_and_web_pairings(self) -> None:
        self.assertEqual(5, self.repository_schema["properties"]["version"]["const"])
        alternatives = self.repository_schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        for alternative in alternatives:
            properties = alternative["properties"]
            self.assertEqual("v3", properties["ticket-specification"]["const"])
            self.assertEqual("v5", properties["development-workflow"]["const"])
            self.assertEqual("v1", properties["repository-documentation"]["const"])
        self.assertNotIn("web-application-baseline", alternatives[0]["properties"])
        self.assertEqual(
            "v1",
            alternatives[1]["properties"]["web-application-baseline"]["const"],
        )
        self.assertEqual(
            "v1",
            alternatives[1]["properties"]["deployment-environments"]["const"],
        )

    def test_compatibility_profile_adds_exact_v5_pairings(self) -> None:
        pairings = [
            item
            for item in self.compatibility["pairings"]
            if item["declaration_schema"] == "v5"
        ]
        self.assertEqual(2, len(pairings))
        for pairing in pairings:
            self.assertEqual("v3", pairing["ticket_specification"])
            self.assertEqual("v5", pairing["development_workflow"])
            self.assertEqual("supported", pairing["status"])
        self.assertEqual(
            "reject",
            self.compatibility["unsupported_pairing_policy"],
        )

    def test_v5_reference_declarations_are_consistent(self) -> None:
        expectations = (
            ("repository-standards-v5.single.yml", "single", False),
            ("repository-standards-v5.integration.yml", "integration", False),
            ("repository-standards-v5.web.single.yml", "single", True),
            ("repository-standards-v5.web.integration.yml", "integration", True),
        )
        for name, model, web in expectations:
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("5", values["version"])
                self.assertEqual("v3", values["standards.ticket-specification"])
                self.assertEqual("v5", values["standards.development-workflow"])
                self.assertEqual("v1", values["standards.repository-documentation"])
                self.assertEqual(model, values["branching.model"])
                if web:
                    self.assertEqual(
                        "v1", values["standards.web-application-baseline"]
                    )
                    self.assertEqual(
                        "v1", values["standards.deployment-environments"]
                    )

    def test_v5_workflow_generated_adapter_is_current(self) -> None:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "render_development_workflow_assets_v5.py"),
                "--check",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_released_v4_assets_and_compatibility_are_byte_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))


if __name__ == "__main__":
    unittest.main()
