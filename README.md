# Repository Standards

Repository Standards is a versioned collection of repository, ticket, development-workflow, web-application, and deployment contracts. It combines normative specifications with machine-readable profiles and schemas, reference configurations, validation tools, and contract tests so repositories and automation can consume the same rules without duplicating them.

This GitHub repository is a **generated public distribution**. The canonical source of truth is maintained in Forgejo. Changes are implemented and qualified there, then a deterministic Public Core is republished to GitHub. GitHub is not synchronized back to Forgejo.

## Why use it?

Repository Standards provides a shared contract for questions that otherwise drift between documentation, CI, issue trackers, and automation:

- how repository documentation is structured and maintained;
- how tickets are authored, classified, estimated, blocked, validated, and completed;
- how branches and pull requests are named and qualified;
- how single-branch and integration-branch repositories behave;
- which web-application and deployment guarantees are required;
- which combinations of contract versions are supported;
- how humans, CI systems, and AI agents resolve the same pinned rules.

## Quick start

For a new consumer, start from a released reference declaration rather than copying rules into local documentation.

For the current core contract set with Development Workflow v4 and single-branch development:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

The complete examples are in:

- `reference/repository-standards-v4.single.yml`
- `reference/repository-standards-v4.integration.yml`
- `reference/repository-standards-v4.web.single.yml`
- `reference/repository-standards-v4.web.integration.yml`

Validate a consumer repository with:

```bash
python3 tools/repository_contract.py validate --root /path/to/repository
```

Run the included contract tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Normative standards and supporting assets

The repository deliberately separates normative rules from their machine-readable and explanatory representations:

```text
standards/    normative, versioned specifications
profiles/     machine-readable rules and compatibility pairings
schemas/      JSON Schemas and artifact contracts
reference/    example declarations, generated adapters, and reference assets
tools/        reusable consumer-side validation and generation tools
tests/        executable contract tests
docs/         adoption, compatibility, and usage guidance
```

`standards/` is normative. Profiles, schemas, references, documentation, tools, and tests support implementation and validation; they do not silently redefine a published normative standard.

## Versioning and immutability

Published contract versions are immutable. A consumer keeps the behavior of the versions it explicitly pins until it deliberately migrates. New mandatory fields or incompatible semantics require a new versioned contract boundary rather than an in-place rewrite.

Repository Standards release **v6.0.0** introduced Development Workflow v4 and declaration schema v4. Earlier released declaration and standard versions remain available for pinned consumers.

## Supported contract sets and compatibility

The current compatibility matrix is `profiles/repository-standards-compatibility-v3.json`.

| Declaration | Ticket Specification | Development Workflow | Repository Documentation | Web Application Baseline | Deployment Environments |
| --- | --- | --- | --- | --- | --- |
| v1 | v1 | v2 | v1 | — | — |
| v2 | v2 | v3 | v1 | — | — |
| v3 | v2 | v3 | v1 | v1 | v1 |
| v4 | v2 | v4 | v1 | — | — |
| v4 | v2 | v4 | v1 | v1 | v1 |

Unsupported combinations must fail validation rather than being guessed or silently upgraded. See `docs/reference/compatibility.md` for the complete compatibility model.

## Ticket Specification

Ticket Specification defines the canonical ticket structure and metadata used by compatible issue-tracker writers. It covers, among other things:

- required `Kind/*`, `Priority/*`, `Status/*`, and `Area/*` labels;
- estimates for implementable leaf tickets;
- canonical relation sections such as `### Blocked by`;
- readiness and missing-information rules;
- validation, documentation, security, compatibility, and deployment impact;
- lifecycle semantics.

Ticket Specification v1 remains supported for declaration-v1 consumers. Ticket Specification v2 adds canonical completed lifecycle semantics. Machine-readable profiles and schemas live in `profiles/` and `schemas/`.

## Development Workflow

Development Workflow defines ticket branches, pull requests, protection, qualification, releases, and Hotfix behavior.

Development Workflow v4 adds a released machine-readable branch/pull-request naming contract and fail-closed validation before automated writes. AI and automation writers must resolve the repository's pinned released contract before creating ticket branches or ticket-linked pull requests.

### Single branching

With `branching.model: single`, regular ticket branches start from `main` and merge back to `main` through a qualified pull request.

### Integration branching

With `branching.model: integration`, regular ticket branches start from `develop` and merge to `develop`. Promotion from `develop` to `main` is a manually created and manually merged release pull request. `main` and `develop` are subject to equivalent protection, review, and quality requirements. Hotfixes may branch from `main`, must merge to `main`, and must then be reintegrated into `develop`.

See `docs/reference/branching-models.md`.

## Web Application and Deployment contracts

Web Application Baseline v1 defines, among other requirements, the canonical `/impressum`, `/datenschutz`, and `/barrierefreiheit` routes, consistent application design, accessibility requirements, and public artifact provenance rendering.

Deployment Environments v1 separates three concepts that are often conflated:

1. source branch or revision;
2. artifact release state;
3. runtime environment.

It defines DEV/STAGE/PROD semantics, immutable promotion, and rollback behavior. See `docs/reference/web-application-and-deployment.md`.

## Machine-readable consumption

Consumers should resolve versions from `.repository-standards.yml` and then load the matching released assets. Useful entry points include:

- `schemas/repository-standards-v4.schema.json`
- `profiles/repository-standards-compatibility-v3.json`
- `profiles/development-workflow-v4.json`
- `profiles/ticket-specification-v2.json`
- `tools/repository_contract.py`

Historical released JSON Schema `$id` values are identifiers and may retain their original canonical URI. They do not require network access to validate local files.

## Using Repository Standards with AI agents

AI prompts should not embed an unversioned copy of the rules. An agent should:

1. read and validate the repository's `.repository-standards.yml`;
2. resolve the pinned Ticket Specification and Development Workflow versions;
3. load the matching released AI adapter from `reference/ai/` where one is defined;
4. validate the complete intended write against the corresponding machine-readable contract;
5. only then perform the repository or ticket mutation.

Ticket authoring adapters are available in `reference/ai/ticket-authoring-v1.md` and `reference/ai/ticket-authoring-v2.md`. Development Workflow v4 automation guidance is available in `reference/ai/development-workflow-v4.md`. See `docs/how-to/use-standards-in-ai-prompts.md`.

## Public Core and source of truth

Forgejo is the only canonical source of Repository Standards. This GitHub repository is assembled from a versioned, explicit file-by-file allowlist. New files in Forgejo are **not** published automatically. Internal control files, operations material, and organization-specific integrations are excluded by default.

A qualified canonical revision is exported into an empty directory, then the assembled result is validated for exact paths, path escapes, symlinks, license state, secrets, credentials, unintended internal references, and excluded control files. Identical source input produces identical file content and permissions.

See `docs/public-distribution.md` for the Public Core boundary.

## Contributing

External contributions are accepted through **GitHub Issues only**.

**GitHub pull requests are not accepted.** Do not fork the repository expecting a GitHub PR to be merged.

Use one of the issue templates for:

- Bug Report
- Standard Change Proposal
- Documentation Proposal

The contribution flow is:

```text
GitHub Issue
→ technical/domain evaluation
→ implementation in the canonical Forgejo repository
→ normal canonical qualification
→ later deterministic republication of the Public Core
```

See `CONTRIBUTING.md` for details.

## License

The Public Core is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The same license applies to the standards text, documentation, schemas, reference material, tools, and tests included in this distribution. See `LICENSE`.
