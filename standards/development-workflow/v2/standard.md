# Ticket-based Development Workflow v2

## Status and normative language

This standard supersedes Ticket-based Development Workflow v1 for repositories that opt into
version 2. Version 1 remains immutable for existing pinned consumers.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

Ticket metadata and description requirements are defined by Ticket Specification v1. A repository
using this workflow MUST also adopt Ticket Specification v1.

## Source of truth

Every implementation starts from a ticket. The complete ticket description and all comments MUST
be read before work begins. The latest explicit requirement wins when statements conflict.

The repository MUST declare its pinned standards and branching model in
`.repository-standards.yml`. Automation MUST use the released versions named by that declaration
and MUST NOT infer policy from an unversioned branch.

## Repository creation

Repository creation MUST ask this explicit question:

> Does this repository use a `develop` branch?

The answer MUST select one branching model:

- `single`: `main` is the integration and release branch;
- `integration`: `develop` is the integration branch and `main` is the release branch.

The selection MUST be stored in `.repository-standards.yml`. Repository bootstrap MUST NOT create a
`develop` branch unless the integration model was selected.

For normal Jenkins Multibranch Pipeline projects, the branch discovery filter MUST be:

```regex
^(main|develop|PR-[0-9]+)$
```

The same filter MAY be used for single-model repositories; a missing `develop` branch simply
produces no matching branch.

## Branch protection

Direct pushes to protected integration and release branches MUST be disabled. Changes MUST use pull
requests.

Protected branches MUST require the same applicable:

- status checks;
- review policy;
- outdated-branch handling;
- signed-commit policy when enabled;
- test, documentation, security, compatibility, and operational quality gates.

In the integration model, `main` and `develop` MUST use equivalent protection and quality
requirements. Their semantic roles differ, but neither branch MAY use a weaker engineering gate.

## Single-branch model

A repository using the single model MUST declare:

```yaml
version: 1
standards:
  ticket-specification: v1
  development-workflow: v2
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Regular ticket branches MUST be created from `main`. Ticket pull requests MUST target `main`.
Successful integration and verification on `main` complete the branch portion of the ticket
Definition of Done.

## Integration-branch model

A repository using the integration model MUST declare:

```yaml
version: 1
standards:
  ticket-specification: v1
  development-workflow: v2
branching:
  model: integration
  default_branch: develop
  integration_branch: develop
  release_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

`develop` MUST initially be created from `main` and SHOULD be configured as the Forgejo default
branch.

Regular ticket branches MUST be created from `develop`. Regular ticket pull requests MUST target
`develop` and MUST NOT target `main`.

Promotion from `develop` to `main` MUST occur through a release pull request. The release pull
request MUST be created manually and merged manually. Automation MUST NOT merge `develop` into
`main`.

A release pull request MUST contain only changes already integrated into `develop` and release
metadata prepared on `develop`. It MUST NOT introduce unrelated implementation changes.

After a release merge, `develop` and `main` MUST represent the same released history, except for
documented transient differences required by the source-control merge strategy.

## Ticket state

The ticket MUST be marked `Status/In Progress` when the implementation branch is created. It MUST
remain in progress until the implementation is merged into the model's integration branch and
verified.

The integration branch is:

- `main` for the single model;
- `develop` for the integration model.

A ticket MAY be marked done only after the branch is closed, the integration-branch build is
successful where applicable, and all acceptance criteria are satisfied.

A regular ticket in the integration model MUST NOT wait for the next release promotion to
`main`.

## Branch names

Ticket branches use one of these forms:

```text
<type>/<ticket-number>-<ticket-title-slug>
<type>/<repository>-<ticket-number>-<ticket-title-slug>
```

The repository-qualified form uses the exact repository name containing the ticket. Slugs are
lowercase ASCII with hyphens and no spaces.

Type prefixes are `feature`, `enhancement`, `bugfix`, `hotfix`, `refactoring`, `maintenance`,
`documentation`, `security`, `test`, and `research`.

The branch prefix MUST match the ticket kind or the explicitly selected Hotfix path.

## Pull requests

