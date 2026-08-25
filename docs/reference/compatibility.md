# Compatibility and Versioning

## Versioning model

`standard_version` identifies a semantic contract. Consumers continue to receive their pinned
version behavior until they explicitly migrate. Published standards, schemas, compatibility
profiles, and reference declarations are immutable.

`ruleset_version` uses semantic versioning inside one standard version:

- patch: corrections and clarifications that add no obligation;
- minor: backward-compatible capabilities, optional fields, and opt-in checks;
- major: a new standard version when obligations or semantics change incompatibly.

Repository declarations are versioned compatibility contracts. Unsupported combinations MUST fail
validation rather than being guessed, coerced, or silently upgraded.

## Canonical compatibility profile

The current additive compatibility matrix is
`profiles/repository-standards-compatibility-v7.json`. Earlier compatibility profiles remain
immutable for consumers pinned to older releases.

| Declaration | Ticket Specification | Development Workflow | Repository Documentation | Technology Baseline | Web Application Baseline | Deployment Environments | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| v1 | v1 | v2 | v1 | — | — | — | Supported |
| v2 | v2 | v3 | v1 | — | — | — | Supported |
| v3 | v2 | v3 | v1 | — | v1 | v1 | Supported |
| v4 | v2 | v4 | v1 | — | — | — | Supported |
| v4 | v2 | v4 | v1 | — | v1 | v1 | Supported |
| v5 | v3 | v5 | v1 | — | — | — | Supported |
| v5 | v3 | v5 | v1 | — | v1 | v1 | Supported |
| v6 | v3 | v5 | v1 | v1 | — | — | Supported |
| v6 | v3 | v5 | v1 | v1 | v1 | v1 | Supported |
| v7 | v3 | v6 | v1 | v1 | — | — | Supported |
| v7 | v3 | v6 | v1 | v1 | v1 | v1 | Supported |
| v8 | v3 | v7 | v2 | v1 | — | — | Supported |
| v8 | v3 | v7 | v2 | v1 | v1 | v1 | Supported |

No other pairing is supported.

Released reference declarations are grouped by declaration version under `reference/`. Declaration
v8 references are:

- `repository-standards-v8.single.yml`;
- `repository-standards-v8.integration.yml`;
- `repository-standards-v8.web.single.yml`; and
- `repository-standards-v8.web.integration.yml`.

Changing declaration schema or a selected standard version is an explicit repository migration.

## Repository Documentation compatibility

### Repository Documentation v1

Repository Documentation v1 remains the immutable documentation contract for declaration v1 through
v7 pairings. Publication of v2 does not change a v1 consumer.

### Repository Documentation v2

Repository Documentation v2 introduces purpose-specific normative quality criteria for Tutorial,
How-to Guide, Reference, Explanation, Architecture, Decision / ADR, Operations / Runbook,
Verification / Evidence, and Index / Navigation. Verification becomes an explicit point-in-time
evidence class rather than ordinary Reference documentation.

Those are new obligations, so v2 is selected only by declaration v8. Declaration v7 + Repository
Documentation v2 and declaration v8 + Repository Documentation v1 are unsupported and fail closed.

See `../repository-documentation-v2-migration.md` and
`../repository-contract-v8-migration.md`.

## Ticket Specification compatibility

### Ticket Specification v1

Ticket Specification v1 introduced mandatory metadata, description sections, readiness decisions,
and relative Story Point semantics. It remains valid for the declaration v1 / Development Workflow
v2 pairing.

### Ticket Specification v2

Ticket Specification v2 defines the canonical completed representation as Forgejo `state=closed`
plus exactly `Status/Done`. An open issue must not carry `Status/Done`. It is paired with Development
Workflow v3 under declarations v2/v3 and Development Workflow v4 under declaration v4.

### Ticket Specification v3

Ticket Specification v3 preserves v2 lifecycle semantics and adds canonical Story Point anchors for
`1, 2, 3, 5, 8, 13`. Story Points MUST NOT be converted mechanically to hours, person-days,
duration, staffing, file counts, task counts, lines of code, or another single proxy.

