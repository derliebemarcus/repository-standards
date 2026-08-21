# Compatibility and Versioning

## Standard version

`standard_version` identifies a semantic contract. Consumers continue to receive their pinned version behavior until they explicitly migrate.

Published versions are immutable. New mandatory fields or incompatible semantics require a new major standard version rather than modifying an existing released version in place.

Ticket Specification v1 remains supported for pinned consumers. Ticket Specification v2 adds the canonical completed lifecycle representation. Ticket Specification v3 preserves the v2 lifecycle contract and adds canonical Story Point estimation anchors.

Development Workflow v1 remains available for pinned legacy consumers. Development Workflow v2 provides explicit branching and release promotion for Ticket Specification v1. Development Workflow v3 preserves those branching semantics while adopting Ticket Specification v2 lifecycle semantics. Development Workflow v4 preserves v3 lifecycle and branching semantics while adding machine-readable branch/pull-request naming and fail-closed pre-write validation. Development Workflow v5 preserves v4 behavior and changes only the released coupling required for Ticket Specification v3 and declaration schema v5.

Web Application Baseline v1 and Deployment Environments v1 remain independently versioned, opt-in contracts and must be adopted together where the declaration schema supports the web/deployment variant.

## Ruleset version

`ruleset_version` uses semantic versioning within a standard version:

- patch: corrections and clarifications that do not add obligations;
- minor: backward-compatible capabilities, optional fields, and opt-in checks;
- major: represented by a new standard version when obligations or semantics change incompatibly.

Existing consumers remain on their pinned ruleset until explicit migration.

## Supported repository contract sets

Repository declarations are versioned compatibility contracts. Published compatibility profiles remain immutable. The current canonical matrix is `profiles/repository-standards-compatibility-v4.json`, which supersedes v3 additively.

| Declaration schema | Ticket Specification | Development Workflow | Repository Documentation | Web Application Baseline | Deployment Environments | Status |
| --- | --- | --- | --- | --- | --- | --- |
| v1 | v1 | v2 | v1 | — | — | Supported |
| v2 | v2 | v3 | v1 | — | — | Supported |
| v3 | v2 | v3 | v1 | v1 | v1 | Supported |
| v4 | v2 | v4 | v1 | — | — | Supported |
| v4 | v2 | v4 | v1 | v1 | v1 | Supported |
| v5 | v3 | v5 | v1 | — | — | Supported |
| v5 | v3 | v5 | v1 | v1 | v1 | Supported |

No other pairing is supported. Unsupported combinations MUST fail validation rather than being guessed, coerced, or silently upgraded.

Released reference declarations are:

- declaration v1: `reference/repository-standards.single.yml`, `reference/repository-standards.integration.yml`;
- declaration v2: `reference/repository-standards-v2.single.yml`, `reference/repository-standards-v2.integration.yml`;
- declaration v3 web/deployment: `reference/repository-standards-v3.single.yml`, `reference/repository-standards-v3.integration.yml`;
- declaration v4 core: `reference/repository-standards-v4.single.yml`, `reference/repository-standards-v4.integration.yml`;
- declaration v4 web/deployment: `reference/repository-standards-v4.web.single.yml`, `reference/repository-standards-v4.web.integration.yml`;
- declaration v5 core: `reference/repository-standards-v5.single.yml`, `reference/repository-standards-v5.integration.yml`;
- declaration v5 web/deployment: `reference/repository-standards-v5.web.single.yml`, `reference/repository-standards-v5.web.integration.yml`.

Changing declaration schema or any selected standard version is an explicit repository migration and MUST NOT occur merely because a newer standard is published.

## Ticket Specification compatibility

### Ticket Specification v1

Ticket Specification v1 introduced mandatory metadata, description sections, readiness decisions, and relative Story Point semantics. Its staged migration rules remain valid for repositories pinned to declaration schema v1 and Development Workflow v2.

Its Story Point values are `1, 2, 3, 5, 8, 13`; they represent relative effort, complexity, risk, and uncertainty and are not time estimates.

### Ticket Specification v2

Ticket Specification v2 changes lifecycle write semantics. Its canonical completed representation is Forgejo `state=closed` plus exactly `Status/Done`. An open issue must not carry `Status/Done`.

