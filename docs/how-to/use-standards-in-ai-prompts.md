# Use repository standards in AI prompts

## Principle

Do not copy the complete standard into project prompts. A copied prompt becomes an uncontrolled
policy fork.

Use three layers:

1. released normative standards in `siczb/repository-standards`;
2. generated AI adapters in `reference/ai/`;
3. a short project bootstrap instruction that loads the pinned declaration and adapter.

## Repository declaration

Each repository adopting the standards stores `.repository-standards.yml`. The declaration version,
standard versions, and branching model form one compatibility contract. An AI agent MUST validate
the complete pairing and MUST NOT infer compatibility from independently available artifacts.

Declaration schema v1 uses Ticket Specification v1 and Development Workflow v2:

- `reference/repository-standards.single.yml`;
- `reference/repository-standards.integration.yml`.

Declaration schema v2 uses Ticket Specification v2 and Development Workflow v3:

- `reference/repository-standards-v2.single.yml`;
- `reference/repository-standards-v2.integration.yml`.

Declaration schema v3 reuses Ticket Specification v2 and Development Workflow v3 and additionally
adopts Web Application Baseline v1 plus Deployment Environments v1:

- `reference/repository-standards-v3.single.yml`;
- `reference/repository-standards-v3.integration.yml`.

The current canonical pairing matrix is
`profiles/repository-standards-compatibility-v2.json`. The published v1 matrix remains immutable for
older contract releases. Unsupported combinations are rejected.

An AI agent must not infer Ticket Specification v2, Web Application Baseline v1, or Deployment
Environments v1 adoption merely because those standards or adapters exist. The repository must
explicitly declare a supported contract set and required lifecycle/deployment writers must already be
compatible.

## Web/deployment reasoning boundary

For a declaration-v3 consumer, an AI agent MUST keep these dimensions distinct:

- source branch/revision;
- artifact release state (`non-release`, `release-candidate`, or `release`);
- runtime environment (DEV, optional STAGE, or PROD).

The agent MUST NOT infer release state from `main`, DEV, STAGE, or PROD. Public provenance is read
from artifact metadata. PROD requires an immutable final-release artifact.

When changing a user-facing website under Web Application Baseline v1, the agent must assess impact
on `/impressum`, `/datenschutz`, and `/barrierefreiheit` whenever operator facts, data processing,
accessibility status, application shell/design, or artifact-provenance behavior changes. Unknown
legal facts must not be invented.

## Bootstrap instruction

A project prompt should contain only the loading and enforcement contract:

```text
Before any ticket or repository write, read `.repository-standards.yml`, validate its complete
released contract set, load the declared standards and matching AI adapter from
`siczb/repository-standards`, and validate the proposed change. Do not reconstruct rules from memory
or an older conversation. Do not invent missing facts. Apply defaults and trigger required
reconciliation exactly as defined by the loaded adapter.
```

Repository-specific operational instructions MAY be added after this bootstrap. They MUST NOT
weaken or duplicate the standard.

## Agent write flow

An AI agent should perform these steps:

1. read `.repository-standards.yml`;
2. validate the declaration version and standard pairing against the released compatibility matrix;
3. resolve released standard artifacts;
4. determine the declared Ticket Specification version;
5. load the matching `reference/ai/ticket-authoring-v<major>.md` adapter;
6. select the ticket family;
7. collect available facts;
8. render the generated family template;
9. classify labels and impacts;
10. validate the complete proposal;
11. write through a standard-aware wrapper;
12. trigger dependency reconciliation when direct blockers changed.

For Ticket Specification v2 lifecycle operations, the adapter additionally validates Forgejo issue
state together with `Status/*`, uses the canonical `closed` plus `Status/Done` completed pair, and
requires an explicit active status for reopen transitions.

A generic Forgejo issue operation should not be the primary AI interface. The wrapper applies
defaults, enforces cardinality, validates required sections, archives changes, and triggers
dependent automation.

## Updating prompts

When a repository changes its declaration or pinned standard versions, update the declaration and
re-run its contract checks. Migration to declaration schema v2 additionally requires the consumer
preconditions in `docs/repository-contract-v2-migration.md`. Migration to declaration schema v3
additionally requires the web/artifact/deployment preconditions in
`docs/repository-contract-v3-migration.md`.

The AI bootstrap itself normally remains unchanged because declaration and adapter selection are
version-aware. Long-lived prompt text must not hard-code a Ticket Specification, Development
Workflow, Web Application Baseline, or Deployment Environments version.
