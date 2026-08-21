from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_BLOB_SHAS = {
    "standards/development-workflow/v3/standard.md":
        "79f5a64e55cc25a0921f091bf1ffbcfd54171afe",
    "schemas/repository-standards-v3.schema.json":
        "83c9e037ab5d6dd73796f32303d20327f060ccad",
    "profiles/repository-standards-compatibility-v2.json":
        "fd0d315d3334a948b05d41cc4f9bae862aafae03",
}


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def regular_branch_valid(
    branch: str,
    kind: str,
    ticket_number: int,
    repository: str | None = None,
) -> bool:
    workflow = load_json("profiles/development-workflow-v4.json")
    ticket = load_json("profiles/ticket-specification-v2.json")
    prefixes = ticket["branch_prefixes"]
    expected_prefix = prefixes.get(kind)
    if not expected_prefix or "/" not in branch:
        return False
    prefix, body = branch.split("/", 1)
    if prefix != expected_prefix:
        return False

    if repository is None:
        expected_start = f"{ticket_number}-"
    else:
        expected_start = f"{repository}-{ticket_number}-"
    if not body.startswith(expected_start):
        return False
    slug = body[len(expected_start):]
    return bool(re.fullmatch(workflow["branch_naming"]["slug_pattern"], slug))


def ticket_linked_pr_valid(title: str, branch_ticket_number: int) -> bool:
    match = re.fullmatch(r"#([0-9]+)\s+(.+)", title)
    return bool(
        match
        and match.group(2).strip()
        and int(match.group(1)) == branch_ticket_number
    )


class DevelopmentWorkflowV4Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = load_json("profiles/development-workflow-v4.json")
        cls.ticket = load_json("profiles/ticket-specification-v2.json")
        cls.compatibility = load_json(
            "profiles/repository-standards-compatibility-v3.json"
        )
        cls.declaration = load_json("schemas/repository-standards-v4.schema.json")

    def test_previously_published_contract_assets_are_immutable(self) -> None:
        for relative_path, expected_sha in IMMUTABLE_BLOB_SHAS.items():
            with self.subTest(path=relative_path):
                self.assertEqual(expected_sha, git_blob_sha(ROOT / relative_path))

    def test_prefix_mapping_has_single_ticket_profile_source(self) -> None:
        branch = self.workflow["branch_naming"]
        self.assertEqual(
            "profiles/ticket-specification-v2.json#/branch_prefixes",
            branch["prefix_source"],
        )
        self.assertFalse(branch["undeclared_prefixes_allowed"])
        self.assertEqual("bugfix", self.ticket["branch_prefixes"]["Kind/Bug"])
        self.assertNotIn("fix", set(self.ticket["branch_prefixes"].values()))

    def test_regular_bug_branch_accepts_bugfix_and_rejects_fix(self) -> None:
        self.assertTrue(
            regular_branch_valid("bugfix/123-example-bug", "Kind/Bug", 123)
        )
        self.assertFalse(
            regular_branch_valid("fix/123-example-bug", "Kind/Bug", 123)
        )

    def test_repository_qualified_branch_is_contract_validated(self) -> None:
        self.assertTrue(
            regular_branch_valid(
                "bugfix/maintenance-123-example-bug",
                "Kind/Bug",
                123,
                "maintenance",
            )
        )
        self.assertFalse(
            regular_branch_valid(
                "bugfix/other-123-example-bug",
                "Kind/Bug",
                123,
                "maintenance",
            )
        )

    def test_hotfix_is_an_explicit_path_not_regular_bug_alias(self) -> None:
        hotfix = self.workflow["branch_naming"]["hotfix"]
        self.assertTrue(hotfix["explicit_path_required"])
        self.assertEqual("main", hotfix["source_branch"])
        self.assertEqual("main", hotfix["target_branch"])
        self.assertFalse(
            regular_branch_valid("hotfix/123-example-bug", "Kind/Bug", 123)
        )

    def test_ticket_linked_pr_requires_summary_and_matching_number(self) -> None:
        self.assertTrue(ticket_linked_pr_valid("#123 Fix example bug", 123))
        self.assertFalse(ticket_linked_pr_valid("#123", 123))
        self.assertFalse(ticket_linked_pr_valid("#124 Fix example bug", 123))

    def test_pre_write_validation_is_fail_closed(self) -> None:
        pre_write = self.workflow["pre_write_validation"]
        self.assertTrue(pre_write["resolve_pinned_declaration"])
        self.assertTrue(pre_write["validate_complete_pairing"])
        self.assertTrue(pre_write["load_released_profiles"])
        self.assertTrue(pre_write["branch_creation"])
        self.assertTrue(pre_write["ticket_linked_pull_request_creation"])
        self.assertTrue(pre_write["fail_closed"])

    def test_v4_removes_legacy_cutoff_but_keeps_dependency_bot_exemption(self) -> None:
        exemptions = self.workflow["exemptions"]
        self.assertFalse(exemptions["legacy_creation_time_cutoff"]["allowed"])
        dependency = exemptions[
            "automated_dependency_pull_requests_without_ticket"
        ]
        self.assertTrue(dependency["may_be_exempt"])
        self.assertTrue(dependency["must_be_explicitly_identified"])

    def test_compatibility_v3_preserves_old_sets_and_adds_v4_sets(self) -> None:
        pairings = self.compatibility["pairings"]
        tuples = {
            (
                item["declaration_schema"],
                item["ticket_specification"],
                item["development_workflow"],
                item.get("web_application_baseline"),
                item.get("deployment_environments"),
            )
            for item in pairings
        }
        self.assertIn(("v1", "v1", "v2", None, None), tuples)
        self.assertIn(("v2", "v2", "v3", None, None), tuples)
        self.assertIn(("v3", "v2", "v3", "v1", "v1"), tuples)
        self.assertIn(("v4", "v2", "v4", None, None), tuples)
        self.assertIn(("v4", "v2", "v4", "v1", "v1"), tuples)
        self.assertEqual("reject", self.compatibility["unsupported_pairing_policy"])

    def test_declaration_v4_has_core_and_web_contract_variants(self) -> None:
        alternatives = self.declaration["properties"]["standards"]["oneOf"]
        self.assertEqual(2, len(alternatives))
        required = [set(item["required"]) for item in alternatives]
        self.assertIn(
            {
                "ticket-specification",
                "development-workflow",
                "repository-documentation",
            },
            required,
        )
        self.assertTrue(
            any("web-application-baseline" in fields for fields in required)
        )
        for alternative in alternatives:
            properties = alternative["properties"]
            self.assertEqual("v2", properties["ticket-specification"]["const"])
            self.assertEqual("v4", properties["development-workflow"]["const"])

    def test_generated_ai_adapter_is_current(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "render_development_workflow_assets.py"),
                "--check",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
