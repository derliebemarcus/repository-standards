from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "product_system_readiness_test_contract.py"
SPEC = importlib.util.spec_from_file_location("readiness_contract", MODULE)
assert SPEC and SPEC.loader
readiness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(readiness)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def codes(errors):
    return {value.split(":", 1)[0] for value in errors}


def prior_trl9():
    return {
        "subject": {"kind": "product", "identity": "product:fixture"},
        "source_revision": "revision-a",
        "artifact": {
            "identity": "oci://fixture/product:1",
            "digest": "sha256:artifact-a",
            "release_state": "release",
        },
        "level": 9,
        "evidence_locator": "fixture://history/revision-a/trl9",
    }


class ProductSystemReadinessV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load("profiles/product-system-readiness-test-contract-v1.json")
        cls.intent_schema = load(
            "schemas/product-system-readiness-intent-v1.schema.json"
        )
        cls.assessment_schema = load(
            "schemas/product-system-readiness-assessment-v1.schema.json"
        )
        cls.trace = load("reference/product-system-readiness-v1-traceability.json")
        cls.positive = load(
            "reference/product-system-readiness-v1-positive-fixtures.json"
        )["fixtures"]
        cls.negative = load(
            "reference/product-system-readiness-v1-controlled-negative-fixtures.json"
        )["fixtures"]
        cls.positive_by_id = {item["id"]: item for item in cls.positive}
        cls.negative_by_id = {item["id"]: item for item in cls.negative}

    def assessment(self, fixture):
        assessment = readiness.make_assessment(**fixture.get("parameters", {}))
        kind = fixture["kind"]
        if kind == "assessment-empty":
            assessment["evidence"] = []
        elif kind == "qualification-shortcut":
            assessment["qualification_context"] = {
                "production_equivalent": True,
                "id": "qualification-context",
            }
        elif kind == "contract-mismatch":
            stale = readiness.canonical_contract_set("stale-test-contract-revision")
            assessment["evidence"][0]["provenance"]["contract_set"] = stale
        elif kind == "subject-mismatch":
            assessment["evidence"][0]["provenance"]["subject"] = {
                "kind": "product",
                "identity": "product:other",
            }
        elif kind == "missing-provenance":
            del assessment["evidence"][0]["provenance"]["report_locator"]
        return assessment

    def preservation(self, fixture):
        impact = {
            "change_kind": fixture.get("change_kind", "feature"),
            "lineage_valid": True,
            "triggers": [],
            "material_boundary_crossed": False,
            "affected_criteria": list(readiness.ALL_CRITERIA),
        }
        assessment = readiness.make_assessment(
            through_level=9,
            mode="preservation",
            prior_established=prior_trl9(),
            change_impact=impact,
        )
        current = assessment["evidence"][0]
        reused = copy.deepcopy(current)
        reused["id"] = "evidence:reused"
        reused["criteria"] = [
            item
            for level in range(1, 8)
            for item in readiness.CRITERIA_BY_LEVEL[level]
        ]
        reused["provenance"]["source_revision"] = "revision-a"
        reused["provenance"]["artifact"] = copy.deepcopy(prior_trl9()["artifact"])
        reused["equivalence"] = {
            "dimensions": ["source_revision", "artifact"],
            "criteria": list(reused["criteria"]),
            "argument": "Impact analysis proves continued validity.",
            "evidence": ["fixture://preservation/impact-analysis"],
        }
        rerun = copy.deepcopy(current)
        rerun["id"] = "evidence:rerun"
        rerun["criteria"] = list(readiness.CRITERIA_BY_LEVEL[8])
        rerun["criteria"] += list(readiness.CRITERIA_BY_LEVEL[9])
        assessment["evidence"] = [reused, rerun]
        return assessment

    def fundamental(self, fixture):
        impact = {
            "change_kind": fixture.get("change_kind", "feature"),
            "lineage_valid": True,
            "triggers": [fixture["trigger"]],
            "material_boundary_crossed": True,
            "affected_criteria": list(readiness.ALL_CRITERIA),
        }
        assessment = readiness.make_assessment(
            through_level=None,
            mode="preservation",
            prior_established=prior_trl9(),
            change_impact=impact,
        )
        assessment["evidence"] = []
        return assessment

    def result(self, fixture):
        kind = fixture["kind"]
        if kind == "preservation-split":
            return readiness.evaluate(self.preservation(fixture))
        if kind == "fundamental-change":
            return readiness.evaluate(self.fundamental(fixture))
        return readiness.evaluate(self.assessment(fixture))

    def assert_expected(self, fixture, result):
        expected = fixture["expected"]
        for key in (
            "candidate",
            "assessed",
            "established",
            "requalification_required",
        ):
            if key in expected:
                self.assertEqual(expected[key], result[key], fixture["id"])
        for code in expected.get("findings", []):
            self.assertIn(code, codes(result["findings"]), fixture["id"])
        if "historical_level" in expected:
            history = result["historical_established"]
            self.assertEqual(expected["historical_level"], history["level"])

    def test_frozen_design_contract_identity(self):
        artifact = self.profile["governing_design_contract"]["artifact"]
        self.assertEqual(readiness.DESIGN_CONTRACT_LOCATOR, artifact["locator"])
        self.assertEqual(readiness.DESIGN_CONTRACT_REVISION, artifact["revision"])
        self.assertEqual(readiness.DESIGN_CONTRACT_BLOB, artifact["digest"])
        self.assertTrue(self.profile["identity"]["predicted_revision_forbidden"])

    def test_schemas_keep_authored_and_derived_separate(self):
        self.assertFalse(self.intent_schema["additionalProperties"])
        self.assertFalse(self.assessment_schema["additionalProperties"])
        subject = self.intent_schema["$defs"]["subject"]["properties"]
        for field in readiness.DERIVED_AUTHORITY_FIELDS:
            self.assertNotIn(field, self.intent_schema["properties"])
            self.assertNotIn(field, subject)
        criteria = self.assessment_schema["$defs"]["criterion"]["enum"]
        self.assertEqual(set(readiness.ALL_CRITERIA), set(criteria))

    def test_intent_fixtures_and_profiles(self):
        for fixture in self.positive:
            if fixture["kind"] == "intent":
                self.assertEqual([], readiness.validate_intent(fixture["payload"]))
        for fixture in self.negative:
            if fixture["kind"] != "intent-negative":
                continue
            actual = codes(readiness.validate_intent(fixture["payload"]))
            self.assertTrue(set(fixture["expected"]["errors"]).issubset(actual))
        required = self.positive_by_id["intent-required-system"]["payload"]
        self.assertEqual(
            "required",
            readiness.declared_applicability(
                required,
                repository_profile="library",
                documentation_profile="infrastructure",
            ),
        )

    def test_every_trl_positive_and_every_criterion_fail_closed(self):
        for level in range(1, 10):
            fixture = self.positive_by_id[f"trl-{level}-cumulative-positive"]
            result = self.result(fixture)
            self.assertEqual(level, result["candidate"])
            self.assertEqual(level, result["established"])
        for criterion in readiness.ALL_CRITERIA:
            level = readiness.CRITERION_LEVEL[criterion]
            assessment = readiness.make_assessment(
                through_level=9,
                missing_criteria=[criterion],
            )
            expected = "unassessed" if level == 1 else level - 1
            self.assertEqual(expected, readiness.evaluate(assessment)["candidate"])

    def test_unassessed_stage_target_and_subject_semantics(self):
        for fixture_id in (
            "unassessed-no-evidence",
            "unknown-r1-does-not-become-trl1",
        ):
            result = self.result(self.negative_by_id[fixture_id])
            self.assertEqual("unassessed", result["candidate"])
            self.assertNotIn(result["candidate"], {0, 1})
        mvp = self.result(self.positive_by_id["mvp-real-use-trl9"])
        self.assertEqual(9, mvp["candidate"])
        production = self.negative_by_id["production-stage-insufficient-evidence"]
        self.assertEqual(3, self.result(production)["candidate"])
        target = self.positive_by_id["target9-assessed6"]
        result = self.result(target)
        self.assertEqual(9, target["target"])
        self.assertEqual(6, result["assessed"])

    def test_provenance_context_and_operational_boundaries(self):
        invalid = (
            "stale-revision-fails-closed",
            "cross-artifact-without-equivalence",
            "cross-context-without-equivalence",
            "contract-mismatch-fails-closed",
            "expired-validity-fails-closed",
            "subject-mismatch-fails-closed",
            "missing-provenance-fails-closed",
        )
        for fixture_id in invalid:
            result = self.result(self.negative_by_id[fixture_id])
            self.assertEqual("unassessed", result["candidate"])
        equivalent = self.positive_by_id[
            "cross-revision-artifact-context-with-equivalence"
        ]
        self.assertEqual(8, self.result(equivalent)["candidate"])
        for fixture_id in (
            "trl8-dev-production-equivalent",
            "trl8-staging-production-equivalent-no-prod",
        ):
            result = self.result(self.positive_by_id[fixture_id])
            self.assertEqual(8, result["candidate"])
        for fixture_id in (
            "trl9-deployment-only",
            "trl9-health-only",
            "trl9-smoke-only",
            "trl9-brief-reachability",
            "trl9-synthetic-only",
        ):
            result = self.result(self.negative_by_id[fixture_id])
            self.assertEqual(8, result["candidate"])
            self.assertIn(
                "E_OPERATIONAL_PROOF_INSUFFICIENT",
                codes(result["findings"]),
            )

    def test_lifecycle_history_and_fundamental_change(self):
        preserved = self.positive_by_id["decision-8-feature-preserves-trl9"]
        self.assertEqual(9, self.result(preserved)["established"])
        fundamental = self.negative_by_id[
            "decision-9-fundamental-architecture-requires-requalification"
        ]
        result = self.result(fundamental)
        self.assertTrue(result["requalification_required"])
        self.assertIsNone(result["established"])
        self.assertEqual(9, result["historical_established"]["level"])
        for trigger in readiness.FUNDAMENTAL_TRIGGERS:
            impact = {
                "triggers": [trigger],
                "material_boundary_crossed": True,
            }
            self.assertTrue(readiness.requires_requalification(impact))

    def test_security_boundary_and_targets(self):
        for claim in self.profile["security_boundary"]["prohibited_inferences"]:
            actual = readiness.validate_governance_inference(claim)
            self.assertIn("E_SECURITY_INFERENCE", codes(actual))
        technical = self.negative_by_id[
            "decision-16-technical-security-qualification-missing"
        ]
        self.assertEqual(7, self.result(technical)["candidate"])
        intent = self.positive_by_id["intent-long-term-9-increment-8"]["payload"]
        subject = intent["subjects"][0]
        self.assertEqual(9, subject["long_term_target"])
        self.assertEqual(8, subject["increment_targets"][0]["target"])

    def test_traceability_covers_46_criteria_and_18_decision_cases(self):
        columns = self.trace["criterion_columns"]
        criteria = [dict(zip(columns, row)) for row in self.trace["criteria"]]
        criterion_ids = {row["criterion"] for row in criteria}
        self.assertEqual(set(readiness.ALL_CRITERIA), criterion_ids)
        self.assertEqual(46, len(criteria))
        fixture_ids = set(self.positive_by_id) | set(self.negative_by_id)
        cases = {case_id: fixtures for case_id, fixtures in self.trace["decision_cases"]}
        self.assertEqual(set(range(1, 19)), set(cases))
        for fixtures in cases.values():
            self.assertTrue(fixtures)
            self.assertTrue(set(fixtures).issubset(fixture_ids))

    def test_all_behavior_fixtures_execute(self):
        for fixture in self.positive + self.negative:
            kind = fixture["kind"]
            if kind == "intent":
                self.assertEqual([], readiness.validate_intent(fixture["payload"]))
            elif kind == "intent-negative":
                self.assertTrue(readiness.validate_intent(fixture["payload"]))
            elif kind == "multi-subject":
                results = {}
                for subject in fixture["subjects"]:
                    assessment = readiness.make_assessment(
                        subject["through_level"],
                        subject_identity=subject["identity"],
                    )
                    result = readiness.evaluate(assessment)
                    results[subject["identity"]] = result["candidate"]
                self.assertEqual(fixture["expected"]["results"], results)
            elif kind == "independent-security-gate":
                assessment = readiness.make_assessment(**fixture["parameters"])
                result = readiness.evaluate(assessment)
                self.assertEqual(fixture["expected"]["candidate"], result["candidate"])
            else:
                self.assert_expected(fixture, self.result(fixture))

    def test_masking_is_prohibited(self):
        prohibited = set(self.profile["masking_prohibited"])
        self.assertEqual(
            {
                "skip",
                "xfail",
                "implicit-baseline-acceptance",
                "materially-over-broad-tolerance",
            },
            prohibited,
        )


if __name__ == "__main__":
    unittest.main()