A ticket-linked pull request title MUST start with `#<ticket-number>`. It is ready for review by
default. Draft status is used only when explicitly requested or when the pull request intentionally
communicates incomplete work.

The pull request target MUST follow the selected branching model.

The pull request MUST describe:

- the implemented scope;
- acceptance-criteria coverage;
- validation performed;
- documentation impact;
- security, compatibility, release, and deployment impact where applicable.

## Documentation impact declaration

Every pull request MUST choose exactly one outcome:

1. affected documentation was updated in the same pull request; or
2. no documentation update is required, with a concrete explanation.

The declaration MUST consider all repository-owned documentation. It MUST NOT be satisfied by
changing an unrelated Markdown file.

## Forgejo automation

Forgejo is the leading source-control and automation system. Active Forgejo Actions workflows MUST
be stored in `.forgejo/workflows/`. Executable workflow files MUST NOT remain in
`.github/workflows/`.

The `.github/` directory MAY contain non-executable compatibility metadata needed by mirrors or
external consumers. GitHub-specific or historical one-shot automation MUST be ported, removed, or
archived outside the active Forgejo workflow path.

Forgejo workflows MUST use Forgejo events, API semantics, and `FORGEJO_*` context where applicable.
Referenced actions MUST use fully qualified trusted URLs. Workflow runtime dependencies MUST be
declared explicitly, and workflows intended for organization runners MUST support ARM64.

Builds of `main` MUST be triggered manually. Automation MAY prepare release evidence and expose a
manual action, but MUST NOT start a `main` build automatically.

## Ticket Definition of Done

Ticket work is done only when:

- all current ticket requirements and acceptance criteria are implemented;
- tests, static checks, contracts, and required external checks pass;
- the complete `docs/` tree was assessed and affected documents were updated;
- architecture changes are reflected in architecture documentation;
- durable decisions are recorded or superseded through ADRs;
- configuration, compatibility, installation, upgrade, release, deployment, and operations
  guidance is current;
- no known placeholder, temporary bypass, or undocumented manual step remains;
- the pull request is merged into the selected integration branch;
- the resulting integration-branch build is successful where applicable.

For the integration model, this Definition of Done ends at verified integration into `develop`.
Release promotion to `main` is governed separately.

## Release process

A repository using the integration model MUST use an explicit release process:

1. create or select a release ticket;
2. fix the release scope from tickets already integrated into `develop`;
3. resolve release blockers;
4. run the complete release validation against `develop`;
5. prepare version, changelog, release notes, and migration guidance on `develop`;
6. create a manual pull request from `develop` to `main`;
7. review release evidence and compatibility;
8. merge the pull request manually;
9. trigger and verify the `main` build manually;
10. create the tag and Forgejo release when versioned releases are used;
11. verify that `develop` contains the released state.

The release pull request MUST NOT be used to implement new ticket scope.

## Release Definition of Done

A release is done only when:

- the release scope and blockers are explicit;
- the selected `develop` state passed required validation;
- versioning, changelog, release notes, migration, and rollback guidance are complete;
- the manual `develop` to `main` pull request was reviewed and merged;
- the resulting manually triggered `main` build is successful;
- required tags and Forgejo releases exist;
- any post-release synchronization is complete.

## Hotfix process

Hotfix is an exception to regular integration flow.

A Hotfix branch MUST be created from `main` and MUST use the `hotfix/` prefix. The Hotfix pull
request MUST target `main`.

In an integration-model repository, the merged Hotfix MUST then be reintegrated into `develop`
through a traceable pull request or equivalent protected merge. The reintegration MUST preserve the
same fix and MUST pass the normal `develop` quality gates.

`main` and `develop` MUST NOT remain permanently divergent after a Hotfix.

## Review and merge

Review MUST assess correctness, maintainability, tests, documentation, security, compatibility,
and operational safety. Passing automation does not replace review of semantic documentation
drift.

Automated dependency pull requests without a project ticket MAY be exempt from ticket naming, but
they remain subject to repository checks, target-branch rules, and documentation-impact
assessment.
