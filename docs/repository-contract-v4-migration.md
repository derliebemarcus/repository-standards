# Repository Contract v4 migration

## Purpose

Repository Standards declaration schema v4 is the explicit adoption boundary for Development
Workflow v4. It adds fail-closed, released-contract validation before automation creates ticket
branches or ticket-linked pull requests.

Publishing v4 does not migrate a repository. Existing declaration v1, v2, and v3 consumers remain
on their pinned behavior until an explicit migration is reviewed and merged.

## Preconditions

Before changing a repository to declaration v4:

1. the current `.repository-standards.yml` MUST validate against its currently pinned contract;
2. Ticket Specification v2 lifecycle writes MUST already be supported by every lifecycle writer;
3. every AI agent or automation that can create ticket branches or ticket-linked pull requests MUST
   support Development Workflow v4 pre-write validation;
4. the compatible Maintenance implementation from `siczb/maintenance#511` MUST be merged and its
   minimum compatible revision MUST be documented;
5. the repository's post-write Forgejo naming check SHOULD be aligned with Development Workflow v4
   semantics in the same rollout; and
6. required branch protection, review, quality, and manual-main-build rules MUST remain effective.

Until the Maintenance prerequisite is released, repositories MUST NOT migrate to declaration v4.

## Core contract migration

A non-web repository adopting Development Workflow v4 uses the core declaration:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Use `reference/repository-standards-v4.integration.yml` instead when the repository uses the
integration branching model.

The migration does not change the selected branching model. A single-model repository remains
single; an integration-model repository remains integration unless a separate approved change
explicitly changes that architecture decision.

## Web/deployment contract migration

A declaration-v3 web/deployment consumer retains both existing opt-in contracts while adopting
Development Workflow v4:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

The corresponding reference declarations are:

- `reference/repository-standards-v4.web.single.yml`;
- `reference/repository-standards-v4.web.integration.yml`.

Web Application Baseline v1 and Deployment Environments v1 remain unchanged. Partial adoption of
only one of those two contracts is unsupported under declaration v4.

## Naming behavior after migration

Development Workflow v4 uses
`profiles/ticket-specification-v2.json#/branch_prefixes` as the single kind-to-prefix source.
Automation MUST resolve the ticket kind and validate the complete proposed mutation before the
Forgejo write.

Examples for a `Kind/Bug` ticket `#123`:

| Proposed branch | Result | Reason |
| --- | --- | --- |
| `bugfix/123-example-bug` | valid naming candidate | `Kind/Bug` maps to `bugfix` |
| `fix/123-example-bug` | reject before write | `fix` is undeclared |
| `hotfix/123-example-bug` | regular path: reject | `hotfix` requires the explicit Hotfix path |

A ticket-linked pull request uses `#<ticket-number> <summary>`. Its title ticket number MUST match the
number encoded in the head branch.

## Rollout sequence

Recommended rollout:

1. release Repository Standards with Development Workflow v4 and declaration schema v4;
2. implement and qualify `siczb/maintenance#511` against the released artifacts;
3. record the minimum compatible Maintenance revision in compatibility documentation;
4. migrate one Canary repository and verify both pre-write and Forgejo defense-in-depth behavior;
5. verify existing branch protection, review, lifecycle, build, and deployment gates; and
6. migrate additional repositories explicitly.

The Canary MUST demonstrate that an invalid alias such as `fix/123-example-bug` is rejected before a
branch write and that the equivalent Forgejo post-write check would reject the same semantics.

## Failure and rollback

A migration MUST fail rather than guess when the declaration pairing is unsupported, ticket kind
cannot be resolved, a canonical prefix cannot be derived, or a proposed branch/pull request violates
the released contract.

If a migration cannot be completed safely, revert the repository migration commit and continue using
the previously pinned, still-supported declaration. Do not alter a published standard or compatibility
profile to make a partially migrated consumer appear valid.
