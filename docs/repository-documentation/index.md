# Repository Documentation

This section explains how to apply the Repository Documentation Standard. It is guidance for
maintainers and consumers; it is **non-normative**.

Normative authority belongs exclusively to the versioned specifications under `standards/`. If this
guidance conflicts with a versioned standard, the standard selected by the repository declaration
wins.

## Normative versions

- [Repository Documentation Standard v1](../../standards/repository-documentation/v1/standard.md) —
  the immutable original contract for repositories that remain pinned to v1.
- [Repository Documentation Standard v2](../../standards/repository-documentation/v2/standard.md) —
  the explicit opt-in contract that adds purpose-specific document types, quality criteria, and
  Verification / Evidence semantics.

## Understand the documentation model

- [Document types](document-types.md) explains the information task of each normative type, typical
  uses, quality characteristics, boundaries, and common misapplications.
- [Methods and models](methods-and-models.md) explains how Diátaxis, arc42-lite, C4, and MADR fit
  together in Repository Standards.

## Adopt or migrate

- [Repository Documentation v2 migration](../repository-documentation-v2-migration.md) describes the
  v1-to-v2 boundary and how existing documentation and historical evidence are handled.
- [Repository contract v8 migration](../repository-contract-v8-migration.md) describes the repository
  declaration and compatibility pairing required to select Repository Documentation v2.
- [Compatibility and versioning](../reference/compatibility.md) is the current compatibility
  reference for all released declaration pairings.

Adoption is explicit. Publishing Repository Documentation v2 does not change the obligations of a
repository that remains pinned to v1.

## Validation

Machine-readable validation should enforce objective invariants such as a supported standard
version, declaration/profile consistency, required roots and files, valid links, and supported
compatibility pairings. Editorial quality remains a review responsibility where it cannot be tested
reliably.

In particular, document quality is based on whether the document fulfills its information task, not
on its length. A short navigation page or a compact evidence record can be complete.
