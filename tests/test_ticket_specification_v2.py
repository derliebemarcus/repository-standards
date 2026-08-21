from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profiles" / "ticket-specification-v2.json"
SCHEMA_PATH = ROOT / "schemas" / "ticket-specification-v2.schema.json"
STANDARD_PATH = (
    ROOT
    / "standards"
    / "ticket-specification"
    / "v2"
    / "standard.md"
)
TEMPLATES = (
    "epic.md",
    "story.md",
    "bug.md",
    "security.md",
    "documentation.md",
    "testing.md",
)
V1_BLOB_SHAS = {
    "standards/ticket-specification/v1/standard.md":
        "baf0a273861b725996bcb2d7a99309b9a33c3372",
    "profiles/ticket-specification-v1.json":
        "07f21a914a0a9c4fe1e665946a202bf73acc7280",
    "schemas/ticket-specification-v1.schema.json":
        "6f469a4bc748a078824116c182c69c0de8b6fec0",
    "reference/ai/ticket-authoring-v1.md":
        "ac1e71966b60146e39ac827e2942702d918a5625",
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def lifecycle_is_canonical(state: str, status: str) -> bool:
    if state == "closed":
        return status == "Status/Done"
    if state == "open":
        return status != "Status/Done"
    return False


class TicketSpecificationV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.standard = STANDARD_PATH.read_text(encoding="utf-8")

    def test_profile_defines_done_lifecycle(self) -> None:
        statuses = self.profile["label_categories"]["status"]["values"]
        lifecycle = self.profile["lifecycle"]

        self.assertIn("Status/Done", statuses)
        self.assertEqual("Status/Done", lifecycle["completed_status"])
        self.assertEqual("closed", lifecycle["completed_state"])
        self.assertEqual("open", lifecycle["open_state"])
        self.assertEqual(
            "replacement-before-removal",
            lifecycle["transition_order"],
        )
        self.assertTrue(lifecycle["reopen_requires_explicit_active_status"])

    def test_canonical_completion_contract(self) -> None:
        self.assertTrue(lifecycle_is_canonical("closed", "Status/Done"))
        self.assertFalse(
            lifecycle_is_canonical("closed", "Status/Review")
        )

    def test_open_done_is_invalid(self) -> None:
        self.assertFalse(lifecycle_is_canonical("open", "Status/Done"))
        self.assertTrue(
            lifecycle_is_canonical("open", "Status/In Progress")
        )

    def test_schema_encodes_state_status_invariants(self) -> None:
        required = self.schema["required"]
        status_values = self.schema["properties"]["status"]["enum"]
        rules = json.dumps(self.schema["allOf"], sort_keys=True)

        self.assertIn("state", required)
        self.assertIn("Status/Done", status_values)
        self.assertIn('"const": "closed"', rules)
        self.assertIn('"const": "open"', rules)
        self.assertIn('"const": "Status/Done"', rules)

    def test_reopen_contract_is_explicit(self) -> None:
        self.assertIn("## Reopening", self.standard)
        self.assertIn("replacement status before removing", self.standard)
        self.assertIn("MUST require an explicit target status", self.standard)

    def test_legacy_compatibility_is_read_only(self) -> None:
        lifecycle = self.profile["lifecycle"]

        self.assertTrue(lifecycle["legacy_closed_read_compatibility"])
        self.assertFalse(lifecycle["legacy_write_compatibility"])
        self.assertIn(
            "Legacy-read compatibility MUST NOT become",
            self.standard,
        )
        self.assertIn(
            "MUST NOT invent retrospective Story Point estimates",
            self.standard,
        )

    def test_v1_contract_is_byte_immutable(self) -> None:
        for relative_path, expected_sha in V1_BLOB_SHAS.items():
            with self.subTest(path=relative_path):
                actual_sha = git_blob_sha(ROOT / relative_path)
                self.assertEqual(expected_sha, actual_sha)

    def test_v2_generated_assets_match_committed_assets(self) -> None:
        generator = ROOT / "tools" / "render_ticket_assets_v2.py"
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory)
            subprocess.run(
                [
                    sys.executable,
                    str(generator),
                    "--root",
                    str(ROOT),
                    "--output",
                    str(output_root),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            for template in TEMPLATES:
                with self.subTest(template=template):
                    generated = (
                        output_root
                        / "reference"
                        / "issue-templates"
                        / template
                    )
                    committed = (
                        ROOT
                        / "reference"
                        / "issue-templates"
                        / template
                    )
                    self.assertEqual(
                        committed.read_bytes(),
                        generated.read_bytes(),
                    )

            generated_adapter = (
                output_root
                / "reference"
                / "ai"
                / "ticket-authoring-v2.md"
            )
            committed_adapter = (
                ROOT
                / "reference"
                / "ai"
                / "ticket-authoring-v2.md"
            )
            self.assertEqual(
                committed_adapter.read_bytes(),
                generated_adapter.read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