It is paired with Development Workflow v5 under declarations v5/v6, Development Workflow v6 under
declaration v7, and Development Workflow v7 under declaration v8.

## Development Workflow compatibility

### Development Workflow v2-v5

Development Workflow v2 is paired with Ticket Specification v1 under declaration v1. Development
Workflow v3 adopts Ticket Specification v2 lifecycle semantics while preserving v2 branching and
release behavior. Development Workflow v4 adds released branch/pull-request naming and fail-closed
pre-write validation. Development Workflow v5 preserves v4 behavior while coupling to Ticket
Specification v3.

### Development Workflow v6

Development Workflow v6 preserves v5 ticket, branch, release, Hotfix, review, merge, and pre-write
semantics. It adds a provider-neutral identity contract for required quality gates.

A required gate has a logical identity independent from a provider's rendered check name. Provider
adapters map that logical identity to a concrete check and MUST fail closed when the configured
required context cannot be produced by an active workflow.

For Forgejo/Gitea Actions the concrete context is:

```text
<workflow> / <job> (<event>)
```

The event is part of the provider-specific identity. Changing from `pull_request` to
`pull_request_target` therefore changes the concrete context and MUST be handled as a coordinated
workflow/branch-protection migration.

For GitHub required status checks, normal workflows use job-based identities; reusable workflows add
the reusable job. The event trigger, workflow name, and matrix are not part of the GitHub Required
Status Check identity. A GitHub adapter MUST NOT invent a Forgejo/Gitea event suffix.

Development Workflow v6 is selected by declaration v7 and remains immutable after publication.

### Development Workflow v7

Development Workflow v7 incorporates Development Workflow v6 and adds canonical pull-request
supersession semantics. It is selected only by declaration v8.

A superseded pull request MUST begin with exactly:

```markdown
# Superseded by / See other

- #<successor-pr>
```

The heading is the first body content and is immediately followed by an unordered list containing at
least one concrete successor pull-request reference. Each list item contains exactly one successor
reference; explanatory prose is not allowed inside this leading block.

The superseded pull request MUST also carry `Status/Superseded`. The label and leading body marker
form one coherent state: one without the other is invalid. A superseded pull request MUST NOT be
merged and SHOULD be closed once at least one successor exists and the relationship is recorded. The
marker and label remain after closure.

Validators SHOULD verify that successor pull requests exist, MUST reject direct self-reference, and
MUST NOT infer supersession solely from branch similarity, title similarity, ticket number, comments,
or closed state.

Development Workflow v7 does not weaken or replace v6 required-check identity or trust-boundary
requirements.

## `pull_request_target` trust boundary

`pull_request_target` evaluates the base/target branch context and may receive privileges or secrets
that are unavailable to an untrusted pull-request workflow. Under Development Workflow v6 and v7, a
privileged `pull_request_target` workflow MUST NOT execute, source, import, build, test, lint, or
otherwise run pull-request-controlled code.

It SHOULD be limited to base-branch policy, metadata, labels, comments, ticket linkage, and repository
governance operations that do not execute untrusted PR content. A gate intended to validate proposed
code MUST use an execution model that actually evaluates PR content under an appropriate untrusted
code boundary.

## Declaration schema compatibility

Declarations v1-v5 preserve their published combinations and branching models. Publication of later
standards does not migrate them implicitly.

Declaration v6 adds Technology Baseline v1 while retaining Ticket Specification v3, Development
Workflow v5, and Repository Documentation v1.

Declaration v7 retains Technology Baseline v1 and changes Development Workflow v5 to v6. It is the
explicit adoption boundary for provider-neutral required-check identities and provider mappings.

Declaration v8 retains Ticket Specification v3 and Technology Baseline v1, changes Development
Workflow v6 to v7, and changes Repository Documentation v1 to v2. It is the explicit adoption
boundary for canonical pull-request supersession semantics and the purpose-specific documentation
model including Verification / Evidence.

## Web Application Baseline compatibility

Web Application Baseline v1 defines canonical static legal/accessibility routes, shared application
design/accessibility expectations, and artifact-state-dependent public provenance. It follows the
repository's explicit Design System decision and does not itself force Design System adoption.

