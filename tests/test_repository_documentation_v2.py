from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTATION_ROOT = ROOT / "standards" / "repository-documentation"
V1_STANDARD = DOCUMENTATION_ROOT / "v1" / "standard.md"
V2_STANDARD = DOCUMENTATION_ROOT / "v2" / "standard.md"
V2_SCHEMA = ROOT / "schemas" / "repository-documentation-v2.schema.json"
V8_SCHEMA = ROOT / "schemas" / "repository-standards-v8.schema.json"
COMPATIBILITY = (
    ROOT / "profiles" / "repository-standards-compatibility-v7.json"
)
PUBLIC_CORE = ROOT / "public" / "public-core-v1.json"

V1_STANDARD_BLOB = "3e2db130f0c3ac89f2207313a272268678e85a76"

DOCUMENT_TYPES = (
    "Tutorial",
    "How-to Guide",
    "Reference",
    "Explanation",
    "Architecture",
    "Decision / ADR",
    "Operations / Runbook",
    "Verification / Evidence",
    "Index / Navigation",
)

GUIDANCE_ROOT = ROOT / "docs" / "repository-documentation"
GUIDANCE_FILES = (
    GUIDANCE_ROOT / "index.md",
    GUIDANCE_ROOT / "document-types.md",
    GUIDANCE_ROOT / "methods-and-models.md",
)

V8_REFERENCES = (
    "reference/repository-standards-v8.single.yml",
    "reference/repository-standards-v8.integration.yml",
    "reference/repository-standards-v8.web.single.yml",
    "reference/repository-standards-v8.web.integration.yml",
)

