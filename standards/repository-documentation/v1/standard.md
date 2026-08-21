# Repository Documentation Standard v1

## Status and scope

This is the canonical version 1 specification for repository documentation. The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

A repository declares conformance in `.repository-documentation.yml` and selects one of the profiles `application`, `library`, or `infrastructure`.

The standard combines Diátaxis, arc42-lite, C4-style text diagrams, MADR-compatible Architecture Decision Records, community health files, and MkDocs-compatible Markdown where publishing is enabled.

## Required declaration

```yaml
documentation:
  standard: repository-documentation
  standard_version: 1
  ruleset_version: 1.2.0
  profile: application
  architecture: arc42-lite
  diagrams: c4
  decisions: madr
  publishing: none
```

Ruleset `1.2.0` introduces the Design System decision requirement for repositories with a relevant user-facing UI. Repositories that still declare an earlier `1.x` ruleset remain governed by that declared ruleset until explicitly migrated; validators MUST NOT apply the `1.2.0` Design System decision requirement retroactively.

## Information architecture

Detailed documentation MUST be organized into tutorials, how-to guides, reference, explanation, architecture, decisions, and operations. Profile files define mandatory documents and explicit omissions. A repository MUST NOT omit documents ad hoc.

The repository README remains a concise landing page and MUST link to the detailed documentation.

## Design System decision for UI repositories

**Effective from ruleset `1.2.0`.** A repository that owns a user-facing web or application UI MUST explicitly document its architecture decision regarding `siczb/design-system`. The standard requires a decision; it does **not** require Design System adoption.

The canonical machine-readable decision MUST be stored as `.design-system-consumer.json` and conform to `schemas/design-system-consumer-v1.schema.json`. The referenced human-readable documentation MUST exist in the repository documentation set.

Two decisions are conformant:

- `decision: use`: the repository has chosen the shared Design System. Technical adoption MUST be recorded separately as `active`, `planned`, or `blocked`.
- `decision: do-not-use`: the repository has consciously chosen not to consume the shared Design System. The contract rationale MUST explain that decision specifically.

For `decision: use`:

- `active` means the referenced package manifest MUST contain actual `@siczb/design-tokens`, `@siczb/ui-css`, or `@siczb/ui-react` dependencies appropriate to the integration;
- `planned` means the architecture decision is made but persistent package adoption is not yet complete;
- `blocked` means adoption is prevented by a concrete technical prerequisite and MUST reference a tracking issue.

For `decision: do-not-use`, the referenced package manifest MUST NOT consume Design System packages. A repository MAY later change this architecture decision through its normal ADR/change process.

Concrete Design System package versions MUST remain authoritative in the package manifest and lockfile. They MUST NOT be duplicated in `.design-system-consumer.json`.

Repositories without a relevant user-facing UI are outside this requirement. The canonical `siczb/design-system` provider repository itself is also outside the consumer-declaration requirement.

## Documentation maintenance policy

Every functional, operational, security, architecture, compatibility, build, release, or deployment change MUST be assessed for documentation impact.

Affected documentation MUST be updated in the same pull request as the change. Deferring known documentation work to an unspecified future ticket is not conformant.

The assessment MUST cover the complete repository-owned documentation set, not only the document nearest to the changed source file. At minimum, the author MUST consider:

- user-visible behavior and interfaces;
- configuration and environment variables;
- installation, upgrade, migration, and compatibility;
- architecture, runtime scenarios, and deployment topology;
- authentication, authorization, secrets, and data protection;
- monitoring, alerting, backup, restore, rollback, and disaster recovery;
- troubleshooting, known limitations, and technical debt;
- release, versioning, and breaking-change behavior.

A pull request with no documentation changes MUST contain a specific explanation of why the change has no documentation impact. A generic `not applicable` statement is insufficient.

## Machine-readable impact mappings

Repositories SHOULD declare source-to-documentation mappings for predictable impacts. A mapping identifies source paths and the documents expected to change when those paths change.

Example:

```yaml
documentation:
  maintenance:
    require_impact_declaration: true
    mappings:
      - source:
          - "src/config/**"
        documentation:
          - "docs/reference/configuration.md"
          - "docs/reference/environment-variables.md"
```

The mapping is a minimum expectation, not proof that no other document is affected.

## Architecture and ADRs

The architecture section MUST cover context, constraints, building blocks, runtime, deployment, cross-cutting concepts, quality requirements, risks, technical debt, and terminology.

Durable architecture decisions MUST be recorded as ADRs. Accepted ADRs are immutable except for status and supersession metadata. Changed decisions require a new ADR.

## Validation contract

Validation MUST check declaration values, profile consistency, required files and headings, unresolved placeholders, local links, README linkage, ADR conventions, required diagram syntax, and publishing configuration where enabled.

For repositories declaring ruleset `1.2.0` or later within standard version 1 and having a relevant UI, validation MUST additionally check the Design System decision contract, referenced documentation and package manifest, adoption semantics, and consistency between the decision and actual Design System package dependencies.

Validation SHOULD also check source-to-documentation mappings and the pull request documentation-impact declaration.

Validation rules are tied to the declared standard and ruleset versions. A later ruleset or standard version MUST NOT silently change the requirements of an earlier declared ruleset.

## Bootstrap and synchronization

Bootstrap and synchronization are additive. They create missing files but MUST NOT overwrite repository-specific content without an explicit migration decision.

Boilerplate MUST be generated from or validated against the same profile and reference sources used by this repository. A separately maintained template tree is prohibited because it would create a second source of truth.