A v2 reader may interpret a legacy closed issue as completed for read/display and migration analysis when canonical lifecycle metadata is absent, but new v2 writes must normalize to the canonical representation. Reopening is a coordinated transition to `state=open` and one explicit active non-Done status. Completion and reopen writers establish the replacement status before removing the previous valid status.

Development Workflow v3/declaration v2 provide the first standards-side v2 adoption contract. Declaration v3 reuses that lifecycle pairing, and declaration v4 pairs Ticket Specification v2 with Development Workflow v4.

### Ticket Specification v3

Ticket Specification v3 preserves the complete v2 lifecycle contract and adds canonical semantic anchors for the unchanged Story Point values.

The estimation dimensions are:

- effort;
- complexity;
- risk; and
- uncertainty.

Estimation is holistic. Story Points MUST NOT be converted to hours, person-days, calendar duration, staffing, file counts, task counts, lines of code, or another single mechanical proxy.

The canonical anchors are summarized in `docs/reference/story-point-estimation.md`; the normative source is `standards/ticket-specification/v3/standard.md` and the machine-readable source is `profiles/ticket-specification-v3.json`.

`Estimate/13` is exceptional and requires documented justification plus explicit consideration of splitting. Historical v1/v2 estimates MUST NOT be rewritten solely because a repository adopts v3.

Ticket Specification v3 is paired only with Development Workflow v5 under declaration schema v5.

## Development Workflow compatibility

Development Workflow v2 is paired only with Ticket Specification v1 under declaration schema v1. Development Workflow v3 is paired with Ticket Specification v2 under declaration schemas v2 and v3. Development Workflow v4 is paired with Ticket Specification v2 under declaration schema v4. Development Workflow v5 is paired with Ticket Specification v3 under declaration schema v5.

Development Workflow v3 incorporates the unchanged branching, protection, pull-request, release, Hotfix, and manual-main-build requirements of v2 and changes the lifecycle coupling. Development Workflow v4 incorporates v3 semantics and adds the released branch/pull-request naming and pre-write validation contract. Its kind-to-prefix source is Ticket Specification v2.

Development Workflow v5 incorporates v4 behavior unchanged except for version coupling. Its canonical kind-to-prefix source is `profiles/ticket-specification-v3.json#/branch_prefixes`, and ticket estimation delegates to Ticket Specification v3. It MUST NOT maintain a second branch-prefix or estimation table.

For v4 and v5, branch and ticket-linked pull-request writers resolve the repository's pinned released contract and validate the complete planned mutation before the Forgejo write. Undeclared aliases such as `fix/` are rejected; regular `Kind/Bug` work uses `bugfix/`; `hotfix/` is reserved for the explicit Hotfix path. Ticket-linked pull-request titles use `#<ticket-number> <summary>` and the title ticket number must match the head-branch ticket number.

Automated dependency pull requests without a project ticket may retain the contract-defined explicit exemption. There is no generic legacy creation-time cutoff exemption.

## Declaration schema compatibility

### Declaration schema v3

Declaration schema v3 is the explicit web/deployment contract set using Ticket Specification v2, Development Workflow v3, Repository Documentation v1, Web Application Baseline v1, and Deployment Environments v1. Existing v1/v2 declarations remain valid and MUST NOT be upgraded implicitly.

See `../repository-contract-v3-migration.md`.

### Declaration schema v4

Declaration schema v4 is the Development Workflow v4 adoption boundary. It supports either the v2/v4 core set or that set with both existing web/deployment v1 contracts. Partial web/deployment adoption is unsupported.

The `single` and `integration` branching declarations and normal `^(main|develop|PR-[0-9]+)$` Multibranch filter are unchanged.

See `../repository-contract-v4-migration.md`.

### Declaration schema v5

