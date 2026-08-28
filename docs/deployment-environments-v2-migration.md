# Deployment Environments v2 and Repository Environments v1 migration

## Purpose

Deployment Environments v2 introduces `STAGING` as the canonical machine-readable staging environment name. Repository Environments v1 adds repository-owned human-web URLs in `.repository-environments.yml`.

Both contracts are opt-in. Deployment Environments v1 remains immutable.

## Compatibility boundary

| Contract | Canonical environments | Repository URL sidecar | Migration behavior |
| --- | --- | --- | --- |
| Deployment Environments v1 | `DEV`, `STAGE`, `PROD` | none | unchanged |
| Deployment Environments v2 | `DEV`, `STAGING`, `PROD` | Repository Environments v1 | explicit opt-in |

`STAGE` is not reinterpreted in v1 and is rejected by v2 metadata. `STAG` may be a UI abbreviation only.

The machine-readable compatibility matrix is `profiles/environment-contract-compatibility-v1.json`.

## Metadata-only adoption

A repository that needs to expose existing human-web environment URLs to inventory/navigation consumers may add `.repository-environments.yml` v1 without changing `.repository-standards.yml`.

The field:

```yaml
deployment-environments: v2
```

selects the v2 environment vocabulary for the sidecar only. It does not upgrade the repository's independently pinned deployment automation or standards bundle.

Example:

```yaml
version: 1
deployment-environments: v2
environments:
  DEV:
    url: "https://dev.example.invalid/"
  PROD:
    url: "https://example.invalid/"
```

A missing `STAGING` key means no STAGING web environment is declared. A repository with no human-web environment should omit the sidecar entirely.

## URL migration rules

Use only URLs verified from the repository's actual deployment/runtime configuration. Do not derive them from repository names, DNS naming conventions, design fixtures, or a central project list.

A declared URL must be absolute HTTP(S), have a host, contain no userinfo/credentials, and contain no fragment. Invalid present metadata fails closed.

Before committing a sidecar, validate it with:

```text
python tools/repository_environments.py path/to/.repository-environments.yml
```

## Runtime/deployment-policy migration

Publishing metadata does not change deployment policy. A repository that intends to adopt Deployment Environments v2 for its actual deployment lifecycle must use a separately released compatible integration path for its `.repository-standards.yml`/deployment tooling. Do not treat sidecar adoption as that migration.

## Existing consumers

Existing repositories pinned to Deployment Environments v1 remain valid and continue to use `STAGE`. No release of v2 or Repository Environments v1 automatically edits consumer repositories.

Consumer-side adoption is performed repository by repository, against each repository's authoritative branch and actual runtime URLs.

## Rollback

For metadata-only adoption, rollback is removal or reversion of `.repository-environments.yml`; this restores the previous state of having no URLs declared under Repository Environments v1. It must not mutate `.repository-standards.yml`.

For deployment-policy adoption, follow the separately released deployment integration's rollback procedure. Do not downgrade by silently interpreting `STAGING` as `STAGE`.
