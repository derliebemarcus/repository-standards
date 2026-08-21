# Deployment Environments v1

## Status and scope

This standard defines the canonical relationship between source revisions, built artifacts, release
state, and runtime environments for repositories that explicitly adopt it.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

The standard is intentionally independent of any specific hosting provider. It applies to web
applications and MAY be adopted by other deployable software where the same environment semantics
are useful.

## Independent dimensions

Source, artifact release state, and runtime environment are independent dimensions and MUST NOT be
collapsed into one another.

- **Source** identifies the repository revision or branch from which an artifact build starts.
- **Artifact release state** identifies whether the immutable built artifact is a `non-release`,
  `release-candidate`, or `release`.
- **Runtime environment** identifies where an already built artifact is deployed.

A branch name MUST NOT by itself make an artifact a release. An environment MUST NOT be used to
infer an artifact's release state. Deployment MUST NOT rewrite release provenance.

## Canonical runtime environments

The canonical environment names are:

- `DEV`: development integration and verification environment;
- `STAGE`: optional release-candidate/staging environment;
- `PROD`: production environment.

An adopting repository MUST have a DEV deployment path when it deploys a continuously testable
application. STAGE is optional. A repository that has a production deployment MUST model it as
PROD.

Pull-request/preview builds are build contexts, not regular environments. A consumer MAY publish a
short-lived preview deployment, but it MUST NOT classify that preview as DEV, STAGE, or PROD unless
it is intentionally using the corresponding shared environment contract.

## Branch-to-DEV mapping

The default DEV source follows the repository's declared Development Workflow branching model.

| Branching model | Integration branch | Default DEV source |
| --- | --- | --- |
| `single` | `main` | `main` |
| `integration` | `develop` | `develop` |

A successful integration-branch artifact MAY be deployed automatically or manually according to the
consumer pipeline, but build triggering MUST continue to obey the adopted Development Workflow. In
particular, this standard does not override the Development Workflow rule governing manual `main`
builds.

A consumer MAY deploy a release-candidate artifact to DEV for verification. Doing so does not change
the default branch-to-DEV mapping and does not make DEV a release environment.

## STAGE semantics

STAGE is optional and, when present, is primarily intended for immutable release-candidate artifacts
or final-release verification before production promotion.

A STAGE deployment MUST identify the exact immutable artifact being verified. Rebuilding from the
same source revision for STAGE is not equivalent to promoting the previously verified artifact.

A consumer MAY omit STAGE when its risk model, release process, and validation gates do not require a
separate staging runtime.

## PROD semantics

PROD MUST deploy only an immutable artifact whose release state is `release`.

A push or merge to `main` MUST NOT implicitly constitute a production release or production
deployment. Production deployment MUST use the final-release artifact selected by the release
process.

The artifact promoted to PROD MUST be byte-identical to the selected released artifact except for
transport/container metadata that is explicitly documented as non-content-changing. Environment-
specific configuration MAY be supplied at deployment time when the application architecture
requires it, but deployment MUST NOT rebuild or mutate versioned application content.

Rollback MUST select a previously known immutable release artifact. Rollback MUST NOT synthesize a
new artifact from the historical branch state.

## Release candidate semantics

A release candidate is an artifact state, not an environment. A release-candidate artifact MAY be
deployed to DEV or STAGE according to the consumer's release process. It MUST NOT be deployed to
PROD as if it were a final release.

Promotion from release candidate to final release MUST establish a final `release` artifact state
through the adopted release process. Merely moving the same deployment to PROD MUST NOT relabel a
release-candidate artifact as final.

## Artifact identity and provenance

Every deployment MUST retain a stable artifact identity sufficient to determine:

- the artifact-producing build;
- the source revision bound to the artifact;
- the artifact release state;
- the release version when applicable.

For consumers of Web Application Baseline v1, the provenance fields and public rendering rules are
defined by that standard.

Environment metadata MAY record deployment time, deployment job, target host, or rollback lineage,
but those fields are deployment provenance and MUST NOT replace build-artifact provenance.

## Promotion rules

Promotion MUST move or select an existing immutable artifact between validation stages. It MUST NOT
silently rebuild application content.

The following transitions are conformant:

- integration-branch `non-release` artifact to DEV;
- `release-candidate` artifact to DEV or STAGE;
- final `release` artifact to STAGE for optional verification;
- final `release` artifact to PROD;
- previously released immutable artifact to PROD for rollback.

The following transitions are non-conformant:

- branch state directly to PROD without a final-release artifact;
- `non-release` artifact to PROD;
- `release-candidate` artifact to PROD as final;
- environment name changing the artifact release state;
- rebuilding an artifact during promotion and treating it as the previously verified artifact.

## Validation contract

For an adopting deployable consumer, validation MUST check at least:

- the declared branching model resolves to the correct default DEV branch;
- source, artifact release state, and environment are represented independently;
- Preview/PR context is not treated as a canonical shared environment;
- PROD accepts only final-release artifacts;
- a production deployment references an immutable released artifact;
- rollback references an existing immutable release artifact;
- promotion does not rebuild application content;
- STAGE, when present, does not weaken PROD release requirements.

Contract failures that would permit an unreleased or ambiguously identified artifact to reach PROD
MUST block deployment.

## Consumer adoption

Adoption MUST be explicit through a released repository declaration schema that lists
`deployment-environments: v1`. Consumers MUST remain pinned until an explicit migration is made.

The concrete Jenkins Shared Library and deployment-job implementation is owned by
`siczb/maintenance`. This repository owns only the normative and machine-readable contract.
