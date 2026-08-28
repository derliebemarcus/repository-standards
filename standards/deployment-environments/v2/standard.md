# Deployment Environments v2

## Status and scope

This standard supersedes Deployment Environments v1 only for consumers that explicitly use the v2 vocabulary. Deployment Environments v1 remains immutable and valid for consumers pinned to it.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences are non-normative.

The standard defines the canonical relationship between source revisions, immutable artifacts, artifact release state, and runtime environments. It is provider-independent.

## Independent dimensions

Source, artifact release state, and runtime environment are independent dimensions and MUST NOT be collapsed into one another.

- **Source** identifies the repository revision or branch from which an artifact build starts.
- **Artifact release state** identifies whether the immutable built artifact is a `non-release`, `release-candidate`, or `release`.
- **Runtime environment** identifies where an already built artifact is deployed.

A branch name MUST NOT by itself make an artifact a release. An environment MUST NOT be used to infer an artifact's release state. Deployment MUST NOT rewrite release provenance.

## Canonical runtime environments

The canonical machine-readable environment names are, in this order:

1. `DEV`: development integration and verification environment;
2. `STAGING`: optional release-candidate/staging environment;
3. `PROD`: production environment.

`STAGE` is not a v2 environment name and MUST be rejected by v2 metadata and validators. `STAG` MAY be used only as a space-constrained UI abbreviation for `STAGING`; it MUST NOT be persisted as a machine-readable key.

A continuously testable deployed application SHOULD have a DEV deployment path. STAGING is optional. A repository that has a production deployment MUST model it as PROD.

Pull-request/preview builds are build contexts, not canonical shared environments. A preview MUST NOT be classified as DEV, STAGING, or PROD unless it intentionally uses that shared environment contract.

## Branch-to-DEV mapping

The default DEV source follows the repository's declared Development Workflow branching model.

| Branching model | Integration branch | Default DEV source |
| --- | --- | --- |
| `single` | `main` | `main` |
| `integration` | `develop` | `develop` |

A successful integration-branch artifact MAY be deployed automatically or manually according to the consumer pipeline. This standard does not override the adopted Development Workflow.

## STAGING semantics

STAGING is optional and, when present, is primarily intended for immutable release-candidate artifacts or final-release verification before production promotion.

A STAGING deployment MUST identify the exact immutable artifact being verified. Rebuilding from the same source revision for STAGING is not equivalent to promoting the previously verified artifact.

A consumer MAY omit STAGING when its risk model, release process, and validation gates do not require a separate staging runtime.

## PROD semantics

PROD MUST deploy only an immutable artifact whose release state is `release`.

A push or merge to `main` MUST NOT implicitly constitute a production release or production deployment. Production deployment MUST use the final-release artifact selected by the release process.

The artifact promoted to PROD MUST be byte-identical to the selected released artifact except for transport/container metadata explicitly documented as non-content-changing. Environment-specific configuration MAY be supplied at deployment time when required, but deployment MUST NOT rebuild or mutate versioned application content.

Rollback MUST select a previously known immutable release artifact. Rollback MUST NOT synthesize a new artifact from historical branch state.

## Release candidate semantics

A release candidate is an artifact state, not an environment. A release-candidate artifact MAY be deployed to DEV or STAGING according to the consumer's release process. It MUST NOT be deployed to PROD as if it were a final release.

Promotion from release candidate to final release MUST establish a final `release` artifact state through the adopted release process. Merely moving the same deployment to PROD MUST NOT relabel a release-candidate artifact as final.

## Artifact identity and provenance

Every deployment MUST retain a stable artifact identity sufficient to determine:

- the artifact-producing build;
- the source revision bound to the artifact;
- the artifact release state; and
- the release version when applicable.

Environment metadata MAY record deployment time, deployment job, target host, or rollback lineage, but those fields are deployment provenance and MUST NOT replace build-artifact provenance.

## Promotion rules

Promotion MUST move or select an existing immutable artifact between validation stages. It MUST NOT silently rebuild application content.

Conformant transitions include:

- integration-branch `non-release` artifact to DEV;
- `release-candidate` artifact to DEV or STAGING;
- final `release` artifact to STAGING for optional verification;
- final `release` artifact to PROD; and
- previously released immutable artifact to PROD for rollback.

Non-conformant transitions include:

- branch state directly to PROD without a final-release artifact;
- `non-release` artifact to PROD;
- `release-candidate` artifact to PROD as final;
- environment name changing the artifact release state; and
- rebuilding an artifact during promotion and treating it as the previously verified artifact.

## Repository-owned web environment metadata

Concrete human-web URLs are repository-owned metadata, not naming-convention output. The released Repository Environments v1 sidecar contract defines `.repository-environments.yml` for this purpose.

A consumer of that sidecar MUST read only declared URLs. It MUST NOT derive URLs from repository names, environment names, DNS conventions, or a centrally maintained project-to-URL table.

The sidecar's `deployment-environments: v2` field selects this v2 environment vocabulary for the metadata document. It does not rewrite, upgrade, or otherwise mutate the repository's independently pinned `.repository-standards.yml` declaration or deployment automation.

## Validation contract

Validation of v2 MUST check at least:

- only `DEV`, `STAGING`, and `PROD` are accepted as canonical environment names;
- `STAGE` is rejected;
- STAGING remains optional;
- the declared branching model resolves to the correct default DEV branch;
- source, artifact release state, and environment are represented independently;
- Preview/PR context is not treated as a canonical shared environment;
- PROD accepts only final-release artifacts;
- a production deployment references an immutable released artifact;
- rollback references an existing immutable release artifact; and
- promotion does not rebuild application content.

Contract failures that would permit an unreleased or ambiguously identified artifact to reach PROD MUST block deployment.

## Compatibility and migration

Deployment Environments v1 remains unchanged. Publishing v2 MUST NOT reinterpret `STAGE` as `STAGING` for a v1 consumer and MUST NOT automatically migrate any pinned consumer.

Migration is explicit. A metadata-only consumer MAY adopt Repository Environments v1 to publish navigation URLs using the v2 vocabulary without changing its `.repository-standards.yml` pin. A deployable consumer that intends to adopt v2 for runtime/deployment policy MUST do so through an explicitly released compatible repository/deployment integration rather than treating metadata publication as an implicit pipeline migration.
