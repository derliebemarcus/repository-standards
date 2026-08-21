# Compatibility and Versioning

## Standard version

`standard_version` identifies a semantic contract. Consumers continue to receive their pinned
version behavior until they explicitly migrate.

Published versions are immutable. New mandatory fields or incompatible semantics require a new
major standard version.

Ticket Specification v1 remains immutable and supported for pinned consumers. Ticket Specification
v2 adds the canonical completed lifecycle representation. Development Workflow v1 remains available
for pinned legacy consumers; Development Workflow v2 provides explicit branching and release
promotion for Ticket Specification v1; Development Workflow v3 preserves those branching semantics
while adopting Ticket Specification v2 lifecycle semantics. Development Workflow v4 preserves v3
lifecycle and branching semantics while adding a released machine-readable branch/pull-request
naming contract and fail-closed pre-write validation for branch and ticket-linked pull-request
writers.

Web Application Baseline v1 and Deployment Environments v1 are independently versioned, opt-in
contracts. Declaration schema v3 combines them with Ticket Specification v2, Development Workflow v3,
and Repository Documentation v1 without changing those previously published standards. Declaration
schema v4 can pair Development Workflow v4 with the core contract set or with the same unchanged
web/deployment contracts.

## Ruleset version

`ruleset_version` uses semantic versioning within a standard version:

- patch: corrections and clarifications that do not add obligations;
- minor: backward-compatible capabilities, optional fields, and opt-in checks;
- major: represented by a new standard version when obligations or semantics change incompatibly.

Repository Documentation Standard v1 Ruleset 1.2.0 adds the explicit Design System architecture
decision for relevant UI repositories. Existing consumers remain on their pinned ruleset until
explicit migration.

## Supported repository contract sets

Repository declarations are versioned compatibility contracts. The published compatibility v1 and
v2 profiles remain immutable. The current canonical matrix is
`profiles/repository-standards-compatibility-v3.json`, which supersedes v2 additively.

| Declaration schema | Ticket Specification | Development Workflow | Repository Documentation | Web Application Baseline | Deployment Environments | Status |
| --- | --- | --- | --- | --- | --- | --- |
| v1 | v1 | v2 | v1 | — | — | Supported |
| v2 | v2 | v3 | v1 | — | — | Supported |
| v3 | v2 | v3 | v1 | v1 | v1 | Supported |
| v4 | v2 | v4 | v1 | — | — | Supported |
| v4 | v2 | v4 | v1 | v1 | v1 | Supported |

No other pairing is currently supported. Unsupported combinations MUST fail validation rather than
being guessed, coerced, or silently upgraded.

Existing declaration-v1 consumers continue to use:

- `reference/repository-standards.single.yml`;
- `reference/repository-standards.integration.yml`.

Ticket Specification v2 consumers using declaration schema v2 use:

- `reference/repository-standards-v2.single.yml`;
- `reference/repository-standards-v2.integration.yml`.

Web/deployment consumers using declaration schema v3 use:

- `reference/repository-standards-v3.single.yml`;
- `reference/repository-standards-v3.integration.yml`.

Development Workflow v4 consumers using the core declaration-v4 set use:

- `reference/repository-standards-v4.single.yml`;
- `reference/repository-standards-v4.integration.yml`.

Development Workflow v4 consumers retaining the web/deployment opt-in use:

- `reference/repository-standards-v4.web.single.yml`;
- `reference/repository-standards-v4.web.integration.yml`.

Changing declaration schema, Ticket Specification, Development Workflow, Web Application Baseline,
or Deployment Environments version is an explicit repository migration and MUST NOT occur merely
because a new standard is published.

## Ticket Specification v1 compatibility

Ticket Specification v1 introduced mandatory metadata, description sections, readiness decisions,
and estimate semantics. Its staged migration rules remain valid for repositories that continue to
pin declaration schema v1 and Development Workflow v2.

During its compatibility phase:

- Workboard may recognize legacy direct-blocker headings;
- `### Blocked by` is canonical for new and migrated tickets;
- open tickets are migrated completely;
- closed tickets are migrated conservatively;
- missing historical evidence is not invented;
- enforcement progresses through audit, warning, write validation, and Ready gating.

## Ticket Specification v2 compatibility

Ticket Specification v2 changes lifecycle write semantics. Its canonical completed representation
is Forgejo `state=closed` plus exactly `Status/Done`. An open issue must not carry `Status/Done`.

A v2 reader may interpret a legacy closed issue as completed for read, display, and migration
analysis when canonical v2 lifecycle metadata is absent. This compatibility behavior is read-only:
new v2 writes must normalize to the canonical representation.

Reopening a v2 ticket is a coordinated transition to `state=open` and one explicit active non-Done
status. Completion and reopen writers must establish the replacement status before removing the
previous valid status.

