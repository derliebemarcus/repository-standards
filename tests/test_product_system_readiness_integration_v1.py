from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from tools.product_system_readiness import (
    load_declaration,
    validate_declaration,
    validate_epic_completion,
)
from tools.product_system_readiness_fixtures import make_assessment
from tools.product_system_readiness_model import declared_applicability

ROOT = Path(__file__).resolve().parents[1]
FROZEN_DESIGN_STANDARD_BLOB = "2729a92f5a35091b0ca28b7eda361007fa7b0c6f"
FROZEN_TEST_PROFILE_BLOB = "bd96ed63fb0d0774ba856d6d39abff17eb6516c1"
RELEASE_VERSION = "9.3.0"


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def exact_reference() -> dict[str, str]:
    return {
        "type": "git",
        "locator": "evidence/product-readiness.json",
        "revision": "qualified-revision",
    }


def epic(
    target: int,
    stage: str = "mvp",
    assessment_reference: dict[str, str] | None = None,
    subject: str = "product:bounded-mvp",
    status: str = "Status/Done",
) -> dict[str, object]:
    return {
        "kind": "Kind/Epic",
        "status": status,
        "product_increment": {
            "kind": "release",
            "subject_identity": subject,
            "stage": stage,
            "readiness_target": target,
            "assessment": assessment_reference,
        },
    }


