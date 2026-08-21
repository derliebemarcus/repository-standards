from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_BLOB_SHAS = {
    "standards/development-workflow/v2/standard.md":
        "4b830a45f048e1384d28cca7afe311b00784494d",
    "schemas/repository-standards-v1.schema.json":
        "68ee6ff2a5e8cdf7fde90cb28f85ed5c6e058b35",
    "reference/repository-standards.single.yml":
        "fa0f4828ab9c61d71439596f68f3ffc40128786c",
    "reference/repository-standards.integration.yml":
        "c1196db91d1009b16e2eb5732a62194308d7b5b1",
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def schema_pair(schema: dict[str, object]) -> tuple[int, str, str, str]:
    standards = schema["properties"]["standards"]["properties"]
    return (
        schema["properties"]["version"]["const"],
        standards["ticket-specification"]["const"],
        standards["development-workflow"]["const"],
        standards["repository-documentation"]["const"],
    )


def compatibility_pairs(profile: dict[str, object]) -> set[tuple[str, str, str, str]]:
    return {
        (
            pairing["declaration_schema"],
            pairing["ticket_specification"],
            pairing["development_workflow"],
            pairing["repository_documentation"],
        )
        for pairing in profile["pairings"]
    }


def pairing_supported(
    profile: dict[str, object],
    declaration: str,
    ticket: str,
    workflow: str,
    documentation: str,
) -> bool:
    return (declaration, ticket, workflow, documentation) in compatibility_pairs(profile)


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


class RepositoryAdoptionContractV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema_v1 = json.loads(
            (ROOT / "schemas" / "repository-standards-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.schema_v2 = json.loads(
            (ROOT / "schemas" / "repository-standards-v2.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.compatibility = json.loads(
            (
                ROOT
                / "profiles"
                / "repository-standards-compatibility-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.workflow_v3 = (
            ROOT
            / "standards"
            / "development-workflow"
            / "v3"
            / "standard.md"
        ).read_text(encoding="utf-8")

    def test_published_legacy_contracts_are_byte_immutable(self) -> None:
        for relative_path, expected_sha in LEGACY_BLOB_SHAS.items():
            with self.subTest(path=relative_path):
                actual_sha = git_blob_sha(ROOT / relative_path)
                self.assertEqual(expected_sha, actual_sha)

    def test_declaration_schemas_encode_supported_pairings(self) -> None:
        self.assertEqual((1, "v1", "v2", "v1"), schema_pair(self.schema_v1))
        self.assertEqual((2, "v2", "v3", "v1"), schema_pair(self.schema_v2))

    def test_compatibility_profile_matches_schema_pairings(self) -> None:
        self.assertEqual(
            {
                ("v1", "v1", "v2", "v1"),
                ("v2", "v2", "v3", "v1"),
            },
            compatibility_pairs(self.compatibility),
        )
        self.assertEqual(
            "reject",
            self.compatibility["unsupported_pairing_policy"],
        )

    def test_unsupported_version_pairings_are_rejected(self) -> None:
        invalid = (
            ("v1", "v2", "v2", "v1"),
            ("v1", "v2", "v3", "v1"),
            ("v2", "v1", "v3", "v1"),
            ("v2", "v2", "v2", "v1"),
        )
        for pairing in invalid:
            with self.subTest(pairing=pairing):
                self.assertFalse(pairing_supported(self.compatibility, *pairing))

    def test_v2_reference_declarations_match_new_pairing(self) -> None:
        for name, model in (
            ("repository-standards-v2.single.yml", "single"),
            ("repository-standards-v2.integration.yml", "integration"),
        ):
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("2", values["version"])
                self.assertEqual(
                    "v2",
                    values["standards.ticket-specification"],
                )
                self.assertEqual(
                    "v3",
                    values["standards.development-workflow"],
                )
                self.assertEqual(
                    "v1",
                    values["standards.repository-documentation"],
                )
                self.assertEqual(model, values["branching.model"])
                self.assertEqual(
                    "^(main|develop|PR-[0-9]+)$",
                    values["branching.multibranch_filter"],
                )

    def test_workflow_v3_adopts_ticket_v2_without_branching_drift(self) -> None:
        normalized = " ".join(self.workflow_v3.split())
        self.assertIn(
            "MUST also adopt Ticket Specification v2",
            normalized,
        )
        self.assertIn("Repository Standards declaration schema v2", normalized)
        self.assertIn("^(main|develop|PR-[0-9]+)$", normalized)
        self.assertIn("state=closed", normalized)
        self.assertIn("Status/Done", normalized)
        self.assertIn("manually created and manually merged", normalized)
        self.assertIn("manual `main` builds", normalized)
        self.assertIn("Unsupported pairings MUST fail declaration validation", normalized)


if __name__ == "__main__":
    unittest.main()
