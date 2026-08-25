#!/usr/bin/env python3
"""Validate Repository Documentation v2 declarations and impact decisions."""

from __future__ import annotations

from pathlib import Path

import repository_contract as base


def validate_declaration(
    root: Path,
    declaration: dict[str, object],
) -> list[str]:
    """Validate v2 identity plus the shared objective documentation invariants."""
    errors: list[str] = []
    if declaration.get("standard_version") != 2:
        errors.append("standard_version must be 2")

    ruleset = declaration.get("ruleset_version")
    if not isinstance(ruleset, str) or not base.SEMVER_PATTERN.fullmatch(ruleset):
        errors.append("ruleset_version must be a semantic version")
    elif not ruleset.startswith("2."):
        errors.append("ruleset_version must belong to Repository Documentation v2")

    shared_declaration = dict(declaration)
    shared_declaration["standard_version"] = 1
    shared_declaration["ruleset_version"] = "1.0.0"
    errors.extend(base.validate_declaration(root, shared_declaration))
    return errors


def main(argv: list[str] | None = None) -> int:
    args = base.build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        declaration = base.normalize_declaration(
            base.parse_yaml_subset(root / ".repository-documentation.yml")
        )
    except (base.ContractError, OSError) as exc:
        return base.print_errors([str(exc)])

    errors = validate_declaration(root, declaration)
    if args.command == "validate":
        if not errors:
            print("Repository Documentation v2 contract validation passed")
        return base.print_errors(errors)

    if errors:
        return base.print_errors(errors)
    try:
        changed_paths = base.read_changed_paths(args.changed_paths_file)
        pull_request_body = args.pr_body_file.read_text(encoding="utf-8")
    except (base.ContractError, OSError) as exc:
        return base.print_errors([str(exc)])

    errors = base.validate_impact(changed_paths, declaration, pull_request_body)
    if not errors:
        print("Repository Documentation v2 impact validation passed")
    return base.print_errors(errors)


if __name__ == "__main__":
    raise SystemExit(main())
