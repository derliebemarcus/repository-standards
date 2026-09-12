"""Semantic oracle for Product/System Readiness v1 contract qualification."""
from __future__ import annotations

from datetime import datetime

DESIGN_CONTRACT_LOCATOR = "standards/product-system-readiness/v1/standard.md"
DESIGN_CONTRACT_REVISION = "fa10d783440c4a798f3fe5b6fa55ac6166ce77da"
DESIGN_CONTRACT_BLOB = "2729a92f5a35091b0ca28b7eda361007fa7b0c6f"
TEST_CONTRACT_LOCATOR = "profiles/product-system-readiness-test-contract-v1.json"

CRITERIA_BY_LEVEL = {
    1: ("R1.1", "R1.2", "R1.3", "R1.4"),
    2: ("R2.1", "R2.2", "R2.3", "R2.4"),
    3: ("R3.1", "R3.2", "R3.3", "R3.4", "R3.5"),
    4: ("R4.1", "R4.2", "R4.3", "R4.4", "R4.5"),
    5: ("R5.1", "R5.2", "R5.3", "R5.4", "R5.5"),
    6: ("R6.1", "R6.2", "R6.3", "R6.4", "R6.5"),
    7: ("R7.1", "R7.2", "R7.3", "R7.4", "R7.5"),
    8: ("R8.1", "R8.2", "R8.3", "R8.4", "R8.5", "R8.6", "R8.7"),
    9: ("R9.1", "R9.2", "R9.3", "R9.4", "R9.5", "R9.6"),
}
ALL_CRITERIA = tuple(
    criterion
    for level in range(1, 10)
    for criterion in CRITERIA_BY_LEVEL[level]
)
CRITERION_LEVEL = {
    criterion: level
    for level, criteria in CRITERIA_BY_LEVEL.items()
    for criterion in criteria
}

EVIDENCE_CLASSES_BY_LEVEL = {
    1: ("research-principle",),
    2: ("concept-architecture-requirement", "analytical-feasibility"),
    3: ("proof-of-concept", "controlled-test", "limitations"),
    4: ("integration", "controlled-validation", "environment-prediction"),
    5: ("end-to-end", "relevant-environment", "fidelity-gap"),
    6: ("high-fidelity-prototype", "realistic-workload", "failure-recovery"),
    7: ("operationally-relevant-demonstration", "scenario", "context-fidelity"),
    8: (
        "final-artifact-configuration",
        "qualification-context",
        "complete-vv-conformance",
        "deployment-rollback",
        "residual-limitations",
    ),
    9: (
        "operational-lineage",
        "real-operational-use",
        "sufficiency-boundary",
        "operational-results",
        "incident-limitations",
        "sustaining-support",
    ),
}

DERIVED_AUTHORITY_FIELDS = {
    "trl",
    "current_trl",
    "candidate_trl",
    "assessed_trl",
    "established_trl",
    "candidate",
    "assessed",
    "established",
    "preservation_result",
    "requalification_result",
}
FUNDAMENTAL_TRIGGERS = {
    "architecture-or-execution-model",
    "runtime-platform-or-infrastructure-model",
    "trust-boundary-or-security-architecture",
    "persistence-or-data-architecture",
    "critical-operating-or-failure-assumptions",
    "subject-identity-or-material-scope",
    "operational-context-or-critical-integrations",
    "operational-evidence-no-longer-representative",
}
MATERIAL_CONTEXT_DIMENSIONS = (
    "runtime",
    "database",
    "infrastructure",
    "platform",
    "security_configuration",
    "trust_relationships",
    "integrations",
    "data_workload",
    "performance",
    "failure_recovery",
    "deployment_rollback",
)
PROHIBITED_GOVERNANCE_INFERENCES = {
    "TRL 9 => secure",
    "TRL 9 => low risk",
    "TRL 9 => low criticality",
    "TRL 9 => security approved",
}


