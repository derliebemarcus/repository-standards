#!/usr/bin/env python3
"""Validate repository-owned Product/System Readiness v1 intent surfaces."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from tools import product_system_readiness_model as contract
from tools.repository_contract import ContractError, parse_yaml_subset

ROOT_FIELDS = {"schema", "applicability", "rationale", "subjects"}
SUBJECT_FIELDS = {"kind", "identity", "long_term_target", "stage"}
IDENTITY = re.compile(
    r"^(product|system):[a-z0-9](?:[a-z0-9._/-]*[a-z0-9])?$"
)
DERIVED_ALIASES = contract.DERIVED_AUTHORITY_FIELDS | {
    "actual",
    "actual_trl",
    "actual_readiness",
    "current",
    "current_readiness",
    "candidate_readiness",
    "assessed_readiness",
    "established_readiness",
    "preservation",
    "requalification",
}


def finding(code: str, path: str) -> str:
    return f"{code}:{path}"


def normalize_yaml_scalars(value: object) -> object:
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if isinstance(value, list):
        return [normalize_yaml_scalars(item) for item in value]
    if isinstance(value, dict):
        return {
            key: normalize_yaml_scalars(item)
            for key, item in value.items()
        }
    return value


def load_declaration(path: Path) -> dict[str, object]:
    parsed = normalize_yaml_scalars(parse_yaml_subset(path))
    if not isinstance(parsed, dict):
        raise ContractError("readiness declaration root must be a mapping")
    return parsed


def _reject_fields(
    raw: dict[str, object],
    allowed: set[str],
    path: str,
    errors: list[str],
) -> None:
    for key in sorted(set(raw) - allowed):
        if key in DERIVED_ALIASES:
            errors.append(finding("E_AUTHORED_CURRENT_READINESS", f"{path}.{key}"))
        elif key == "increment_targets":
            errors.append(finding("E_INCREMENT_TARGET_TICKET_OWNED", f"{path}.{key}"))
        else:
            errors.append(finding("E_UNKNOWN_FIELD", f"{path}.{key}"))


def validate_declaration(raw: object) -> list[str]:
    if not isinstance(raw, dict):
        return [finding("E_SCHEMA", "$")]

    errors = list(contract.validate_intent(raw))
    _reject_fields(raw, ROOT_FIELDS, "$", errors)

    subjects = raw.get("subjects")
    if not isinstance(subjects, list):
        return sorted(set(errors))

    seen: set[str] = set()
    for index, subject in enumerate(subjects):
        path = f"$.subjects[{index}]"
        if not isinstance(subject, dict):
            continue
        _reject_fields(subject, SUBJECT_FIELDS, path, errors)

        identity = subject.get("identity")
        kind = subject.get("kind")
        if isinstance(identity, str):
            match = IDENTITY.fullmatch(identity)
            if not match or match.group(1) != kind:
                errors.append(finding("E_SUBJECT_IDENTITY", f"{path}.identity"))
            if identity in seen:
                errors.append(finding("E_DUPLICATE_SUBJECT", f"{path}.identity"))
            seen.add(identity)

        stage = subject.get("stage")
        if stage is not None and (
            not isinstance(stage, str) or not stage.strip()
        ):
            errors.append(finding("E_STAGE", f"{path}.stage"))

    return sorted(set(errors))


def validate_epic_completion(
    ticket: object,
    assessment: object | None,
) -> list[str]:
    if not isinstance(ticket, dict):
        return [finding("E_TICKET", "$")]
    increment = ticket.get("product_increment")
    if ticket.get("kind") != "Kind/Epic" or not isinstance(increment, dict):
        return []
    if ticket.get("status") != "Status/Done":
        return []

    errors: list[str] = []
    if not isinstance(increment.get("assessment"), dict):
        errors.append(finding("E_READINESS_EVIDENCE_REQUIRED", "$.product_increment.assessment"))
    if not isinstance(assessment, dict):
        errors.append(finding("E_READINESS_EVIDENCE_REQUIRED", "$assessment"))
        return sorted(set(errors))

    subject = assessment.get("subject")
    if not isinstance(subject, dict) or (
        subject.get("identity") != increment.get("subject_identity")
    ):
        errors.append(finding("E_SUBJECT_MISMATCH", "$assessment.subject"))
        return sorted(set(errors))

    result = contract.evaluate(assessment)
    assessed = result.get("assessed")
    target = increment.get("readiness_target")
    if not isinstance(assessed, int):
        errors.append(finding("E_READINESS_NOT_ASSESSED", "$assessment"))
    elif not isinstance(target, int) or isinstance(target, bool) or target not in range(1, 10):
        errors.append(finding("E_TARGET", "$.product_increment.readiness_target"))
    elif assessed < target:
        errors.append(finding("E_INCREMENT_TARGET_UNMET", "$assessment"))
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "declaration",
        nargs="?",
        type=Path,
        default=Path(".product-readiness.yml"),
    )
    args = parser.parse_args()
    try:
        declaration = load_declaration(args.declaration)
    except ContractError as exc:
        print(f"ERROR: {exc}")
        return 1
    errors = validate_declaration(declaration)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Product/System Readiness declaration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
