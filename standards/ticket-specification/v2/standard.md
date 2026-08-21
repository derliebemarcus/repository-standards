# Ticket Specification v2

## Status and scope

Ticket Specification v2 is the successor to Ticket Specification v1. It normatively incorporates all requirements of v1 unless this document explicitly supersedes them. The v1 release remains immutable and valid for consumers that continue to pin it.

This version adds an explicit completed lifecycle state and a canonical invariant between Forgejo issue state and the required `Status/*` label.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences of words such as "must", "should", and "may" are non-normative. Normative obligations MUST use the capitalized BCP 14 forms.

## Source of truth

The normative source is this document together with the requirements incorporated from `standards/ticket-specification/v1/standard.md`. The complete machine-readable representation is `profiles/ticket-specification-v2.json`, validated by `schemas/ticket-specification-v2.schema.json`.

Reference templates and the v2 AI authoring adapter MUST be generated from the v2 machine-readable representation and MUST NOT become separately maintained policy copies.

Consumers MUST pin a released Ticket Specification version. Adoption of v2 MUST be explicit; publishing v2 MUST NOT silently change a consumer that remains pinned to v1.

## Lifecycle vocabulary

Ticket Specification v2 retains the v1 status vocabulary and adds exactly one canonical completed status:

- `Status/Backlog`;
- `Status/Need More Info`;
- `Status/Blocked`;
- `Status/Ready`;
- `Status/In Progress`;
- `Status/Review`;
- `Status/Abandoned`;
- `Status/Done`.

`Status/Done` is reserved for completed tickets. It MUST NOT represent cancellation, abandonment, inactivity, or a generic terminal state. `Status/Abandoned` remains the status for work intentionally not completed.

A ticket MUST continue to carry exactly one `Status/*` label at all times.

## Canonical Forgejo lifecycle invariant

For canonical v2 writes, Forgejo issue state and the `Status/*` category form one lifecycle contract:

- a completed ticket MUST have Forgejo `state=closed` and exactly `Status/Done`;
- a ticket with `Status/Done` MUST have Forgejo `state=closed`;
- an open Forgejo ticket MUST NOT carry `Status/Done`;
- a closed ticket with an active status such as `Status/In Progress` or `Status/Review` is non-canonical under v2;
- a closed ticket without a `Status/*` label is non-canonical under v2.

Automation performing a completion transition MUST establish `Status/Done` before removing the previous valid `Status/*` label and MUST close the Forgejo issue only as part of the same logical transition. A failure MUST preserve or restore a valid, unambiguous lifecycle state rather than leaving the ticket without a canonical status.

Automation MUST NOT infer completion from a status label alone when the Forgejo issue remains open, and MUST NOT emit a new canonical write that closes a ticket while retaining an active status.

## Reopening

Reopening is an explicit lifecycle transition, not merely a Forgejo state toggle.

Before or as part of reopening a canonical `Status/Done` ticket, automation MUST select exactly one active non-Done status appropriate to the resumed work. It MUST establish that replacement status before removing `Status/Done`, and it MUST set Forgejo `state=open` as part of the same logical transition.

A reopened ticket MUST end with:

- Forgejo `state=open`;
- exactly one non-Done `Status/*` label;
- no `Status/Done` label.

Automation MUST NOT guess the resumed status when business context cannot determine it safely. In that case the operation MUST require an explicit target status.

## Readiness and completion

The v1 Definition of Ready remains unchanged. `Status/Done` MUST NOT be used as a substitute for readiness, review, acceptance, deployment, or verification evidence.

A ticket MAY transition to `Status/Done` only when its applicable acceptance criteria and Definition of Done have been satisfied. The ticket's existing evidence MUST be preserved. Closing a ticket MUST NOT cause automation to invent tests, estimates, impact assessments, or historical facts.

## Machine-readable lifecycle contract

The v2 machine profile MUST expose:

- the complete status vocabulary including `Status/Done`;
- the completed Forgejo state `closed`;
- the open Forgejo state `open`;
- the canonical completed pair `state=closed` plus `Status/Done`;
- the prohibition on `Status/Done` for open tickets;
- replacement-before-removal semantics for completion and reopen transitions;
- the legacy-read compatibility boundary.

The v2 JSON Schema MUST reject at least:

- `state=open` with `Status/Done`;
- `state=closed` with a non-Done status.

It MUST accept the canonical completed representation `state=closed` with `Status/Done`.

## AI-assisted authoring and lifecycle writes

An AI agent operating on a v2 repository MUST load the released v2 adapter before creating, changing, classifying, reopening, or closing a ticket.

Before a lifecycle write, the agent MUST validate both Forgejo issue state and the proposed `Status/*` label. When closing completed work, it MUST write the canonical completed pair. When reopening, it MUST require or derive an explicit active target status and MUST NOT leave `Status/Done` on the open ticket.

The agent MUST preserve the v1 rules against inventing missing factual content and historical evidence.

## Compatibility with Ticket Specification v1

Ticket Specification v1 remains immutable. A v1 consumer MAY continue to interpret historical completion according to its pinned implementation until it explicitly migrates.

A v2 reader MAY interpret a legacy Forgejo `state=closed` ticket as completed for read/display and migration purposes when the ticket lacks canonical v2 lifecycle metadata. This compatibility interpretation MUST NOT be serialized as a new canonical write without normalizing the ticket.

New writes by a v2 consumer MUST use the canonical lifecycle invariant. Legacy-read compatibility MUST NOT become a permanent alternate write format.

## Migration from v1

Migration to v2 MUST be staged and auditable:

1. publish and pin the released v2 contract in migration tooling;
2. inventory tickets using both Forgejo issue state and all `Status/*` labels;
3. produce a dry-run classification before any write;
4. validate consumer behavior on a Canary repository;
5. normalize open tickets so none carry `Status/Done`;
6. normalize completed tickets to `state=closed` plus exactly `Status/Done` only where completion is already evidenced by the source system;
7. preserve `Status/Abandoned` semantics rather than converting abandoned work to Done;
8. reconcile reopen and completion automation;
9. enable warning and enforcement only after consumer compatibility is verified.

Migration MUST preserve original descriptions, comments, state history, and available evidence. It MUST NOT invent retrospective Story Point estimates, tests, acceptance evidence, impact assessments, or other facts that were not recorded.

A legacy closed ticket without sufficient evidence to distinguish completed from abandoned or otherwise non-completed work MUST be flagged for deterministic migration handling rather than guessed.

Migration tools MUST be idempotent and MUST provide dry-run evidence containing the original state, original status labels, proposed state, proposed status label, reason, and before/after diff.

## Release and consumer boundary

Ticket Specification v2 changes lifecycle write semantics and therefore requires an explicit consumer migration boundary. Workboard, Maintenance, and other lifecycle writers MUST NOT emit v2 completion writes until they have adopted and validated the released v2 contract.

Repository Standards publishes the contract only. Consumer implementation, organization-label creation, and mutation of existing tickets are separate rollout work and are not performed by this standard release.
