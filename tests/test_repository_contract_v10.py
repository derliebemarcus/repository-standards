from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_V9_WEB_BLOBS = {
    "standards/web-application-baseline/v2/standard.md":
        "d2f20cc847142e48681d58028a36f68fe25025ab",
    "profiles/web-application-baseline-v2.json":
        "a1c3988801b569f688a645df897e72b8ecebda18",
    "schemas/repository-standards-v9.schema.json":
        "90a3466e8157df3de625e3dd904fa163fd93e52d",
    "profiles/repository-standards-compatibility-v8.json":
        "909790cc11d3be0826f65b77b743984bc2cb639a",
    "reference/repository-standards-v9.single.yml":
        "191a5843566da32ad52fb0ae5db5888991a60b0c",
    "reference/repository-standards-v9.integration.yml":
        "f3420e15553daa90630b378f7994c80992e7a7ba",
    "reference/repository-standards-v9.web.single.yml":
        "173c16a1c86027d48d5e21002adee8ef001d2c3c",
    "reference/repository-standards-v9.web.integration.yml":
        "171d02f1102c94fee1143497b6687ef179f853c8",
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


class RepositoryContractV10Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json("schemas/repository-standards-v10.schema.json")
        cls.compatibility_v8 = load_json(
            "profiles/repository-standards-compatibility-v8.json"
        )
        cls.compatibility_v9 = load_json(
            "profiles/repository-standards-compatibility-v9.json"
        )
        cls.web_v3 = load_json("profiles/web-application-baseline-v3.json")

    def test_v9_web_contract_assets_remain_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_V9_WEB_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))

    def test_web_v3_defines_language_prefix_and_stable_route_ids(self) -> None:
        routing = self.web_v3["routing"]
        self.assertEqual(
            "/<iso-639-1>/<stable-route-id>",
            routing["canonical_user_facing_content_form"],
        )
        self.assertEqual(
            ["impressum", "datenschutz", "barrierefreiheit"],
            routing["required_route_ids"],
        )
        self.assertTrue(routing["route_ids_stable_across_languages"])
        self.assertFalse(routing["localized_canonical_slugs"])
        self.assertFalse(routing["technical_endpoints_language_prefix_required"])
        self.assertFalse(
            self.web_v3["localization"]["unsupported_namespace_fallback_in_place"]
        )
        self.assertEqual(
            ".repository-localization.yml",
            self.web_v3["localization"]["declaration"],
        )

    def test_web_v3_preserves_root_accessibility_and_indexing_invariants(self) -> None:
        self.assertTrue(self.web_v3["root"]["redirect_required"])
        self.assertTrue(
            self.web_v3["root"]["deterministic_default_fallback_required"]
        )
        self.assertTrue(
            self.web_v3["accessibility"]["html_lang_matches_delivered_language"]
        )
        self.assertTrue(self.web_v3["indexing"]["canonical_per_language"])
        self.assertTrue(
            self.web_v3["indexing"]["hreflang_for_equivalent_indexable_pages"]
        )

    def test_v10_schema_has_core_and_web_v3_pairings(self) -> None:
        self.assertEqual(10, self.schema["properties"]["version"]["const"])
        alternatives = self.schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        web = alternatives[1]["properties"]
        self.assertEqual("v4", web["ticket-specification"]["const"])
        self.assertEqual("v8", web["development-workflow"]["const"])
        self.assertEqual("v1", web["contract-first-delivery"]["const"])
        self.assertEqual("v3", web["web-application-baseline"]["const"])
        self.assertEqual("v1", web["deployment-environments"]["const"])

    def test_compatibility_v9_preserves_v8_and_adds_v10(self) -> None:
        prior = self.compatibility_v8["pairings"]
        current = self.compatibility_v9["pairings"]
        self.assertEqual(prior, current[: len(prior)])
        v10 = [item for item in current if item["declaration_schema"] == "v10"]
        self.assertEqual(2, len(v10))
        web = [item for item in v10 if "web_application_baseline" in item][0]
        self.assertEqual("v3", web["web_application_baseline"])
        self.assertEqual("v1", web["repository_localization"])
        self.assertEqual("supported", web["status"])
        self.assertEqual(
            "reject",
            self.compatibility_v9["unsupported_pairing_policy"],
        )

    def test_v10_references_cover_core_and_web_branch_models(self) -> None:
        expectations = (
            ("repository-standards-v10.single.yml", "single", False),
            ("repository-standards-v10.integration.yml", "integration", False),
            ("repository-standards-v10.web.single.yml", "single", True),
            ("repository-standards-v10.web.integration.yml", "integration", True),
        )
        for name, model, web in expectations:
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("10", values["version"])
                self.assertEqual(model, values["branching.model"])
                if web:
                    self.assertEqual(
                        "v3",
                        values["standards.web-application-baseline"],
                    )
                    self.assertEqual(
                        "v1",
                        values["standards.deployment-environments"],
                    )

    def test_public_core_contains_v3_and_v10_contract_surface(self) -> None:
        manifest = load_json("public/public-core-v1.json")
        files = set(manifest["files"])
        required = {
            "standards/web-application-baseline/v3/standard.md",
            "standards/repository-localization/v1/standard.md",
            "schemas/repository-localization-v1.schema.json",
            "schemas/repository-standards-v10.schema.json",
            "profiles/web-application-baseline-v3.json",
            "profiles/repository-localization-v1.json",
            "profiles/repository-standards-compatibility-v9.json",
            "reference/repository-localization-v1.yml",
            "reference/repository-standards-v10.web.integration.yml",
            "reference/repository-standards-v10.web.single.yml",
            "tools/repository_localization.py",
            "docs/web-application-baseline-v3-migration.md",
            "tests/test_repository_localization_v1.py",
            "tests/test_repository_contract_v10.py",
        }
        self.assertTrue(required.issubset(files))
        allowed = {
            item["path"] for item in manifest["allowedInternalReferences"]
        }
        self.assertIn("schemas/repository-localization-v1.schema.json", allowed)
        self.assertIn("schemas/repository-standards-v10.schema.json", allowed)


if __name__ == "__main__":
    unittest.main()
