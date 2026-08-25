from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6_STANDARD = ROOT / "standards" / "development-workflow" / "v6" / "standard.md"
V7_STANDARD = ROOT / "standards" / "development-workflow" / "v7" / "standard.md"
V7_PROFILE = ROOT / "profiles" / "development-workflow-v7.json"
V7_SCHEMA = ROOT / "schemas" / "development-workflow-v7.schema.json"
V8_SCHEMA = ROOT / "schemas" / "repository-standards-v8.schema.json"
COMPATIBILITY = ROOT / "profiles" / "repository-standards-compatibility-v7.json"
PUBLIC_CORE = ROOT / "public" / "public-core-v1.json"
AI_ADAPTER = ROOT / "reference" / "ai" / "development-workflow-v7.md"
RENDERER = ROOT / "tools" / "render_development_workflow_assets_v7.py"

V6_STANDARD_BLOB = "46139bafb9502ed1157a60b8a4f8695df2b45154"
HEADING = "# Superseded by / See other"
LABEL = "Status/Superseded"

V8_REFERENCES = (
    ROOT / "reference" / "repository-standards-v8.single.yml",
    ROOT / "reference" / "repository-standards-v8.integration.yml",
    ROOT / "reference" / "repository-standards-v8.web.single.yml",
    ROOT / "reference" / "repository-standards-v8.web.integration.yml",
)

PUBLIC_V7_FILES = {
    "standards/development-workflow/v7/standard.md",
    "profiles/development-workflow-v7.json",
    "schemas/development-workflow-v7.schema.json",
    "reference/ai/development-workflow-v7.md",
    "tools/render_development_workflow_assets_v7.py",
    "tests/test_pull_request_supersession.py",
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()


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
        key, value = (part.strip().strip('"') for part in line.split(":", 1))
        values[f"{section}.{key}" if section else key] = value
    return values


class PullRequestSupersessionContractTest(unittest.TestCase):
    def test_released_v6_standard_is_byte_immutable(self) -> None:
        self.assertEqual(V6_STANDARD_BLOB, git_blob_sha(V6_STANDARD))

    def test_v7_standard_defines_exact_supersession_contract(self) -> None:
        text = V7_STANDARD.read_text(encoding="utf-8")
        self.assertIn(HEADING, text)
        self.assertIn(LABEL, text)
        self.assertIn("MUST be the first content", text)
        self.assertIn("unordered Markdown list", text)
        self.assertIn("at least one pull-request reference", text)
        self.assertIn("Each list item MUST contain exactly one", text)
        self.assertIn("Explanatory prose MUST NOT appear", text)
        self.assertIn("MUST NOT be merged", text)
        self.assertIn("self-reference", text)

    def test_v7_profile_encodes_body_label_coherence(self) -> None:
        profile = json.loads(V7_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual("7.0.0", profile["version"])
        self.assertEqual("v8", profile["requires"]["declaration_schema"])
        supersession = profile["pull_request_supersession"]
        self.assertEqual(HEADING, supersession["heading"])
        self.assertEqual("first-content", supersession["position"])
        self.assertEqual("unordered", supersession["successor_list"]["style"])
        self.assertEqual(1, supersession["successor_list"]["minimum_items"])
        self.assertTrue(
            supersession["successor_list"]["one_pull_request_reference_per_item"]
        )
        self.assertFalse(supersession["successor_list"]["prose_allowed"])
        self.assertEqual(LABEL, supersession["required_label"])
        self.assertTrue(supersession["label_and_body_marker_must_match"])
        self.assertFalse(supersession["merge_allowed"])
        self.assertFalse(supersession["self_reference_allowed"])

    def test_v7_schema_matches_profile_contract(self) -> None:
        schema = json.loads(V7_SCHEMA.read_text(encoding="utf-8"))
        supersession = schema["properties"]["pull_request_supersession"]["const"]
        self.assertEqual(HEADING, supersession["heading"])
        self.assertEqual(LABEL, supersession["required_label"])
        self.assertFalse(supersession["merge_allowed"])
        self.assertFalse(supersession["self_reference_allowed"])

    def test_declaration_v8_selects_workflow_v7(self) -> None:
        schema = json.loads(V8_SCHEMA.read_text(encoding="utf-8"))
        variants = schema["properties"]["standards"]["oneOf"]
        self.assertTrue(variants)
        for variant in variants:
            workflow = variant["properties"]["development-workflow"]["const"]
            self.assertEqual("v7", workflow)

    def test_v8_references_select_workflow_v7(self) -> None:
        for path in V8_REFERENCES:
            values = reference_values(path)
            self.assertEqual("8", values["version"])
            self.assertEqual("v7", values["standards.development-workflow"])

    def test_v8_compatibility_pairings_select_workflow_v7(self) -> None:
        profile = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
        v8_pairings = [
            item for item in profile["pairings"]
            if item["declaration_schema"] == "v8"
        ]
        self.assertEqual(2, len(v8_pairings))
        self.assertTrue(
            all(item["development_workflow"] == "v7" for item in v8_pairings)
        )
        v7_pairings = [
            item for item in profile["pairings"]
            if item["declaration_schema"] == "v7"
        ]
        self.assertTrue(
            all(item["development_workflow"] == "v6" for item in v7_pairings)
        )

    def test_public_core_exports_v7_contract(self) -> None:
        manifest = json.loads(PUBLIC_CORE.read_text(encoding="utf-8"))
        files = set(manifest["files"])
        missing = PUBLIC_V7_FILES - files
        self.assertFalse(missing, missing)

    def test_generated_adapter_contains_supersession_contract(self) -> None:
        text = AI_ADAPTER.read_text(encoding="utf-8")
        self.assertIn(HEADING, text)
        self.assertIn(LABEL, text)
        self.assertIn("MUST NOT be merged", text)
        self.assertTrue(RENDERER.is_file())


if __name__ == "__main__":
    unittest.main()
