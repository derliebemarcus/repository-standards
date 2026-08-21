# Version Ticket and Branch Contracts Together

- Status: accepted
- Date: 2026-07-30

## Context

Ticket metadata, description structure, dependency declarations, AI authoring, repository
bootstrap, branching, and release promotion need one testable contract. Copying rules into prompts,
templates, Workboard, and Jenkins would create drift.

The existing Development Workflow v1 cannot receive incompatible mandatory branching semantics
without violating the repository versioning policy.

## Decision drivers

- normative policy must remain implementation-neutral;
- generated templates and AI instructions must not become policy forks;
- open and closed ticket migration must be safe and auditable;
- `develop` must be an explicit repository decision;
- release promotion must remain manual;
- existing pinned v1 workflow consumers must not change silently.

## Decision

Create Ticket Specification v1 as a new standard. Publish Development Workflow v2 for the
single-branch and integration-branch models.

Store machine-readable representations under `profiles/` and `schemas/`. Generate reference ticket
templates and the AI adapter from the ticket profile. Keep Workboard migration and dependency
reconciliation in Workboard, and Jenkins enforcement and repository bootstrap implementation in
Maintenance.

## Consequences

Repositories opt in by pinning released versions in `.repository-standards.yml`. Development
Workflow v1 remains immutable.

Organization labels and all existing tickets require a staged migration. Workboard and Maintenance
need explicit follow-up implementation and compatibility tests.

## Risks

Generated assets can drift if edited directly. Contract tests therefore regenerate them and compare
the results byte for byte.

A partial organizational migration can expose mixed ticket structures. Consumers retain legacy
dependency headings during the compatibility phase and use bounded Canary batches.
