"""Executable Product/System Readiness v1 Test Contract facade.

The semantic oracle and deterministic builders are split for reviewability.
This module remains the stable import surface used by the contract tests.
"""
from tools.product_system_readiness_fixtures import (
    canonical_context,
    canonical_operational_proof,
    make_assessment,
)
from tools.product_system_readiness_model import (
    ALL_CRITERIA,
    CRITERIA_BY_LEVEL,
    CRITERION_LEVEL,
    DERIVED_AUTHORITY_FIELDS,
    DESIGN_CONTRACT_BLOB,
    DESIGN_CONTRACT_LOCATOR,
    DESIGN_CONTRACT_REVISION,
    EVIDENCE_CLASSES_BY_LEVEL,
    FUNDAMENTAL_TRIGGERS,
    MATERIAL_CONTEXT_DIMENSIONS,
    PROHIBITED_GOVERNANCE_INFERENCES,
    TEST_CONTRACT_LOCATOR,
    canonical_contract_set,
    declared_applicability,
    derive_candidate,
    evaluate,
    requires_requalification,
    satisfied_criteria,
    validate_assessment,
    validate_governance_inference,
    validate_intent,
)

__all__ = [
    "ALL_CRITERIA",
    "CRITERIA_BY_LEVEL",
    "CRITERION_LEVEL",
    "DERIVED_AUTHORITY_FIELDS",
    "DESIGN_CONTRACT_BLOB",
    "DESIGN_CONTRACT_LOCATOR",
    "DESIGN_CONTRACT_REVISION",
    "EVIDENCE_CLASSES_BY_LEVEL",
    "FUNDAMENTAL_TRIGGERS",
    "MATERIAL_CONTEXT_DIMENSIONS",
    "PROHIBITED_GOVERNANCE_INFERENCES",
    "TEST_CONTRACT_LOCATOR",
    "canonical_context",
    "canonical_contract_set",
    "canonical_operational_proof",
    "declared_applicability",
    "derive_candidate",
    "evaluate",
    "make_assessment",
    "requires_requalification",
    "satisfied_criteria",
    "validate_assessment",
    "validate_governance_inference",
    "validate_intent",
]
