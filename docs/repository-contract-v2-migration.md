# Repository contract v2 migration

Repository declaration schema v2 is the adoption boundary for Ticket Specification v2 and
Development Workflow v3. Migration is explicit and release-pinned; publishing the contract does not
change existing repositories.

## Source contract

The currently supported legacy contract set is:

```yaml
version: 1
standards:
  ticket-specification: v1
  development-workflow: v2
  repository-documentation: v1
```

Its branching model may be `single` or `integration`. Existing declaration-v1 files remain valid
against `schemas/repository-standards-v1.schema.json` and MUST NOT be rewritten merely because schema
v2 exists.

## Target contract

The Ticket Specification v2 contract set is:

```yaml
version: 2
standards:
  ticket-specification: v2
  development-workflow: v3
  repository-documentation: v1
```

Use one of the released reference declarations:

- `reference/repository-standards-v2.single.yml`;
- `reference/repository-standards-v2.integration.yml`.

The selected branching model MUST remain unchanged unless a separate approved migration explicitly
changes it. The Jenkins Multibranch Pipeline filter remains `^(main|develop|PR-[0-9]+)$`.

## Preconditions

Before changing `.repository-standards.yml` to version 2:

1. the repository's current declaration MUST validate against declaration schema v1;
2. Ticket Specification v2 lifecycle-data migration MUST have completed or produced an accepted
   deterministic migration plan;
3. Workboard MUST support the canonical `state=closed` plus `Status/Done` representation, explicit
   reopen semantics, and legacy-read behavior when the repository uses Workboard writes;
4. Maintenance MUST support the same lifecycle invariant, organization-level canonical status
   labels, and replacement-before-removal transitions when the repository uses Maintenance writes;
5. required Canary validation MUST be successful;
6. blocking enforcement MUST remain disabled until the migrated repository demonstrates compatible,
   idempotent reads and writes.

If any required lifecycle writer is incompatible, the repository MUST remain on declaration schema
v1 even though the v2 contract is published.

## Migration procedure

1. record the current declaration and its validation result;
2. preserve the existing branching model and branch-protection policy;
3. complete the Ticket Specification v2 lifecycle migration defined in
   `docs/ticket-standard-v2-migration.md`;
4. replace `.repository-standards.yml` with the matching declaration-v2 reference;
5. validate the declaration against `schemas/repository-standards-v2.schema.json`;
6. run repository, ticket, documentation, and CI contract checks in warning mode;
7. verify Workboard and Maintenance writes on the migrated repository;
8. verify completion and reopen transitions end in canonical Ticket Specification v2 states;
9. enable blocking enforcement only after the Canary and repository-specific evidence is green.

## Invalid combinations

The canonical compatibility matrix is
`profiles/repository-standards-compatibility-v1.json`. Currently only these pairings are valid:

- declaration v1 + Ticket Specification v1 + Development Workflow v2 + Repository Documentation v1;
- declaration v2 + Ticket Specification v2 + Development Workflow v3 + Repository Documentation v1.

A mixed declaration such as Ticket Specification v2 with Development Workflow v2 MUST fail
validation. Automation MUST NOT infer a migration target or silently coerce versions.

## Rollback

Before migration, retain the complete declaration-v1 file and lifecycle before-state evidence.
Rollback restores the recorded declaration and any lifecycle data through the Ticket Specification
v2 migration rollback process. It MUST NOT modify published standards, schemas, or reference
artifacts.
