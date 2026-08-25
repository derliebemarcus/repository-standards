# Changelog

All notable changes to the repository standards are recorded here.

## 8.0.0 - 2026-08-25

### Added

- Technology Baseline v1 with normative lifecycle, supported-runtime, container-image, database,
  exception, review, and automated compliance requirements;
- Repository Standards declaration schema v6 and compatibility profile v5 for explicit Technology
  Baseline v1 adoption;
- Development Workflow v6 with provider-neutral logical required-gate identities and explicit
  Forgejo/Gitea and GitHub status/check adapters;
- Repository Standards declaration schema v7 and compatibility profile v6 for explicit Development
  Workflow v6 adoption;
- Development Workflow v7 as the immutable successor to v6, adding canonical pull-request
  supersession semantics while preserving v6 required-check, trust-boundary, branching, release,
  review, naming, and pre-write behavior;
- the exact leading supersession marker `# Superseded by / See other`, followed immediately by an
  unordered list containing at least one concrete successor pull-request reference;
- the PR metadata label `Status/Superseded`, required to remain coherent with the leading supersession
  block, plus a normative prohibition on merging superseded pull requests;
- Repository Documentation v2 with purpose-specific quality criteria for Tutorial, How-to Guide,
  Reference, Explanation, Architecture, Decision / ADR, Operations / Runbook,
  Verification / Evidence, and Index / Navigation;
- an explicit Verification / Evidence class for revision-, build-, release-, test-, audit-, and
  time-bounded proof that must remain distinguishable from durable current documentation;
- Repository Standards declaration schema v8 and compatibility profile v7 as the explicit adoption
  boundary for Development Workflow v7 and Repository Documentation v2 while preserving all v1-v7
  pairings;
- v2 migration guidance and non-normative Repository Documentation guidance covering document types,
  Diátaxis, arc42-lite, C4, and MADR with primary-source references;
- a version-specific Repository Documentation v2 consumer validator that reuses the established
  objective documentation-impact contract without turning editorial quality into heuristics;
- fail-closed required-check migration rules for Forgejo/Gitea event changes such as
  `pull_request` to `pull_request_target`;
- an explicit `pull_request_target` trust boundary prohibiting privileged execution of
  pull-request-controlled code;
- expanded deterministic Public Core coverage for Development Workflow v7, the v2 normative
  documentation contract, v8 declarations, compatibility, migration, explanatory guidance,
  validators, generated AI adapters, and regression tests; and
- regression tests protecting Development Workflow v6 and Repository Documentation v1 byte-for-byte
  and verifying v7 supersession semantics, v2 document semantics, v8 pairings, fail-closed
  compatibility, navigation, and Public Core coverage.

### Changed

- declaration v8 now selects Development Workflow v7 rather than v6, while declaration v7 remains
  pinned to Development Workflow v6;
- a superseded pull request is represented by both the canonical leading successor block and
  `Status/Superseded`; either representation without the other is invalid;
- superseded pull requests are not merge candidates and SHOULD be closed once at least one successor
  exists and the supersession relationship is recorded;
- documentation quality under Repository Documentation v2 is evaluated by the information task a
  document performs rather than by word count, line count, or another mechanical length proxy;
- historical Verification / Evidence may be retained, but it must not be presented as permanently
  current Reference, Architecture, or Operations documentation;
- Diátaxis and arc42 are documented as complementary rather than competing models: Diátaxis organizes
  reader information needs, arc42-lite structures architecture content, C4 supplies useful views,
  and MADR records significant decisions;
- required quality gates are now identified logically first and mapped to provider-specific concrete
  check/status identities by an adapter;
- Forgejo/Gitea status identity includes the triggering event in
  `<workflow> / <job> (<event>)`, so event changes require coordinated workflow and branch-protection
  migration;
- GitHub Required Status Check mappings remain job-based and MUST NOT invent a Forgejo/Gitea event
  suffix; and
- bounded provider-supported pattern matching may be used only when it cannot allow unrelated checks
  to satisfy the intended logical gate.

### Compatibility

- every previously published standard, schema, compatibility profile, and reference declaration
  remains supported and immutable for pinned consumers;
- Development Workflow v6 remains paired with declaration v7 and receives no retroactive v7
  supersession semantics;
- Repository Documentation v1 remains paired with declaration v1-v7 consumers and receives no
  retroactive v2 semantics;
- declaration v8 is paired with Development Workflow v7 and Repository Documentation v2 through
  compatibility profile v7; declaration v8 + Workflow v6, declaration v7 + Workflow v7,
  declaration v7 + Documentation v2, and declaration v8 + Documentation v1 are unsupported and fail
  closed;
- `Status/Superseded` is pull-request metadata and MUST NOT be interpreted as a Ticket Specification
  issue lifecycle status;
