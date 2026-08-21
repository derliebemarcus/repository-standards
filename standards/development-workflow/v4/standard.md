# Ticket-based Development Workflow v4

## Status and normative language

This standard supersedes Ticket-based Development Workflow v3 only for repositories that explicitly
adopt version 4. Development Workflow v1, v2, and v3 remain immutable for repositories pinned to
those versions.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

Ticket metadata, lifecycle, description requirements, and the canonical kind-to-branch-prefix
mapping are defined by Ticket Specification v2. A repository using Development Workflow v4 MUST
also adopt Ticket Specification v2.

## Incorporated Development Workflow v3 requirements

Except where this document explicitly supersedes a requirement, every normative requirement of
Ticket-based Development Workflow v3 remains in force for Development Workflow v4. Through v3,
this includes the unchanged Development Workflow v2 requirements for:

- repository bootstrap and the explicit `develop`-branch decision;
- single and integration branching models;
- branch protection and equivalent `main`/`develop` quality gates;
- branch naming and pull-request targeting;
- documentation-impact declarations;
- Forgejo workflow placement and runtime requirements;
- manual `main` builds;
- ticket and release Definitions of Done;
- manual `develop` to `main` release promotion;
- Hotfix reintegration;
- review and merge requirements;
- Ticket Specification v2 completion and reopen integration.

Development Workflow v4 supersedes the inherited branch- and pull-request-naming requirements only
where the rules below are more specific.

## Source of truth and released machine-readable assets

A repository MUST declare the released standards it adopts and its branching model in
`.repository-standards.yml`. A Development Workflow v4 repository MUST use Repository Standards
declaration schema v4.

Automation MUST validate the complete declared version set and MUST NOT infer, coerce, or silently
upgrade an unsupported combination.

The released machine-readable Development Workflow v4 profile is
`profiles/development-workflow-v4.json`. The canonical kind-to-prefix mapping is not duplicated in
that profile. It is referenced from the compatible Ticket Specification v2 profile at
`profiles/ticket-specification-v2.json#/branch_prefixes`.

A consumer MUST treat these released profiles as a single versioned contract set. It MUST NOT use
an unversioned branch, remembered rules, prompt history, or an independently maintained prefix list
as a substitute for the repository's pinned released contract.

## Pre-write validation

Before creating a ticket branch, an AI agent or other automation MUST:

1. read the target repository's `.repository-standards.yml`;
2. validate the complete declaration against its pinned released schema and compatibility profile;
3. load the released Development Workflow profile and compatible Ticket Specification profile;
4. read the referenced ticket metadata required for the naming decision, including the ticket kind;
5. validate the complete proposed branch name and source branch; and
6. perform the Forgejo branch write only after validation succeeds.

Before creating a ticket-linked pull request, an AI agent or other automation MUST perform the same
version resolution and MUST validate the proposed title, head branch, target branch, and ticket
correspondence before issuing the Forgejo pull-request write.

Pre-write validation MUST fail closed. A consumer MUST NOT create an intentionally invalid temporary
branch or pull request merely to discover whether post-write Forgejo validation rejects it.

A validation error SHOULD identify the violated rule and the expected canonical value when that
value can be derived without guessing.

## Branch naming contract

A regular ticket branch MUST use one of these forms:

```text
<prefix>/<ticket-number>-<ticket-title-slug>
<prefix>/<repository>-<ticket-number>-<ticket-title-slug>
```

The repository-qualified form MUST use the exact repository name containing the referenced ticket.
The ticket number MUST identify the ticket used for the naming decision.

The ticket-title slug MUST contain lowercase ASCII letters, digits, and single hyphens between
components. It MUST NOT contain spaces, uppercase letters, underscores, leading or trailing hyphens,
or empty hyphen-separated components.

For a regular ticket branch, `<prefix>` MUST equal the value selected from the compatible Ticket
Specification profile's `branch_prefixes` mapping for the ticket's single `Kind/*` label. An
undeclared alias MUST NOT be accepted. In particular, `Kind/Bug` maps to `bugfix`; `fix` is not a
canonical prefix and MUST be rejected.

The `hotfix` prefix is reserved for the explicit Hotfix process. It MUST NOT be treated as a generic
alias for `bugfix` or as a fallback when the ticket kind cannot be resolved. The inherited Hotfix
requirements remain in force: the branch is created from `main`, targets `main`, and is reintegrated
into `develop` in an integration-model repository.

## Pull-request naming contract

A ticket-linked pull request title MUST use this form:

```text
#<ticket-number> <summary>
```

The summary MUST contain non-whitespace content. The ticket number in the pull-request title MUST
match the ticket number encoded in the head branch name.

For a repository-qualified head branch, the repository segment MUST identify the repository that
contains that ticket. A consumer MUST NOT silently reinterpret a branch as referring to a different
ticket repository merely because the numeric ticket identifier exists there.

The pull-request target MUST follow the selected branching model. Regular branches target the
integration branch. Hotfix branches follow the inherited Hotfix target and reintegration rules.

## Exemptions

Automated dependency pull requests without a project ticket MAY remain exempt from ticket branch and
pull-request naming, as permitted by the inherited Development Workflow contract. An implementation
MUST identify such an exemption explicitly; a normal human- or agent-authored ticket pull request
MUST NOT receive the exemption merely because its actor name resembles a bot.

Development Workflow v4 defines no legacy creation-time cutoff exemption. A post-write naming check
implementing v4 MUST NOT bypass a ticket-linked pull request solely because it was created before an
implementation-specific date.

Any future naming exemption that changes which branch or pull-request names are accepted is a
contract change and MUST NOT be introduced only in a Forgejo workflow or consumer implementation.

## Defense-in-depth Forgejo validation

Repositories MAY and normally SHOULD retain a required Forgejo check for branch and pull-request
naming. For a Development Workflow v4 repository, that post-write check MUST implement semantics
consistent with the released v4 machine-readable profile and compatible Ticket Specification
profile.

The Forgejo check is defense in depth. Its existence does not remove the pre-write obligations for
AI agents or other automation that create branches or ticket-linked pull requests.

A repository-specific implementation MAY choose concrete trusted dependency-bot identities for the
contract-defined dependency-update exemption. It MUST NOT add accepted prefixes, title forms,
ticket-number exceptions, or legacy cutoffs that are absent from the released contract.

## Repository declaration schema v4

Development Workflow v4 repositories use declaration schema v4. The schema supports the same two
branching models and keeps the normal Jenkins Multibranch Pipeline filter:

```regex
^(main|develop|PR-[0-9]+)$
```

The schema supports the core contract set:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
```

It also supports the existing opt-in Web Application Baseline v1 and Deployment Environments v1 as
a paired extension of that same v4 workflow contract. Those web/deployment standards remain
independently versioned and unchanged.

The branching declaration remains `single` or `integration` exactly as defined by the inherited
workflow requirements. Regular ticket branches MUST continue to start from and target the selected
integration branch.

## Compatibility and migration boundary

Development Workflow v4 MUST NOT be combined with Ticket Specification v1. Unsupported declaration
and standard pairings MUST fail validation instead of being interpreted heuristically.

Publishing Development Workflow v4 does not migrate repositories pinned to earlier declaration or
workflow versions. Migration is an explicit repository change and MUST preserve all existing
branching-model, lifecycle, protection, release, documentation, web, and deployment semantics unless
a separately approved requirement changes them.

Before adopting Development Workflow v4, every branch- or pull-request-writing automation used by
the repository MUST support the released pre-write naming contract. Existing post-write Forgejo
naming enforcement SHOULD be aligned in the same rollout so both layers evaluate the same semantics.