PUBLIC_V2_FILES = {
    "standards/repository-documentation/v2/standard.md",
    "schemas/repository-documentation-v2.schema.json",
    "schemas/repository-standards-v8.schema.json",
    "profiles/repository-standards-compatibility-v7.json",
    "docs/repository-documentation/index.md",
    "docs/repository-documentation/document-types.md",
    "docs/repository-documentation/methods-and-models.md",
    "docs/repository-documentation-v2-migration.md",
    "docs/repository-contract-v8-migration.md",
    "tests/test_repository_documentation_v2.py",
    *V8_REFERENCES,
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()


def standard_properties(
    schema: dict[str, object],
) -> list[dict[str, object]]:
    standards = schema["properties"]["standards"]
    return [variant["properties"] for variant in standards["oneOf"]]


def reference_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not raw_line.startswith(" ") and line.endswith(":"):
            section = line[:-1]
            continue
        if ":" not in line:
            continue
        parts = line.split(":", 1)
        key, value = (part.strip().strip('"') for part in parts)
        values[f"{section}.{key}" if section else key] = value
    return values


class RepositoryDocumentationV2Test(unittest.TestCase):
    def test_v1_standard_is_byte_immutable(self) -> None:
        self.assertEqual(V1_STANDARD_BLOB, git_blob_sha(V1_STANDARD))

    def test_v2_standard_has_all_document_types(self) -> None:
        text = V2_STANDARD.read_text(encoding="utf-8")
        self.assertIn("BCP 14", text)
        for document_type in DOCUMENT_TYPES:
            self.assertIn(document_type, text)
        current_evidence = (
            "Verification Evidence MUST NOT be represented as permanently current"
        )
        self.assertIn(current_evidence, text)
        self.assertIn("Historical evidence MAY be retained indefinitely", text)
        self.assertIn("A very short Evidence document MAY be complete", text)

    def test_v2_rejects_length_as_quality_proxy(self) -> None:
        text = V2_STANDARD.read_text(encoding="utf-8")
        self.assertIn("MUST NOT depend on a minimum word count", text)
        self.assertIn("Validation MUST NOT use minimum word counts", text)
        self.assertIn("information task", text)

    def test_v2_schema_selects_only_v2_rulesets(self) -> None:
        schema = json.loads(V2_SCHEMA.read_text(encoding="utf-8"))
        documentation = schema["properties"]["documentation"]["properties"]
        standard_version = documentation["standard_version"]["const"]
        ruleset_pattern = documentation["ruleset_version"]["pattern"]
        self.assertEqual(2, standard_version)
        self.assertEqual("^2\\.[0-9]+\\.[0-9]+$", ruleset_pattern)

    def test_v8_schema_selects_documentation_v2(self) -> None:
        schema = json.loads(V8_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(8, schema["properties"]["version"]["const"])
        for properties in standard_properties(schema):
            ticket = properties["ticket-specification"]["const"]
            workflow = properties["development-workflow"]["const"]
            documentation = properties["repository-documentation"]["const"]
            technology = properties["technology-baseline"]["const"]
            self.assertEqual("v3", ticket)
            self.assertEqual("v7", workflow)
            self.assertEqual("v2", documentation)
            self.assertEqual("v1", technology)

    def test_compatibility_is_additive_and_fail_closed(self) -> None:
        profile = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
        self.assertEqual("7.0.0", profile["version"])
        self.assertEqual("reject", profile["unsupported_pairing_policy"])
        pairings = profile["pairings"]
        v7_pairings = [
            item for item in pairings if item["declaration_schema"] == "v7"
        ]
        v8_pairings = [
            item for item in pairings if item["declaration_schema"] == "v8"
        ]
        self.assertEqual(2, len(v7_pairings))
        self.assertEqual(2, len(v8_pairings))
        self.assertTrue(
            all(item["repository_documentation"] == "v1" for item in v7_pairings)
        )
        self.assertTrue(
            all(item["repository_documentation"] == "v2" for item in v8_pairings)
        )
        self.assertTrue(
            all(item["development_workflow"] == "v6" for item in v7_pairings)
        )
        self.assertTrue(
            all(item["development_workflow"] == "v7" for item in v8_pairings)
        )

    def test_v8_reference_declarations_select_v2(self) -> None:
        for relative_path in V8_REFERENCES:
            values = reference_values(ROOT / relative_path)
            self.assertEqual("8", values["version"])
            self.assertEqual("v3", values["standards.ticket-specification"])
            self.assertEqual("v7", values["standards.development-workflow"])
            documentation = values["standards.repository-documentation"]
            self.assertEqual("v2", documentation)
            self.assertEqual("v1", values["standards.technology-baseline"])

    def test_guidance_is_non_normative_and_links_to_standard(self) -> None:
        standard_path = "standards/repository-documentation/v2/standard.md"
        for path in GUIDANCE_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text.lower(), r"non[- ]normative")
            self.assertIn(standard_path, text)

    def test_methods_guidance_covers_models_and_primary_sources(self) -> None:
        text = GUIDANCE_FILES[2].read_text(encoding="utf-8")
        for term in ("Diátaxis", "arc42-lite", "C4", "MADR"):
            self.assertIn(term, text)
        for url in (
            "https://diataxis.fr/",
            "https://arc42.org/",
            "https://docs.arc42.org/home/",
            "https://c4model.com/",
            "https://adr.github.io/madr/",
        ):
            self.assertIn(url, text)

    def test_new_documentation_links_resolve_locally(self) -> None:
        files = (
            *GUIDANCE_FILES,
            ROOT / "docs" / "repository-documentation-v2-migration.md",
            ROOT / "docs" / "repository-contract-v8-migration.md",
        )
        pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        for path in files:
            text = path.read_text(encoding="utf-8")
            for target in pattern.findall(text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                relative = target.split("#", 1)[0]
                if not relative:
                    continue
                exists = (path.parent / relative).resolve().exists()
                self.assertTrue(exists, f"broken link in {path}: {target}")

    def test_public_core_contains_v2_contract_and_guidance(self) -> None:
        manifest = json.loads(PUBLIC_CORE.read_text(encoding="utf-8"))
        files = set(manifest["files"])
        missing = PUBLIC_V2_FILES - files
        self.assertTrue(PUBLIC_V2_FILES.issubset(files), missing)


if __name__ == "__main__":
    unittest.main()
