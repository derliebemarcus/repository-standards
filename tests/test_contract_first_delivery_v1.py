from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "contract_first_delivery.py"
spec = importlib.util.spec_from_file_location("contract_first_delivery", MODULE_PATH)
assert spec and spec.loader
contract_first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract_first)


def artifact(locator: str, revision: str = "rev-1") -> dict[str, str]:
    return {
        "type": "git",
        "locator": locator,
        "revision": revision,
    }


def reference(work_item: str, resolved: bool) -> dict[str, object]:
    return {
        "work_item": work_item,
        "artifact": artifact(f"contracts/{work_item}.yml") if resolved else None,
    }


def implementation(status: str, resolved: bool) -> dict[str, object]:
    return {
        "status": status,
        "delivery": {
            "model": "contract-first-v1",
            "applicability": "required",
            "rationale": None,
            "role": "implementation",
            "design_contracts": [reference("#42", resolved)],
            "test_contracts": [reference("#53", resolved)],
            "evidence": [],
        },
    }


class ContractFirstDeliveryV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(
            (
                ROOT / "profiles" / "contract-first-delivery-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.web = json.loads(
            (
                ROOT / "profiles" / "web-application-baseline-v2.json"
            ).read_text(encoding="utf-8")
        )

    def test_profile_orders_four_work_products_and_freezes_at_ready(self) -> None:
        self.assertEqual(
            [
                "design-contract",
                "test-contract",
                "implementation",
                "conformance-evidence",
            ],
            self.profile["sequence"],
        )
        self.assertFalse(self.profile["separate_ticket_per_work_product_required"])
        self.assertEqual("Status/Ready", self.profile["freeze"]["implementation_status"])
        reference_contract = self.profile["contract_reference"]
        self.assertTrue(
            reference_contract["unresolved_work_item_reference_allowed_before_ready"]
        )
        self.assertTrue(reference_contract["all_required_references_resolved_at_ready"])

    def test_planned_implementation_may_reference_unresolved_work_items(self) -> None:
        ticket = implementation("Status/Blocked", resolved=False)
        self.assertEqual([], contract_first.validate_ticket(ticket))

    def test_ready_implementation_rejects_unresolved_contracts(self) -> None:
        ticket = implementation("Status/Ready", resolved=False)
        errors = contract_first.validate_ticket(ticket)
        self.assertTrue(any("must be resolved" in error for error in errors))

    def test_ready_implementation_accepts_exact_contract_set(self) -> None:
        ticket = implementation("Status/Ready", resolved=True)
        self.assertEqual([], contract_first.validate_ticket(ticket))

    def test_not_applicable_requires_rationale_and_empty_contracts(self) -> None:
        ticket = {
            "status": "Status/Backlog",
            "delivery": {
                "model": "contract-first-v1",
                "applicability": "not-applicable",
                "rationale": "",
                "role": None,
                "design_contracts": [],
                "test_contracts": [],
                "evidence": [],
            },
        }
        errors = contract_first.validate_ticket(ticket)
        self.assertIn("not-applicable requires a non-empty rationale", errors)
        ticket["delivery"]["rationale"] = "Documentation-only correction."
        self.assertEqual([], contract_first.validate_ticket(ticket))

    def test_graph_blocks_ready_when_upstream_contract_work_is_not_done(self) -> None:
        ticket = implementation("Status/Ready", resolved=True)
        work_items = {
            "#42": {"status": "Status/Done"},
            "#53": {"status": "Status/In Progress"},
        }
        errors = contract_first.validate_graph(ticket, work_items)
        self.assertIn("upstream work item is not Done: #53", errors)
        work_items["#53"] = {"status": "Status/Done"}
        self.assertEqual([], contract_first.validate_graph(ticket, work_items))

    def test_done_implementation_requires_evidence_reference(self) -> None:
        ticket = implementation("Status/Done", resolved=True)
        errors = contract_first.validate_ticket(ticket)
        self.assertIn("Done implementation requires Conformance Evidence", errors)
        ticket["delivery"]["evidence"] = [artifact("evidence/build-381.json")]
        self.assertEqual([], contract_first.validate_ticket(ticket))

    def test_evidence_rejects_contract_mutation_and_unresolved_contracts(self) -> None:
        evidence = {
            "schema": "contract-first-evidence-v1",
            "consumer": "siczb/example",
            "design_contracts": [reference("#42", True)],
            "test_contracts": [reference("#53", True)],
            "implementation": {
                "repository": "siczb/example",
                "revision": "abc123",
                "artifact": artifact("oci/example", "sha256:abc"),
            },
            "runtime": None,
            "execution": {
                "timestamp": "2026-08-27T05:00:00Z",
                "method": "playwright",
                "runner": "reference-runner-v1",
                "parameters": {},
                "result": "conformant",
            },
            "contract_mutation": False,
            "artifacts": [],
            "limitations": [],
        }
        self.assertEqual([], contract_first.validate_evidence(evidence))
        mutated = copy.deepcopy(evidence)
        mutated["contract_mutation"] = True
        self.assertIn(
            "evidence.contract_mutation must be false",
            contract_first.validate_evidence(mutated),
        )
        unresolved = copy.deepcopy(evidence)
        unresolved["test_contracts"][0]["artifact"] = None
        errors = contract_first.validate_evidence(unresolved)
        self.assertTrue(any("must be resolved" in error for error in errors))

    def test_web_v2_keeps_conformance_classes_distinct(self) -> None:
        classes = self.web["conformance_classes"]["classes"]
        self.assertEqual(
            {
                "functional",
                "accessibility",
                "reflow-responsive",
                "live-runtime",
                "visual",
            },
            set(classes),
        )
        self.assertFalse(classes["accessibility"]["visual_may_substitute"])
        self.assertFalse(
            classes["reflow-responsive"]["single_viewport_visual_may_substitute"]
        )
        self.assertEqual(
            "required",
            self.web["ui_impact"]["contract_first_applicability"],
        )

    def test_test_contract_forbids_masking_and_requires_negative_case(self) -> None:
        contract = self.profile["work_products"]["test-contract"]
        self.assertTrue(contract["controlled_negative_case_required"])
        self.assertFalse(contract["product_conformance_required_before_implementation"])
        for prohibited in (
            "skip",
            "xfail",
            "implicit-baseline-acceptance",
            "materially-over-broad-tolerance",
        ):
            self.assertIn(prohibited, contract["masking_prohibited"])


if __name__ == "__main__":
    unittest.main()
