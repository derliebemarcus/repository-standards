from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TechnologyBaselinePublicationTest(unittest.TestCase):
    def test_public_core_externalizes_contract_assets(self) -> None:
        manifest = json.loads(
            (ROOT / "public" / "public-core-v1.json").read_text(encoding="utf-8")
        )
        published = set(manifest["files"])
        expected = {
            "standards/technology-baseline/v1/standard.md",
            "profiles/technology-baseline-v1.json",
            "profiles/repository-standards-compatibility-v5.json",
            "schemas/repository-standards-v6.schema.json",
            "reference/repository-standards-v6.single.yml",
            "reference/repository-standards-v6.integration.yml",
            "reference/repository-standards-v6.web.single.yml",
            "reference/repository-standards-v6.web.integration.yml",
            "docs/repository-contract-v6-migration.md",
            "tests/test_technology_baseline_v1.py",
            "tests/test_technology_baseline_publication.py",
        }
        self.assertTrue(expected.issubset(published), sorted(expected - published))

    def test_externalized_notification_value_is_placeholder(self) -> None:
        profile = json.loads(
            (ROOT / "profiles" / "technology-baseline-v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            "${TECHNOLOGY_BASELINE_NOTIFICATION_EMAIL}",
            profile["externalization"]["notification_address_placeholder"],
        )
        self.assertFalse(
            profile["externalization"]["personal_notification_addresses_allowed"]
        )


if __name__ == "__main__":
    unittest.main()