def finding(code: str, path: str) -> str:
    return f"{code}:{path}"


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_intent(raw: object) -> list[str]:
    if not isinstance(raw, dict):
        return [finding("E_SCHEMA", "$")]
    errors = []
    for key in DERIVED_AUTHORITY_FIELDS & set(raw):
        errors.append(finding("E_AUTHORED_CURRENT_READINESS", f"$.{key}"))
    if raw.get("schema") != "product-system-readiness-intent-v1":
        errors.append(finding("E_SCHEMA", "$.schema"))
    subjects = raw.get("subjects")
    applicability = raw.get("applicability")
    if applicability not in {"required", "not-applicable"}:
        errors.append(finding("E_APPLICABILITY", "$.applicability"))
        return sorted(set(errors))
    if not isinstance(subjects, list):
        errors.append(finding("E_SCHEMA", "$.subjects"))
        return sorted(set(errors))
    if applicability == "not-applicable":
        if not nonempty(raw.get("rationale")):
            errors.append(finding("E_RATIONALE_REQUIRED", "$.rationale"))
        if subjects:
            errors.append(finding("E_APPLICABILITY", "$.subjects"))
        return sorted(set(errors))
    if not subjects:
        errors.append(finding("E_SUBJECT_REQUIRED", "$.subjects"))
    seen = set()
    for index, subject in enumerate(subjects):
        path = f"$.subjects[{index}]"
        if not isinstance(subject, dict):
            errors.append(finding("E_SCHEMA", path))
            continue
        for key in DERIVED_AUTHORITY_FIELDS & set(subject):
            errors.append(finding("E_AUTHORED_CURRENT_READINESS", f"{path}.{key}"))
        if subject.get("kind") not in {"product", "system"}:
            errors.append(finding("E_SUBJECT_KIND", f"{path}.kind"))
        identity = subject.get("identity")
        if not nonempty(identity):
            errors.append(finding("E_SUBJECT_IDENTITY", f"{path}.identity"))
        elif identity in seen:
            errors.append(finding("E_DUPLICATE_SUBJECT", f"{path}.identity"))
        else:
            seen.add(identity)
        target = subject.get("long_term_target")
        if isinstance(target, bool) or target not in range(1, 10):
            errors.append(finding("E_TARGET", f"{path}.long_term_target"))
        for inner, increment in enumerate(subject.get("increment_targets", [])):
            ipath = f"{path}.increment_targets[{inner}]"
            value = increment.get("target") if isinstance(increment, dict) else None
            if not isinstance(increment, dict) or value not in range(1, 10):
                errors.append(finding("E_TARGET", f"{ipath}.target"))
    return sorted(set(errors))


def declared_applicability(intent: object, **_profiles: object) -> str | None:
    if not isinstance(intent, dict):
        return None
    return intent.get("applicability")


def canonical_contract_set(
    test_revision: str = "fixture-test-contract-revision",
) -> dict[str, object]:
    return {
        "design": {
            "locator": DESIGN_CONTRACT_LOCATOR,
            "revision": DESIGN_CONTRACT_REVISION,
            "digest": DESIGN_CONTRACT_BLOB,
        },
        "test": {
            "locator": TEST_CONTRACT_LOCATOR,
            "revision": test_revision,
        },
    }


