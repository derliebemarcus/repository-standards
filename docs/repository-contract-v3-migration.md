# Repository Contract v3 Migration

## Purpose

Declaration schema v3 is the explicit opt-in contract set for organization-owned user-facing web
applications adopting Web Application Baseline v1 and Deployment Environments v1.

Publishing schema v3 does not migrate existing consumers. Declaration schema v1 and v2 remain valid
for repositories pinned to those released contract sets.

## Contract set

A v3 consumer declares:

```yaml
version: 3
standards:
  ticket-specification: v2
  development-workflow: v3
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

The branching block remains the existing `single` or `integration` model. Use the released reference
matching the repository's existing branching decision.

## Preconditions

Before migration, the repository MUST:

1. validate its current `.repository-standards.yml` against the currently pinned declaration schema;
2. already satisfy the Ticket Specification v2 / Development Workflow v3 lifecycle-writer
   prerequisites required by declaration v2, or complete that migration first;
3. identify that the repository owns a user-facing website or web application to which Web
   Application Baseline v1 is intended to apply;
4. have a current Design System decision where Repository Documentation rules require one;
5. implement the canonical static routes `/impressum`, `/datenschutz`, and `/barrierefreiheit` with
   project-specific, factually current content;
6. ensure those pages use the same application shell/design and accessibility gates as the rest of
   the website;
7. generate immutable artifact provenance containing source commit, build number, build time,
   release state, and release version when applicable;
8. implement deployment behavior that keeps source, artifact release state, and runtime environment
   independent;
9. ensure PROD accepts only immutable final-release artifacts and rollback selects a previously
   released artifact;
10. pass the required Maintenance/consumer Canary before blocking v3 enforcement is enabled.

A repository MUST NOT migrate merely because declaration schema v3 exists.

## Design System boundary

Web Application Baseline v1 does not force Design System adoption. It follows the repository's
existing `.design-system-consumer.json` decision:

- `decision: use`: the three required static pages use the same active Design System integration as
  the rest of the website;
- `decision: do-not-use`: the pages use the repository's own shared website design.

A separate legal-page theme is non-conformant in both cases.

## Artifact provenance migration

The artifact-producing pipeline becomes authoritative for release state and provenance. Deployment
MUST NOT reconstruct provenance from the current repository head or infer it from DEV/STAGE/PROD.

The public footer contract is:

- `non-release`: Commit · Build number · Build time;
- `release-candidate`: Release version · Build number · Build time;
- `release`: Release version only.

Build time is stored as ISO-8601 with an explicit timezone. A release candidate preserves its full
version identifier, including the RC suffix.

The final release MAY retain commit/build metadata internally for audit and rollback. Those fields
are not rendered publicly for the final-release state.

## Environment migration

Map the existing deployment flow to the canonical dimensions and environments.

### Single model

- `main` remains the integration branch;
- `main` is the default DEV source;
- a `main` build is not automatically a final release;
- PROD uses an explicitly selected immutable final-release artifact.

### Integration model

- `develop` remains the integration branch and default DEV source;
- existing manual `develop` to `main` release promotion remains unchanged;
- an RC may run on DEV or optional STAGE;
- PROD uses an explicitly selected immutable final-release artifact.

Preview/PR contexts are not canonical shared environments. STAGE remains optional.

## Migration procedure

1. complete the preconditions and downstream Maintenance compatibility work;
2. validate the current declaration and consumer state;
3. replace the declaration with the matching v3 reference structure;
4. validate the new declaration against `schemas/repository-standards-v3.schema.json` and the current
   compatibility profile;
5. validate Web Application Baseline v1 route, design, accessibility, and public-provenance rules;
6. validate Deployment Environments v1 source/artifact/environment, PROD, promotion, and rollback
   rules;
7. run repository, application, accessibility, release, deployment, and rollback tests;
8. run Canary validation with the compatible Maintenance implementation;
9. enable warning mode before blocking enforcement when the consumer rollout requires staging;
10. enable blocking enforcement only after the v3 contract is fully conformant.

## Failure handling

Migration MUST fail closed when:

- a required static page or navigation path is missing;
- project-specific legal or accessibility facts are unknown and would need to be invented;
- artifact release state or provenance cannot be determined from the built artifact;
- an environment is being used to infer release state;
- PROD can receive a non-release or release-candidate artifact;
- promotion rebuilds application content rather than selecting the verified immutable artifact;
- rollback cannot identify an existing immutable final-release artifact.

Failure to satisfy v3 does not invalidate the repository's previously supported declaration if that
previous declaration remains unchanged and conformant.

## Downstream responsibility

Repository Standards publishes the contract. `siczb/maintenance` owns Jenkins Shared Library,
artifact-provenance generation, deployment enforcement, and Canary implementation. Consumer
repositories own their legal text, application integration, environment configuration, and explicit
migration decision.
