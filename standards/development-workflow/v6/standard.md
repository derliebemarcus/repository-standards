# Ticket-based Development Workflow v6

## Status and normative language

This standard supersedes Ticket-based Development Workflow v5 only for repositories that explicitly
adopt version 6. Development Workflow v1 through v5 remain immutable for repositories pinned to
those versions.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

Ticket metadata, lifecycle, estimation, and the canonical kind-to-branch-prefix mapping remain
defined by Ticket Specification v3. A repository using Development Workflow v6 MUST also adopt
Ticket Specification v3.

## Incorporated Development Workflow v5 requirements

Except where this document explicitly supersedes required-check identity and provider mapping,
every normative requirement of Ticket-based Development Workflow v5 remains in force for
Development Workflow v6. This includes unchanged requirements for repository bootstrap, branching,
branch protection, naming, pre-write validation, documentation impact, Forgejo workflow placement,
manual `main` builds, Definitions of Done, release promotion, Hotfix reintegration, review, merge,
lifecycle integration, dependency-update exemptions, and defense-in-depth validation.

Development Workflow v6 changes neither ticket semantics nor branch/release semantics. It adds a
portable identity contract for required quality gates and the provider-specific mapping needed to
implement that contract safely.

## Logical required quality gates

A required quality gate MUST have a logical identity that is independent from the source-control
provider's rendered commit-status or check name. Standards and repository policy MUST describe the
required engineering outcome by this logical identity rather than treating one provider-specific
status string as portable semantics.

An implementation MUST map every logical required gate to the concrete status/check identity
produced by the selected provider. The mapping MUST be deterministic, MUST be validated against the
active workflow configuration, and MUST fail closed when the configured required context cannot be
produced.

Changing workflow names, job names, event types, reusable-workflow structure, or another provider
input that changes the rendered required-check identity MUST be treated as a required-check identity
migration where that provider includes the changed input in the identity.

## Forgejo and Gitea Actions mapping

For Forgejo/Gitea Actions, a workflow job commit-status context is rendered as:

```text
<workflow> / <job> (<event>)
```

The event is therefore part of the concrete Forgejo/Gitea status-context identity. An implementation
MUST NOT assume that contexts produced by `pull_request` and `pull_request_target` are interchangeable
merely because workflow and job names are unchanged.

When a required Forgejo/Gitea workflow changes from one status-producing event to another, the
workflow change and the protected-branch required-context change MUST be planned and applied as one
logical migration. Validation MUST establish that every required context is producible by the active
workflow before the migration is considered complete.

Forgejo/Gitea implementations MAY use provider-supported glob or pattern matching to abstract an
event suffix only when the pattern is bounded to the intended logical gate. A pattern MUST NOT be so
broad that unrelated workflows or jobs can satisfy the required gate.

A repository MUST NOT leave a protected branch requiring a stale event-specific context after the
corresponding workflow no longer produces that context.

## GitHub Actions mapping

For GitHub required status checks, normal workflow checks are identified by job name; reusable
workflow checks add the reusable job name. GitHub required status-check identity does not include the
workflow name, matrix, or event trigger type.

A GitHub adapter MUST therefore map the logical gate to the check identity actually used by GitHub
and MUST NOT invent a Forgejo/Gitea-style event suffix. Provider adapters MUST remain distinct even
when the underlying workflow YAML is syntactically similar.

## `pull_request` and `pull_request_target` trust boundary

`pull_request_target` executes in the base/target-branch context and may receive privileges or
secrets unavailable to an untrusted pull-request workflow. A workflow using `pull_request_target`
MUST NOT execute, source, import, build, test, lint, or otherwise run pull-request-controlled code in
that privileged context.

`pull_request_target` SHOULD be limited to base-branch policy, metadata, labels, comments, ticket or
repository-policy evaluation, and equivalent operations that do not execute untrusted PR content.

A quality gate whose purpose is to validate the code proposed by the pull request MUST use an event
and checkout/execution model that actually validates that PR content with an appropriate untrusted
code boundary. A migration from `pull_request` to `pull_request_target` MUST NOT silently change a
code-validation gate into a base-branch-only validation.

## Required-check migration procedure

A required-check identity migration MUST:

1. identify the logical gate and its current provider mapping;
2. calculate the concrete context/check identity produced after the workflow change;
3. verify that the new workflow produces the expected identity on the intended commit;
4. update branch protection or rulesets consistently with the new provider mapping;
5. verify that no required context refers exclusively to a no-longer-producible identity; and
6. retain rollback information for both workflow and protection configuration until qualification
   succeeds.

Where the provider cannot make workflow and protection changes transactionally, automation MUST
order the migration so that it does not create an unintended merge-permission gap. A temporary
configuration MUST NOT weaken the required logical quality gate merely to avoid a pending status.

## Repository declaration schema v7

Development Workflow v6 repositories use Repository Standards declaration schema v7. The schema
retains Ticket Specification v3, Repository Documentation v1, Technology Baseline v1, the existing
optional Web Application Baseline v1 plus Deployment Environments v1 pair, and the existing single
or integration branching models.

The normal Jenkins Multibranch Pipeline filter remains:

```regex
^(main|develop|PR-[0-9]+)$
```

Publishing Development Workflow v6 does not migrate repositories pinned to earlier declarations.
Consumer adoption is explicit and release-pinned.

## Compatibility and implementation boundary

Forgejo remains the canonical source-control and automation provider for the canonical repository.
The provider-neutral logical-gate contract is portable; concrete provider adapters are not assumed to
share rendered status identities.

Before a repository adopts Development Workflow v6, every automation component that manages
required checks or branch protection MUST support the provider mapping and migration invariants in
this standard. Existing consumers MUST NOT be reinterpreted as v6 merely because their workflows
happen to use compatible names.
