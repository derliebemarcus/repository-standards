# Ticket-based Development Workflow v3

## Status and normative language

This standard supersedes Ticket-based Development Workflow v2 only for repositories that explicitly
adopt version 3. Development Workflow v1 and v2 remain immutable for repositories pinned to those
versions.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

Ticket metadata, lifecycle, and description requirements are defined by Ticket Specification v2. A
repository using Development Workflow v3 MUST also adopt Ticket Specification v2.

## Incorporated Development Workflow v2 requirements

Except where this document explicitly supersedes a requirement, every normative requirement of
Ticket-based Development Workflow v2 remains in force for Development Workflow v3. This includes:

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
- review and merge requirements.

Where Development Workflow v2 refers to Ticket Specification v1, Development Workflow v3 instead
uses Ticket Specification v2. Where Development Workflow v2 describes ticket completion without a
canonical Forgejo representation, the lifecycle rules in this document supersede that description.

## Source of truth

A repository MUST declare the released standards it adopts and its branching model in
`.repository-standards.yml`. A Development Workflow v3 repository MUST use Repository Standards
declaration schema v2. Automation MUST validate the complete declared version set and MUST NOT infer,
coerce, or silently upgrade an unsupported combination.

## Repository creation

Repository creation MUST continue to ask:

> Does this repository use a `develop` branch?

The answer selects the same branching models as Development Workflow v2:

- `single`: `main` is the integration and release branch;
- `integration`: `develop` is the integration branch and `main` is the release branch.

For normal Jenkins Multibranch Pipeline projects, the branch discovery filter remains:

```regex
^(main|develop|PR-[0-9]+)$
```

## Single-branch declaration

A Development Workflow v3 repository using the single model MUST declare:

```yaml
version: 2
standards:
  ticket-specification: v2
  development-workflow: v3
  repository-documentation: v1
branching:
  model: single
  default_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Regular ticket branches MUST be created from `main` and ticket pull requests MUST target `main`.

## Integration-branch declaration

A Development Workflow v3 repository using the integration model MUST declare:

```yaml
version: 2
standards:
  ticket-specification: v2
  development-workflow: v3
  repository-documentation: v1
branching:
  model: integration
  default_branch: develop
  integration_branch: develop
  release_branch: main
  multibranch_filter: "^(main|develop|PR-[0-9]+)$"
```

Regular ticket branches MUST be created from `develop` and ticket pull requests MUST target
`develop`. Promotion from `develop` to `main` remains a manually created and manually merged release
pull request. Automation MUST NOT merge `develop` into `main`.

## Ticket lifecycle integration

A ticket branch MUST identify its ticket according to the Development Workflow branch naming rules.
When implementation begins, lifecycle automation MUST leave the Forgejo issue open and MUST set
exactly `Status/In Progress` as the active `Status/*` label.

A ticket MUST NOT enter the canonical completed state until all applicable Ticket Definition of Done
requirements are satisfied, including successful integration-branch verification where applicable.

The canonical completed transition is defined by Ticket Specification v2:

- Forgejo `state=closed`;
- exactly `Status/Done`;
- no active non-Done `Status/*` label.

Completion automation MUST establish `Status/Done` before removing the previous valid status and MUST
close the Forgejo issue as part of the same logical transition. A partial failure MUST preserve or
restore an unambiguous lifecycle state.

For the integration branching model, completion still occurs after verified integration into
`develop`; a regular ticket MUST NOT remain open merely to wait for the next release promotion to
`main`.

## Reopening

Reopening follows Ticket Specification v2. Automation MUST select exactly one active non-Done status,
MUST establish that replacement before removing `Status/Done`, and MUST set Forgejo `state=open` as
part of the same logical transition.

Automation MUST NOT guess a resumed status when the ticket context cannot determine it safely. An
explicit target status is required in that case.

## Compatibility contract

The supported released declaration pairings are machine-readable and validated by the repository
schema and compatibility profile.

Development Workflow v3 MUST NOT be combined with Ticket Specification v1. Development Workflow v2
MUST NOT be combined with Ticket Specification v2. Unsupported pairings MUST fail declaration
validation instead of being interpreted heuristically.

Repositories pinned to declaration schema v1, Ticket Specification v1, and Development Workflow v2
remain valid and unchanged. Publishing Development Workflow v3 does not migrate those repositories.

Before a repository adopts declaration schema v2, Ticket Specification v2, and Development Workflow
v3, every lifecycle writer used by that repository, including Workboard and Maintenance where
applicable, MUST support the Ticket Specification v2 completion and reopen invariants and MUST have
passed the required Canary validation.

## Migration boundary

Migration to Development Workflow v3 is an explicit repository change. It MUST:

1. validate the current declaration against its pinned schema;
2. verify lifecycle-writer compatibility with Ticket Specification v2;
3. validate or normalize ticket lifecycle data according to the Ticket Specification v2 migration
   process;
4. replace the repository declaration with a schema-v2 declaration using the supported v2/v3
   pairing;
5. run repository contract checks before enforcement is enabled;
6. preserve all existing branching-model semantics unless a separate approved requirement changes
   them.

Migration MUST NOT modify an already published standard or declaration schema in place.
