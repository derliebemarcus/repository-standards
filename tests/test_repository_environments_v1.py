from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from tools.repository_environments import (
    EnvironmentContractError,
    load_and_validate,
    validate_declaration,
)

ROOT = Path(__file__).resolve().parents[1]
V1_BLOBS = {
    "standards/deployment-environments/v1/standard.md": "3582470ebf8c3c5292c217e8fe109696ae92f017",
    "profiles/deployment-environments-v1.json": "f7ea839f733a8e00c4ada4ac00e0ded66b3ad115",
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def declaration(**environments: object) -> dict[str, object]:
    return {
        "version": 1,
        "deployment-environments": "v2",
        "environments": environments,
    }


class DeploymentEnvironmentsV2Test(unittest.TestCase):
    def test_profile_uses_staging_and_preserves_v1_guarantees(self) -> None:
        profile = json.loads(
            (ROOT / "profiles/deployment-environments-v2.json").read_text(encoding="utf-8")
        )
        self.assertEqual("2.0.0", profile["version"])
        self.assertEqual(["DEV", "STAGING", "PROD"], profile["canonical_order"])
        self.assertEqual({"DEV", "STAGING", "PROD"}, set(profile["environments"]))
        self.assertNotIn("STAGE", profile["environments"])
        self.assertEqual(["STAGE"], profile["rejected_environment_keys"])
        self.assertFalse(profile["environments"]["STAGING"]["required"])
        self.assertEqual(["release"], profile["environments"]["PROD"]["accepted_release_states"])
        self.assertTrue(profile["environments"]["PROD"]["immutable_release_artifact_required"])
        self.assertFalse(profile["promotion"]["rebuild_application_content"])
        self.assertTrue(profile["promotion"]["rollback_uses_existing_release_artifact"])

    def test_released_v1_assets_remain_byte_immutable(self) -> None:
        for relative_path, expected_sha in V1_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))


class RepositoryEnvironmentsV1Test(unittest.TestCase):
    def test_reference_declaration_is_valid_and_canonical(self) -> None:
        parsed = load_and_validate(ROOT / "reference/repository-environments-v1.yml")
        self.assertEqual(["DEV", "STAGING", "PROD"], list(parsed))

    def test_missing_environment_is_valid(self) -> None:
        parsed = validate_declaration(declaration(DEV={"url": "https://dev.example.invalid/"}))
        self.assertEqual({"DEV": "https://dev.example.invalid/"}, parsed)

    def test_http_and_https_are_valid(self) -> None:
        parsed = validate_declaration(
            declaration(
                DEV={"url": "http://dev.example.invalid/path"},
                PROD={"url": "https://example.invalid/app?view=home"},
            )
        )
        self.assertEqual(["DEV", "PROD"], list(parsed))

    def assert_invalid(self, raw: object) -> None:
        with self.assertRaises(EnvironmentContractError):
            validate_declaration(raw)

    def test_empty_environment_map_is_invalid(self) -> None:
        self.assert_invalid(declaration())

    def test_stage_is_rejected(self) -> None:
        self.assert_invalid(declaration(STAGE={"url": "https://stage.example.invalid/"}))

    def test_unknown_root_key_is_rejected(self) -> None:
        raw = declaration(DEV={"url": "https://dev.example.invalid/"})
        raw["project"] = "example"
        self.assert_invalid(raw)

    def test_unsupported_versions_are_rejected(self) -> None:
        raw = declaration(DEV={"url": "https://dev.example.invalid/"})
        raw["version"] = 2
        self.assert_invalid(raw)
        raw["version"] = 1
        raw["deployment-environments"] = "v1"
        self.assert_invalid(raw)

    def test_missing_empty_and_invalid_urls_are_rejected(self) -> None:
        for entry in (
            {},
            {"url": ""},
            {"url": "   "},
            {"url": "dev.example.invalid"},
            {"url": "ftp://dev.example.invalid/"},
            {"url": "https://"},
            {"url": "https://dev.example.invalid:invalid/"},
        ):
            with self.subTest(entry=entry):
                self.assert_invalid(declaration(DEV=entry))

    def test_credentials_fragments_whitespace_and_unknown_fields_are_rejected(self) -> None:
        credential_url = "https://user" + ":secret@" + "dev.example.invalid/"
        for entry in (
            {"url": credential_url},
            {"url": "https://dev.example.invalid/#section"},
            {"url": " https://dev.example.invalid/"},
            {"url": "https://dev.example.invalid/a b"},
            {"url": "https://dev.example.invalid/", "name": "DEV"},
        ):
            with self.subTest(entry=entry):
                self.assert_invalid(declaration(DEV=entry))

    def test_schema_matches_released_shape(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/repository-environments-v1.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(False, schema["additionalProperties"])
        self.assertEqual(1, schema["properties"]["version"]["const"])
        self.assertEqual("v2", schema["properties"]["deployment-environments"]["const"])
        environments = schema["properties"]["environments"]
        self.assertEqual({"DEV", "STAGING", "PROD"}, set(environments["properties"]))
        self.assertEqual(False, environments["additionalProperties"])
        self.assertEqual(1, environments["minProperties"])


if __name__ == "__main__":
    unittest.main()
