# Changelog

All notable changes to the repository standards are recorded here.

## 9.3.2 - 2026-09-12

### Fixed

- release-facing entry points now derive their current compatibility boundary from compatibility
  profile v10 and identify declaration v11 as the latest supported portable pairing instead of
  presenting declaration v8/v3-era guidance as current;
- the canonical README, generated Public Core README, reference catalog, architecture guidance,
  branching guidance, Story Point reference, Contract-first reference, Design Source reference,
  Design System decision reference, and pre-write naming guidance now distinguish current portable
  pairings from immutable historical/version-specific semantics;
- declaration-v10 migration guidance is explicitly historical to its release boundary, is linked from
  internal and Public Core navigation, and is included in the deterministic Public Core manifest;
- the initial canary rollout and original Maintenance migration documents are explicitly marked as
  historical evidence rather than current adoption instructions; and
- release-guidance freshness regression tests derive the newest compatibility profile and highest
  supported declaration from machine-readable artifacts, include a controlled stale-pin negative,
  and protect the repository's deliberate declaration-v10 self-adoption from implicit migration.

### Compatibility

- v9.3.2 changes guidance, navigation, Public Core composition, and regression coverage only; no
  published normative standard, schema, compatibility pairing, or reference declaration is changed;
- the v11 Web pairing continues to select Web Application Baseline v3, Deployment Environments v1,
  and Repository Localization v1; the independently published Deployment Environments v2 contract is
  not substituted into that pairing;
- the frozen #58 Product/System Readiness Design Contract and #59 Test Contract remain byte-identical;
- Repository Standards itself remains explicitly pinned to declaration v10 until a separate reviewed
  self-adoption migration is qualified; and
- consumer adoption and Maintenance/Jenkins provider activation remain explicit, release-pinned, and
  fail-closed.

## 9.3.1 - 2026-09-12

### Fixed

- release-facing Product/System Readiness v1 guidance now consistently reflects that the declaration-v11 pairings are `supported` beginning with immutable Repository Standards release v9.3.0 rather than retaining pre-release `candidate` wording;
- Public Core navigation, AI-consumption guidance, readiness reference guidance, Ticket Specification v5 migration guidance, and the internal documentation index now expose the same explicit release-pinned adoption boundary;
- regression coverage prevents stale declaration-v11 candidate-state wording from reappearing on the released guidance surfaces.

### Compatibility

- v9.3.1 changes guidance and release evidence only; the Product/System Readiness v1, Ticket Specification v5, declaration-v11, and compatibility-v10 normative contracts are unchanged from v9.3.0;
- the frozen #58 Design Contract and #59 Test Contract remain byte-identical, and all earlier released standards and compatibility pairings remain immutable;
- consumer adoption remains explicit and release-pinned, and productive Maintenance/Jenkins readiness evaluation remains out of scope.

## 9.3.0 - 2026-09-12

### Added

- Product/System Readiness v1 with frozen Design Contract and Test Contract provenance, cumulative software TRL 1-9 qualification semantics, explicit repository-owned applicability and Subject targets, assessment/evidence schemas, complete traceability, and deterministic positive and controlled-negative fixtures;
- Ticket Specification v5 as the additive successor to v4, adding Product-/Release-Epic Product Stage, Subject binding, Increment Readiness Target, and exact assessment provenance while keeping current readiness evidence-derived;
- Repository Standards declaration schema v11, compatibility profile v10, Core/Web reference declarations, validators, generated Ticket v5 AI/templates, migration guidance, documentation, tests, and deterministic Public Core coverage for explicit Product/System Readiness v1 adoption.

### Changed

- compatibility profile v10 transitions only its two previously unreleased declaration-v11 pairings from `candidate` to `supported` after the #61 release/conformance qualification while preserving every v9 pairing unchanged;
- `target != candidate != assessed != established`, `deployment != operational proof`, `PROD != TRL 9`, and `Product Stage != TRL` remain mandatory semantic boundaries;
- an MVP may establish TRL 9 for its deliberately bounded scope only when cumulative qualification and successful real operational use are evidenced;
- Readiness Applicability remains an explicit governance decision, and Candidate, Assessed, Established, Preservation, and Requalification remain derived rather than authored states; repository-wide TRL aggregation remains forbidden.

### Compatibility

- Repository Standards v9.2.0 and all earlier released standards, schemas, profiles, references, compatibility pairings, and consumer pins remain immutable and supported;
- declaration v11, Ticket Specification v5, and Product/System Readiness v1 are additive and opt-in; publication does not migrate any consumer automatically;
- consumers may adopt declaration v11 only by pinning an immutable release that contains the supported v11 pairing and after compatible Ticket Specification v5 / Product/System Readiness v1 writers and validators are qualified; productive Maintenance/Jenkins readiness assessment and gate activation remain out of scope;
- TRL 9 is not a Security-, Risk-, Exposure-, Data-, or Criticality-classification and cannot satisfy those independent governance gates;
- Capability Promotion v1 from #47 / PR #51 is not part of v9.3.0 and remains excluded from this release.

## 9.2.0 - 2026-09-09

### Added

