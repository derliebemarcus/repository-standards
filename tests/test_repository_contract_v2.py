from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
MODULE_PATH = TOOLS / "repository_contract_v2.py"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

SPEC = importlib.util.spec_from_file_location("repository_contract_v2", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)

DECLARATION = """\
documentation:
  standard: repository-documentation
  standard_version: 2
  ruleset_version: 2.0.0
  profile: library
  architecture: arc42-lite
  diagrams: c4
  decisions: madr
  publishing: none
"""


class RepositoryContractV2Test(unittest.TestCase):
    def create_repository(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".repository-documentation.yml").write_text(
            DECLARATION,
            encoding="utf-8",
        )
        (root / "docs").mkdir()
        for name in (
            "README.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "SUPPORT.md",
        ):
            (root / name).write_text(f"# {name}\n", encoding="utf-8")
        return temporary, root

    def load_declaration(self, root: Path) -> dict[str, object]:
        raw = CONTRACT.base.parse_yaml_subset(
            root / ".repository-documentation.yml"
        )
        return CONTRACT.base.normalize_declaration(raw)

    def test_v2_declaration_validates(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)

        self.assertEqual([], CONTRACT.validate_declaration(root, declaration))

    def test_v1_declaration_is_rejected_by_v2_validator(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)
        declaration["standard_version"] = 1
        declaration["ruleset_version"] = "1.2.0"

        errors = CONTRACT.validate_declaration(root, declaration)

        self.assertIn("standard_version must be 2", errors)
        self.assertIn(
            "ruleset_version must belong to Repository Documentation v2",
            errors,
        )

    def test_wrong_ruleset_major_is_rejected(self) -> None:
        temporary, root = self.create_repository()
        self.addCleanup(temporary.cleanup)
        declaration = self.load_declaration(root)
        declaration["ruleset_version"] = "1.2.0"

        errors = CONTRACT.validate_declaration(root, declaration)

        self.assertIn(
            "ruleset_version must belong to Repository Documentation v2",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
