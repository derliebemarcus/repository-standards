#!/usr/bin/env python3
"""Validate repository documentation declarations and pull-request impact decisions."""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_PROFILES = {"application", "library", "infrastructure"}
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
CHECKBOX_PATTERN = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.+?)\s*$")
UPDATED_LABEL = "Documentation updated in this pull request."
NO_IMPACT_LABEL = "No documentation impact."


class ContractError(Exception):
    """Raised when the repository documentation contract is invalid."""


@dataclass(frozen=True)
class MappingResult:
    source_patterns: tuple[str, ...]
    documentation_patterns: tuple[str, ...]
    changed_sources: tuple[str, ...]
    changed_documentation: tuple[str, ...]


def scalar_value(raw_value: str) -> object:
    value = raw_value.strip()
    if not value:
        return ""
    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in {"'", '"'}
    ):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def yaml_lines(path: Path) -> list[tuple[int, int, str]]:
    parsed: list[tuple[int, int, str]] = []
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "\t" in raw_line:
            raise ContractError(f"{path}:{number}: tabs are not supported")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise ContractError(
                f"{path}:{number}: indentation must use multiples of two spaces"
            )
        parsed.append((number, indent, stripped))
    return parsed


def parse_yaml_subset(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ContractError(f"missing declaration: {path}")
    lines = yaml_lines(path)
    if not lines:
        raise ContractError(f"empty declaration: {path}")

    def parse_block(index: int, indent: int) -> tuple[object, int]:
        if index >= len(lines) or lines[index][1] < indent:
            return {}, index
        is_list = lines[index][2].startswith("- ")
        container: object = [] if is_list else {}

        while index < len(lines):
            number, current_indent, text = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ContractError(f"{path}:{number}: unexpected indentation")

            if is_list:
                if not text.startswith("- "):
                    raise ContractError(
                        f"{path}:{number}: mixed list and mapping syntax"
                    )
                item_text = text[2:].strip()
                if not item_text:
                    if index + 1 >= len(lines) or lines[index + 1][1] <= indent:
                        raise ContractError(f"{path}:{number}: empty list item")
                    item, index = parse_block(index + 1, indent + 2)
                    assert isinstance(container, list)
                    container.append(item)
                    continue

                key, separator, raw_value = item_text.partition(":")
                if separator:
                    item_mapping: dict[str, object] = {}
                    if raw_value.strip():
                        item_mapping[key.strip()] = scalar_value(raw_value)
                        index += 1
                    else:
                        if index + 1 >= len(lines) or lines[index + 1][1] <= indent:
                            item_mapping[key.strip()] = {}
                            index += 1
                        else:
                            value, index = parse_block(index + 1, indent + 4)
                            item_mapping[key.strip()] = value

                    while index < len(lines) and lines[index][1] == indent + 2:
                        child_number, _, child_text = lines[index]
                        child_key, child_separator, child_raw = child_text.partition(":")
                        if not child_separator or child_text.startswith("- "):
                            raise ContractError(
                                f"{path}:{child_number}: expected mapping entry"
                            )
                        child_key = child_key.strip()
                        if child_raw.strip():
                            item_mapping[child_key] = scalar_value(child_raw)
                            index += 1
                        else:
                            if (
                                index + 1 >= len(lines)
                                or lines[index + 1][1] <= indent + 2
                            ):
                                item_mapping[child_key] = {}
                                index += 1
                            else:
                                child_value, index = parse_block(index + 1, indent + 4)
                                item_mapping[child_key] = child_value
                    assert isinstance(container, list)
                    container.append(item_mapping)
                    continue

                assert isinstance(container, list)
                container.append(scalar_value(item_text))
                index += 1
                continue

            if text.startswith("- "):
                raise ContractError(f"{path}:{number}: mixed mapping and list syntax")
            key, separator, raw_value = text.partition(":")
            if not separator or not key.strip():
                raise ContractError(f"{path}:{number}: expected key: value")
            key = key.strip()
            assert isinstance(container, dict)
            if raw_value.strip():
                container[key] = scalar_value(raw_value)
                index += 1
            else:
                if index + 1 >= len(lines) or lines[index + 1][1] <= indent:
                    container[key] = {}
                    index += 1
                else:
                    value, index = parse_block(index + 1, indent + 2)
                    container[key] = value

        return container, index

    parsed, next_index = parse_block(0, lines[0][1])
    if next_index != len(lines) or not isinstance(parsed, dict):
        raise ContractError(f"{path}: declaration root must be a mapping")
    return parsed


def normalize_declaration(raw: dict[str, object]) -> dict[str, object]:
    legacy = raw.get("documentation")
    if isinstance(legacy, dict):
        return {
            "standard_version": legacy.get("standard_version"),
            "ruleset_version": legacy.get("ruleset_version", "1.0.0"),
            "profile": legacy.get("profile"),
            "docs_roots": ["docs", "README.md"],
            "required_documents": [
                "README.md",
                "CONTRIBUTING.md",
                "SECURITY.md",
                "SUPPORT.md",
            ],
            "ignored_paths": [],
            "maintenance": {
                "require_impact_decision": False,
                "mappings": [],
            },
        }
    return raw


def string_list(value: object, field: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty list")
        return []
    strings = [item for item in value if isinstance(item, str) and item.strip()]
    if len(strings) != len(value):
        errors.append(f"{field} must contain only non-empty strings")
    return strings


def validate_declaration(root: Path, declaration: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if declaration.get("standard_version") != 1:
        errors.append("standard_version must be 1")

    ruleset = declaration.get("ruleset_version")
    if not isinstance(ruleset, str) or not SEMVER_PATTERN.fullmatch(ruleset):
        errors.append("ruleset_version must be a semantic version")

    profile = declaration.get("profile")
    if profile not in SUPPORTED_PROFILES:
        errors.append("profile must be application, library, or infrastructure")

    docs_roots = string_list(declaration.get("docs_roots"), "docs_roots", errors)
    required_documents = string_list(
        declaration.get("required_documents"),
        "required_documents",
        errors,
    )
    ignored_paths = declaration.get("ignored_paths", [])
    if not isinstance(ignored_paths, list) or any(
        not isinstance(item, str) or not item.strip() for item in ignored_paths
    ):
        errors.append("ignored_paths must contain only non-empty strings")

    for relative_path in docs_roots:
        if not (root / relative_path).exists():
            errors.append(f"missing documentation root: {relative_path}")
    for relative_path in required_documents:
        if not (root / relative_path).is_file():
            errors.append(f"missing required document: {relative_path}")

    maintenance = declaration.get("maintenance")
    if not isinstance(maintenance, dict):
        errors.append("maintenance must be a mapping")
        return errors
    if not isinstance(maintenance.get("require_impact_decision"), bool):
        errors.append("maintenance.require_impact_decision must be true or false")

    mappings = maintenance.get("mappings")
    if not isinstance(mappings, list):
        errors.append("maintenance.mappings must be a list")
        return errors
    for index, mapping in enumerate(mappings):
        if not isinstance(mapping, dict):
            errors.append(f"maintenance.mappings[{index}] must be a mapping")
            continue
        string_list(mapping.get("source"), f"maintenance.mappings[{index}].source", errors)
        string_list(
            mapping.get("documentation"),
            f"maintenance.mappings[{index}].documentation",
            errors,
        )
    return errors


def path_matches(path: str, pattern: str) -> bool:
    normalized_path = path.lstrip("./")
    normalized_pattern = pattern.lstrip("./")
    if normalized_pattern.endswith("/"):
        return normalized_path.startswith(normalized_pattern)
    return fnmatch.fnmatchcase(normalized_path, normalized_pattern)


def is_ignored(path: str, patterns: list[str]) -> bool:
    return any(path_matches(path, pattern) for pattern in patterns)


def evaluate_mappings(
    changed_paths: list[str],
    declaration: dict[str, object],
) -> list[MappingResult]:
    ignored = declaration.get("ignored_paths", [])
    ignored_patterns = ignored if isinstance(ignored, list) else []
    relevant_paths = [
        path for path in changed_paths if not is_ignored(path, ignored_patterns)
    ]
    maintenance = declaration.get("maintenance")
    mappings = maintenance.get("mappings", []) if isinstance(maintenance, dict) else []
    results: list[MappingResult] = []

    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        source_patterns = tuple(
            item for item in mapping.get("source", []) if isinstance(item, str)
        )
        documentation_patterns = tuple(
            item for item in mapping.get("documentation", []) if isinstance(item, str)
        )
        changed_sources = tuple(
            path
            for path in relevant_paths
            if any(path_matches(path, pattern) for pattern in source_patterns)
        )
        changed_documentation = tuple(
            path
            for path in relevant_paths
            if any(
                path_matches(path, pattern)
                for pattern in documentation_patterns
            )
        )
        if changed_sources:
            results.append(
                MappingResult(
                    source_patterns,
                    documentation_patterns,
                    changed_sources,
                    changed_documentation,
                )
            )
    return results


def section_text(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*{re.escape(heading)}\s*$\n(.*?)(?=^\s*##\s|\Z)"
    )
    match = pattern.search(body)
    return match.group(1).strip() if match else ""


def field_text(section: str, label: str, next_label: str | None = None) -> str:
    if next_label:
        pattern = re.compile(
            rf"(?ims)^\s*{re.escape(label)}\s*$\n(.*?)"
            rf"(?=^\s*{re.escape(next_label)}\s*$|\Z)"
        )
    else:
        pattern = re.compile(rf"(?ims)^\s*{re.escape(label)}\s*$\n(.*)\Z")
    match = pattern.search(section)
    return match.group(1).strip() if match else ""


def parse_impact_decision(body: str) -> tuple[str, str, list[str]]:
    section = section_text(body, "## Documentation impact")
    if not section:
        raise ContractError("pull request body is missing '## Documentation impact'")

    checked: list[str] = []
    for line in section.splitlines():
        match = CHECKBOX_PATTERN.match(line)
        if match and match.group(1).strip().lower() == "x":
            checked.append(match.group(2).strip())

    recognized = [label for label in checked if label in {UPDATED_LABEL, NO_IMPACT_LABEL}]
    if len(recognized) != 1 or len(checked) != 1:
        raise ContractError("select exactly one documentation-impact outcome")

    affected = field_text(
        section,
        "Affected documentation:",
        "No-impact justification:",
    )
    affected_paths = re.findall(r"`([^`]+)`", affected)
    justification = field_text(section, "No-impact justification:")
    decision = "updated" if recognized[0] == UPDATED_LABEL else "none"
    return decision, justification, affected_paths


def validate_impact(
    changed_paths: list[str],
    declaration: dict[str, object],
    pull_request_body: str,
) -> list[str]:
    errors: list[str] = []
    maintenance = declaration.get("maintenance")
    require_decision = (
        maintenance.get("require_impact_decision")
        if isinstance(maintenance, dict)
        else False
    )
    if not require_decision:
        return errors

    try:
        decision, justification, affected_paths = parse_impact_decision(
            pull_request_body
        )
    except ContractError as exc:
        return [str(exc)]

    mapping_results = evaluate_mappings(changed_paths, declaration)
    violations = [result for result in mapping_results if not result.changed_documentation]

    if decision == "updated":
        changed_documentation = {
            path
            for result in mapping_results
            for path in result.changed_documentation
        }
        if violations:
            for result in violations:
                errors.append(
                    "mapped source change requires documentation update: "
                    f"sources={', '.join(result.changed_sources)}; "
                    "expected one of "
                    f"{', '.join(result.documentation_patterns)}"
                )
        if mapping_results and not changed_documentation:
            errors.append("documentation-updated decision has no mapped documentation change")
        if not affected_paths:
            errors.append("affected documentation must list at least one path")
        return errors

    if mapping_results:
        sources = sorted(
            {
                path
                for result in mapping_results
                for path in result.changed_sources
            }
        )
        errors.append(
            "no-impact decision is not allowed for mapped source changes: "
            + ", ".join(sources)
        )
    normalized_justification = " ".join(justification.split())
    placeholders = {
        "",
        "explain specifically why behavior, interfaces, operations, security, "
        "and architecture remain unchanged.",
    }
    if normalized_justification.lower() in placeholders or len(normalized_justification) < 20:
        errors.append(
            "no-impact justification must be specific and at least 20 characters"
        )
    return errors


def read_changed_paths(path: Path) -> list[str]:
    if not path.is_file():
        raise ContractError(f"missing changed-paths file: {path}")
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def print_errors(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--root", type=Path, default=Path("."))

    impact_parser = subparsers.add_parser("impact")
    impact_parser.add_argument("--root", type=Path, default=Path("."))
    impact_parser.add_argument("--changed-paths-file", type=Path, required=True)
    impact_parser.add_argument("--pr-body-file", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        declaration = normalize_declaration(
            parse_yaml_subset(root / ".repository-documentation.yml")
        )
    except (ContractError, OSError) as exc:
        return print_errors([str(exc)])

    errors = validate_declaration(root, declaration)
    if args.command == "validate":
        if not errors:
            print("Repository documentation contract validation passed")
        return print_errors(errors)

    if errors:
        return print_errors(errors)
    try:
        changed_paths = read_changed_paths(args.changed_paths_file)
        pull_request_body = args.pr_body_file.read_text(encoding="utf-8")
    except (ContractError, OSError) as exc:
        return print_errors([str(exc)])
    errors = validate_impact(changed_paths, declaration, pull_request_body)
    if not errors:
        print("Repository documentation impact validation passed")
    return print_errors(errors)


if __name__ == "__main__":
    raise SystemExit(main())
