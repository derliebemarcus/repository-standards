# Repository contract v8 migration

## Purpose

Declaration schema v8 is the explicit opt-in boundary for Repository Documentation v2 and
Development Workflow v7. It retains Ticket Specification v3, Technology Baseline v1, the existing
branching models, and the optional Web Application Baseline v1 plus Deployment Environments v1 pair.

Development Workflow v7 incorporates Development Workflow v6 required-check identity and trust-boundary
semantics and adds the canonical pull-request supersession contract. Publishing declaration v8 does
not implicitly migrate declaration-v1 through declaration-v7 consumers.

## Why v8 is required

Repository Documentation v2 adds new mandatory semantics: purpose-specific quality criteria for the
normative document types and an explicit Verification / Evidence validity model. These obligations
require a new immutable Repository Documentation version.

Development Workflow v7 adds a new mandatory representation for superseded pull requests. A
superseded pull request must begin with the exact `# Superseded by / See other` block, list at least
one concrete successor pull request as an unordered list, carry `Status/Superseded`, and must not be
merged. Development Workflow v6 is already released and remains immutable, so the supersession
semantics are introduced through v7 rather than modifying v6.

The repository declaration binds independently versioned standards into one supported set.
Declaration v7 remains paired with Development Workflow v6 and Repository Documentation v1;
declaration v8 selects Development Workflow v7 and Repository Documentation v2.

## Supported v8 pairings

Core repositories use:

```yaml
version: 8
standards:
  ticket-specification: v3
  development-workflow: v7
  repository-documentation: v2
  technology-baseline: v1
```

Web repositories additionally select both:

```yaml
  web-application-baseline: v1
  deployment-environments: v1
```

The canonical references are:

- `reference/repository-standards-v8.single.yml`;
- `reference/repository-standards-v8.integration.yml`;
- `reference/repository-standards-v8.web.single.yml`; and
- `reference/repository-standards-v8.web.integration.yml`.

The canonical additive compatibility matrix is
`profiles/repository-standards-compatibility-v7.json`.

## Preconditions

Before changing a consumer to `version: 8`:

1. validate the current declaration against its pinned released schema;
2. review the [Repository Documentation v2 migration](repository-documentation-v2-migration.md);
3. classify the repository's existing documentation by information task where useful;
4. identify historical evidence that could be mistaken for current Reference, Architecture, or
   Operations documentation;
5. verify that profile-required documents and repository navigation satisfy the intended v2
   information tasks;
6. retain the Development Workflow v6 required-check mapping and `pull_request_target` trust-boundary
   behavior incorporated by Development Workflow v7;
7. ensure pull-request metadata writers and validators can enforce the Development Workflow v7
   supersession contract, including `Status/Superseded`, the exact leading successor block, and the
   prohibition on merging superseded pull requests; and
8. where Maintenance performs blocking enforcement or migration writes, verify that a compatible
   Maintenance release explicitly supports the v8 pairing.

## Pull-request supersession contract

Development Workflow v7 introduces one canonical representation for a pull request that has been
replaced by another pull request. The first content of the superseded pull-request body is:

```markdown
# Superseded by / See other

- #577
```

The list is unordered and contains at least one successor pull-request reference. Each list item
contains exactly one successor reference; explanatory prose does not belong in the leading block.

The pull request also carries `Status/Superseded`. The body marker and label are one coherent state:
one without the other is invalid. A superseded pull request is not a merge candidate and must not be
merged. It should be closed once at least one successor exists and the relationship is recorded. The
marker and label remain after closure.

Validators should verify that referenced successor pull requests exist, reject direct self-reference,
and must not infer supersession solely from branch similarity, title similarity, ticket number,
comments, or closed state.

## Documentation declaration

The repository's `.repository-documentation.yml` must select Repository Documentation v2, for
example:

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

The profile remains repository-specific. Migration does not require changing an `application`,
`library`, or `infrastructure` profile merely because the standard version changes.

## Compatibility behavior

Compatibility profile v7 is additive: all pairings already published in compatibility profile v6
remain supported and unchanged, and the two declaration-v8 pairings are added.

No other combination is supported. In particular:

- declaration v7 + Development Workflow v7 is unsupported;
- declaration v8 + Development Workflow v6 is unsupported;
- declaration v7 + Repository Documentation v2 is unsupported;
- declaration v8 + Repository Documentation v1 is unsupported;
- a partial Web Application Baseline / Deployment Environments selection remains unsupported; and
- unsupported pairings continue to fail closed rather than being guessed or silently upgraded.

## Relationship to Development Workflow v6

Development Workflow v7 incorporates the provider-neutral required-check identity,
Forgejo/Gitea event-specific context mapping, GitHub mapping, `pull_request_target` trust boundary,
branching, release, review, naming, and pre-write semantics of Development Workflow v6.

The v7 change is intentionally narrow: it adds canonical superseded-pull-request metadata and its
lifecycle/merge invariants. Declaration v7 remains on v6. Declaration v8 adopts v7 together with
Repository Documentation v2. A v7-to-v8 repository migration must therefore preserve the already
qualified required-check configuration while adding v7 supersession support.

## Maintenance and Jenkins boundary

Repository Standards owns the portable normative contract, schemas, profiles, compatibility
pairings, and references. Jenkins is an implementation and is not required to interpret or validate
v8 in another environment.

Where `siczb/maintenance` supplies blocking validators or performs repository writes, consumers must
wait until a compatible Maintenance version advertises declaration v8 support and passes its
applicable compatibility/Canary validation. Any Maintenance component that marks pull requests as
superseded must write and validate the body marker and `Status/Superseded` coherently and must prevent
a superseded pull request from being merged.

## Qualification

A v8 migration is qualified when:

- `.repository-standards.yml` matches one of the v8 reference pairings and selects Development
  Workflow v7;
- `.repository-documentation.yml` selects standard version 2 and a supported 2.x ruleset;
- the declarations validate against the v8 and Repository Documentation v2 schemas;
- the compatibility resolver selects the v8/v7 pairing from compatibility profile v7;
- unsupported pairings still fail closed;
- pull-request metadata tooling validates the v7 supersession marker/label coherence and no-merge
  invariant;
- documentation required by the selected profile is present and correctly navigated;
- the repository has addressed v2 information-task and evidence distinctions relevant to its
  documentation set; and
- the consumer's normal repository qualification succeeds.

## Rollback

If v8 adoption cannot be qualified safely, restore the previously pinned declaration and
`.repository-documentation.yml` version together. Do not weaken checks, mutate released v1-v7
contracts, or add an undeclared compatibility pairing to bypass the failure.

Documentation improvements and historical evidence created during migration may remain when they are
compatible with the restored contract and accurately labeled. A pull request already marked
superseded must not be made mergeable merely as a rollback shortcut; restore metadata only when the
supersession fact itself was incorrect.
