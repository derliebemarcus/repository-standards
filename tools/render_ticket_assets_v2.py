#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_ticket_assets import GENERATED_HEADER, template_body

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = (
    "epic",
    "story",
    "bug",
    "security",
    "documentation",
    "testing",
)


def load_profile(root: Path) -> dict[str, object]:
    path = root / "profiles" / "ticket-specification-v2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def ai_adapter(profile: dict[str, object]) -> str:
    defaults = profile["defaults"]
    lifecycle = profile["lifecycle"]
    estimates = profile["label_categories"]["estimate"]["values"]
    kinds = profile["label_categories"]["kind"]["values"]
    kinds_text = ", ".join(kinds)
    estimates_text = ", ".join(str(value) for value in estimates)
    done = lifecycle["completed_status"]
    completed_state = lifecycle["completed_state"]
    open_state = lifecycle["open_state"]
    transition_order = lifecycle["transition_order"]

    return GENERATED_HEADER + f"""# Ticket authoring adapter v2

Before creating, changing, classifying, reopening, or closing a ticket, the AI agent MUST
determine the released Ticket Specification version declared by `.repository-standards.yml`
and MUST load the matching adapter. It MUST NOT reconstruct rules from memory, an
unversioned branch, or an older conversation.

The agent MUST validate the complete proposed ticket before any write.

Defaults:

- assignee: `{defaults["assignee"]}`;
- priority: `{defaults["priority"]}`;
- status: `{defaults["status"]}`.

Required label cardinality:

- exactly one `Kind/*`;
- exactly one `Priority/*`;
- exactly one `Status/*`;
- at least one `Area/*`.

Allowed kinds: {kinds_text}.

Implementable Ready leaf tickets MUST have exactly one estimate from: {estimates_text}.
Epics MUST NOT have an estimate.

`{done}` is the only canonical completed status. A completed ticket MUST have Forgejo
`state={completed_state}` and exactly `{done}`. An open ticket MUST NOT carry `{done}`.

Completion and reopen transitions MUST use `{transition_order}` ordering: establish the
replacement status before removing the previous valid status. Reopening MUST produce
`state={open_state}` and exactly one active non-Done status. If the resumed status cannot
be determined safely, the agent MUST require an explicit target status rather than
guessing.

Legacy closed tickets MAY be interpreted as completed for read and migration purposes,
but new v2 writes MUST use the canonical completed pair. Historical evidence, tests,
estimates, and facts MUST NOT be invented during migration.

The agent MUST render the correct family template and preserve every required heading.
Direct blockers MUST be standalone references in `### Blocked by`. `Parent`, `Blocks`,
and `Related` MUST NOT be treated as direct blockers.

Missing factual content MUST NOT be invented. Unknown facts MUST be marked explicitly
and MUST prevent `Status/Ready` when they affect readiness, validation, documentation,
security, compatibility, deployment, scope, or dependencies.

After ticket creation or a direct-blocker change, the agent MUST trigger
`workboard_forgejo_issue_dependency_sync` for the affected ticket with `STATE=all`.

For repository creation, the agent MUST ask whether a `develop` branch is used. Normal
Jenkins Multibranch Pipeline projects MUST use `^(main|develop|PR-[0-9]+)$`.
"""


def render(root: Path, output_root: Path) -> list[Path]:
    profile = load_profile(root)
    assets = profile["generated_assets"]
    template_root = output_root / assets["template_directory"]
    ai_path = output_root / assets["ai_adapter"]
    template_root.mkdir(parents=True, exist_ok=True)
    ai_path.parent.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for family in FAMILIES:
        path = template_root / f"{family}.md"
        body = template_body(family, profile)
        path.write_text(body, encoding="utf-8")
        written.append(path)

    ai_path.write_text(ai_adapter(profile), encoding="utf-8")
    written.append(ai_path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    output = arguments.output or arguments.root
    for path in render(arguments.root, output):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