Web Application Baseline v1 and Deployment Environments v1 are a paired opt-in extension wherever a
declaration schema supports a web variant. Partial adoption is unsupported.

## Deployment Environments compatibility

Deployment Environments v1 reuses the selected Development Workflow branching model: `single` maps
default DEV source to `main`; `integration` maps it to `develop`. Preview/PR is not a canonical
environment, STAGE is optional, and PROD accepts only immutable final-release artifacts. Promotion
and rollback select existing immutable artifacts rather than rebuilding application content.

## Technology Baseline compatibility

Technology Baseline v1 is mandatory in declarations v6, v7, and v8. It remains independently
versioned and is not modified by Development Workflow v6/v7 or Repository Documentation v2.

## Maintenance compatibility

Maintenance may embed compatible validators and operational resources during migrations. Repository
Standards remains the portable source of normative contracts; Jenkins and Maintenance are
implementations, not prerequisites for interpreting or locally validating the standards.

Repositories MUST NOT migrate to a newer declaration when active writing/enforcement automation
cannot implement the selected contract. For v7/v8 consumers, Maintenance automation that manages
required checks or branch protection must implement Development Workflow v6 provider mapping,
producibility validation, coordinated migration, and `pull_request_target` trust-boundary rules.

For declaration-v8 consumers, any Maintenance automation that writes or validates pull-request
supersession metadata must additionally implement Development Workflow v7: exact leading body block,
`Status/Superseded`, marker/label coherence, successor validation where supported, and the no-merge
invariant. Maintenance validators that enforce Repository Documentation must also support the v2
declaration and objective contract invariants without inventing editorial word-count or similar
quality proxies.

## Workboard compatibility

Workboard owns ticket migration and dependency reconciliation. Its parser and migration tooling must
pass compatibility tests against the released Ticket Specification profile and canonical relation
headings before organization-wide ticket writes begin. Ticket Specification v3 does not require
historical re-estimation.

Pull-request supersession is Development Workflow metadata, not an issue lifecycle status. A
consumer MUST NOT apply `Status/Superseded` to ordinary issues merely because the label shares the
`Status/` prefix.

## Forgejo workflow compatibility

Forgejo remains the canonical automation provider. Active workflows are discovered from
`.forgejo/workflows/`; `.github/workflows/` is not a supported active source after migration.
GitHub-compatible workflow syntax may be retained only where Forgejo supports it.

Required pull-request checks, protected-branch rules, review gates, manual-main-build requirements,
and supersession semantics remain those of the selected Development Workflow. Under Development
Workflow v6/v7 the logical required gate is portable, but the concrete status/check identity is
provider-specific.

## Published-artifact immutability

Tests protect previously released standards, compatibility profiles, schemas, generated adapters,
and reference declarations by Git blob SHA or equivalent regression assertions. New contract
versions MUST be introduced as new files. Existing released files MUST NOT be edited to add fields,
pairings, or semantics.

Development Workflow v7, Repository Documentation v2, declaration schema v8, and compatibility
profile v7 extend the contract set without modifying Development Workflow v6, Repository
Documentation v1, declaration schemas v1-v7, or compatibility profiles v1-v6.

## Failure behavior

Validation fails rather than guessing when:

- declaration/standard pairings are unsupported;
- a required contract field is missing;
- a consumer attempts partial web/deployment adoption;
- a branch or ticket-linked pull request violates its released naming contract;
- a required concrete status/check context cannot be produced by an active workflow;
- a provider mapping substitutes another provider's status-identity semantics;
- a privileged `pull_request_target` workflow would execute pull-request-controlled code;
- a superseded pull request has the leading supersession marker without `Status/Superseded`;
- `Status/Superseded` exists without the canonical leading successor block;
- a superseded pull request is treated as a merge candidate;
- artifact release state is ambiguous;
- PROD could receive an unreleased artifact; or
- consumer automation is not compatible with the selected contract set.

Failure of a proposed migration does not invalidate the previously pinned declaration when that
previous contract remains unchanged and conformant.

## Deprecation

A compatibility path may be deprecated only after known consumers have migrated and a replacement
has passed Canary validation. Removal requires a documented migration window and a new release.