- v8 publication does not migrate any consumer repository automatically or require an existing
  `docs/` tree to be reorganized merely to match an illustrative layout;
- the current Maintenance `main` revision `efe19a3f2a1bc6bb8cd2ff95496ac4454e4e960c` supports the
  protected Public Core publication path, while its consumer release manifest does not yet advertise
  v8; consumer migration to declaration v6/v7/v8 therefore remains blocked until a compatible
  Maintenance revision explicitly registers v8;
- Jenkins remains an implementation and is not required to interpret, adopt, or locally validate the
  portable Repository Standards contracts; and
- the Public Core release-tag publisher is available from the Maintenance #549 publication contract;
  external publication remains dry-run-first and release tags remain immutable.

## 7.0.0 - 2026-08-24

### Added

- Ticket Specification v3 with canonical Story Point anchors for `1`, `2`, `3`, `5`, `8`, and `13`;
- holistic estimation across effort, complexity, risk, and uncertainty;
- explicit prohibition of converting Story Points mechanically to hours, person-days, calendar
  duration, staffing, file counts, task counts, lines of code, or another single proxy;
- exceptional `Estimate/13` semantics requiring documented justification and explicit split
  consideration;
- machine-readable Ticket Specification v3 profile/schema and generated AI authoring guidance;
- Development Workflow v5 and Repository Standards declaration schema v5 as the compatible explicit
  adoption boundary.

### Compatibility

- Ticket Specification v1/v2, Development Workflow v1-v4, declaration schemas v1-v4, and prior
  compatibility profiles remain immutable and supported for pinned consumers;
- adoption of Ticket Specification v3 is explicit through declaration v5 and Development Workflow v5;
- existing tickets are not re-estimated automatically and unsupported mixed pairings fail closed.

## 6.0.0 - 2026-08-21

### Added

- Development Workflow v4 with fail-closed validation before automated ticket-branch and
  ticket-linked pull-request writes;
- a machine-readable Development Workflow v4 profile and schema referencing Ticket Specification v2
  as the single canonical kind-to-prefix source;
- Repository Standards declaration schema v4 with core and web/deployment-compatible variants;
- compatibility profile v3 preserving all released v1-v3 pairings and adding the explicit v4 sets;
- generated Development Workflow v4 AI guidance plus migration and pre-write authoring guidance;
- contract regression coverage for `bugfix/`, invalid `fix/`, explicit Hotfix routing, PR-title ticket
  correspondence, declaration-v4 compatibility, generated assets, and published-v3 immutability.

### Changed

- Development Workflow v4 makes ticket-linked PR naming explicit as
  `#<ticket-number> <summary>` and requires the title ticket number to match the head branch;
- undeclared branch-prefix aliases are rejected; regular `Kind/Bug` work uses `bugfix/` while
  `hotfix/` remains reserved for the explicit Hotfix path;
- post-write Forgejo naming checks are defined as defense in depth and must implement semantics
  equivalent to the released v4 contract;
- v4 removes implementation-specific legacy creation-time cutoff exemptions while retaining the
  explicit dependency-update PR exemption inherited from the workflow contract.

### Compatibility

- declaration schemas v1-v3, Development Workflow v1-v3, and compatibility profiles v1-v2 remain
  supported and immutable for pinned consumers;
- declaration v4 uses Ticket Specification v2 and Development Workflow v4, with optional Web
  Application Baseline v1 and Deployment Environments v1 only as the existing paired extension;
- repositories must not migrate to declaration v4 until `siczb/maintenance#511` is merged and the
  minimum compatible Maintenance revision is documented;
- publishing this release does not migrate consumer declarations, rename existing branches, or
  weaken protected-branch, review, lifecycle, release, or deployment gates.

## 5.0.0 - 2026-08-20

### Added

- Web Application Baseline v1 with required `/impressum`, `/datenschutz`, and `/barrierefreiheit`
  routes, shared website design/accessibility requirements, and minimum accessibility-statement
  structure;
- artifact-state-dependent public provenance for non-release, release-candidate, and final-release
  web artifacts;
- Artifact Provenance schema v1 for immutable source/build/release identity;
- Deployment Environments v1 with independent source, artifact release state, and runtime environment
  dimensions;
- canonical DEV, optional STAGE, PROD, branch-to-DEV, immutable promotion, and rollback semantics;
- Repository Standards declaration schema v3 and single/integration reference declarations;
- compatibility profile v2 preserving v1/v2 pairings and adding the explicit v3 web/deployment set;
- declaration-v3 migration and web/deployment interaction guidance;
- regression tests protecting published v1/v2 compatibility and declaration artifacts by Git blob
  SHA.

### Changed

