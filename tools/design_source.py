#!/usr/bin/env python3
"""Reference validator for Design Source Declaration v1."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from .repository_contract import ContractError as YamlContractError, parse_yaml_subset
except ImportError:  # pragma: no cover - script execution path
    from repository_contract import ContractError as YamlContractError, parse_yaml_subset

ROOT_REQUIRED_KEYS = {"version", "source"}
ROOT_OPTIONAL_KEYS = {"automation"}
SOURCE_KEYS = {"provider", "team", "project"}
IDENTITY_REQUIRED_KEYS = {"id"}
IDENTITY_OPTIONAL_KEYS = {"name"}
AUTOMATION_KEYS = {"interface"}
SUPPORTED_PROVIDERS = {"penpot"}
SUPPORTED_AUTOMATION_INTERFACES = {"penpot-rpc"}
UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


class DesignSourceContractError(ValueError):
    """Raised when design-source metadata violates the released contract."""


def _validate_exact_keys(
    value: object,
    required: set[str],
    optional: set[str],
    context: str,
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise DesignSourceContractError(f"{context} must be a mapping")
    keys = set(value)
    missing = sorted(required - keys)
    unknown = sorted(keys - required - optional)
    if missing or unknown:
        raise DesignSourceContractError(
            f"{context} fields invalid; missing={missing}, unknown={unknown}"
        )
    return value


def _validate_identity(value: object, context: str) -> dict[str, str]:
    identity = _validate_exact_keys(
        value,
        IDENTITY_REQUIRED_KEYS,
        IDENTITY_OPTIONAL_KEYS,
        context,
    )
    raw_id = identity.get("id")
    if not isinstance(raw_id, str) or not UUID_RE.fullmatch(raw_id):
        raise DesignSourceContractError(f"{context}.id must be a UUID")

    result = {"id": raw_id}
    if "name" in identity:
        raw_name = identity.get("name")
        if (
            not isinstance(raw_name, str)
            or not raw_name.strip()
            or raw_name != raw_name.strip()
        ):
            raise DesignSourceContractError(
                f"{context}.name must be a non-empty trimmed string"
            )
        result["name"] = raw_name
    return result


def validate_declaration(raw: object) -> dict[str, object]:
    root = _validate_exact_keys(
        raw,
        ROOT_REQUIRED_KEYS,
        ROOT_OPTIONAL_KEYS,
        "declaration root",
    )
    if root.get("version") != 1:
        raise DesignSourceContractError("version must be 1")

    source = _validate_exact_keys(root.get("source"), SOURCE_KEYS, set(), "source")
    provider = source.get("provider")
    if provider not in SUPPORTED_PROVIDERS:
        raise DesignSourceContractError(f"unsupported design provider: {provider!r}")

    team = _validate_identity(source.get("team"), "source.team")
    project = _validate_identity(source.get("project"), "source.project")

    result: dict[str, object] = {
        "version": 1,
        "source": {
            "provider": provider,
            "team": team,
            "project": project,
        },
    }

    if "automation" in root:
        automation = _validate_exact_keys(
            root.get("automation"), AUTOMATION_KEYS, set(), "automation"
        )
        interface = automation.get("interface")
        if interface not in SUPPORTED_AUTOMATION_INTERFACES:
            raise DesignSourceContractError(
                f"unsupported automation interface: {interface!r}"
            )
        if interface == "penpot-rpc" and provider != "penpot":
            raise DesignSourceContractError("penpot-rpc requires provider penpot")
        result["automation"] = {"interface": interface}

    return result


def validate_design_contract_source(
    declaration: dict[str, object],
    *,
    provider: str,
    project_id: str,
) -> None:
    """Validate project-level provenance for a concrete Design Contract."""
    validated = validate_declaration(declaration)
    source = validated["source"]
    assert isinstance(source, dict)
    declared_provider = source["provider"]
    project = source["project"]
    assert isinstance(project, dict)
    declared_project_id = project["id"]

    if provider != declared_provider:
        raise DesignSourceContractError(
            f"Design Contract provider mismatch: declared={declared_provider!r}, "
            f"contract={provider!r}"
        )
    if project_id != declared_project_id:
        raise DesignSourceContractError(
            "Design Contract project mismatch: "
            f"declared={declared_project_id!r}, contract={project_id!r}"
        )


def load_and_validate(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise DesignSourceContractError(f"missing declaration: {path}")
    try:
        raw = parse_yaml_subset(path)
    except (YamlContractError, OSError) as exc:
        raise DesignSourceContractError(str(exc)) from exc
    return validate_declaration(raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", nargs="?", type=Path, default=Path(".repository-design-source.yml")
    )
    args = parser.parse_args()
    try:
        declaration = load_and_validate(args.path)
    except DesignSourceContractError as exc:
        print(f"ERROR: {exc}")
        return 1

    source = declaration["source"]
    assert isinstance(source, dict)
    team = source["team"]
    project = source["project"]
    assert isinstance(team, dict)
    assert isinstance(project, dict)
    print("Design Source Declaration v1 validation passed")
    print(f"provider={source['provider']}")
    print(f"team_id={team['id']}")
    print(f"project_id={project['id']}")
    if "automation" in declaration:
        automation = declaration["automation"]
        assert isinstance(automation, dict)
        print(f"automation={automation['interface']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
