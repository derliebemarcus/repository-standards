# Repository Documentation Standard v2

## Status and scope

This is the canonical version 2 specification for repository documentation. The key words MUST,
MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and
OPTIONAL in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174) when,
and only when, they appear in all capitals.

A repository declares conformance in `.repository-documentation.yml` and selects one of the profiles
`application`, `library`, or `infrastructure`.

Repository Documentation v2 preserves the v1 documentation-maintenance, architecture, ADR,
validation, bootstrap, and Design System decision concepts while adding a normative document-type
model and purpose-specific quality criteria. Published Repository Documentation v1 artifacts remain
immutable and are not changed by this specification.

Explanatory guidance is available under `docs/repository-documentation/`. That guidance is
non-normative. If explanatory guidance conflicts with this specification, this versioned standard is
authoritative.

## Required declaration

```yaml
documentation:
  standard: repository-documentation
  standard_version: 2
  ruleset_version: 2.0.0
  profile: application
  architecture: arc42-lite
  diagrams: c4
  decisions: madr
  publishing: none
```

Ruleset versions are scoped to this standard version. Validators MUST NOT apply v2 obligations to a
repository that still declares Repository Documentation v1.

## Information architecture

Documentation quality MUST be evaluated against the information task the document is intended to
perform. Conformance MUST NOT depend on a minimum word count, minimum line count, or another
mechanical length metric.

A repository documentation set MUST make the following document types distinguishable where those
information tasks exist:

- Tutorial;
- How-to Guide;
- Reference;
- Explanation;
- Architecture;
- Decision / ADR;
- Operations / Runbook;
- Verification / Evidence; and
- Index / Navigation.

These types describe information tasks, not mandatory directory names. A repository MAY use another
directory structure when the selected profile, declarations, navigation, and document purpose remain
clear. A document MAY contain more than one type when the boundaries between the information tasks
are explicit and the combined document remains usable for each task.

Troubleshooting, migration, upgrade, release, and security documentation do not require additional
normative document types. They MUST use the type that matches their information task: for example, a
migration procedure is normally a How-to Guide or Operations / Runbook, while a compatibility table
is Reference and a migration rationale is Explanation.

The repository README remains a concise landing page and MUST link to the detailed documentation.

## Document-type quality criteria

### Tutorial

A Tutorial exists to enable learning through guided execution.

A conformant Tutorial MUST:

- state or make unambiguous the learning objective;
- identify meaningful prerequisites;
- present an ordered path that a learner can follow;
- lead to a working, observable target state; and
- avoid unnecessary reference completeness or digressions that obstruct the learning sequence.

A Tutorial SHOULD favor a dependable learning experience over exhaustive coverage. It MAY link to
Reference or Explanation for detail that is not required to complete the learning path.

### How-to Guide

A How-to Guide exists to help a competent reader accomplish a concrete task.

A conformant How-to Guide MUST:

- identify the intended goal;
- state relevant prerequisites and preconditions;
- provide executable or otherwise actionable steps;
- identify the expected result; and
- provide the verification necessary to establish that the task succeeded.

A How-to Guide SHOULD remain task-oriented. It MAY link to Reference for exhaustive facts and to
Explanation for rationale.

### Reference

Reference exists to support precise lookup of durable facts about the current described contract or
system state.

A conformant Reference document MUST:

- define its scope;
- be precise within that scope;
- be complete enough within that scope to support reliable lookup;
- minimize narrative material that distracts from lookup; and
- have a stable authority boundary so readers can determine what is and is not defined there.

Reference MUST distinguish current authoritative facts from historical observations or evidence.
Reference MUST NOT present a point-in-time verification result as if that result were a permanently
current property of the system.

### Explanation

Explanation exists to build understanding and connect concepts.

A conformant Explanation document MUST address the context and relationships necessary to understand
its subject. Where relevant, it SHOULD cover motivation, boundaries, trade-offs, alternatives, and
consequences.

Explanation MAY be discursive and MAY express a reasoned perspective. It MUST NOT be presented as a
normative standard unless it is itself a versioned normative artifact under `standards/`.

### Architecture

Architecture documentation exists to describe durable system architecture and the constraints and
relationships needed to understand and evolve it.

Architecture documentation MUST cover, to the extent relevant to the system:

- context and system boundaries;
- architectural constraints;
- building blocks and responsibilities;
- runtime relationships and significant scenarios;
- deployment topology and deployment relationships;
- cross-cutting concepts;
- quality requirements;
- known risks and technical debt;
- terminology; and
- links to relevant ADRs.

Repository Standards uses `arc42-lite` as a pragmatic organization of these architecture concerns.
`arc42-lite` does not require every repository to reproduce every chapter of the full arc42 template.
The architecture documentation MUST nevertheless satisfy the information tasks above when they are
relevant.

