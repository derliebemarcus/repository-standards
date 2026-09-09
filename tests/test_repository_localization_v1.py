from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.repository_localization import (
    ISO_639_1_CODES,
    LocalizationContractError,
    load_and_validate,
    validate_declaration,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUPPORTED = object()


def declaration(
    default_language: object = "de",
    supported_languages: object = DEFAULT_SUPPORTED,
) -> dict[str, object]:
    supported = (
        ["de", "en"]
        if supported_languages is DEFAULT_SUPPORTED
        else supported_languages
    )
    return {
        "version": 1,
        "web-application-baseline": "v3",
        "default-language": default_language,
        "supported-languages": supported,
    }


class RepositoryLocalizationV1Test(unittest.TestCase):
    def test_reference_declaration_is_valid(self) -> None:
        parsed = load_and_validate(ROOT / "reference/repository-localization-v1.yml")
        self.assertEqual("de", parsed["default-language"])
        self.assertEqual(["de", "en"], parsed["supported-languages"])

    def test_iso_639_1_registry_is_complete_and_contains_expected_codes(self) -> None:
        self.assertEqual(184, len(ISO_639_1_CODES))
        for code in ("de", "en", "fr", "it", "rm", "zh", "zu"):
            self.assertIn(code, ISO_639_1_CODES)

    def assert_invalid(self, raw: object) -> None:
        with self.assertRaises(LocalizationContractError):
            validate_declaration(raw)

    def test_unknown_uppercase_regional_and_three_letter_codes_are_rejected(self) -> None:
        for code in ("zz", "DE", "de-CH", "deu", ""):
            with self.subTest(code=code):
                self.assert_invalid(declaration(code, [code]))

    def test_valid_iso_code_can_still_be_unsupported_for_consumer(self) -> None:
        parsed = validate_declaration(declaration("de", ["de", "en"]))
        self.assertNotIn("fr", parsed["supported-languages"])

    def test_default_language_must_be_supported_exactly_once(self) -> None:
        self.assert_invalid(declaration("de", ["en"]))
        self.assert_invalid(declaration("de", ["de", "de"]))

    def test_supported_languages_must_be_non_empty_list(self) -> None:
        for value in ([], "de", None):
            with self.subTest(value=value):
                self.assert_invalid(declaration("de", value))

    def test_versions_and_unknown_fields_fail_closed(self) -> None:
        wrong_version = declaration()
        wrong_version["version"] = 2
        self.assert_invalid(wrong_version)

        wrong_baseline = declaration()
        wrong_baseline["web-application-baseline"] = "v2"
        self.assert_invalid(wrong_baseline)

        unknown = declaration()
        unknown["locale"] = "de-CH"
        self.assert_invalid(unknown)

    def test_schema_and_profile_match_contract(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/repository-localization-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        profile = json.loads(
            (ROOT / "profiles/repository-localization-v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(1, schema["properties"]["version"]["const"])
        self.assertEqual(
            "v3",
            schema["properties"]["web-application-baseline"]["const"],
        )
        self.assertEqual("ISO-639-1", profile["language_identity"]["registry"])
        self.assertTrue(profile["language_identity"]["registry_membership_required"])
        self.assertTrue(profile["default_language"]["must_be_supported"])
        self.assertFalse(profile["supported_languages"]["inference_allowed"])


if __name__ == "__main__":
    unittest.main()