Development Workflow v3 and declaration schema v2 provide the first standards-side adoption contract
for Ticket Specification v2. Declaration schema v3 reuses the same lifecycle pairing. Development
Workflow v4 and declaration schema v4 continue to use Ticket Specification v2 without changing its
lifecycle semantics.

This does not by itself make a consumer repository migration-safe. Workboard, Maintenance, and every
other lifecycle writer used by a repository MUST support the v2 completion/reopen invariants and pass
Canary validation before that repository adopts declaration-v2, declaration-v3, or declaration-v4
lifecycle semantics.

See `../ticket-standard-v2-migration.md` for lifecycle-data migration and ambiguity handling.

## Development Workflow compatibility

Development Workflow v2 is paired only with Ticket Specification v1 under declaration schema v1.
Development Workflow v3 is paired with Ticket Specification v2 under declaration schemas v2 and v3.
Development Workflow v4 is paired with Ticket Specification v2 under declaration schema v4.

Development Workflow v3 normatively incorporates the unchanged branching, protection, pull-request,
release, Hotfix, and manual-main-build requirements of v2 and supersedes only the Ticket
Specification coupling, declaration examples, and completion/reopen integration semantics.

Development Workflow v4 in turn incorporates unchanged v3 semantics and supersedes branch and
pull-request naming only where the v4 contract is more specific. The v4 profile references
`profiles/ticket-specification-v2.json#/branch_prefixes` as the single machine-readable kind-to-prefix
source. It does not maintain a second prefix table.

For v4, branch and ticket-linked pull-request writers MUST resolve the repository's pinned released
contract and validate the complete planned mutation before the Forgejo write. Undeclared aliases such
as `fix/` are rejected; the regular `Kind/Bug` prefix is `bugfix/`; `hotfix/` is reserved for the
explicit Hotfix path. Ticket-linked pull-request titles use `#<ticket-number> <summary>` and the title
ticket number must match the head-branch ticket number.

Automated dependency pull requests without a project ticket may retain the inherited explicit
exemption. Development Workflow v4 defines no legacy creation-time cutoff exemption.

This additive structure prevents published workflow text from being modified in place while avoiding
independently maintained copies of unchanged workflow or prefix rules.

## Declaration schema v3 compatibility

Declaration schema v3 is the explicit opt-in web/deployment contract set:

```yaml
version: 3
standards:
  ticket-specification: v2
  development-workflow: v3
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

A v3 consumer MUST satisfy all v2 lifecycle-writer prerequisites and additionally have compatible
artifact-provenance generation and deployment enforcement before blocking v3 enforcement is enabled.
Existing v1/v2 declarations remain valid and MUST NOT be upgraded implicitly.

See `../repository-contract-v3-migration.md`.

## Declaration schema v4 compatibility

Declaration schema v4 is the explicit Development Workflow v4 adoption boundary. It accepts either
the core v4 set:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
```

or the same set with both existing web/deployment contracts:

```yaml
version: 4
standards:
  ticket-specification: v2
  development-workflow: v4
  repository-documentation: v1
  web-application-baseline: v1
  deployment-environments: v1
```

Web Application Baseline v1 and Deployment Environments v1 remain a pair in the web variant; partial
web/deployment adoption is unsupported. The `single` and `integration` branching declarations and the
normal `^(main|develop|PR-[0-9]+)$` Multibranch filter are unchanged.

A repository MUST NOT migrate to declaration v4 until every automation that can create ticket
branches or ticket-linked pull requests supports Development Workflow v4 pre-write validation. A
post-write Forgejo naming check SHOULD be aligned during the same rollout.

## Web Application Baseline compatibility

Web Application Baseline v1 requires the canonical static routes:

- `/impressum`;
- `/datenschutz`;
- `/barrierefreiheit`.

The pages use the same application shell/design and accessibility gates as the owning website. The
standard follows the repository's explicit Design System decision and does not force Design System
adoption.

The standard uses `schemas/artifact-provenance-v1.schema.json` for immutable build/release identity.
Public footer rendering depends on artifact release state rather than runtime environment.

Artifact Provenance v1 uses semantic versioning for release identity. Final releases use `X.Y.Z` and
release candidates use the complete `X.Y.Z-rc.N` form, with optional SemVer build metadata.

## Deployment Environments compatibility

Deployment Environments v1 uses the existing Development Workflow branching decision:

| Branching model | Default DEV source |
| --- | --- |
| `single` | `main` |
| `integration` | `develop` |

The standard does not change build-trigger rules. It adds runtime deployment semantics: Preview/PR is
not a canonical environment, STAGE is optional, and PROD accepts only immutable final-release
artifacts.

Source, artifact release state, and environment remain independent. A `main` merge does not imply
PROD and an environment does not change release state. Promotion selects an existing immutable
artifact rather than rebuilding application content; rollback selects a previously released
immutable artifact.

