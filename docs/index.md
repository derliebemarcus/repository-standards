# Repository Standards documentation

This directory contains public guidance that complements the normative standards, profiles, schemas,
references, tools, and tests in the Repository Standards Public Core.

Normative requirements live under `standards/`. Guidance under `docs/` is non-normative and does not
silently override a published standard selected by a consumer declaration.

## Current compatibility boundary

The current additive compatibility matrix is
`../profiles/repository-standards-compatibility-v10.json`. It preserves earlier released pairings and
contains supported declarations through v11. The latest supported pairing is an available migration
target, not an automatic upgrade for pinned consumers.

Start with:

- `../README.md` for purpose, Quick Start, compatibility, branching, AI use, and contribution rules;
- `reference/compatibility.md` for the current additive compatibility matrix and immutability model;
- `reference/branching-models.md` for single/integration branching and version-aware workflow
  resolution;
- `repository-documentation/index.md` for Repository Documentation adoption and navigation;
- `repository-documentation/document-types.md` for practical guidance on the normative document
  types, including Verification / Evidence;
- `repository-documentation/methods-and-models.md` for Diátaxis, arc42-lite, C4, and MADR;
- `repository-documentation-v2-migration.md` for the explicit v1-to-v2 migration boundary;
- `design-source-declaration-v1-migration.md` for repository-owned design-source adoption;
- `reference/design-source-declaration.md` for the Design Source/automation/Design Contract boundary;
- `repository-contract-v10-migration.md` for the immutable declaration-v10 / Web Application
  Baseline v3 adoption boundary;
- `../standards/product-system-readiness/v1/standard.md` for the normative Product/System Readiness
  v1 Design Contract;
- `../standards/ticket-specification/v5/standard.md` for Product-/Release-Epic increment metadata and
  fail-closed completion semantics;
- `reference/product-system-readiness.md` for the readiness authority model, repository sidecar,
  Ticket Specification v5 integration, lifecycle, and security boundary;
- `repository-contract-v11-migration.md` for the explicit Repository Standards declaration-v11
  migration boundary;
- `ticket-standard-v5-migration.md` for explicit Ticket Specification v5 migration;
- `reference/web-application-and-deployment.md` for the web/deployment interaction model;
- `how-to/use-standards-in-ai-prompts.md` for AI-agent consumption; and
- `public-distribution.md` for the generated GitHub/Public Core boundary.

Product/System Readiness v1 has an additive repository/ticket integration surface:
`.product-readiness.yml`, its fail-closed declaration schema/profile, Ticket Specification v5, and
Repository Standards declaration v11. The declaration-v11 compatibility pairings are `supported`
beginning with immutable Repository Standards release v9.3.0. Existing released declaration and
Ticket Specification versions are unchanged and do not adopt readiness implicitly; migration remains
explicit and release-pinned.

Applicability, Subject Identity, long-term targets, Product Stage, and Product-/Release-Epic
Increment Targets are authored intent. Candidate, Assessed, Established, Preservation, and
Requalification remain evidence-derived. Product Stage does not imply TRL: a deliberately bounded
MVP may establish TRL 9 when the complete criteria including successful intended operational use are
satisfied, while a `production` stage implies no TRL.

Product/System Readiness is not a security/risk classification. TRL 9 does not imply secure, low
risk, security approved, or low criticality. Provider-side Maintenance/Jenkins evidence evaluation
and organization-wide readiness gate activation remain outside this portable integration and require
separate qualification.

Design Source Declaration v1 remains additive metadata. It does not implicitly migrate a
repository's Repository Standards declaration or make Penpot-RPC a portable Web Application
Baseline dependency.

Repository Documentation v1 remains an immutable released contract. Later Repository Documentation
versions are adopted only through compatible explicit Repository Standards declaration pairings;
publication does not migrate existing consumers implicitly.
