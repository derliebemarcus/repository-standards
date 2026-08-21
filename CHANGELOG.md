# Changelog

All notable changes to the repository standards are recorded here.

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
