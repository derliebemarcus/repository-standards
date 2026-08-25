# Repository contract v6 migration

## Purpose

Declaration schema v6 is the explicit opt-in boundary for Technology Baseline v1. It does not
implicitly migrate declaration-v1 through declaration-v5 consumers.

## Preconditions

Before changing a consumer to `version: 6`:

1. validate the repository against Technology Baseline v1;
2. identify runtime, database, framework, and container-base deviations;
3. create ADR-backed exceptions for deviations that cannot be removed before migration;
4. ensure the Jenkins implementation can evaluate the consumer and publish the Technology Baseline
   compliance gate;
5. verify that notification and finding state are operationally configured.

## Declaration change

Core single-branch consumers migrate to the structure in
`reference/repository-standards-v6.single.yml`. Integration-branch consumers use
`reference/repository-standards-v6.integration.yml`. Web consumers use the corresponding
`repository-standards-v6.web.*.yml` reference.

The new mandatory entry is:

```yaml
standards:
  technology-baseline: v1
```

Ticket Specification v3, Development Workflow v5, and Repository Documentation v1 remain unchanged
from declaration v5. Web Application Baseline v1 and Deployment Environments v1 remain required for
the v6 web pairing.

## Initial compliance work

A migration assessment MUST record at least:

- Java/Node.js/Python runtime lines in use;
- database technologies and release lines;
- server-side Java framework choice where applicable;
- package/build tooling relevant to the baseline;
- first-party container base images;
- vendor-bound runtime/database exceptions;
- active ADR exceptions and expiry dates.

Baseline drift discovered during migration SHOULD be converted into implementation-sized tickets.
The 90-day migration window defined by Technology Baseline v1 applies to newly applicable upstream
target lines; it does not require an unsafe big-bang migration solely because declaration v6 is
published.

## Jenkins activation

The operational implementation is owned by `siczb/maintenance`. A consumer MUST NOT be considered
fully migrated until its regular build exposes the Technology Baseline compliance result expected by
the current Jenkins contract.

## Notification privacy

Concrete personal notification recipients are operational configuration and MUST NOT be copied into
externalized declarations, public documentation, examples, or generated public-core artifacts.
Externalized material MUST use a neutral placeholder such as
`${TECHNOLOGY_BASELINE_NOTIFICATION_EMAIL}` when a recipient value needs to be illustrated.

## Rollback

If the v6 enforcement implementation is not operationally safe, revert the consumer declaration to
its previously released pinned contract and restore the previous enforcement path. Do not mutate an
already released schema or compatibility profile.