class ProductSystemReadinessIntegrationV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.declaration_schema = load_json(
            "schemas/product-system-readiness-declaration-v1.schema.json"
        )
        cls.declaration_profile = load_json(
            "profiles/product-system-readiness-declaration-v1.json"
        )
        cls.ticket_schema = load_json("schemas/ticket-specification-v5.schema.json")
        cls.ticket_profile = load_json("profiles/ticket-specification-v5.json")
        cls.compatibility_v9 = load_json(
            "profiles/repository-standards-compatibility-v9.json"
        )
        cls.compatibility_v10 = load_json(
            "profiles/repository-standards-compatibility-v10.json"
        )
        cls.repository_schema = load_json(
            "schemas/repository-standards-v11.schema.json"
        )
        cls.fixtures = load_json(
            "reference/product-system-readiness-declaration-v1-fixtures.json"
        )

    def test_frozen_design_contract_standard_is_byte_immutable(self) -> None:
        path = ROOT / "standards/product-system-readiness/v1/standard.md"
        self.assertEqual(FROZEN_DESIGN_STANDARD_BLOB, git_blob_sha(path))

    def test_frozen_test_contract_profile_is_byte_immutable(self) -> None:
        path = ROOT / "profiles/product-system-readiness-test-contract-v1.json"
        self.assertEqual(FROZEN_TEST_PROFILE_BLOB, git_blob_sha(path))

    def test_repository_sidecar_is_canonical_and_valid(self) -> None:
        declaration = load_declaration(ROOT / ".product-readiness.yml")
        self.assertEqual([], validate_declaration(declaration))
        self.assertEqual("not-applicable", declaration["applicability"])
        self.assertTrue(str(declaration["rationale"]).strip())

    def test_declaration_profile_pins_frozen_contracts(self) -> None:
        governing = self.declaration_profile["governing_contracts"]
        self.assertEqual(
            "fa10d783440c4a798f3fe5b6fa55ac6166ce77da",
            governing["design"]["revision"],
        )
        self.assertEqual(
            "a8fa9519a97f188d5918aee79d5203f3f8deb25d",
            governing["test"]["revision"],
        )
        self.assertEqual(
            FROZEN_TEST_PROFILE_BLOB,
            governing["test"]["digest"],
        )
        self.assertTrue(self.declaration_profile["fail_closed"])
        self.assertEqual(
            "forbidden",
            self.declaration_profile["repository_aggregation"],
        )

    def test_declaration_schema_is_fail_closed(self) -> None:
        self.assertFalse(self.declaration_schema["additionalProperties"])
        subject = self.declaration_schema["$defs"]["subject"]
        self.assertFalse(subject["additionalProperties"])
        self.assertEqual(["product", "system"], subject["properties"]["kind"]["enum"])
        target = subject["properties"]["long_term_target"]
        self.assertEqual("#/$defs/trlTarget", target["$ref"])
        self.assertEqual(1, self.declaration_schema["$defs"]["trlTarget"]["minimum"])
        self.assertEqual(9, self.declaration_schema["$defs"]["trlTarget"]["maximum"])

    def test_positive_declaration_fixtures_pass(self) -> None:
        for case in self.fixtures["positive_declarations"]:
            with self.subTest(case=case["name"]):
                self.assertEqual([], validate_declaration(case["declaration"]))

    def test_controlled_negative_declarations_fail_deterministically(self) -> None:
        for case in self.fixtures["negative_declarations"]:
            with self.subTest(case=case["name"]):
                errors = validate_declaration(case["declaration"])
                self.assertIn(case["finding"], errors)

    def test_applicability_is_not_inferred_from_repository_profiles(self) -> None:
        intent = self.fixtures["positive_declarations"][2]["declaration"]
        actual = declared_applicability(
            intent,
            repository_profile="application",
            documentation_profile="web-application",
        )
        self.assertEqual("not-applicable", actual)

    def test_ticket_v5_incorporates_v4_and_keeps_readiness_derived(self) -> None:
        self.assertEqual(
            "profiles/ticket-specification-v4.json",
            self.ticket_profile["incorporates"],
        )
        increment = self.ticket_profile["product_increment"]
        self.assertTrue(increment["stage_is_authored"])
        self.assertTrue(increment["readiness_target_is_authored"])
        self.assertFalse(increment["current_readiness_authored"])
        self.assertEqual("forbidden", increment["stage_to_trl_inference"])
        self.assertEqual("forbidden", increment["repository_trl_aggregation"])

    def test_ticket_v5_schema_requires_explicit_product_increment(self) -> None:
        self.assertIn("product_increment", self.ticket_schema["required"])
        properties = self.ticket_schema["$defs"]["productIncrement"]["properties"]
        self.assertEqual(["product", "release"], properties["kind"]["enum"])
        self.assertEqual(1, properties["readiness_target"]["minimum"])
        self.assertEqual(9, properties["readiness_target"]["maximum"])
        forbidden = {
            "current_trl",
            "actual_trl",
            "candidate",
            "assessed",
            "established",
            "preservation",
            "requalification",
        }
        self.assertTrue(forbidden.isdisjoint(properties))

    def test_mvp_target_nine_can_complete_with_derived_trl_nine(self) -> None:
        ticket = epic(9, stage="mvp", assessment_reference=exact_reference())
        assessment = make_assessment(
            9,
            subject_identity="product:bounded-mvp",
            operational_mode="real",
        )
        self.assertEqual([], validate_epic_completion(ticket, assessment))

    def test_stage_never_satisfies_readiness_target(self) -> None:
        ticket = epic(9, stage="production", assessment_reference=None)
        errors = validate_epic_completion(ticket, None)
        self.assertIn(
            "E_READINESS_EVIDENCE_REQUIRED:$.product_increment.assessment",
            errors,
        )
        self.assertIn("E_READINESS_EVIDENCE_REQUIRED:$assessment", errors)

    def test_epic_completion_fails_below_target(self) -> None:
        ticket = epic(8, assessment_reference=exact_reference())
        assessment = make_assessment(
            7,
            subject_identity="product:bounded-mvp",
            operational_mode="none",
        )
        errors = validate_epic_completion(ticket, assessment)
        self.assertIn("E_INCREMENT_TARGET_UNMET:$assessment", errors)

    def test_epic_completion_fails_for_subject_mismatch(self) -> None:
        ticket = epic(8, assessment_reference=exact_reference())
        assessment = make_assessment(8, subject_identity="product:other")
        errors = validate_epic_completion(ticket, assessment)
        self.assertIn("E_SUBJECT_MISMATCH:$assessment.subject", errors)

    def test_epic_fixture_requires_evidence_at_done(self) -> None:
        cases = {case["name"]: case for case in self.fixtures["epic_cases"]}
        case = cases["targeted-epic-without-qualified-evidence"]
        errors = validate_epic_completion(case["ticket"], None)
        self.assertIn(case["finding"], errors)

    def test_compatibility_v10_preserves_all_v9_pairings(self) -> None:
        prior = self.compatibility_v9["pairings"]
        current = self.compatibility_v10["pairings"]
        self.assertEqual(prior, current[: len(prior)])
        v11 = [item for item in current if item["declaration_schema"] == "v11"]
        self.assertEqual(2, len(v11))
        self.assertTrue(all(item["status"] == "supported" for item in v11))
        self.assertTrue(
            all(item["product_system_readiness"] == "v1" for item in v11)
        )
        self.assertEqual(
            "explicit-release-pinned-migration",
            self.compatibility_v10["consumer_activation"],
        )
        self.assertEqual(
            "supported-after-qualified-release; "
            "explicit-release-pinned-migration-and-compatible-automation-required",
            self.compatibility_v10["v11_activation_policy"],
        )
        activations = {item["activation"] for item in v11}
        self.assertEqual(
            {
                "requires-compatible-ticket-v5-and-product-system-readiness-v1-automation",
                "requires-compatible-ticket-v5-product-system-readiness-v1-"
                "and-qualified-web-v3-automation",
            },
            activations,
        )

    def test_release_documentation_exposes_v9_3_0_opt_in_boundary(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        compatibility = (ROOT / "docs/reference/compatibility.md").read_text(
            encoding="utf-8"
        )
        migration = (ROOT / "docs/repository-contract-v11-migration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"## {RELEASE_VERSION} - 2026-09-12", changelog)
        for text in (compatibility, migration):
            self.assertIn("v9.3.0", text)
            self.assertIn("supported", text)
            self.assertIn("explicit", text.lower())
        self.assertNotIn("v11 candidate pairing", compatibility.lower())
        self.assertNotIn(
            "pairings in `profiles/repository-standards-compatibility-v10.json` "
            "are `candidate`",
            migration,
        )

    def test_release_does_not_implicitly_self_migrate_or_activate_provider(self) -> None:
        declaration = (ROOT / ".repository-standards.yml").read_text(encoding="utf-8")
        compatibility = (ROOT / "docs/reference/compatibility.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("version: 10", declaration)
        self.assertNotIn("product-system-readiness:", declaration)
        self.assertIn("not activated merely by publication", compatibility)

    def test_public_core_contains_complete_readiness_release_surface(self) -> None:
        manifest = load_json("public/public-core-v1.json")
        files = set(manifest["files"])
        required = {
            "CHANGELOG.md",
            "standards/product-system-readiness/v1/standard.md",
            "schemas/product-system-readiness-assessment-v1.schema.json",
            "schemas/product-system-readiness-declaration-v1.schema.json",
            "schemas/product-system-readiness-intent-v1.schema.json",
            "schemas/repository-standards-v11.schema.json",
            "schemas/ticket-specification-v5.schema.json",
            "profiles/product-system-readiness-declaration-v1.json",
            "profiles/product-system-readiness-test-contract-v1.json",
            "profiles/repository-standards-compatibility-v10.json",
            "profiles/ticket-specification-v5.json",
            "reference/product-system-readiness-v1-controlled-negative-fixtures.json",
            "reference/product-system-readiness-v1-positive-fixtures.json",
            "reference/product-system-readiness-v1-traceability.json",
            "reference/repository-standards-v11.single.yml",
            "reference/repository-standards-v11.integration.yml",
            "reference/repository-standards-v11.web.single.yml",
            "reference/repository-standards-v11.web.integration.yml",
            "docs/reference/product-system-readiness.md",
            "docs/reference/compatibility.md",
            "docs/repository-contract-v11-migration.md",
            "docs/ticket-standard-v5-migration.md",
            "tools/product_system_readiness.py",
            "tools/product_system_readiness_model.py",
            "tests/test_product_system_readiness_integration_v1.py",
            "tests/test_product_system_readiness_v1.py",
        }
        self.assertTrue(required.issubset(files))
        self.assertFalse(any("capability-promotion" in path for path in files))

    def test_repository_v11_is_explicit_opt_in(self) -> None:
        self.assertEqual(11, self.repository_schema["properties"]["version"]["const"])
        alternatives = self.repository_schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        for pairing in alternatives:
            properties = pairing["properties"]
            self.assertEqual("v5", properties["ticket-specification"]["const"])
            self.assertEqual(
                "v1",
                properties["product-system-readiness"]["const"],
            )

    def test_security_governance_remains_independent(self) -> None:
        text = (
            ROOT / "standards/ticket-specification/v5/standard.md"
        ).read_text(encoding="utf-8")
        for inference in (
            "TRL 9 => secure",
            "TRL 9 => low risk",
            "TRL 9 => security approved",
            "TRL 9 => low criticality",
        ):
            self.assertIn(inference, text)


if __name__ == "__main__":
    unittest.main()