- repository validation now checks the web/deployment profiles, artifact-provenance schema,
  declaration schema v3, compatibility profile v2, required static routes, public provenance matrix,
  branch-to-DEV mapping, and immutable-PROD requirements;
- architecture and AI/consumer guidance distinguish source, artifact release state, and runtime
  environment and identify Maintenance as the downstream enforcement owner.

### Compatibility

- declaration schema v1 and v2 contract sets remain supported and immutable;
- declaration schema v3 reuses Ticket Specification v2 and Development Workflow v3 while adding Web
  Application Baseline v1 and Deployment Environments v1;
- v3 adoption is explicit and requires compatible artifact-provenance/deployment enforcement and
  Canary validation before blocking rollout;
- publishing this release does not migrate consumer declarations or deploy applications.

## 4.0.0 - 2026-08-16

### Added

- Development Workflow v3 as the Ticket Specification v2-compatible workflow contract;
- Repository Standards declaration schema v2;
- machine-readable supported-version pairings in
  `profiles/repository-standards-compatibility-v1.json`;
- declaration-v2 single and integration reference files;
- explicit repository contract v1-to-v2 migration guidance;
- contract tests protecting Development Workflow v2, declaration schema v1, and declaration-v1
  references byte-for-byte.

### Changed

- Development Workflow v3 normatively incorporates unchanged v2 branching, protection, release,
  Hotfix, review, and manual-main-build requirements while adopting Ticket Specification v2;
- repository and AI documentation now validate the complete declaration/standard pairing rather
  than inferring compatibility from independently available versions;
- Repository Standards validation now covers workflow v3, declaration schema v2, and the
  compatibility matrix.

### Compatibility

- declaration schema v1 + Ticket Specification v1 + Development Workflow v2 remains supported and
  immutable;
- declaration schema v2 supports Ticket Specification v2 only with Development Workflow v3;
- unsupported version pairings are rejected;
- Workboard, Maintenance, and other lifecycle writers must support Ticket Specification v2 and pass
  Canary validation before a consumer repository migrates to declaration schema v2;
- no consumer declaration, organization label, or existing ticket is migrated by this release.

## 3.0.0 - 2026-08-16

### Added

- Ticket Specification v2 with the canonical completed pair `state=closed` plus `Status/Done`;
- explicit reopen semantics using one active non-Done status and `state=open`;
- machine-readable v2 lifecycle profile and JSON Schema contract;
- generated Ticket Specification v2 AI authoring adapter;
- staged v1-to-v2 lifecycle migration and legacy-read compatibility guidance;
- contract tests for canonical completion, invalid open Done, reopen behavior, legacy compatibility,
  generated assets, and Ticket Specification v1 immutability.

### Changed

- lifecycle writers adopting v2 must use replacement-before-removal transitions;
- v2 consumers may read legacy closed tickets compatibly but may emit only canonical v2 writes;
- Workboard, Maintenance, and other lifecycle writers require an explicit consumer migration before
  adopting v2 write semantics.

### Compatibility

- Ticket Specification v1 remains immutable and supported for pinned consumers;
- `Status/Abandoned` remains distinct from completed work;
- no organization labels or existing tickets are mutated by this release.

## 2.1.0 - 2026-08-16

### Added

- Repository Documentation Ruleset 1.2.0;
- explicit Design System architecture decision for repositories with a relevant UI;
- canonical `.design-system-consumer.json` contract and schema;
- `use` and `do-not-use` decision semantics with `active`, `planned`, and `blocked` adoption states.

### Compatibility

- existing Repository Documentation ruleset consumers remain pinned until explicit migration;
- Design System use is not mandatory; the architecture decision is mandatory for relevant UI
  repositories adopting Ruleset 1.2.0.

## 2.0.0 - 2026-07-30

### Added

- Ticket Specification v1 using BCP 14;
- machine-readable ticket and repository-declaration schemas;
- generated Epic, Story, Bug, Security, Documentation, and Testing templates;
- generated AI ticket-authoring adapter and prompt-consumption guidance;
- staged migration rules for open and closed tickets;
- Development Workflow v2 with explicit single and integration branching models;
- mandatory Multibranch Pipeline filter `^(main|develop|PR-[0-9]+)$`;
- manual `develop` to `main` release promotion and Hotfix reintegration;
- contract tests for generated assets, dependency headings, estimation, and branching.

## 1.1.1 - 2026-07-13

### Added

- executable consumer-side repository documentation impact validator;
- pull-request impact decision enforcement;
- compatibility parsing for existing Maintenance declarations;
- Canary contract tests.

## 1.1.0 - 2026-07-13

### Added

- canonical home for technical repository standards and development workflows;
- explicit documentation maintenance and impact-declaration rules;
- machine-readable profiles and schema;
- application, library, and infrastructure reference implementations;
- boilerplate generation and executable validation contracts.
