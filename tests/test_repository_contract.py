from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "repository_contract.py"
SPEC = importlib.util.spec_from_file_location("repository_contract", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
CONTRACT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CONTRACT
SPEC.loader.exec_module(CONTRACT)

DECLARATION = """\
standard_version: 1
ruleset_version: 1.1.0
profile: library
docs_roots:
  - docs
  - README.md
required_documents:
  - README.md
  - CONTRIBUTING.md
  - SECURITY.md
  - SUPPORT.md
ignored_paths:
  - coverage/
  - dist/
  - "*.lock"
maintenance:
  require_impact_decision: true
  mappings:
    - source:
        - src/**
      documentation:
        - README.md
        - docs/reference/**
    - source:
        - Jenkinsfile
      documentation:
        - docs/how-to/**
        - docs/operations/**
"""

UPDATED_BODY = """\
## Documentation impact

- [x] Documentation updated in this pull request.
- [ ] No documentation impact.

Affected documentation:

- `docs/reference/interfaces.md`

No-impact justification:

Not applicable.

## Validation

Contract tests.
"""

NO_IMPACT_BODY = """\
## Documentation impact

- [ ] Documentation updated in this pull request.
- [x] No documentation impact.

Affected documentation:

No files.

No-impact justification:

The test fixture changes only an isolated test-data file and leaves behavior unchanged.

## Validation

Contract tests.
"""


class RepositoryImpactContractTest(unittest.TestCase):
    def create_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".repository-documentation.yml").write_text(
            DECLARATION,
            encoding="utf-8",
        )
        (root / "docs").mkdir()
        for name in ("README.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md"):
            (root / name).write_text(f"# {name}\n", encoding="utf-8")
        return temporary, root

    def load_declaration(self, root: Path) -> dict[str, object]:
        return CONTRACT.normalize_declaration(
            CONTRACT.parse_yaml_subset(root / ".repository-documentation.yml")
        )

    def test_nested_declaration_validates(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        self.assertEqual([], CONTRACT.validate_declaration(root, declaration))

    def test_source_with_mapped_documentation_passes(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        errors = CONTRACT.validate_impact(
            ["src/card.js", "docs/reference/interfaces.md"],
            declaration,
            UPDATED_BODY,
        )

        self.assertEqual([], errors)

    def test_source_without_mapped_documentation_fails(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        errors = CONTRACT.validate_impact(
            ["src/card.js"],
            declaration,
            UPDATED_BODY,
        )

        self.assertTrue(any("requires documentation update" in error for error in errors))

    def test_no_impact_passes_without_mapping_violation(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        errors = CONTRACT.validate_impact(
            ["tests/fixtures/sample.json"],
            declaration,
            NO_IMPACT_BODY,
        )

        self.assertEqual([], errors)

    def test_no_impact_fails_for_mapped_source(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        errors = CONTRACT.validate_impact(
            ["Jenkinsfile"],
            declaration,
            NO_IMPACT_BODY,
        )

        self.assertTrue(any("not allowed" in error for error in errors))

    def test_missing_explicit_decision_fails(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        errors = CONTRACT.validate_impact(
            ["README.md"],
            declaration,
            "## Summary\n\nNo impact section.\n",
        )

        self.assertTrue(any("Documentation impact" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