## Artifact provenance compatibility

Artifact provenance v1 models:

- `releaseState`: `non-release`, `release-candidate`, or `release`;
- `commit`;
- `buildNumber`;
- `buildTime`;
- `releaseVersion` for release candidates and final releases.

A non-release artifact does not carry a release version. A release candidate carries the complete RC
identifier. A final release carries the final release version. Build provenance remains bound to the
artifact through deployment and rollback.

The public web footer exposes only the fields required by Web Application Baseline v1. A final
release may retain commit/build metadata internally for audit and rollback while rendering only the
release version publicly.

## Maintenance compatibility

Maintenance embeds compatible validators and operational resources during migration. A standards
release must document the minimum compatible Maintenance revision before repositories pin that
release in blocking CI.

Canonical-source outages must not turn established builds into infrastructure failures. Consumers
use a released pinned artifact or a tested embedded fallback rather than fetching an unversioned
branch during every build.

For declaration-v2 and declaration-v3 consumers, Maintenance MUST support canonical `Status/Done`
completion, explicit reopen transitions, organization-level canonical status labels, and fail-safe
replacement-before-removal writes before it may enable blocking lifecycle enforcement.

For declaration-v3 consumers, Maintenance additionally owns compatible immutable artifact-provenance
generation, source/artifact/environment separation, PROD final-release enforcement, promotion
without application-content rebuild, rollback to existing immutable release artifacts, and Canary
validation before blocking deployment enforcement.

For declaration-v4 consumers, Maintenance must additionally support Development Workflow v4 naming
resolution and fail-closed validation before branch and ticket-linked pull-request writes, and its
Forgejo naming enforcement must use equivalent released semantics.

The minimum compatible Maintenance revision for Development Workflow v4 is not yet released while
`siczb/maintenance#511` is blocked on this standards contract. Repositories MUST NOT migrate to
v4 until that implementation is merged, released where applicable, and its compatible revision is
identified.

## Workboard compatibility

Workboard owns ticket migration and dependency reconciliation. Its parser and migration tooling
must pass compatibility tests against the released Ticket Specification profile and canonical
relation headings before organization-wide writes begin.

For Ticket Specification v2, Workboard must additionally preserve the completed-state invariant,
reopen semantics, legacy read compatibility, and ambiguous closed-ticket handling before a
repository is migrated to declaration schema v2, v3, or v4.

Development Workflow v4 does not add Workboard lifecycle write semantics. Web Application Baseline v1
and Deployment Environments v1 likewise do not add Workboard write semantics.

## Forgejo workflow compatibility

Forgejo is the canonical automation provider. Active workflows are discovered from
`.forgejo/workflows/`. The former `.github/workflows/` location is not a supported active source
after migration.

GitHub-compatible workflow syntax may be retained only where Forgejo documents support for it.
Actions must use fully qualified trusted URLs, and workflow dependencies must be available on the
ARM64 organization runners. GitHub-only API calls, events, actions, and historical one-shot
workflows require explicit porting or removal.

Declaration v3 does not weaken required pull-request status checks, protected-branch rules, or
manual-main-build requirements inherited from the selected Development Workflow.

For declaration-v4 repositories, a required branch/pull-request naming check remains defense in
depth. If present, it MUST enforce semantics consistent with the released Development Workflow v4
profile and compatible Ticket Specification profile. Concrete trusted dependency-bot identities may
implement the contract-defined dependency-update exemption; implementations MUST NOT add undeclared
prefix aliases, ticket-number exceptions, title forms, or legacy creation-time cutoffs.

## Published-artifact immutability

Tests protect previously released compatibility and declaration artifacts by Git blob SHA. New
schema/profile versions MUST be introduced as new files. Existing released files MUST NOT be edited
to add fields or pairings.

This applies in particular to:

- declaration schemas v1, v2, and v3;
- declaration-v1, declaration-v2, and declaration-v3 reference files;
- compatibility profiles v1 and v2;
- released normative standards through Development Workflow v3.

## Failure behavior

Validation fails rather than guessing when:

- declaration/standard pairings are unsupported;
- a required contract field is missing;
- a consumer attempts partial declaration-v3 or declaration-v4 web/deployment adoption;
- a v4 writer cannot resolve ticket kind or the canonical branch prefix;
- a proposed v4 branch or ticket-linked pull request violates the released naming contract;
- artifact release state is ambiguous;
- PROD could receive an unreleased artifact;
- consumer automation is not compatible with the selected contract set.

Failure of a proposed migration does not invalidate the previously pinned declaration when that
previous contract remains unchanged and conformant.

## Deprecation

A compatibility path may be deprecated only after all known consumers have migrated and a
replacement has passed Canary validation. Removal requires a documented migration window and a new
release.
