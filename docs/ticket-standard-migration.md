# Ticket Specification v1 migration

## Objective

Migrate every Forgejo ticket to Ticket Specification v1 without losing original information,
inventing historical evidence, or breaking dependency reconciliation.

The migration covers open and closed tickets. It is coordinated across:

- `repository-standards`, which owns the normative contract and generated assets;
- `workboard`, which owns dependency reconciliation and migration execution;
- `maintenance`, which owns Jenkins enforcement and repository bootstrap automation.

## Preconditions

Before organization-wide writes:

1. Ticket Specification v1 and Development Workflow v2 are released.
2. Workboard accepts the canonical `### Blocked by` section and retains compatible legacy
   headings during migration.
3. The migration tool supports `STATE=all`, dry-run, idempotent apply, archived originals,
   before/after diffs, and machine-readable reports.
4. Required organization labels exist.
5. A rollback and incident procedure is documented.

## Required organization labels

The migration MUST provide these missing kinds:

- `Kind/Epic`;
- `Kind/Refactoring`;
- `Kind/Maintenance`;
- `Kind/Research`.

It MUST provide the exclusive estimate labels:

- `Estimate/1`;
- `Estimate/2`;
- `Estimate/3`;
- `Estimate/5`;
- `Estimate/8`;
- `Estimate/13`.

`Priority/Medium` MUST be migrated to `Priority/Normal` and then removed after no ticket uses it.

## Inventory

The first run MUST be read-only and MUST include every open and closed issue.

For each ticket, the report records:

- original title and description;
- assignees;
- all labels grouped by category;
- detected family and kind;
- existing parent, blocker, blocked-ticket, and related references;
- proposed metadata;
- proposed normalized description;
- unresolved facts and ambiguous classifications;
- possible self-dependencies, cycles, or inaccessible references;
- exact before/after diff.

The report MUST be archived before any apply run.

## Canary sequence

Migration proceeds in this order:

1. `siczb/repository-standards`;
2. `siczb/workboard`;
3. `siczb/maintenance`;
4. remaining repositories in bounded batches.

Each Canary or batch requires:

1. migration dry run;
2. human review of ambiguous changes;
3. idempotence check by repeating the dry run;
4. bounded apply;
5. dependency-sync dry run with `STATE=all`;
6. dependency-sync apply;
7. Workboard hierarchy and dependency-view validation;
8. archived evidence and rollback data.

## Open tickets

Open tickets receive the complete current structure.

Automation MAY safely apply:

- missing assignee `marcus`;
- missing `Priority/Low`;
- missing `Status/Backlog`;
- normalized exclusive label categories;
- known relations;
- canonical headings;
- content moved without semantic alteration.

Automation MUST NOT invent requirements, acceptance criteria, impact decisions, validation
evidence, estimates, or kind-specific facts.

A ticket with unresolved required content MUST use `Status/Need More Info` or `Status/Blocked`.
It MUST NOT use `Status/Ready`.

## Closed tickets

Closed tickets receive normalized assignees, label categories, and relations. They do not receive
new Story Point estimates.

Missing historical evidence is represented by:

```text
Not recorded before Ticket Specification v1.
```

Migration MUST NOT claim tests, acceptance evidence, security review, documentation updates, or
deployment validation that did not exist in the original ticket or linked evidence.

## Dependency reconciliation

`### Blocked by` is canonical. Direct blockers are standalone references. The migration MUST retain
references to closed tickets.

The Workboard compatibility phase MAY continue accepting legacy direct-blocker headings. It MUST
not reinterpret `Parent`, `Blocks`, `Related`, explanatory prose, transitive predecessors, or
inverse relations as direct blockers.

After a ticket description changes, the affected ticket is reconciled with:

```text
SCOPE=issue
STATE=all
APPLY=true
ALLOW_UNRESOLVED=false
CAUSE=ticket-standard-migration
```

Organization-wide reconciliation is performed only after the current batch has passed issue-level
checks.

## Enforcement rollout

Enforcement has four stages:

| Stage | Behavior |
| --- | --- |
| Audit | Generate reports without affecting work |
| Warning | Surface violations on changed tickets |
| Write validation | Reject non-conformant new or changed tickets |
| Ready gate | Prevent `Status/Ready` when Definition of Ready fails |

Legacy headings are removed only in a later incompatible consumer release after all known tickets
have been migrated.

## Rollback

Every apply run MUST retain:

- original descriptions;
- original assignees and labels;
- applied request and response data;
- the standards version;
- migration-tool version;
- dependency-sync report;
- repository and ticket scope.

Rollback MUST restore the bounded batch rather than mixing unrelated repositories in one recovery
operation.
