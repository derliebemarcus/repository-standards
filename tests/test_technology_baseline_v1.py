from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PERSONAL_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def declaration_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        if raw_line == raw_line.lstrip() and raw_line.endswith(":"):
            section = raw_line[:-1]
            continue
        key, separator, value = raw_line.strip().partition(":")
        if not separator:
            continue
        normalized = value.strip().strip('"')
        values[f"{section}.{key}" if section else key] = normalized
    return values


class TechnologyBaselineV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard_path = ROOT / "standards" / "technology-baseline" / "v1" / "standard.md"
        cls.standard = cls.standard_path.read_text(encoding="utf-8")
        cls.profile = json.loads(
            (ROOT / "profiles" / "technology-baseline-v1.json").read_text(encoding="utf-8")
        )
        cls.schema = json.loads(
            (ROOT / "schemas" / "repository-standards-v6.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.compatibility = json.loads(
            (
                ROOT
                / "profiles"
                / "repository-standards-compatibility-v5.json"
            ).read_text(encoding="utf-8")
        )

    def test_normative_standard_uses_bcp14_and_approved_initial_baseline(self) -> None:
        self.assertIn("RFC 2119", self.standard)
        self.assertIn("RFC 8174", self.standard)
        self.assertIn("OpenJDK 25", self.standard)
        self.assertIn("Node.js 24", self.standard)
        self.assertIn("Python 3.14", self.standard)
        self.assertIn("PostgreSQL 18", self.standard)
        self.assertIn("PostGIS 3.6", self.standard)
        self.assertIn("90 calendar days", self.standard)
        self.assertIn("at least weekly", self.standard)
        self.assertIn("at least quarterly", self.standard)

    def test_machine_readable_profile_matches_decision(self) -> None:
        self.assertEqual("1.0.0", self.profile["version"])
        self.assertEqual("25", self.profile["technologies"]["java"]["initial_line"])
        self.assertEqual("24", self.profile["technologies"]["nodejs"]["initial_line"])
        self.assertEqual("3.14", self.profile["technologies"]["python"]["initial_line"])
        self.assertEqual("18", self.profile["technologies"]["postgresql"]["initial_line"])
        self.assertEqual("3.6", self.profile["technologies"]["postgis"]["initial_line"])
        self.assertEqual(90, self.profile["review"]["migration_window_days"])
        self.assertLessEqual(
            self.profile["review"]["automated_check_max_interval_days"], 7
        )
        self.assertFalse(self.profile["containers"]["latest_tag_allowed"])
        self.assertEqual(
            "block", self.profile["findings"]["deadline_expiry_consumer_gate"]
        )

    def test_externalized_contract_uses_placeholder_and_no_personal_email(self) -> None:
        placeholder = "${TECHNOLOGY_BASELINE_NOTIFICATION_EMAIL}"
        self.assertIn(placeholder, self.standard)
        self.assertEqual(
            placeholder,
            self.profile["externalization"]["notification_address_placeholder"],
        )
        self.assertFalse(PERSONAL_EMAIL.search(self.standard))
        self.assertFalse(PERSONAL_EMAIL.search(json.dumps(self.profile, sort_keys=True)))

    def test_declaration_v6_requires_technology_baseline(self) -> None:
        self.assertEqual(6, self.schema["properties"]["version"]["const"])
        alternatives = self.schema["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        for alternative in alternatives:
            self.assertIn("technology-baseline", alternative["required"])
            self.assertEqual(
                "v1", alternative["properties"]["technology-baseline"]["const"]
            )

    def test_compatibility_profile_adds_exact_v6_pairings(self) -> None:
        pairings = [
            item
            for item in self.compatibility["pairings"]
            if item["declaration_schema"] == "v6"
        ]
        self.assertEqual(2, len(pairings))
        for pairing in pairings:
            self.assertEqual("v3", pairing["ticket_specification"])
            self.assertEqual("v5", pairing["development_workflow"])
            self.assertEqual("v1", pairing["technology_baseline"])
            self.assertEqual("supported", pairing["status"])

    def test_v6_reference_declarations_are_consistent(self) -> None:
        expectations = (
            ("repository-standards-v6.single.yml", "single", False),
            ("repository-standards-v6.integration.yml", "integration", False),
            ("repository-standards-v6.web.single.yml", "single", True),
            ("repository-standards-v6.web.integration.yml", "integration", True),
        )
        for name, model, web in expectations:
            with self.subTest(name=name):
                values = declaration_values(ROOT / "reference" / name)
                self.assertEqual("6", values["version"])
                self.assertEqual("v3", values["standards.ticket-specification"])
                self.assertEqual("v5", values["standards.development-workflow"])
                self.assertEqual("v1", values["standards.repository-documentation"])
                self.assertEqual("v1", values["standards.technology-baseline"])
                self.assertEqual(model, values["branching.model"])
                if web:
                    self.assertEqual(
                        "v1", values["standards.web-application-baseline"]
                    )
                    self.assertEqual(
                        "v1", values["standards.deployment-environments"]
                    )


if __name__ == "__main__":
    unittest.main()
