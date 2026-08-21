# Separate Standards Ownership from CI Implementation

- Status: accepted
- Date: 2026-07-13

## Context

Repository Documentation Standard v1 was originally specified and implemented inside `siczb/maintenance`. The same repository therefore owned normative policy, templates, validation resources, and Jenkins implementation.

## Decision drivers

- standards must be discoverable independently from Jenkins implementation;
- reference repositories and boilerplate need a natural home;
- existing CI consumers must continue working during migration;
- project-specific documentation must remain beside project code.

## Considered options

- keep all assets in Maintenance;
- move standards and Jenkins implementation together;
- create a standards repository while retaining CI implementation in Maintenance.

## Decision

Create `siczb/repository-standards` as the canonical source for normative standards, schemas, profiles, references, and boilerplate generation. Keep Jenkins Shared Library code and operational automation in `siczb/maintenance`.

Maintenance may retain compatibility copies while consumers migrate. Normative changes originate in this repository.

## Rationale

The split gives policies a stable, implementation-neutral home without coupling every standards change to Jenkins internals or breaking current consumers.

## Consequences

Cross-repository compatibility tests are required. Releases of the standards repository must state which Maintenance validator versions support them.

## Risks

Mirrored resources can drift during migration. The migration process therefore requires explicit versioning and tests before compatibility copies are removed.

## References

- `siczb/maintenance#37`
- `siczb/repository-standards#1`
