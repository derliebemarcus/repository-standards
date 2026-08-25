# Repository contract v7 migration

## Purpose

Declaration schema v7 is the explicit opt-in boundary for Development Workflow v6 and its
provider-neutral required-check identity contract. It preserves Ticket Specification v3,
Repository Documentation v1, Technology Baseline v1, the existing optional Web Application
Baseline v1 plus Deployment Environments v1 pair, and the existing branching models.

Publishing declaration v7 does not implicitly migrate declaration-v1 through declaration-v6
consumers.

## Why v7 is required

Forgejo/Gitea and GitHub expose different concrete identities for Actions checks that represent the
same logical engineering gate. Forgejo/Gitea includes the triggering event in the rendered status
context:

```text
<workflow> / <job> (<event>)
```

GitHub required status checks use job-based identities and do not include the event trigger in that
identity. Treating either concrete string as portable policy causes migration defects.

Development Workflow v6 therefore separates a stable logical required gate from the provider
adapter that maps it to a concrete status/check identity.

## Preconditions

Before changing a consumer to `version: 7`:

1. validate the current declaration against its pinned released schema;
2. verify that branch-protection and required-check automation supports Development Workflow v6;
3. inventory every logical required gate and its concrete provider mapping;
4. verify that each required context/check can be produced by the active workflow configuration;
5. classify every `pull_request_target` workflow by trust boundary and ensure that it does not
   execute pull-request-controlled code in a privileged base-branch context;
6. verify that the existing Technology Baseline v1 enforcement remains operational; and
7. retain rollback information for the current workflow and branch-protection configuration.

## Declaration change

Core single-branch consumers use `reference/repository-standards-v7.single.yml`. Integration-branch
consumers use `reference/repository-standards-v7.integration.yml`. Web consumers use the
corresponding `repository-standards-v7.web.*.yml` reference.

The Development Workflow entry changes from v5 to v6:

```yaml
version: 7
standards:
  ticket-specification: v3
  development-workflow: v6
  repository-documentation: v1
  technology-baseline: v1
```

The branching model and Jenkins Multibranch filter remain unchanged.

## Required-check inventory

For every protected branch, record:

- logical gate identity and intended engineering outcome;
- provider (`forgejo_gitea` or `github` where applicable);
- workflow name and job name;
- triggering event;
- concrete context/check identity currently required by branch protection or a ruleset;
- whether the gate evaluates base-branch policy/metadata or executes pull-request content; and
- rollback values for workflow and protection configuration.

A context that cannot be produced by an active workflow is a migration blocker.

## Forgejo/Gitea event migrations

For Forgejo/Gitea, the event is part of the concrete status-context identity. A change from
`pull_request` to `pull_request_target`, or another status-producing event change, MUST therefore be
handled as a required-check identity migration.

The migration MUST:

1. calculate the new `<workflow> / <job> (<event>)` context;
2. verify that the changed workflow produces that context on the intended commit;
3. update branch protection consistently with the workflow change;
4. reject a configuration that leaves only the old event-specific context required; and
5. verify the logical gate again after the migration.

Provider-supported glob or pattern matching MAY be used only when the pattern is bounded to the
intended workflow/job gate. A broad wildcard that allows unrelated checks to satisfy protection is
not conformant.

## GitHub mapping

A GitHub adapter maps a normal workflow gate to the job check name and a reusable-workflow gate to
the job plus reusable-job identity used by GitHub. It MUST NOT add the Forgejo/Gitea event suffix.

Workflow YAML compatibility does not imply status-identity compatibility. Provider adapters remain
separate.

## `pull_request_target` security boundary

`pull_request_target` runs in the base/target-branch context and can have privileges unavailable to
an untrusted pull-request workflow. It MUST NOT execute, source, import, build, test, lint, or
otherwise run pull-request-controlled code in that privileged context.

Use `pull_request_target` only for operations such as base-branch policy, metadata, labels, comments,
ticket linkage, and repository-governance evaluation where untrusted PR content is not executed.

A gate intended to validate proposed code MUST use an event and checkout/execution model that
actually validates the PR content under an appropriate untrusted-code boundary. An event migration
must not silently turn a code-validation gate into base-branch-only validation.

## Qualification

A v7 migration is qualified only when:

- the declaration validates against schema v7 and compatibility profile v6;
- all required logical gates still exist;
- every concrete required check/context is producible;
- Forgejo/Gitea event-specific mappings and GitHub mappings match their provider semantics;
- no privileged `pull_request_target` workflow executes PR-controlled code;
- branch protection has no stale required context;
- normal repository validation and Jenkins qualification succeed; and
- rollback evidence remains available until qualification is complete.

## Rollback

If required-check migration or enforcement is not operationally safe, restore both the previous
workflow configuration and its matching branch-protection/ruleset mapping, then restore the
previously pinned repository declaration. Do not weaken the logical gate to clear a pending status
and do not mutate any published schema, standard, compatibility profile, or reference declaration.
