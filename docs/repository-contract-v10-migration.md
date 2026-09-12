# Repository declaration v10 migration

## Purpose

Declaration v10 is the explicit adoption boundary for Web Application Baseline v3. It does not
reinterpret or mutate Declaration v9.

For the declaration-v10 release boundary, the additive compatibility profile is:

`profiles/repository-standards-compatibility-v9.json`

Later Repository Standards releases may publish newer additive compatibility profiles. Those newer
profiles preserve this released v10 pairing rather than changing its meaning. Unsupported pairings
fail closed.

## Supported v10 pairings

### Core

Declaration v10 Core retains the v9 core contract set:

- Ticket Specification v4;
- Development Workflow v8;
- Repository Documentation v2;
- Technology Baseline v1; and
- Contract-first Delivery v1.

Core v10 does not select a Web Application Baseline and does not require Repository Localization v1.

### Web

Declaration v10 Web selects:

- Ticket Specification v4;
- Development Workflow v8;
- Repository Documentation v2;
- Technology Baseline v1;
- Contract-first Delivery v1;
- Web Application Baseline v3; and
- Deployment Environments v1.

WAB v3 additionally requires the independently versioned Repository Localization v1 sidecar at
`.repository-localization.yml`. The sidecar is not duplicated as a `.repository-standards.yml`
standard key.

## Branching references

The four canonical v10 references are:

- `reference/repository-standards-v10.single.yml`;
- `reference/repository-standards-v10.integration.yml`;
- `reference/repository-standards-v10.web.single.yml`; and
- `reference/repository-standards-v10.web.integration.yml`.

Both branching models retain `^(main|develop|PR-[0-9]+)$` as the normal Jenkins Multibranch filter.

## v9 compatibility boundary

Declaration v9 remains immutable. Its web pairing continues to select Web Application Baseline v2
and Deployment Environments v1. A v9 consumer must not be treated as a WAB v3 consumer merely
because its application happens to contain language-prefixed routes.

Migration to v10 is explicit and release-pinned. It requires compatible writing/lifecycle/CI
automation and, for the web pairing, valid Repository Localization v1 plus qualified WAB v3
conformance enforcement.

## Later declaration generations

Publication of declaration v11 does not obsolete or reinterpret v10. A v10 consumer remains on the
v10 pairing until it deliberately migrates. The current additive compatibility profile can therefore
be newer than compatibility v9 while the v10 contract described here stays unchanged.

Use `docs/reference/compatibility.md` to resolve the latest additive compatibility profile; use this
document to understand the immutable v10 migration boundary.

## Localization and design-source sidecars

Repository Localization v1 is mandatory only for the v10 WAB v3 web pairing. Design Source
Declaration v1 remains independently versioned and may be adopted where the repository requires a
repository-owned normative design-source binding. Neither sidecar changes an older declaration pin
implicitly.

## Deployment Environments

Declaration v10 Web intentionally retains Deployment Environments v1. Deployment Environments v2
and Repository Environments v1 remain independently additive contracts and are not coupled to the
WAB v3 migration.

## Rollback

Rollback restores the previous released declaration and all declaration-required sidecars as one
coherent contract set. A repository must not roll back only `.repository-standards.yml` while
continuing to interpret routes under an incompatible Web Application Baseline, or activate v10 Web
without valid localization metadata.
