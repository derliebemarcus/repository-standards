#!/usr/bin/env python3
"""Reference validator for Repository Localization v1 declarations."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .repository_contract import ContractError as YamlContractError, parse_yaml_subset
except ImportError:  # pragma: no cover - script execution path
    from repository_contract import ContractError as YamlContractError, parse_yaml_subset

ISO_639_1_CODES = {
    'aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'be', 'bg',
    'bi', 'bm', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy',
    'da', 'de', 'dv', 'dz', 'ee', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 'fj',
    'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht',
    'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv',
    'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'ku', 'kv', 'kw', 'ky',
    'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn',
    'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny',
    'oc', 'oj', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru',
    'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr',
    'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr',
    'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi',
    'yo', 'za', 'zh', 'zu',
}
ROOT_KEYS = {
    "version",
    "web-application-baseline",
    "default-language",
    "supported-languages",
}


class LocalizationContractError(ValueError):
    """Raised when Repository Localization metadata violates the released contract."""


def validate_language(value: object) -> str:
    if not isinstance(value, str):
        raise LocalizationContractError("language code must be a string")
    if value not in ISO_639_1_CODES:
        raise LocalizationContractError(
            f"language code must be a lowercase ISO 639-1 identifier: {value!r}"
        )
    return value


def validate_declaration(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise LocalizationContractError("declaration root must be a mapping")
    if set(raw) != ROOT_KEYS:
        unknown = sorted(set(raw) - ROOT_KEYS)
        missing = sorted(ROOT_KEYS - set(raw))
        raise LocalizationContractError(
            f"declaration root keys invalid; missing={missing}, unknown={unknown}"
        )
    if raw.get("version") != 1:
        raise LocalizationContractError("version must be 1")
    if raw.get("web-application-baseline") != "v3":
        raise LocalizationContractError("web-application-baseline must be v3")

    default_language = validate_language(raw.get("default-language"))
    supported = raw.get("supported-languages")
    if not isinstance(supported, list) or not supported:
        raise LocalizationContractError("supported-languages must be a non-empty list")

    normalized = [validate_language(value) for value in supported]
    if len(set(normalized)) != len(normalized):
        raise LocalizationContractError("supported-languages must not contain duplicates")
    if normalized.count(default_language) != 1:
        raise LocalizationContractError(
            "default-language must occur exactly once in supported-languages"
        )

    return {
        "default-language": default_language,
        "supported-languages": normalized,
    }


def load_and_validate(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise LocalizationContractError(f"missing declaration: {path}")
    try:
        raw = parse_yaml_subset(path)
    except (YamlContractError, OSError) as exc:
        raise LocalizationContractError(str(exc)) from exc
    return validate_declaration(raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(".repository-localization.yml"),
    )
    args = parser.parse_args()
    try:
        localization = load_and_validate(args.path)
    except LocalizationContractError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("Repository Localization v1 validation passed")
    print(f"default-language={localization['default-language']}")
    print("supported-languages=" + ",".join(localization["supported-languages"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