def validate_assessment(raw: object) -> list[str]:
    if not isinstance(raw, dict):
        return [finding("E_ASSESSMENT", "$")]
    errors = []
    if raw.get("schema") != "product-system-readiness-assessment-v1":
        errors.append(finding("E_SCHEMA", "$.schema"))
    modes = {"establishment", "preservation", "requalification"}
    if raw.get("mode") not in modes:
        errors.append(finding("E_ASSESSMENT", "$.mode"))
    design = (raw.get("contract_set") or {}).get("design", {})
    if design.get("locator") != DESIGN_CONTRACT_LOCATOR:
        errors.append(finding("E_CONTRACT_MISMATCH", "$.contract_set.design"))
    if design.get("revision") != DESIGN_CONTRACT_REVISION:
        errors.append(finding("E_CONTRACT_MISMATCH", "$.contract_set.design"))
    evidence = raw.get("evidence")
    if not isinstance(evidence, list):
        errors.append(finding("E_ASSESSMENT", "$.evidence"))
        return sorted(set(errors))
    for index, item in enumerate(evidence):
        provenance = item.get("provenance") if isinstance(item, dict) else None
        validity = item.get("validity") if isinstance(item, dict) else None
        if not isinstance(provenance, dict):
            errors.append(finding("E_MISSING_PROVENANCE", f"$.evidence[{index}]"))
        elif not nonempty(provenance.get("report_locator")):
            errors.append(finding("E_MISSING_PROVENANCE", f"$.evidence[{index}]"))
        if not isinstance(validity, dict):
            errors.append(finding("E_MISSING_PROVENANCE", f"$.evidence[{index}]"))
        elif not isinstance(validity.get("boundaries"), list):
            errors.append(finding("E_MISSING_PROVENANCE", f"$.evidence[{index}]"))
    if raw.get("mode") in {"preservation", "requalification"}:
        if not isinstance(raw.get("prior_established"), dict):
            path = "$.prior_established"
            errors.append(finding("E_PRIOR_ESTABLISHMENT_REQUIRED", path))
    return sorted(set(errors))


def context_adequate(context: object) -> bool:
    if not isinstance(context, dict) or "production_equivalent" in context:
        return False
    material = context.get("material_dimensions", [])
    dimensions = context.get("dimensions", {})
    if not nonempty(context.get("id")):
        return False
    if not nonempty(context.get("intended_context")):
        return False
    if not material or not isinstance(dimensions, dict):
        return False
    for name in material:
        detail = dimensions.get(name, {})
        if detail.get("status") not in {"equivalent", "qualified-difference"}:
            return False
        if not detail.get("evidence"):
            return False
    return True


