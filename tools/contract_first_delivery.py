#!/usr/bin/env python3
"""Provider-neutral reference validation for Contract-first Delivery v1."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

ROLES = {
    "design-contract",
    "test-contract",
    "implementation",
    "conformance-evidence",
}
FROZEN_STATUSES = {
    "Status/Ready",
    "Status/In Progress",
    "Status/Review",
    "Status/Done",
}
DONE_STATUS = "Status/Done"


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_artifact(artifact: Any, path: str) -> list[str]:
    if not isinstance(artifact, Mapping):
        return [f"{path} must be an artifact object"]
    errors: list[str] = []
    if not _nonempty(artifact.get("type")):
        errors.append(f"{path}.type must be non-empty")
    if not _nonempty(artifact.get("locator")):
        errors.append(f"{path}.locator must be non-empty")
    if not (
        _nonempty(artifact.get("revision"))
        or _nonempty(artifact.get("digest"))
    ):
        errors.append(f"{path} must contain revision and/or digest")
    return errors


def _validate_reference(
    reference: Any,
    path: str,
    *,
    exact: bool,
) -> list[str]:
    if not isinstance(reference, Mapping):
        return [f"{path} must be a contract reference object"]
    work_item = reference.get("work_item")
    artifact = reference.get("artifact")
    if artifact is None:
        if exact:
            return [f"{path}.artifact must be resolved at this lifecycle state"]
        if not _nonempty(work_item):
            return [f"{path}.work_item is required while artifact is unresolved"]
        return []
    errors = _validate_artifact(artifact, f"{path}.artifact")
    if work_item is not None and not _nonempty(work_item):
        errors.append(f"{path}.work_item must be null or non-empty")
    return errors


def _references(delivery: Mapping[str, Any], key: str) -> list[Any]:
    value = delivery.get(key)
    return value if isinstance(value, list) else []


def validate_ticket(ticket: Mapping[str, Any]) -> list[str]:
    """Validate Ticket Specification v4 Contract-first fields and freeze boundaries."""
    errors: list[str] = []
    delivery = ticket.get("delivery")
    if not isinstance(delivery, Mapping):
        return ["delivery must be an object"]
    if delivery.get("model") != "contract-first-v1":
        errors.append("delivery.model must be contract-first-v1")

    applicability = delivery.get("applicability")
    role = delivery.get("role")
    rationale = delivery.get("rationale")
    design = _references(delivery, "design_contracts")
    tests = _references(delivery, "test_contracts")
    evidence = delivery.get("evidence")
    if not isinstance(evidence, list):
        errors.append("delivery.evidence must be an array")
        evidence = []

    if applicability == "not-applicable":
        if not _nonempty(rationale):
            errors.append("not-applicable requires a non-empty rationale")
        if role is not None:
            errors.append("not-applicable requires role=null")
        if design or tests or evidence:
            errors.append("not-applicable requires empty contract/evidence arrays")
        return errors

    if applicability != "required":
        errors.append("delivery.applicability must be required or not-applicable")
        return errors
    if role not in ROLES:
        errors.append("required applicability needs a valid delivery.role")
        return errors

    status = ticket.get("status")
    exact = status in FROZEN_STATUSES

    if role == "test-contract" and not design:
        errors.append("test-contract requires at least one Design Contract reference")
    if role in {"implementation", "conformance-evidence"}:
        if not design:
            errors.append(f"{role} requires at least one Design Contract reference")
        if not tests:
            errors.append(f"{role} requires at least one Test Contract reference")

    for index, reference in enumerate(design):
        errors.extend(
            _validate_reference(
                reference,
                f"delivery.design_contracts[{index}]",
                exact=exact and role != "design-contract",
            )
        )
    for index, reference in enumerate(tests):
        errors.extend(
            _validate_reference(
                reference,
                f"delivery.test_contracts[{index}]",
                exact=exact and role in {"implementation", "conformance-evidence"},
            )
        )

    if status == DONE_STATUS and role == "implementation" and not evidence:
        errors.append("Done implementation requires Conformance Evidence")
    for index, artifact in enumerate(evidence):
        errors.extend(_validate_artifact(artifact, f"delivery.evidence[{index}]"))
    return errors


def validate_graph(
    implementation: Mapping[str, Any],
    work_items: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    """Validate upstream work-item completion for a frozen implementation."""
    errors = validate_ticket(implementation)
    if errors:
        return errors
    if implementation.get("status") not in FROZEN_STATUSES:
        return []
    delivery = implementation["delivery"]
    if delivery.get("applicability") != "required":
        return []
    if delivery.get("role") != "implementation":
        return []

    for key in ("design_contracts", "test_contracts"):
        for reference in _references(delivery, key):
            work_item = reference.get("work_item")
            if work_item is None:
                continue
            upstream = work_items.get(work_item)
            if upstream is None:
                errors.append(f"referenced upstream work item not found: {work_item}")
                continue
            if upstream.get("status") != DONE_STATUS:
                errors.append(f"upstream work item is not Done: {work_item}")
    return errors


def validate_evidence(evidence: Mapping[str, Any]) -> list[str]:
    """Validate core Contract-first Evidence v1 provenance invariants."""
    errors: list[str] = []
    if evidence.get("schema") != "contract-first-evidence-v1":
        errors.append("evidence.schema must be contract-first-evidence-v1")
    if evidence.get("contract_mutation") is not False:
        errors.append("evidence.contract_mutation must be false")
    if not _nonempty(evidence.get("consumer")):
        errors.append("evidence.consumer must be non-empty")

    for key in ("design_contracts", "test_contracts"):
        references = evidence.get(key)
        if not isinstance(references, list) or not references:
            errors.append(f"evidence.{key} must be a non-empty array")
            continue
        for index, reference in enumerate(references):
            errors.extend(
                _validate_reference(
                    reference,
                    f"evidence.{key}[{index}]",
                    exact=True,
                )
            )

    implementation = evidence.get("implementation")
    if not isinstance(implementation, Mapping):
        errors.append("evidence.implementation must be an object")
    else:
        if not _nonempty(implementation.get("repository")):
            errors.append("evidence.implementation.repository must be non-empty")
        if not _nonempty(implementation.get("revision")):
            errors.append("evidence.implementation.revision must be non-empty")
        artifact = implementation.get("artifact")
        if artifact is not None:
            errors.extend(
                _validate_artifact(artifact, "evidence.implementation.artifact")
            )

    execution = evidence.get("execution")
    if not isinstance(execution, Mapping):
        errors.append("evidence.execution must be an object")
    else:
        for key in ("timestamp", "method", "runner", "result"):
            if not _nonempty(execution.get(key)):
                errors.append(f"evidence.execution.{key} must be non-empty")
    return errors