Repository Standards uses C4 as a view and diagram model within architecture documentation. A System
Context view SHOULD be provided when external people or systems are material to understanding the
boundary. A Container view SHOULD be provided when multiple deployable or runtime units are material.
Component and Code views MAY be provided when they improve understanding. Repositories MUST NOT
create C4 levels that add no useful architectural information merely to satisfy a perceived diagram
count.

### Decision / ADR

A Decision / ADR exists to preserve the rationale and consequences of an architecturally significant
decision.

A conformant ADR MUST contain or make unambiguous:

- Status;
- Context / Problem;
- Decision; and
- Consequences.

Where a decision is replaced, supersession MUST be traceable from the old and/or new ADR so a reader
can follow the decision history without rewriting historical rationale.

Accepted ADR contents SHOULD remain immutable. A changed decision SHOULD be recorded in a new ADR.
Status and supersession metadata MAY be updated on an accepted ADR when needed to preserve the
current decision graph.

Repository Standards uses MADR-compatible Markdown conventions for ADRs under `docs/decisions/` by
default. Another location MAY be used when profile/declaration rules and navigation identify it
unambiguously.

### Operations / Runbook

An Operations / Runbook document exists to execute operational work safely and repeatably.

A conformant Operations / Runbook document MUST include, to the extent relevant:

- the operational goal;
- prerequisites and required access or state;
- safe execution conditions;
- concrete steps;
- verification of the resulting state;
- failure handling;
- stop conditions; and
- rollback or recovery.

A runbook MUST make safety-relevant stop conditions explicit where continuing could worsen an
incident, damage data, invalidate evidence, or cross an authorization boundary.

### Verification / Evidence

Verification / Evidence exists to record a demonstrable result for a particular point in time,
revision, version, pull request, build, test, audit, release, or other examination. It is an evidence
class, not ordinary Reference documentation.

A conformant Verification / Evidence document MUST identify, to the extent applicable:

- the scope or subject being verified;
- the relevant revision, version, pull request, build, release, or equivalent identity;
- the verification time or evidence time;
- the verification method or procedure;
- the result;
- the provenance or origin of the evidence;
- relevant artifacts or reproducible steps when available; and
- limitations, validity boundaries, or known gaps.

Verification Evidence MUST NOT be represented as permanently current system documentation.
Historical evidence MAY be retained indefinitely. A very short Evidence document MAY be complete
when its entire purpose is to provide one clearly identified and traceable proof.

Verification content MUST be distinguishable from durable Reference, Architecture, and Operations
documentation. When evidence demonstrates a current-state claim documented elsewhere, the durable
documentation SHOULD link to the relevant evidence without becoming dependent on that evidence as
its only description of the system.

### Index / Navigation

An Index / Navigation document exists to provide orientation and entry points.

A conformant Index MUST:

- make relevant entry points discoverable;
- avoid creating competing detail documentation; and
- make the authority structure understandable where normative, explanatory, operational, current,
  or historical sources coexist.

An Index MAY intentionally be very short. It is conformant when it performs its navigation task.
An Index MUST NOT be judged incomplete merely because it has little prose.

## Required distinctions

### Tutorial vs. How-to Guide

A Tutorial serves learning and guided skill acquisition. A How-to Guide serves a reader who is doing
work and needs to complete a task. Ordered steps alone do not determine the type; the reader's
information task does.

### How-to Guide vs. Operations / Runbook

Both may provide executable steps. A How-to Guide optimizes for completing a task. An Operations /
Runbook additionally carries operational safety, stop, failure-handling, and rollback/recovery
obligations where relevant. Procedures whose failure can materially affect a running environment,
data, availability, security, or recovery SHOULD be treated as Operations / Runbook content.

### Reference vs. Verification

Reference describes durable facts within a current authority boundary. Verification records evidence
that a claim or state was checked under identified conditions at an identified time or revision.
Verification MAY support Reference, but it MUST NOT impersonate current Reference.

### Explanation vs. normative Standard

Explanation helps a reader understand why or how concepts relate. A normative Standard defines
binding requirements for a declared contract version. Explanatory documents under `docs/` MAY
summarize or illustrate a Standard but MUST NOT create, override, or extend normative requirements.

### Architecture vs. ADR

Architecture describes the durable system structure and relationships currently relevant to
understanding the system. ADRs preserve significant decisions and their rationale over time.
Architecture SHOULD link to the ADRs that explain significant choices; ADRs SHOULD NOT be used as a
substitute for a coherent current architecture description.

### Index vs. content page

An Index is complete when it provides adequate navigation and authority cues. A content page is
complete only when it fulfills the information task of its document type. Therefore short documents
are not automatically incomplete, but heading-only or bullet-fragment content is insufficient when
it does not perform the required information task.

### Current documentation vs. historical evidence

Current documentation describes the present contract, system, procedure, or architecture within its
authority boundary. Historical evidence records a verified observation for a bounded time or
revision. Historical evidence MAY remain available, but navigation and labeling MUST prevent it from
being mistaken for current documentation.

