import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DesignSystemDecisionContractTest(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(
            (ROOT / "schemas/design-system-consumer-v1.schema.json").read_text(encoding="utf-8")
        )
        self.standard = (
            ROOT / "standards/repository-documentation/v1/standard.md"
        ).read_text(encoding="utf-8")
        self.reference = (
            ROOT / "docs/reference/design-system-decision.md"
        ).read_text(encoding="utf-8")

    def test_schema_requires_explicit_architecture_decision(self):
        self.assertEqual(self.schema["properties"]["schemaVersion"]["const"], 1)
        self.assertEqual(
            self.schema["properties"]["designSystem"]["const"],
            "siczb/design-system",
        )
        self.assertEqual(
            set(self.schema["properties"]["decision"]["enum"]),
            {"use", "do-not-use"},
        )
        self.assertEqual(
            set(self.schema["properties"]["adoption"]["enum"]),
            {"active", "planned", "blocked"},
        )
        self.assertNotIn("version", self.schema["properties"])
        self.assertNotIn("packages", self.schema["properties"])

    def test_use_requires_adoption_and_blocked_requires_tracking_issue(self):
        rules = self.schema["allOf"]
        self.assertIn("adoption", rules[0]["then"]["required"])
        self.assertIn("trackingIssue", rules[1]["then"]["required"])

    def test_standard_does_not_force_design_system_adoption(self):
        self.assertIn("does **not** require Design System adoption", self.standard)
        self.assertIn("`decision: do-not-use`", self.standard)
        self.assertIn("Repositories without a relevant user-facing UI", self.standard)
        self.assertIn(
            "Concrete Design System package versions MUST remain authoritative",
            self.standard,
        )

    def test_design_system_requirement_starts_with_ruleset_1_2_0(self):
        self.assertIn("ruleset_version: 1.2.0", self.standard)
        self.assertIn("Effective from ruleset `1.2.0`", self.standard)
        self.assertIn(
            "MUST NOT apply the `1.2.0` Design System decision requirement "
            "retroactively",
            self.standard,
        )
        self.assertIn("Ruleset **1.2.0** introduces", self.reference)
        self.assertIn("migration to `1.2.0` is explicit", self.reference)


if __name__ == "__main__":
    unittest.main()
