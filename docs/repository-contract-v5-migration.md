# Repository Standards declaration v5 migration

## Purpose

Declaration schema v5 is the explicit adoption boundary for Ticket Specification v3 and Development Workflow v5. It does not alter the existing branching models, Repository Documentation v1, or the optional Web Application Baseline v1 / Deployment Environments v1 pair.

## Supported pairings

Core:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
```

Web/deployment extension:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

No partial web/deployment extension is supported.

## Why a new workflow version is required

Development Workflow v4 is a released immutable contract that explicitly requires Ticket Specification v2 and declaration schema v4. Ticket Specification v3 therefore cannot be paired with v4 without changing published semantics after release.

Development Workflow v5 preserves v4 behavior and changes only the compatible Ticket Specification and declaration references. This keeps the compatibility matrix explicit and prevents consumers from guessing version combinations.

## Branching behavior

Declaration v5 keeps both existing branching models:

- `single`: regular ticket branches start from and target `main`;
- `integration`: regular ticket branches start from and target `develop`, with manual release pull requests from `develop` to `main`.

The normal Jenkins Multibranch Pipeline filter remains:

```regex
^(main|develop|PR-[0-9]+)$
```

Development Workflow v5 retains v4 branch/pull-request naming, fail-closed pre-write validation, protection, review, release, Hotfix, and manual-main-build rules unchanged.

## Migration prerequisites

Before a repository adopts declaration v5:

1. ticket writers must support Ticket Specification v3 and its estimation anchors;
2. branch and pull-request writers must support Development Workflow v5 and continue to perform the v4-derived pre-write validation;
3. lifecycle writers must continue to support the Ticket Specification v2/v3 `Status/Done` invariant;
4. any Web Application Baseline / Deployment Environments adoption must remain a complete paired extension; and
5. the complete v5 declaration must validate against `schemas/repository-standards-v5.schema.json` and the current compatibility profile.

## Migration procedure

1. Select the released v5 reference matching the repository's branching model and web/deployment decision.
2. Validate all automation prerequisites before modifying `.repository-standards.yml`.
3. Replace the declaration atomically with the selected v5 pairing.
4. Validate the complete resulting declaration and load the released v3/v5 adapters before subsequent writes.
5. Do not reinterpret existing ticket estimates merely because v3 has been adopted.

## Compatibility

Declarations v1 through v4 remain supported according to their released compatibility matrix entries. Publishing declaration v5 must not silently upgrade or invalidate repositories pinned to prior declarations.

Unsupported mixtures such as Ticket Specification v3 with Development Workflow v4, or Ticket Specification v2 with Development Workflow v5, must fail closed.

## Rollback

Rollback means restoring a complete previously supported declaration pairing, not mixing individual old and new standards. Reverting from v5 must restore the prior declaration version and the matching released workflow/ticket adapters used by automation.