## Documentation methods and models

Repository Documentation v2 uses the methods and models below in complementary roles:

- Diátaxis organizes the primary documentation information tasks: Tutorial, How-to Guide, Reference,
  and Explanation.
- arc42-lite organizes architecture-specific content inside the broader documentation set.
- C4 provides architecture views and diagrams where they improve communication.
- MADR provides a consistent Markdown structure for architecture decision records.

Diátaxis and arc42 are not competing models. Diátaxis classifies documentation by reader information
need; arc42 structures architecture information. C4 complements architecture documentation with
views, and MADR complements it with traceable decisions.

An illustrative layout such as `docs/tutorials/`, `docs/how-to/`, `docs/explanation/`,
`docs/reference/`, `docs/architecture/`, `docs/decisions/`, `docs/operations/`, and
`docs/verification/` MAY be used. This example is not a mandatory directory contract unless a
selected machine-readable profile requires the corresponding path.

## Design System decision for UI repositories

A repository that owns a user-facing web or application UI MUST explicitly document its architecture
decision regarding `siczb/design-system`. The standard requires a decision; it does not require
Design System adoption.

The canonical machine-readable decision MUST be stored as `.design-system-consumer.json` and conform
to `schemas/design-system-consumer-v1.schema.json`. The referenced human-readable documentation MUST
exist in the repository documentation set.

Two decisions are conformant:

- `decision: use`: the repository has chosen the shared Design System. Technical adoption MUST be
  recorded separately as `active`, `planned`, or `blocked`.
- `decision: do-not-use`: the repository has consciously chosen not to consume the shared Design
  System. The contract rationale MUST explain that decision specifically.

For `decision: use`, `active` means the referenced package manifest MUST contain actual
`@siczb/design-tokens`, `@siczb/ui-css`, or `@siczb/ui-react` dependencies appropriate to the
integration; `planned` means persistent package adoption is not yet complete; and `blocked` means a
concrete technical prerequisite prevents adoption and MUST reference a tracking issue.

For `decision: do-not-use`, the referenced package manifest MUST NOT consume Design System packages.
Concrete Design System package versions MUST remain authoritative in the package manifest and
lockfile and MUST NOT be duplicated in `.design-system-consumer.json`.

Repositories without a relevant user-facing UI and the canonical `siczb/design-system` provider
repository are outside the consumer-declaration requirement.

## Documentation maintenance policy

Every functional, operational, security, architecture, compatibility, build, release, or deployment
change MUST be assessed for documentation impact.

Affected documentation MUST be updated in the same pull request as the change. Deferring known
documentation work to an unspecified future ticket is not conformant.

The assessment MUST cover the complete repository-owned documentation set. At minimum, the author
MUST consider:

- user-visible behavior and interfaces;
- configuration and environment variables;
- installation, upgrade, migration, and compatibility;
- architecture, runtime scenarios, and deployment topology;
- authentication, authorization, secrets, and data protection;
- monitoring, alerting, backup, restore, rollback, and disaster recovery;
- troubleshooting, known limitations, and technical debt; and
- release, versioning, and breaking-change behavior.

A pull request with no documentation changes MUST contain a specific explanation of why the change
has no documentation impact. A generic `not applicable` statement is insufficient.

## Machine-readable impact mappings

Repositories SHOULD declare source-to-documentation mappings for predictable impacts. A mapping
identifies source paths and the documents expected to change when those paths change. The mapping is
a minimum expectation, not proof that no other document is affected.

Machine-readable validation MUST be limited to robust, objective invariants. Validators MUST NOT
attempt to infer subjective editorial quality through word counts or comparable proxies.

## Architecture and ADRs

The architecture documentation MUST satisfy the Architecture quality criteria in this specification.
Durable architecture decisions MUST be recorded as ADRs. Accepted ADRs are immutable except for
status and supersession metadata; changed decisions require a new ADR.

## Validation contract

Validation MUST check declaration values, profile consistency, required files and headings,
unresolved placeholders, local links, README linkage, ADR conventions, required diagram syntax, and
publishing configuration where enabled.

Validation of Repository Documentation v2 MUST additionally verify objective contract invariants for
the v2 declaration and the presence/navigation of profile-required documents. Validation MAY verify
declared evidence roots or evidence files when a future v2 ruleset introduces an explicit
machine-readable field for them; v2.0.0 introduces no such field.

Validation MUST NOT use minimum word counts or another length proxy as evidence that a document
fulfills its information task.

Validation rules are tied to the declared standard and ruleset versions. A later ruleset or standard
version MUST NOT silently change the requirements of an earlier declared ruleset.

## Bootstrap and synchronization

Bootstrap and synchronization are additive. They create missing files but MUST NOT overwrite
repository-specific content without an explicit migration decision.

Boilerplate MUST be generated from or validated against the same profile and reference sources used
by this repository. A separately maintained template tree is prohibited because it would create a
second source of truth.
