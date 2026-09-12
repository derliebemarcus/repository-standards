# Repository Standards

Repository Standards is a versioned collection of repository, documentation, ticket,
development-workflow, technology, web-application, deployment, and Product/System Readiness
contracts. Normative specifications are combined with machine-readable schemas and compatibility
profiles, reference declarations, portable validation tools, explanatory guidance, and contract tests
so consumers can resolve one explicitly pinned contract set.

## Purpose and value

Repository Standards turns recurring engineering and governance decisions into explicit, versioned,
machine-readable contracts that can be shared by people, CI/CD automation, and AI agents. The goal is
to make the compliant delivery path the default: less repository-by-repository reinvention, less
ambiguous process knowledge, reproducible decisions and evidence, predictable migrations, and
traceable quality gates from ticket to release and operation. Its core values are **explicitness over
inference, contract-first change, immutable published versions, declared compatibility, evidence over
claims, fail-closed validation, provider portability, and automation that removes manual governance
work instead of adding bureaucracy**.

## Key features

- **Versioned contract sets and explicit compatibility** — repositories pin compatible, immutable
  standards instead of inheriting moving rules implicitly.
- **Ticket and delivery governance** — Ticket Specification and Development Workflow standardize
  lifecycle, estimation, branching, review, release, and Contract-first Delivery.
- **Documentation as an engineering contract** — Repository Documentation defines required document
  semantics, quality expectations, maintenance, and evidence/navigation responsibilities.
- **Technology, web, design, localization, and deployment baselines** — reusable contracts cover
  runtime lifecycle, web behavior, design-source decisions, language routing, environments, promotion,
  and rollback without collapsing these concerns into one profile.
- **Machine-readable and automation-ready** — schemas, profiles, reference declarations, validators,
  generated consumer assets, and AI adapters derive from the same versioned sources.
- **Product/System Readiness v1 — latest addition (Repository Standards v9.3.0)** — evidence-based,
  cumulative TRL 1-9 assessment for concrete products and operated systems, including preservation,
  requalification, and real operational proof for TRL 9.

This GitHub repository is a **generated public distribution**. The canonical source of truth is
maintained in Forgejo. Changes are implemented and qualified there, then a deterministic Public Core
is republished to GitHub. GitHub is not synchronized back to Forgejo.

## Quick start

Start from a released reference declaration instead of copying rules into local documentation. The
latest supported portable declaration pairing is declaration v11, introduced with Repository
Standards v9.3.0. Its core contract set is:

