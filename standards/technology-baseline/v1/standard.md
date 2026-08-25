# Technology Baseline v1

## Status and scope

This standard defines the canonical technology lifecycle, runtime, database, container-base, review,
and enforcement baseline for first-party `siczb` software.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

The standard defines normative outcomes and machine-readable policy. Concrete Jenkins jobs,
notification credentials, and operational implementation belong to `siczb/maintenance`.

## Baseline principles

A first-party repository that adopts this standard MUST use supported technology lines and MUST NOT
introduce end-of-life runtimes, databases, frameworks, or base images.

For technologies with an LTS model, the current final LTS release line MUST be the target baseline.
For technologies without an LTS model, the current supported final stable feature or major line MUST
be the target baseline. Preview, alpha, beta, milestone, and release-candidate versions MUST NOT be
used as the production baseline.

Within an adopted release line, the latest applicable security and patch release MUST be used unless
a documented exception applies.

## Initial baseline

The initial Technology Baseline v1 is:

| Capability | Baseline |
| --- | --- |
| Java | current LTS; initially OpenJDK 25 |
| Java build | Gradle Wrapper |
| Server-side Java | Spring Boot SHOULD be preferred when Java is chosen and no other stack fits the requirements more precisely |
| Node.js | current LTS; initially Node.js 24 |
| JavaScript package manager | npm |
| Python | current supported stable feature line; initially Python 3.14 |
| Frontend framework | governed by the adopted Design System decision; this standard MUST NOT duplicate that framework selection |
| Relational database | current stable PostgreSQL major; initially PostgreSQL 18 |
| Geospatial database extension | current stable compatible PostGIS line; initially PostGIS 3.6 |
| Embedded relational database | SQLite MAY be used when architecturally appropriate; current stable release applies |

A repository using server-side Java MAY select another framework where it better fits the
requirements, but the deviation from the preferred Spring Boot baseline MUST be justified by an ADR.

Python does not use an LTS model for this contract. Its current supported stable feature line is
therefore governed by the stable-line rule rather than by the LTS rule.

## Database rules

New first-party applications requiring a relational database MUST use the current baseline
PostgreSQL major unless an ADR-approved exception applies. Where geospatial capabilities are
required, the current baseline PostGIS line compatible with the mandated PostgreSQL major MUST be
used.

SQLite MAY be used where an embedded database is architecturally appropriate. If SQLite is supplied
by a language runtime instead of being independently packaged, CI MUST verify the SQLite version
actually used by that runtime.

Databases that are runtime dependencies of third-party/vendor software MUST follow the supported
upstream compatibility matrix. Such vendor-bound versions MUST NOT redefine the first-party database
baseline.

## Container Base Contract

There is no universal organization-wide base image. A first-party image MUST use an approved base
image family appropriate to its runtime or software.

The initial approved families are:

| Workload | Approved family |
| --- | --- |
| Python application | official `python:<baseline>-slim` family |
| Node.js application/build | official `node:<baseline>-bookworm-slim` family |
| Java build/runtime | Eclipse Temurin JDK/JRE matching the Java baseline |
| Static frontend/runtime | slim web-server runtime; Node.js MUST NOT remain solely for build-time needs |
| PostgreSQL | official PostgreSQL image matching the database baseline |
| PostgreSQL with PostGIS | official PostGIS image matching the PostgreSQL/PostGIS baseline |
| Fully static binary | `scratch` MAY be used where technically appropriate |
| Third-party software | upstream/vendor-supported image |

Debian/glibc-based slim families SHOULD be preferred as the general Linux base. Alpine MAY be used
when the concrete software stack deliberately supports and tests musl-based operation.

`latest` tags MUST NOT be used. Release artifacts MUST be reproducibly traceable to a concrete base
image version. Immutable digest pinning SHOULD be used for production/release image resolution.

Built applications SHOULD use multi-stage builds. Runtime images MUST NOT contain build tools or
other packages that are unnecessary at runtime. Containers SHOULD run as a non-root user wherever
the workload and upstream image support it.

Base images MUST be checked automatically for baseline drift, security support, and end-of-life.
Use of a non-approved first-party base-image family MUST be justified by an ADR.

## Lifecycle detection and migration window

Technology lifecycle and baseline compliance MUST be checked automatically at least weekly.
Detection MUST cover at least:

- new final LTS releases for LTS-governed technologies;
- new final stable feature/major releases for stable-line technologies;
- announced and reached end-of-life dates;
- patch/security drift within mandated lines;
- approved container-base families and their support state;
- consumer repositories that no longer conform to the active baseline.

A new final LTS or relevant stable major/feature release MUST trigger an out-of-cycle baseline
review. An announced EOL that can affect an adopted technology MUST also trigger an out-of-cycle
review.

For a newly applicable LTS or stable target line, consumers MUST migrate within 90 calendar days of
the final upstream release unless a documented exception exists. Security fixes are not governed by
that 90-day window; they MUST follow the applicable security-priority and vulnerability-remediation
policy.

## Findings and enforcement

The automated check MUST emit a finding when the normative baseline, upstream lifecycle state, or a
consumer no longer conforms. A finding MUST contain at least:

- technology or image family;
- normative baseline;
- detected upstream version or lifecycle state;
- affected consumers when known;
- relevant release or EOL date when known;
- detection date;
- migration deadline when applicable;
- severity/status;
- required action.

A newly detected finding and a material finding-state change MUST notify the responsible owner.
Unresolved findings MUST be re-notified at least weekly. A successful run with no findings SHOULD
NOT generate a routine notification.

Before the migration deadline, baseline drift MAY be represented as a warning/unstable state. After
an applicable migration deadline expires, the central compliance check MUST fail for unresolved
non-conformance, and affected consumer compliance gates MUST block non-conformant builds unless an
active exception applies.

## Governance review

The Technology Baseline MUST receive a governance review at least quarterly. The governance review
MUST evaluate technology choices that cannot be decided solely from version metadata, including
preferred frameworks, database strategy, approved base-image families, and active exceptions.

The due date of the governance review MUST itself be monitored automatically. An overdue governance
review MUST create a finding and notify the responsible owner.

## Exceptions

A deviation from a mandatory baseline requirement MUST be documented by an ADR. The exception MUST
record:

- rationale;
- accountable owner;
- tracking ticket;
- review or expiry date;
- affected technology and repositories;
- migration or retirement condition.

An expired exception MUST be treated as non-conformance.

## Notification and externalization

The concrete notification destination is deployment-specific operational configuration and MUST NOT
be part of the normative public contract.

Internal implementations MAY configure a concrete recipient. Any externalized or public-core
artifact that represents such configuration MUST replace personal notification addresses with a
neutral placeholder such as `${TECHNOLOGY_BASELINE_NOTIFICATION_EMAIL}`.

Public examples, schemas, profiles, migration guidance, and generated artifacts MUST NOT contain a
personal notification address.

## Consumer adoption

Adoption MUST be explicit through a released repository declaration schema that lists
`technology-baseline: v1`. Consumers remain pinned until an explicit migration is performed.

The concrete Jenkins Shared Library, scheduled job, notification transport, upstream-resolution
logic, and consumer enforcement implementation are owned by `siczb/maintenance`.