def operational_adequate(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    boundary = value.get("sufficiency_boundary")
    return (
        value.get("actual_use") is True
        and value.get("real_context") is True
        and bool(value.get("actors_or_workload"))
        and isinstance(boundary, dict)
        and boundary.get("predefined") is True
        and nonempty(boundary.get("kind"))
        and nonempty(boundary.get("value"))
        and value.get("success") is True
        and value.get("incidents_evaluated") is True
        and value.get("sustaining_ownership") is True
        and bool(value.get("traceability"))
    )


def equivalence_covers(item: dict, dimension: str, criterion: str) -> bool:
    value = item.get("equivalence") or {}
    return (
        dimension in value.get("dimensions", [])
        and criterion in value.get("criteria", [])
        and nonempty(value.get("argument"))
        and bool(value.get("evidence"))
    )


def evidence_supports(item: dict, assessment: dict, criterion: str):
    if criterion not in item.get("criteria", []):
        return False, []
    if item.get("result") == "unknown":
        return False, [finding("E_UNKNOWN_NOT_SATISFIED", criterion)]
    if item.get("result") != "pass":
        return False, []
    level = CRITERION_LEVEL[criterion]
    needed = set(EVIDENCE_CLASSES_BY_LEVEL[level])
    if not needed.issubset(set(item.get("classes", []))):
        return False, [finding("E_EVIDENCE_CLASS", criterion)]
    provenance = item.get("provenance", {})
    checks = (
        ("subject", "E_SUBJECT_MISMATCH"),
        ("repository", "E_REPOSITORY_MISMATCH"),
        ("contract_set", "E_CONTRACT_MISMATCH"),
    )
    for key, code in checks:
        if provenance.get(key) != assessment.get(key):
            return False, [finding(code, criterion)]
    if provenance.get("source_revision") != assessment.get("source_revision"):
        if not equivalence_covers(item, "source_revision", criterion):
            return False, [finding("E_REVISION_MISMATCH", criterion)]
    if provenance.get("artifact") != assessment.get("artifact"):
        if not equivalence_covers(item, "artifact", criterion):
            return False, [finding("E_ARTIFACT_MISMATCH", criterion)]
    context = assessment.get("qualification_context") or {}
    actual_context = item.get("qualification_context_id")
    if actual_context is not None and actual_context != context.get("id"):
        if not equivalence_covers(item, "qualification_context", criterion):
            return False, [finding("E_CONTEXT_MISMATCH", criterion)]
    until = (item.get("validity") or {}).get("valid_until")
    if until:
        now = assessment["evaluation_time"].replace("Z", "+00:00")
        current = datetime.fromisoformat(now)
        expiry = datetime.fromisoformat(until.replace("Z", "+00:00"))
        if current > expiry:
            return False, [finding("E_EXPIRED_EVIDENCE", criterion)]
    if criterion == "R8.3" and not context_adequate(context):
        return False, [finding("E_QUALIFICATION_CONTEXT", criterion)]
    if criterion.startswith("R9."):
        if not operational_adequate(item.get("operational")):
            return False, [finding("E_OPERATIONAL_PROOF_INSUFFICIENT", criterion)]
    return True, []


def satisfied_criteria(assessment: dict):
    satisfied, findings = set(), []
    for criterion in ALL_CRITERIA:
        local = []
        for item in assessment.get("evidence", []):
            ok, errors = evidence_supports(item, assessment, criterion)
            local += errors
            if ok:
                satisfied.add(criterion)
                break
        else:
            findings += local
    return satisfied, sorted(set(findings))


def derive_candidate(assessment: dict):
    satisfied, _ = satisfied_criteria(assessment)
    required, highest = set(), 0
    for level in range(1, 10):
        required.update(CRITERIA_BY_LEVEL[level])
        if required.issubset(satisfied):
            highest = level
        else:
            break
    return highest if highest else "unassessed"


def requires_requalification(change_impact: object) -> bool:
    if not isinstance(change_impact, dict):
        return False
    if not change_impact.get("material_boundary_crossed"):
        return False
    return any(
        item in FUNDAMENTAL_TRIGGERS
        for item in change_impact.get("triggers", [])
    )


def evaluate(assessment: dict) -> dict:
    errors = validate_assessment(assessment)
    prior = assessment.get("prior_established")
    if errors:
        return _result("unassessed", None, False, prior, errors)
    candidate = derive_candidate(assessment)
    _, findings = satisfied_criteria(assessment)
    established = candidate if isinstance(candidate, int) else None
    requalify = False
    if assessment["mode"] == "preservation":
        established = None
        impact = assessment.get("change_impact") or {}
        if requires_requalification(impact):
            requalify = True
            findings.append(finding("E_REQUALIFICATION_REQUIRED", "$.change_impact"))
        elif prior and prior.get("subject") != assessment.get("subject"):
            requalify = True
            findings.append(finding("E_REQUALIFICATION_REQUIRED", "$.subject"))
        elif impact.get("lineage_valid") is not True:
            findings.append(finding("E_LINEAGE", "$.change_impact.lineage_valid"))
        elif prior and isinstance(candidate, int):
            if candidate >= prior.get("level", 10):
                established = prior["level"]
    return _result(candidate, established, requalify, prior, findings)


def _result(candidate, established, requalify, prior, findings):
    return {
        "candidate": candidate,
        "assessed": candidate,
        "established": established,
        "requalification_required": requalify,
        "historical_established": prior,
        "findings": sorted(set(findings)),
    }


def validate_governance_inference(claim: str) -> list[str]:
    if claim in PROHIBITED_GOVERNANCE_INFERENCES:
        return [finding("E_SECURITY_INFERENCE", claim)]
    return []
