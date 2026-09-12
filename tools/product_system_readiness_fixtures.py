"""Deterministic fixture builders for Product/System Readiness v1 tests."""
from __future__ import annotations

from tools.product_system_readiness_model import (
    CRITERIA_BY_LEVEL,
    EVIDENCE_CLASSES_BY_LEVEL,
    MATERIAL_CONTEXT_DIMENSIONS,
    canonical_contract_set,
)


def canonical_context(
    context_id="qualification-context",
    environment_name="DEV",
    adequate=True,
    difference_dimension=None,
):
    dimensions = {}
    for name in MATERIAL_CONTEXT_DIMENSIONS:
        status = "qualified-difference" if name == difference_dimension else "equivalent"
        evidence = [f"fixture://context/{name}/qualified"]
        if not adequate and name == MATERIAL_CONTEXT_DIMENSIONS[0]:
            status, evidence = "unknown", []
        dimensions[name] = {"status": status, "evidence": evidence}
    return {
        "id": context_id,
        "environment_name": environment_name,
        "intended_context": "intended-real-operation",
        "material_dimensions": list(MATERIAL_CONTEXT_DIMENSIONS),
        "dimensions": dimensions,
        "limitations": [],
    }


def canonical_operational_proof(mode="real"):
    weak = {
        "actual_use": False,
        "real_context": False,
        "actors_or_workload": [],
        "sufficiency_boundary": None,
        "success": True,
        "incidents_evaluated": False,
        "sustaining_ownership": False,
        "traceability": [f"fixture://{mode}"],
    }
    if mode == "none":
        return None
    if mode in {"deployment-only", "health-only", "smoke-only"}:
        return weak
    if mode == "brief-reachability":
        weak.update(
            actual_use=True,
            real_context=True,
            actors_or_workload=["brief-reachability"],
            sustaining_ownership=True,
            sufficiency_boundary={
                "predefined": False,
                "kind": "elapsed-service-exposure",
                "value": "a few minutes",
            },
        )
        return weak
    if mode == "synthetic-only":
        weak.update(
            actors_or_workload=["synthetic-load"],
            incidents_evaluated=True,
            sustaining_ownership=True,
            sufficiency_boundary={
                "predefined": True,
                "kind": "workload-volume",
                "value": "10000 synthetic transactions",
            },
        )
        return weak
    return {
        "actual_use": True,
        "real_context": True,
        "actors_or_workload": ["real-actors", "representative-live-workload"],
        "sufficiency_boundary": {
            "predefined": True,
            "kind": "operating-cycles",
            "value": "two representative operating cycles",
        },
        "success": True,
        "incidents_evaluated": True,
        "sustaining_ownership": True,
        "traceability": ["fixture://operations/lineage"],
    }


def make_assessment(through_level, **options):
    subject = {
        "kind": options.get("subject_kind", "product"),
        "identity": options.get("subject_identity", "product:fixture"),
    }
    repository = options.get("repository", "example/readiness-fixture")
    revision = options.get("source_revision", "revision-b")
    digest = options.get("artifact_digest", "sha256:artifact-b")
    artifact = None
    if options.get("artifact", True):
        artifact = {
            "identity": "oci://fixture/product:1",
            "digest": digest,
            "release_state": "release",
        }
    evidence_artifact = None if artifact is None else dict(artifact)
    if evidence_artifact is not None:
        evidence_artifact["digest"] = options.get("evidence_artifact_digest") or digest
    contract_set = canonical_contract_set()
    context = canonical_context(
        options.get("context_id", "qualification-context"),
        options.get("environment_name", "DEV"),
        options.get("context_adequate", True),
        options.get("context_difference_dimension"),
    )
    criteria, classes = [], []
    if through_level is not None:
        for level in range(1, through_level + 1):
            criteria += list(CRITERIA_BY_LEVEL[level])
            classes += list(EVIDENCE_CLASSES_BY_LEVEL[level])
    missing = set(options.get("missing_criteria", ()))
    criteria = [item for item in criteria if item not in missing]
    provenance = {
        "subject": dict(subject),
        "repository": repository,
        "source_revision": options.get("evidence_source_revision") or revision,
        "artifact": evidence_artifact,
        "contract_set": options.get("evidence_contract_set") or contract_set,
        "build_ci": {"result": "pass", "locator": "fixture://build/1"},
        "security": {"result": "pass", "locator": "fixture://security/1"},
        "accessibility": {"result": "pass", "locator": "fixture://a11y/1"},
        "deployment": {"result": "pass", "locator": "fixture://deployment/1"},
        "operations": {"result": "pass", "locator": "fixture://operations/1"},
        "tool": "readiness-test-oracle",
        "runner": "repository-standards-unittest",
        "runner_version": "v1",
        "parameters": {"deterministic": True},
        "timestamp": "2026-09-11T12:00:00Z",
        "report_locator": "fixture://report/consolidated",
    }
    item = {
        "id": "evidence:consolidated",
        "criteria": criteria,
        "classes": sorted(set(classes)) or ["research-principle"],
        "result": "pass",
        "provenance": provenance,
        "qualification_context_id": options.get("evidence_context_id") or context["id"],
        "operational": canonical_operational_proof(options.get("operational_mode", "real")),
        "equivalence": None,
        "limitations": [],
        "validity": {
            "valid_from": "2026-09-01T00:00:00Z",
            "valid_until": (
                "2026-09-10T00:00:00Z"
                if options.get("expired")
                else "2027-09-11T00:00:00Z"
            ),
            "boundaries": [
                "subject",
                "revision",
                "artifact",
                "contract-set",
                "qualification-context",
            ],
        },
    }
    unknown = set(options.get("unknown_criteria", ()))
    evidence = [item]
    if unknown:
        item["criteria"] = [value for value in criteria if value not in unknown]
        other = dict(item)
        other.update(
            id="evidence:unknown",
            criteria=list(unknown),
            result="unknown",
        )
        evidence.append(other)
    dimensions = options.get("equivalence_dimensions", ())
    if dimensions:
        for entry in evidence:
            entry["equivalence"] = {
                "dimensions": list(dimensions),
                "criteria": list(entry["criteria"]),
                "argument": "Changed dimensions are proven immaterial.",
                "evidence": ["fixture://equivalence/qualified"],
            }
    assessment = {
        "schema": "product-system-readiness-assessment-v1",
        "mode": options.get("mode", "establishment"),
        "subject": subject,
        "repository": repository,
        "source_revision": revision,
        "artifact": artifact,
        "contract_set": contract_set,
        "qualification_context": context,
        "evidence": evidence,
        "evaluation_time": "2026-09-11T13:00:00Z",
    }
    if options.get("prior_established") is not None:
        assessment["prior_established"] = options["prior_established"]
    if options.get("change_impact") is not None:
        assessment["change_impact"] = options["change_impact"]
    return assessment
