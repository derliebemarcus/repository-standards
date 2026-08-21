from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "ticket-specification-v3.json"
SCHEMA = ROOT / "schemas" / "ticket-specification-v3.schema.json"
STANDARD = ROOT / "standards" / "ticket-specification" / "v3" / "standard.md"
TEMPLATES = (
    "epic.md",
    "story.md",
    "bug.md",
    "security.md",
    "documentation.md",
    "testing.md",
)
IMMUTABLE_BLOBS = {
    "standards/ticket-specification/v1/standard.md":
        "baf0a273861b725996bcb2d7a99309b9a33c3372",
    "profiles/ticket-specification-v1.json":
        "07f21a914a0a9c4fe1e665946a202bf73acc7280",
    "schemas/ticket-specification-v1.schema.json":
        "6f469a4bc748a078824116c182c69c0de8b6fec0",
    "reference/ai/ticket-authoring-v1.md":
        "ac1e71966b60146e39ac827e2942702d918a5625",
    "standards/ticket-specification/v2/standard.md":
        "332185e721c31c865ff2d62383d3df93cafc17e7",
    "profiles/ticket-specification-v2.json":
        "22c461f45e388ae34b1f5aa302e554e02f785afb",
    "schemas/ticket-specification-v2.schema.json":
        "7b1378a1bbc465054f5563ec3ea213f3d0a8575f",
    "reference/ai/ticket-authoring-v2.md":
        "0e1638830f06b8eacaa1d8687805854e45851e2f",
}


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


class TicketSpecificationV3Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.standard = STANDARD.read_text(encoding="utf-8")

    def test_estimation_dimensions_and_anchors_are_canonical(self) -> None:
        estimation = self.profile["estimation"]
        self.assertEqual(
            ["effort", "complexity", "risk", "uncertainty"],
            estimation["dimensions"],
        )
        self.assertEqual(
            [1, 2, 3, 5, 8, 13],
            [anchor["value"] for anchor in estimation["anchors"]],
        )
        for anchor in estimation["anchors"]:
            self.assertTrue(anchor["summary"].strip())

    def test_mechanical_time_and_size_proxies_are_forbidden(self) -> None:
        proxies = set(self.profile["estimation"]["forbidden_proxies"])
        self.assertTrue(
            {
                "hours",
                "person-days",
                "calendar-duration",
                "file-count",
                "task-count",
                "lines-of-code",
                "single-dimension",
            }.issubset(proxies)
        )
        self.assertIn("MUST NOT be derived from or converted to hours", self.standard)

    def test_estimate_13_is_exceptional_and_split_is_explicit(self) -> None:
        thirteen = self.profile["estimation"]["estimate_13"]
        self.assertTrue(thirteen["exceptional"])
        self.assertTrue(thirteen["requires_documented_justification"])
        self.assertTrue(thirteen["requires_split_consideration"])
        self.assertEqual(
            8,
            self.profile["label_categories"]["estimate"]["split_threshold"],
        )

    def test_v2_lifecycle_and_estimate_values_are_preserved(self) -> None:
        v2 = json.loads(
            (ROOT / "profiles" / "ticket-specification-v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(v2["lifecycle"], self.profile["lifecycle"])
        self.assertEqual(
            v2["label_categories"]["estimate"]["values"],
            self.profile["label_categories"]["estimate"]["values"],
        )
        rules = json.dumps(self.schema["allOf"], sort_keys=True)
        self.assertIn('"const": "closed"', rules)
        self.assertIn('"const": "open"', rules)
        self.assertIn('"const": "Status/Done"', rules)

    def test_released_ticket_v1_and_v2_assets_are_byte_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_BLOBS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))

    def test_v3_generated_assets_match_committed_assets(self) -> None:
        generator = ROOT / "tools" / "render_ticket_assets_v3.py"
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
                        output_root / "reference" / "issue-templates" / template
                    )
                    committed = ROOT / "reference" / "issue-templates" / template
                    self.assertEqual(committed.read_bytes(), generated.read_bytes())

            generated_adapter = (
                output_root / "reference" / "ai" / "ticket-authoring-v3.md"
            )
            committed_adapter = (
                ROOT / "reference" / "ai" / "ticket-authoring-v3.md"
            )
            self.assertEqual(
                committed_adapter.read_bytes(),
                generated_adapter.read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
