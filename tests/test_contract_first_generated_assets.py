from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractFirstGeneratedAssetsTest(unittest.TestCase):
    def run_check(self, script: str) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools" / script), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            0,
            completed.returncode,
            completed.stdout + completed.stderr,
        )

    def test_ticket_v4_assets_are_current(self) -> None:
        self.run_check("render_ticket_assets_v4.py")

    def test_development_workflow_v8_adapter_is_current(self) -> None:
        self.run_check("render_development_workflow_assets_v8.py")


if __name__ == "__main__":
    unittest.main()