```yaml
version: 11
standards:
  ticket-specification: v5
  development-workflow: v8
  repository-documentation: v2
  technology-baseline: v1
  contract-first-delivery: v1
  product-system-readiness: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Canonical v11 references are:

- `reference/repository-standards-v11.single.yml`;
- `reference/repository-standards-v11.integration.yml`;
- `reference/repository-standards-v11.web.single.yml`; and
- `reference/repository-standards-v11.web.integration.yml`.

The v11 web pairing additionally selects Web Application Baseline v3, Deployment Environments v1,
and Repository Localization v1. Deployment Environments v2 is also a published contract, but it is
not implicitly selected by v11 merely because it is newer.

A supported pairing is an available portable contract set, not an automatic migration. Consumers
must pin an immutable Repository Standards release and may migrate only when their active writers,
validators, and required provider automation support the selected contracts. Product/System
Readiness applicability is separately authored in `.product-readiness.yml`; publishing or selecting
v11 does not infer applicability or activate productive Maintenance/Jenkins readiness gates.

Earlier released declarations remain available and keep their published semantics.

## Current compatibility boundary

The current additive compatibility matrix is:

`profiles/repository-standards-compatibility-v10.json`

It preserves every earlier released pairing and contains the supported declaration-v11 Core/Web
pairings. The matrix is the machine-readable source of pairing truth; documentation must not invent
or silently upgrade combinations.

Published standards, schemas, compatibility profiles, and reference declarations are immutable. A
consumer keeps the behavior of the versions it explicitly pins until it deliberately migrates. New
mandatory fields or incompatible semantics require a new versioned contract boundary rather than an
in-place rewrite.

See `docs/reference/compatibility.md` and the version-specific migration guides, including
`docs/repository-contract-v10-migration.md` and `docs/repository-contract-v11-migration.md`.

## Published standard families

The Public Core contains immutable released versions of these independently versioned families:

- Repository Documentation v1-v2;
- Ticket Specification v1-v5;
- Development Workflow v1-v8;
- Technology Baseline v1;
- Web Application Baseline v1-v3;
- Deployment Environments v1-v2;
- Contract-first Delivery v1;
- Repository Environments v1;
- Repository Localization v1;
- Design Source Declaration v1; and
- Product/System Readiness v1.

A newer published family version never upgrades a pinned consumer implicitly.

## Product/System Readiness v1

Product/System Readiness v1 is a provider-neutral, evidence-based readiness model for concrete
software products and operated systems. It adapts the ordinal NASA TRL 1-9 progression while keeping
authored intent distinct from evidence-derived readiness.

Key boundaries are:

```text
authored intent != derived readiness
target != candidate != assessed != established
deployment != operational proof
PROD != TRL 9
Product Stage != TRL
```

An MVP may establish TRL 9 for its deliberately bounded scope only when the complete cumulative
criteria through TRL 9 are satisfied, including successful real intended operational use. TRL is not
a security, risk, exposure, data, or criticality classification.

Start with:

- `standards/product-system-readiness/v1/standard.md` for the normative contract;
- `docs/reference/product-system-readiness.md` for the integration/authority model;
- `docs/repository-contract-v11-migration.md` for declaration-v11 adoption; and
- `docs/ticket-standard-v5-migration.md` for Ticket Specification v5 adoption.

## Repository Documentation v2

Repository Documentation v1 remains an immutable released contract. Repository Documentation v2 is
an explicit opt-in evolution; publication does not apply its rules retroactively to v1 consumers.

v2 normatively distinguishes Tutorial, How-to Guide, Reference, Explanation, Architecture,
Decision / ADR, Operations / Runbook, Verification / Evidence, and Index / Navigation. Document
quality is evaluated by whether the document performs its information task, not by a minimum word
count or another mechanical length metric.

Start with:

- `standards/repository-documentation/v2/standard.md`;
- `docs/repository-documentation/index.md`;
- `docs/repository-documentation/document-types.md`;
- `docs/repository-documentation/methods-and-models.md`; and
- `docs/repository-documentation-v2-migration.md`.

Guidance under `docs/` is explanatory, not normative. When it conflicts with a selected versioned
standard under `standards/`, the versioned standard is authoritative.

## Development workflow and branching

Development Workflow v8 is the latest published workflow contract. It includes Contract-first
Delivery integration and the logical conformance gates used by compatible providers. Earlier
workflow versions remain immutable for their supported declaration pairings.

Repository declarations select either the `single` or `integration` branching model. Normal Jenkins
Multibranch Pipeline projects use:

```regex
^(main|develop|PR-[0-9]+)$
```

Provider-specific concrete status identities are adapters around the selected portable workflow
contract. Jenkins itself is not required to interpret, adopt, or locally validate Repository
Standards.

See `docs/reference/branching-models.md` and `docs/reference/contract-first-delivery.md`.

## Technology, web, and deployment baselines

Technology Baseline v1 defines lifecycle, supported-runtime, container-image, database, exception,
review, and automated compliance requirements.

Web Application Baseline v3 is the latest published web baseline and adds canonical
language-prefixed user-facing routing with Repository Localization v1. Earlier Web Application
Baseline versions remain immutable for pinned consumers.

Deployment Environments v1 and v2 are both published contracts. The selected version is determined
by the consumer's compatible contract set or another explicit adoption boundary. Source revision,
artifact release state, and runtime environment remain independent dimensions; a `main` merge is not
itself a production release.

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

Run the included contract tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Machine-readable consumption

Consumers should resolve versions from `.repository-standards.yml` and load the matching released
assets. Current release-facing entry points include:

- `schemas/repository-standards-v11.schema.json`;
- `profiles/repository-standards-compatibility-v10.json`;
- `profiles/development-workflow-v8.json`;
- `profiles/ticket-specification-v5.json`;
- `profiles/product-system-readiness-declaration-v1.json`;
- `schemas/product-system-readiness-declaration-v1.schema.json`;
- `reference/repository-standards-v11.single.yml`; and
- `reference/ai/ticket-authoring-v5.md`.

These entry points describe the latest published portable pairing. They do not override a consumer's
existing immutable pin.

Historical released JSON Schema `$id` values are identifiers and may retain their original canonical
URI. They do not require network access to validate local files.

## Using Repository Standards with AI agents

AI prompts should not embed an unversioned copy of the rules. An agent should read and validate the
repository's `.repository-standards.yml`, resolve the complete pinned compatibility pairing, load the
matching released adapters where defined, load required repository-owned sidecars, validate the
intended write against that contract, and only then mutate the repository or ticket system.

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

**GitHub pull requests are not accepted.** Changes are evaluated publicly, implemented and qualified
in the canonical Forgejo repository, and included in a later deterministic Public Core publication
when appropriate.

See `CONTRIBUTING.md` for details.

## License

The Public Core is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The same license
applies to the standards text, documentation, schemas, reference material, tools, and tests included
in this distribution. See `LICENSE`.