Declaration schema v5 is the Ticket Specification v3 / Development Workflow v5 adoption boundary. It supports either:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
```

or the same core set plus both existing web/deployment contracts:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

The branching models and Multibranch filter remain unchanged. A repository MUST NOT migrate to v5 until every ticket writer can apply Ticket Specification v3 estimation semantics and every branch/pull-request writer can apply the unchanged v4-derived pre-write workflow contract.

See `../repository-contract-v5-migration.md` and `../ticket-standard-v3-migration.md`.

## Web Application Baseline compatibility

Web Application Baseline v1 defines the canonical static routes `/impressum`, `/datenschutz`, and `/barrierefreiheit`, shared application design/accessibility expectations, and artifact-state-dependent public provenance. It follows the repository's explicit Design System decision and does not itself force Design System adoption.

The standard uses Artifact Provenance v1 for immutable build/release identity. Final releases use semantic version `X.Y.Z`; release candidates use `X.Y.Z-rc.N` with optional SemVer build metadata.

## Deployment Environments compatibility

Deployment Environments v1 reuses the selected Development Workflow branching model: `single` maps default DEV source to `main`; `integration` maps it to `develop`.

Preview/PR is not a canonical environment, STAGE is optional, and PROD accepts only immutable final-release artifacts. Source, artifact release state, and runtime environment remain independent. Promotion and rollback select existing immutable artifacts rather than rebuilding application content.

## Maintenance compatibility

Maintenance embeds compatible validators and operational resources during migrations. A standards release must identify a compatible Maintenance revision before repositories pin that release in blocking CI where Maintenance enforcement is required.

For Ticket Specification v2/v3 consumers, Maintenance lifecycle writers must preserve canonical `Status/Done` completion, explicit reopen transitions, canonical organization-level status labels, and replacement-before-removal semantics.

For declaration v4/v5 consumers, Maintenance branch and ticket-linked pull-request writers must implement the matching released pre-write naming contract. For v5, ticket-estimation automation must additionally load Ticket Specification v3 anchors instead of maintaining a private estimation mapping.

Repositories MUST NOT migrate to a newer declaration until their active writing/enforcement automation has passed the applicable compatibility and Canary validation.

## Workboard compatibility

Workboard owns ticket migration and dependency reconciliation. Its parser and migration tooling must pass compatibility tests against the released Ticket Specification profile and canonical relation headings before organization-wide writes begin.

For Ticket Specification v2/v3, Workboard must preserve the completed-state invariant, reopen semantics, legacy read compatibility, and ambiguous closed-ticket handling. Ticket Specification v3 does not require historical re-estimation.

## Forgejo workflow compatibility

Forgejo is the canonical automation provider. Active workflows are discovered from `.forgejo/workflows/`; `.github/workflows/` is not a supported active source after migration.

GitHub-compatible workflow syntax may be retained only where Forgejo supports it. Required pull-request status checks, protected-branch rules, review gates, and manual-main-build requirements remain those of the selected Development Workflow.

For declaration v4/v5 repositories, branch/pull-request naming checks are defense in depth and MUST enforce semantics consistent with the corresponding released workflow and Ticket Specification profiles.

## Published-artifact immutability

Tests protect previously released standards, compatibility profiles, schemas, generated adapters, and reference declarations by Git blob SHA. New contract versions MUST be introduced as new files. Existing released files MUST NOT be edited to add fields, pairings, or semantics.

In particular, publishing Ticket Specification v3, Development Workflow v5, declaration schema v5, and compatibility profile v4 does not modify Ticket Specification v1/v2, Development Workflow v1-v4, declaration schemas v1-v4, or compatibility profiles v1-v3.

## Failure behavior

Validation fails rather than guessing when:

- declaration/standard pairings are unsupported;
- a required contract field is missing;
- a consumer attempts partial web/deployment adoption;
- a v4/v5 writer cannot resolve ticket kind or the canonical branch prefix;
- a proposed branch or ticket-linked pull request violates the released naming contract;
- a v3 estimator attempts to replace relative estimation with a mechanical time/size proxy;
- artifact release state is ambiguous;
- PROD could receive an unreleased artifact; or
- consumer automation is not compatible with the selected contract set.

Failure of a proposed migration does not invalidate the previously pinned declaration when that previous contract remains unchanged and conformant.

## Deprecation

A compatibility path may be deprecated only after known consumers have migrated and a replacement has passed Canary validation. Removal requires a documented migration window and a new release.