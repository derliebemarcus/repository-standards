# Ticket Specification v2 migration

Ticket Specification v2 introduces a canonical completed lifecycle representation. It does not
rewrite Ticket Specification v1 and it does not authorize an immediate organization-wide mutation.
Consumers migrate explicitly after the released v2 contract is available.

## Canonical target

For v2 writes:

- completed work is Forgejo `state=closed` plus exactly `Status/Done`;
- open work has Forgejo `state=open` plus exactly one active non-Done `Status/*` label;
- `Status/Abandoned` remains distinct from completed work;
- reopening replaces `Status/Done` with an explicit active status and opens the issue.

A v2 reader may interpret a legacy closed issue as completed for display or migration analysis. That
compatibility interpretation is read-only and must not be emitted as a new v2 write.

## Migration phases

### 1. Pin the released contract

Migration tooling must resolve a released Repository Standards version containing Ticket
Specification v2. It must not read policy from an unversioned branch.

### 2. Inventory

Inventory all tickets, including closed tickets. Record at least:

- Forgejo issue state;
- all `Status/*` labels;
- issue description and comments;
- available lifecycle evidence;
- whether the current state is already canonical, legacy-compatible, ambiguous, or invalid.

### 3. Dry run

Before any mutation, produce a dry-run record containing:

- original Forgejo state and status labels;
- proposed Forgejo state and status label;
- classification and migration reason;
- unresolved ambiguity;
- before/after diff.

The dry run must be idempotent and reproducible.

### 4. Canary

Run migration and consumer compatibility on one Canary repository. Verify Workboard, Maintenance,
Forgejo lifecycle automation, dependency synchronization, and reopen/close behavior before wider
writes are enabled.

### 5. Normalize open tickets

Open tickets must remain `state=open` and must have exactly one active non-Done status. An open
legacy ticket carrying `Status/Done` is invalid and requires an explicit active target status.
Migration must not guess that status when the ticket context is insufficient.

### 6. Normalize closed tickets

A closed ticket may be migrated to `Status/Done` only when the available source state or history
already establishes completion. `Status/Abandoned` must not be converted to Done merely because the
Forgejo issue is closed.

When a legacy closed ticket cannot be classified deterministically, migration must report the
ambiguity for explicit handling rather than inventing a lifecycle history.

### 7. Consumer transition

Lifecycle writers adopt v2 only after their implementations can write the canonical pair and apply
replacement-before-removal semantics for completion and reopen transitions. Workboard and
Maintenance are separate consumer rollouts.

### 8. Warning and enforcement

Enable warning mode only after Canary validation. Enable blocking enforcement only after migrated
repositories and lifecycle writers have demonstrated compatible writes and idempotent reads.

## Evidence preservation

Migration must preserve original descriptions, comments, state history, and existing evidence. It
must not invent retrospective Story Point estimates, tests, acceptance evidence, impact
assessments, or other historical facts.

## Rollback

Before broad writes, migration tooling must retain sufficient before-state data to restore the
original Forgejo state and labels. A rollback restores recorded state; it must not synthesize a
third lifecycle representation.
