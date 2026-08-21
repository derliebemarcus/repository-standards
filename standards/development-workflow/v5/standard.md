# Ticket-based Development Workflow v5

## Status and normative language

This standard supersedes Ticket-based Development Workflow v4 only for repositories that explicitly adopt version 5. Development Workflow v1 through v4 remain immutable for repositories pinned to those versions.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences are non-normative.

Ticket metadata, lifecycle, description requirements, estimation anchors, and the canonical kind-to-branch-prefix mapping are defined by Ticket Specification v3. A repository using Development Workflow v5 MUST also adopt Ticket Specification v3.

## Incorporated Development Workflow v4 requirements

Except where this document explicitly supersedes the version coupling below, every normative requirement of Ticket-based Development Workflow v4 remains in force for Development Workflow v5. This includes unchanged requirements for:

- repository bootstrap and the explicit `develop`-branch decision;
- single and integration branching models;
- branch protection and equivalent `main`/`develop` quality gates;
- branch and pull-request naming and fail-closed pre-write validation;
- documentation-impact declarations;
- Forgejo workflow placement and runtime requirements;
- manual `main` builds;
- ticket and release Definitions of Done;
- manual `develop` to `main` release promotion;
- Hotfix creation, merge, and reintegration;
- review and merge requirements;
- canonical completion and reopen integration;
- dependency-update exemptions; and
- defense-in-depth post-write naming validation.

Development Workflow v5 does not alter these behaviors. It supersedes only references that couple Development Workflow v4 to Ticket Specification v2 and Repository Standards declaration schema v4.

## Source of truth and released machine-readable assets

A repository MUST declare the released standards it adopts and its branching model in `.repository-standards.yml`. A Development Workflow v5 repository MUST use Repository Standards declaration schema v5.

Automation MUST validate the complete declared version set and MUST NOT infer, coerce, or silently upgrade an unsupported combination.

The released machine-readable Development Workflow v5 profile is `profiles/development-workflow-v5.json`. The canonical kind-to-prefix mapping is referenced from the compatible Ticket Specification v3 profile at `profiles/ticket-specification-v3.json#/branch_prefixes` and MUST NOT be duplicated as a separately maintained mapping.

A consumer MUST treat these released profiles as a single versioned contract set. It MUST NOT use an unversioned branch, remembered rules, prompt history, or an independently maintained prefix list as a substitute for the repository's pinned released contract.

## Pre-write validation

Development Workflow v5 retains the complete v4 pre-write validation contract. Before creating a ticket branch or ticket-linked pull request, automation MUST resolve and validate the repository's released declaration-v5 pairing and MUST load Development Workflow v5 plus Ticket Specification v3 before issuing the Forgejo write.

All v4 branch-name forms, slug rules, ticket-number correspondence, source/target rules, Hotfix restrictions, dependency-update exemptions, and fail-closed behavior remain unchanged.

## Ticket estimation integration

Development Workflow v5 does not create a second estimation policy. When estimation is required by Ticket Specification v3, automation MUST load and apply the v3 estimation model and canonical Story Point anchors from `profiles/ticket-specification-v3.json`.

A branch or pull-request workflow MUST NOT reinterpret Story Points as time, use a private anchor table, or infer an estimate from implementation size after the fact.

## Repository declaration schema v5

Development Workflow v5 repositories use declaration schema v5. The schema supports the same two branching models and keeps the normal Jenkins Multibranch Pipeline filter:

```regex
^(main|develop|PR-[0-9]+)$
```

The core contract set is:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
```

The schema also supports Web Application Baseline v1 and Deployment Environments v1 as an existing paired opt-in extension:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

The branching declaration remains `single` or `integration` exactly as defined by the incorporated workflow requirements. Regular ticket branches MUST continue to start from and target the selected integration branch.

## Compatibility and migration boundary

Development Workflow v5 MUST NOT be combined with Ticket Specification v1 or v2. Development Workflow v4 MUST NOT be silently reinterpreted as supporting Ticket Specification v3. Unsupported declaration and standard pairings MUST fail validation rather than being inferred heuristically.

Publishing Development Workflow v5 does not migrate repositories pinned to earlier declaration or workflow versions. Migration is an explicit repository change and MUST preserve all existing branching-model, lifecycle, protection, release, documentation, web, and deployment semantics unless a separately approved requirement changes them.

Before adopting Development Workflow v5, every ticket-, branch-, and pull-request-writing automation used by the repository MUST support Ticket Specification v3 estimation semantics and the unchanged v4 pre-write workflow contract.
