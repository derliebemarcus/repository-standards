# Repository Standards

Repository Standards is a versioned collection of repository, documentation, ticket,
development-workflow, technology, web-application, and deployment contracts. Normative specifications
are combined with machine-readable schemas and compatibility profiles, reference declarations,
portable validation tools, explanatory guidance, and contract tests so consumers can resolve one
explicitly pinned contract set.

This GitHub repository is a **generated public distribution**. The canonical source of truth is
maintained in Forgejo. Changes are implemented and qualified there, then a deterministic Public Core
is republished to GitHub. GitHub is not synchronized back to Forgejo.

## Quick start

Start from a released reference declaration instead of copying rules into local documentation.
Repository Standards v8.0.0 adds declaration v8 as the explicit adoption boundary for Repository
Documentation v2:

```yaml
version: 8
standards:
  ticket-specification: v3
  development-workflow: v6
  repository-documentation: v2
  technology-baseline: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Canonical v8 references are:

- `reference/repository-standards-v8.single.yml`;
- `reference/repository-standards-v8.integration.yml`;
- `reference/repository-standards-v8.web.single.yml`; and
- `reference/repository-standards-v8.web.integration.yml`.

Web consumers additionally select both Web Application Baseline v1 and Deployment Environments v1.
Earlier released declarations remain available and keep their published semantics.

## Repository Documentation v2

Repository Documentation v1 remains an immutable released contract. Repository Documentation v2 is
an explicit opt-in evolution; publication does not apply its rules retroactively to v1 consumers.

v2 normatively distinguishes these information tasks:

- Tutorial;
- How-to Guide;
- Reference;
- Explanation;
- Architecture;
- Decision / ADR;
- Operations / Runbook;
- Verification / Evidence; and
- Index / Navigation.

Document quality is evaluated by whether the document performs its information task, not by a minimum
word count or another mechanical length metric. Verification / Evidence is a separate point-in-time
evidence class for an identified revision, build, release, test, audit, or other examination. It must
remain distinguishable from durable current Reference, Architecture, and Operations documentation.

Start with:

- `standards/repository-documentation/v2/standard.md` for the normative v2 contract;
- `docs/repository-documentation/index.md` for non-normative adoption guidance;
- `docs/repository-documentation/document-types.md` for practical document-type guidance;
- `docs/repository-documentation/methods-and-models.md` for Diátaxis, arc42-lite, C4, and MADR; and
- `docs/repository-documentation-v2-migration.md` for the v1-to-v2 migration boundary.

Guidance under `docs/` is explanatory, not normative. When it conflicts with a selected versioned
standard under `standards/`, the versioned standard is authoritative.

## Compatibility and immutability

Published standards, schemas, compatibility profiles, and reference declarations are immutable. A
consumer keeps the behavior of the versions it explicitly pins until it deliberately migrates. New
mandatory fields or incompatible semantics require a new versioned contract boundary rather than an
in-place rewrite.

The current additive compatibility matrix is
`profiles/repository-standards-compatibility-v7.json`. It preserves every previously published
pairing and adds declaration v8 with Repository Documentation v2:

| Declaration | Ticket Specification | Development Workflow | Repository Documentation | Technology Baseline | Web / Deployment |
| --- | --- | --- | --- | --- | --- |
| v1 | v1 | v2 | v1 | — | — |
| v2 | v2 | v3 | v1 | — | — |
| v3 | v2 | v3 | v1 | — | v1 / v1 |
| v4 | v2 | v4 | v1 | — | optional v1 / v1 |
| v5 | v3 | v5 | v1 | — | optional v1 / v1 |
| v6 | v3 | v5 | v1 | v1 | optional v1 / v1 |
| v7 | v3 | v6 | v1 | v1 | optional v1 / v1 |
| v8 | v3 | v6 | v2 | v1 | optional v1 / v1 |

Where a declaration supports a web variant, Web Application Baseline v1 and Deployment Environments
v1 are selected together. Unsupported combinations fail closed rather than being guessed, coerced,
or silently upgraded. See `docs/reference/compatibility.md` and
`docs/repository-contract-v8-migration.md`.

## Development Workflow v6

Development Workflow defines ticket branches, pull requests, protection, qualification, releases,
and Hotfix behavior. Development Workflow v6 adds a provider-neutral logical identity for required
quality gates while keeping provider-specific concrete check/status names in adapters.

For Forgejo/Gitea Actions, concrete status identity includes the event in
`<workflow> / <job> (<event>)`. A migration from `pull_request` to `pull_request_target` therefore
requires a coordinated workflow and branch-protection change. Privileged `pull_request_target`
workflows must not execute pull-request-controlled code.

GitHub required status checks retain GitHub's job-based identity semantics; a GitHub adapter must not
invent Forgejo/Gitea event suffixes.

## Technology, web, and deployment baselines

Technology Baseline v1 defines technology lifecycle, supported-runtime, container-image, database,
exception, review, and automated compliance requirements.

Web Application Baseline v1 includes the canonical `/impressum`, `/datenschutz`, and
`/barrierefreiheit` routes together with application design, accessibility, and public artifact
provenance requirements.

Deployment Environments v1 separates source revision, artifact release state, and runtime
environment. It defines DEV/STAGE/PROD semantics, immutable promotion, and rollback behavior. A
`main` merge is not itself a production release.

See `docs/reference/web-application-and-deployment.md`.

## Portable validation

Repository Documentation validation is version-specific so publishing v2 cannot silently change v1
consumer behavior:

```bash
python3 tools/repository_contract.py validate --root /path/to/v1-repository
python3 tools/repository_contract_v2.py validate --root /path/to/v2-repository
```

The validators enforce objective declaration, profile, file, mapping, navigation, and impact
invariants. They do not use word counts or comparable proxies for subjective editorial quality.
Jenkins is one implementation environment and is not required to interpret, adopt, or locally
validate Repository Standards.

Run the included contract tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Machine-readable consumption

Consumers should resolve versions from `.repository-standards.yml` and load the matching released
assets. Current v8 entry points include:

- `schemas/repository-standards-v8.schema.json`;
- `schemas/repository-documentation-v2.schema.json`;
- `profiles/repository-standards-compatibility-v7.json`;
- `profiles/development-workflow-v6.json`;
- `profiles/ticket-specification-v3.json`;
- `reference/repository-standards-v8.single.yml`; and
- `tools/repository_contract_v2.py`.

Historical released JSON Schema `$id` values are identifiers and may retain their original canonical
URI. They do not require network access to validate local files.

## Using Repository Standards with AI agents

AI prompts should not embed an unversioned copy of the rules. An agent should read and validate the
repository's `.repository-standards.yml`, resolve the complete pinned compatibility pairing, load the
matching released adapters where defined, validate the intended write against that contract, and only
then mutate the repository or ticket system.

See `docs/how-to/use-standards-in-ai-prompts.md`.

## Public Core and source of truth

Forgejo is the only canonical source of Repository Standards. This GitHub repository is assembled
from a versioned, explicit file-by-file allowlist. New files in Forgejo are **not** published
automatically. Internal control files, operations material, and organization-specific integrations
are excluded by default.

A qualified canonical revision is exported into an empty directory, then the assembled result is
validated for exact paths, path escapes, symlinks, license state, secrets, credentials, unintended
internal references, and excluded control files. Identical source input produces identical file
content and permissions.

See `docs/public-distribution.md` for the Public Core boundary.

## Contributing

External contributions are accepted through **GitHub Issues only**.

**GitHub pull requests are not accepted.** Do not fork the repository expecting a GitHub PR to be
merged.

Use one of the issue templates for Bug Report, Standard Change Proposal, or Documentation Proposal.
Changes are evaluated publicly, implemented and qualified in the canonical Forgejo repository, and
included in a later deterministic Public Core publication when appropriate.

See `CONTRIBUTING.md` for details.

## License

The Public Core is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The same license
applies to the standards text, documentation, schemas, reference material, tools, and tests included
in this distribution. See `LICENSE`.
