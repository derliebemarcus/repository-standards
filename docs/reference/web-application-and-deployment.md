# Web Application and Deployment Interaction Model

## Purpose

Web Application Baseline v1 and Deployment Environments v1 are separate contracts with one shared
boundary: immutable artifact provenance. The web baseline defines what a website exposes to users;
the deployment standard defines how an artifact moves through runtime environments.

Neither standard changes Development Workflow v3 branch, review, or build-trigger semantics.

## Three independent dimensions

A deployment must retain three independent facts:

| Dimension | Examples | Meaning |
| --- | --- | --- |
| Source | `feature/*`, `develop`, `main`, tag/source revision | Where the build started |
| Artifact release state | `non-release`, `release-candidate`, `release` | What the built artifact is |
| Runtime environment | DEV, STAGE, PROD | Where the existing artifact runs |

An environment never changes artifact release state. A branch name never proves that an artifact is
a final release.

## Default environment mapping

The default DEV source follows the Development Workflow branching model:

- `single`: `main` is the integration branch and default DEV source;
- `integration`: `develop` is the integration branch and default DEV source.

Preview or pull-request builds are build contexts and are not canonical shared environments. STAGE
is optional. PROD accepts only an immutable final-release artifact.

The Development Workflow rule for manually triggered `main` builds remains in force. A deployment
implementation may deploy a successful artifact automatically only when doing so does not implicitly
create or trigger a forbidden build.

## Artifact release states and public provenance

The artifact-producing pipeline creates one immutable provenance record. At minimum it identifies the
source commit, build number, build time, release state, and release version when applicable.

Web Application Baseline v1 renders only the state-appropriate public subset in the global footer of
`/impressum`, `/datenschutz`, and `/barrierefreiheit`:

| State | Public rendering |
| --- | --- |
| `non-release` | Commit · Build number · Build time |
| `release-candidate` | Release version · Build number · Build time |
| `release` | Release version |

The final-release artifact can retain commit/build metadata internally for audit and rollback even
though the public footer renders only the release version.

## Example: single branching model

A normal `main` build produces a `non-release` artifact unless the release process explicitly creates
a release candidate or final release. The artifact may be deployed to DEV.

A final release is an immutable artifact selected by the release process. Only that artifact may be
promoted to PROD. A later `main` commit does not retroactively change the deployed release identity.

## Example: integration branching model

A normal `develop` build produces a `non-release` artifact for DEV. The existing Development Workflow
continues to require manual release promotion from `develop` to `main`.

A release candidate may be deployed to DEV or optional STAGE. A final release artifact may be
verified on STAGE and promoted unchanged to PROD.

## Rollback

Rollback selects a previously released immutable artifact. It does not rebuild historical branch
state. Consequently the public provenance shown after rollback is the provenance embedded in that
released artifact rather than metadata from the current repository head.

## Design and accessibility

The required static pages are part of the user-facing application, not a detached legal microsite.
They use the same application shell, design conventions, responsive behavior, and accessibility
quality gates as the rest of the website.

If `.design-system-consumer.json` declares `decision: use`, the pages use the same active
`siczb/design-system` integration. If the repository deliberately does not use the Design System,
the pages still use the repository's shared application design.

## Validation boundary

Repository Standards defines normative and machine-readable rules. `siczb/maintenance` owns build
metadata generation and Jenkins/deployment enforcement. A consumer migration to declaration schema
v3 must not enable blocking enforcement until the corresponding Maintenance implementation has
passed Canary validation.
