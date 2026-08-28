#!/usr/bin/env python3
"""Reference validator for Repository Environments v1 declarations."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .repository_contract import ContractError as YamlContractError, parse_yaml_subset
except ImportError:  # pragma: no cover - script execution path
    from repository_contract import ContractError as YamlContractError, parse_yaml_subset

CANONICAL_ENVIRONMENTS = ("DEV", "STAGING", "PROD")
ROOT_KEYS = {"version", "deployment-environments", "environments"}


class EnvironmentContractError(ValueError):
    """Raised when Repository Environments metadata violates the released contract."""


def validate_web_url(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EnvironmentContractError("url must be a non-empty string")
    if value != value.strip() or any(character.isspace() for character in value):
        raise EnvironmentContractError("url must not contain surrounding or embedded whitespace")
    try:
        parsed = urlsplit(value)
        _ = parsed.port
    except ValueError as exc:
        raise EnvironmentContractError(f"invalid url: {value!r}") from exc
    if parsed.scheme not in {"http", "https"}:
        raise EnvironmentContractError("url scheme must be http or https")
    if not parsed.hostname:
        raise EnvironmentContractError("url must contain a host")
    if parsed.username is not None or parsed.password is not None:
        raise EnvironmentContractError("url userinfo and credentials are forbidden")
    if parsed.fragment:
        raise EnvironmentContractError("url fragments are forbidden")
    return value


def validate_declaration(raw: object) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise EnvironmentContractError("declaration root must be a mapping")
    if set(raw) != ROOT_KEYS:
        unknown = sorted(set(raw) - ROOT_KEYS)
        missing = sorted(ROOT_KEYS - set(raw))
        raise EnvironmentContractError(
            f"declaration root keys invalid; missing={missing}, unknown={unknown}"
        )
    if raw.get("version") != 1:
        raise EnvironmentContractError("version must be 1")
    if raw.get("deployment-environments") != "v2":
        raise EnvironmentContractError("deployment-environments must be v2")

    environments = raw.get("environments")
    if not isinstance(environments, dict) or not environments:
        raise EnvironmentContractError("environments must be a non-empty mapping")

    unknown_environments = sorted(set(environments) - set(CANONICAL_ENVIRONMENTS))
    if unknown_environments:
        raise EnvironmentContractError(
            f"unknown environment keys: {', '.join(unknown_environments)}"
        )

    result: dict[str, str] = {}
    for environment in CANONICAL_ENVIRONMENTS:
        if environment not in environments:
            continue
        entry = environments[environment]
        if not isinstance(entry, dict):
            raise EnvironmentContractError(f"{environment} must be a mapping")
        if set(entry) != {"url"}:
            unknown = sorted(set(entry) - {"url"})
            missing = [] if "url" in entry else ["url"]
            raise EnvironmentContractError(
                f"{environment} fields invalid; missing={missing}, unknown={unknown}"
            )
        result[environment] = validate_web_url(entry.get("url"))
    return result


def load_and_validate(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise EnvironmentContractError(f"missing declaration: {path}")
    try:
        raw = parse_yaml_subset(path)
    except (YamlContractError, OSError) as exc:
        raise EnvironmentContractError(str(exc)) from exc
    return validate_declaration(raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path(".repository-environments.yml"))
    args = parser.parse_args()
    try:
        environments = load_and_validate(args.path)
    except EnvironmentContractError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("Repository Environments v1 validation passed")
    for environment in CANONICAL_ENVIRONMENTS:
        if environment in environments:
            print(f"{environment}={environments[environment]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