- Design Source Declaration v1 with the independently versioned `.repository-design-source.yml` sidecar for stable repository-owned design-source identity, Penpot team/project UUIDs, and optional automation metadata;
- Web Application Baseline v3 with canonical `/<ISO-639-1>/<stable-route-id>` user-facing content routing;
- Repository Localization v1 with repository-owned supported/default language metadata in `.repository-localization.yml` and fail-closed ISO-639-1 validation;
- Repository Standards declaration schema v10, compatibility profile v9, Core/Web single/integration references, validators, migration/AI guidance, tests, and Public Core assets required for explicit WAB v3 adoption.

### Changed

- WAB v3 keeps `impressum`, `datenschutz`, and `barrierefreiheit` as stable route IDs across languages; localized aliases are non-canonical;
- `/` under WAB v3 redirects to a supported language with deterministic fallback to the declared default language;
- unsupported language namespaces fail closed, while technical APIs, health endpoints, callbacks, and static assets are not blanket-prefixed by the user-facing content routing rule;
- publicly indexable language variants use language-specific canonical URLs and consistent `hreflang` relationships.

### Compatibility

- Repository Standards v9.1.0, Web Application Baseline v1/v2, declaration schemas v1-v9, and all existing consumer pins remain immutable and supported;
- Design Source Declaration v1 and WAB v3 / Declaration v10 are additive and opt-in; publication does not migrate any consumer automatically;
- Capability Promotion v1 from #47 / PR #51 is not part of v9.2.0 and remains blocked on real cross-consumer qualification in `siczb/maintenance#616`.

## 9.1.0 - 2026-08-29

### Added

- Deployment Environments v2 with canonical `DEV`, optional `STAGING`, and `PROD`, while rejecting `STAGE` in the v2 machine-readable contract;
- Repository Environments v1 as the independently versioned repository-owned `.repository-environments.yml` sidecar for explicit human-web environment URLs;
- machine-readable profiles, schema, reference declaration, compatibility metadata, migration and AI guidance, validator tooling, regression tests, and Public Core distribution assets for the new contracts.

### Changed

- environment URLs are explicit repository-owned metadata and are never inferred from repository names, hostname conventions, or a centrally maintained project-to-URL mapping;
- declared environment URLs must be non-empty absolute HTTP(S) URLs; userinfo/credentials, fragments, unknown environment keys, missing URLs, and invalid URLs fail closed;
- `STAG` may be used only as a presentation abbreviation and is not a machine-readable environment key.

### Compatibility

- Deployment Environments v1 remains immutable and supported for pinned consumers, including its canonical `STAGE` name;
- Deployment Environments v2 and Repository Environments v1 are additive and opt-in; publication does not migrate `.repository-standards.yml`, deployment automation, or consumer repositories automatically;
- Repository Standards v9.0.0 and all earlier release identities remain immutable;
- downstream consumers may pin these new contracts only from a release that contains them.

## 9.0.0 - 2026-08-28

### Added

- Contract-first Delivery v1 with revision-bound Design Contract, Test Contract, Implementation and
  Conformance Evidence roles and an explicit Contract Set freeze at `Status/Ready`;
- Ticket Specification v4 with mandatory machine-readable `delivery` metadata and fail-closed
  Contract-first applicability semantics;
- Development Workflow v8 with Design → Test → Implementation → Evidence ordering, downstream
  invalidation/requalification rules, and logical conformance gates;
- Web Application Baseline v2 with distinct functional, accessibility, reflow/responsive,
  live-runtime and visual conformance evidence classes;
- Contract-first Evidence schema v1 binding evidence to exact contract and
  implementation/deployed-artifact revisions while prohibiting contract mutation during evidence
  collection;
- Repository Standards declaration schema v9, compatibility profile v8, canonical v9 Core/Web
  reference declarations, migration guidance, generated AI adapters, validators, regression tests,
  and Public Core coverage.

### Changed

- required implementation work freezes resolved Design and Test Contract identities before entering
  `Status/Ready`; unresolved future revisions or digests may not be invented;
- a changed Design Contract invalidates dependent Test Contract qualification, implementation
  qualification, and evidence; a changed Test Contract invalidates implementation qualification and
  evidence; an implementation revision change invalidates prior evidence;
- failed Conformance Evidence must be repaired by changing the implementation or by explicit
  upstream contract evolution followed by downstream requalification, never by weakening
  assertions, baselines, or tolerances inside the evidence step;
- web UI design-source provenance remains normative while baseline screenshots are treated as
  derived test artifacts rather than an independent design authority;
- DEV is not required for Design/Test Contract authoring; runtime-bound evidence requires an actual
  deployed runtime and should have a reliably deployable DEV path before implementation begins.

### Compatibility

- Repository Standards v8.0.0 and all earlier released standard, schema, profile, reference, and
  migration assets remain immutable and supported for pinned consumers;
- v9 is an explicit opt-in contract set; publication does not migrate any consumer automatically;
- v9 consumer activation remains fail-closed until compatible downstream ticket, lifecycle, and CI
  automation is qualified and explicitly advertises the released v9 contract set;
- unsupported mixed v8/v9 pairings are rejected rather than guessed or silently coerced;
- Jenkins and Maintenance remain implementation layers and are not required to interpret the
  portable normative contracts themselves.

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
