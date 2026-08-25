# Repository Standards documentation

This directory contains public guidance that complements the normative standards, profiles, schemas,
references, tools, and tests in the Repository Standards Public Core.

Normative requirements live under `standards/`. Guidance under `docs/` is non-normative and does not
silently override a published standard selected by a consumer declaration.

Start with:

- `../README.md` for purpose, Quick Start, compatibility, branching, AI use, and contribution rules;
- `repository-documentation/index.md` for Repository Documentation adoption and navigation;
- `repository-documentation/document-types.md` for practical guidance on the normative document
  types, including Verification / Evidence;
- `repository-documentation/methods-and-models.md` for Diátaxis, arc42-lite, C4, and MADR;
- `repository-documentation-v2-migration.md` for the explicit v1-to-v2 migration boundary;
- `repository-contract-v8-migration.md` for declaration-v8 adoption of Repository Documentation v2;
- `reference/compatibility.md` for supported contract sets and immutability;
- `reference/branching-models.md` for single and integration branching;
- `reference/web-application-and-deployment.md` for the web/deployment interaction model;
- `how-to/use-standards-in-ai-prompts.md` for AI-agent consumption; and
- `public-distribution.md` for the generated GitHub/Public Core boundary.

Repository Documentation v1 remains an immutable released contract. Repository Documentation v2 is
adopted only through its supported declaration-v8 compatibility pairing; publication does not
migrate existing consumers implicitly.
