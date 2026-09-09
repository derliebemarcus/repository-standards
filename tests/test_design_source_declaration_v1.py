from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.design_source import (
    DesignSourceContractError,
    load_and_validate,
    validate_declaration,
    validate_design_contract_source,
)

ROOT = Path(__file__).resolve().parents[1]
TEAM_ID = "11111111-1111-4111-8111-111111111111"
PROJECT_ID = "22222222-2222-4222-8222-222222222222"


def declaration(*, automation: bool = True) -> dict[str, object]:
    raw: dict[str, object] = {
        "version": 1,
        "source": {
            "provider": "penpot",
            "team": {"id": TEAM_ID, "name": "siczb"},
            "project": {"id": PROJECT_ID, "name": "example-web"},
        },
    }
    if automation:
        raw["automation"] = {"interface": "penpot-rpc"}
    return raw


class DesignSourceDeclarationV1Test(unittest.TestCase):
    def assert_invalid(self, raw: object) -> None:
        with self.assertRaises(DesignSourceContractError):
            validate_declaration(raw)

    def test_reference_declaration_is_valid(self) -> None:
        parsed = load_and_validate(ROOT / "reference/repository-design-source-v1.yml")
        source = parsed["source"]
        self.assertIsInstance(source, dict)
        assert isinstance(source, dict)
        self.assertEqual("penpot", source["provider"])
        self.assertEqual(TEAM_ID, source["team"]["id"])
        self.assertEqual(PROJECT_ID, source["project"]["id"])
        self.assertEqual({"interface": "penpot-rpc"}, parsed["automation"])

    def test_automation_is_optional(self) -> None:
        parsed = validate_declaration(declaration(automation=False))
        self.assertNotIn("automation", parsed)

    def test_names_are_optional_but_ids_are_required(self) -> None:
        raw = declaration()
        source = raw["source"]
        assert isinstance(source, dict)
        source["team"] = {"id": TEAM_ID}
        source["project"] = {"id": PROJECT_ID}
        parsed = validate_declaration(raw)
        self.assertEqual({"id": TEAM_ID}, parsed["source"]["team"])
        self.assertEqual({"id": PROJECT_ID}, parsed["source"]["project"])

        for identity in ("team", "project"):
            invalid = declaration()
            invalid_source = invalid["source"]
            assert isinstance(invalid_source, dict)
            invalid_source[identity] = {"name": "display-only"}
            with self.subTest(identity=identity):
                self.assert_invalid(invalid)

    def test_malformed_ids_fail_closed(self) -> None:
        for value in (
            "",
            "project-name",
            "22222222-2222-2222-2222-222222222222",
            "22222222-2222-6222-8222-222222222222",
            "22222222-2222-4222-7222-222222222222",
        ):
            raw = declaration()
            source = raw["source"]
            assert isinstance(source, dict)
            source["project"] = {"id": value}
            with self.subTest(value=value):
                self.assert_invalid(raw)

    def test_unknown_provider_and_automation_fail_closed(self) -> None:
        raw = declaration()
        source = raw["source"]
        assert isinstance(source, dict)
        source["provider"] = "figma"
        self.assert_invalid(raw)

        raw = declaration()
        raw["automation"] = {"interface": "generic-mcp"}
        self.assert_invalid(raw)

    def test_unknown_fields_and_secret_like_fields_fail_closed(self) -> None:
        variants = []

        root_secret = declaration()
        root_secret["token"] = "secret"
        variants.append(root_secret)

        source_secret = declaration()
        source = source_secret["source"]
        assert isinstance(source, dict)
        source["credential"] = "secret"
        variants.append(source_secret)

        team_secret = declaration()
        team_source = team_secret["source"]
        assert isinstance(team_source, dict)
        team_source["team"] = {"id": TEAM_ID, "api_key": "secret"}
        variants.append(team_secret)

        automation_secret = declaration()
        automation_secret["automation"] = {
            "interface": "penpot-rpc",
            "session": "secret",
        }
        variants.append(automation_secret)

        for raw in variants:
            with self.subTest(raw=raw):
                self.assert_invalid(raw)

    def test_multiple_or_ambiguous_primary_sources_are_not_v1_fields(self) -> None:
        raw = declaration()
        raw["sources"] = [raw["source"]]
        self.assert_invalid(raw)

        raw = declaration()
        source = raw["source"]
        assert isinstance(source, dict)
        source["role"] = "primary"
        self.assert_invalid(raw)

    def test_design_contract_project_and_provider_must_match(self) -> None:
        raw = declaration()
        validate_design_contract_source(
            raw,
            provider="penpot",
            project_id=PROJECT_ID,
        )

        with self.assertRaisesRegex(DesignSourceContractError, "provider mismatch"):
            validate_design_contract_source(
                raw,
                provider="figma",
                project_id=PROJECT_ID,
            )
        with self.assertRaisesRegex(DesignSourceContractError, "project mismatch"):
            validate_design_contract_source(
                raw,
                provider="penpot",
                project_id="33333333-3333-4333-8333-333333333333",
            )

    def test_schema_matches_validator_contract(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/design-source-declaration-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(False, schema["additionalProperties"])
        self.assertEqual({"version", "source"}, set(schema["required"]))
        self.assertEqual(1, schema["properties"]["version"]["const"])
        source = schema["properties"]["source"]
        self.assertEqual("penpot", source["properties"]["provider"]["const"])
        self.assertEqual(False, source["additionalProperties"])
        self.assertEqual(
            "penpot-rpc",
            schema["properties"]["automation"]["properties"]["interface"]["const"],
        )

    def test_profile_keeps_source_and_automation_separate(self) -> None:
        profile = json.loads(
            (ROOT / "profiles/design-source-declaration-v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("1.0.0", profile["version"])
        self.assertEqual(".repository-design-source.yml", profile["canonical_path"])
        self.assertEqual(["penpot"], profile["primary_source"]["supported_providers"])
        automation = profile["automation"]["penpot-rpc"]
        self.assertFalse(automation["normative_source"])
        self.assertFalse(automation["required_for_source_validity"])
        self.assertEqual("fail-closed", profile["design_contract_refinement"]["mismatch_behavior"])


if __name__ == "__main__":
    unittest.main()
