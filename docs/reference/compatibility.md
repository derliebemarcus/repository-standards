# Compatibility and Versioning

## Versioning model

A published standard version is a semantic contract. Consumers keep the behavior of their pinned
contract set until they explicitly migrate. Published standards, schemas, compatibility profiles,
generated adapters/templates, and released reference declarations are immutable.

Repository declarations are versioned compatibility contracts. Unsupported combinations MUST fail
validation rather than being guessed, coerced, or silently upgraded.

## Canonical compatibility profiles

Compatibility profiles are additive and immutable after release. Product/System Readiness v1 adds:

```text
profiles/repository-standards-compatibility-v10.json
```

It supersedes v9 by copying every v9 pairing unchanged and appending declaration-v11 pairings.
Repository Standards v9.3.0 is the first release in which those v11 pairings are `supported`.
Earlier compatibility profiles remain authoritative for releases that pin them.

The machine-readable profile is the exact source of pairing truth. Documentation MUST NOT mutate an
older profile to add a new declaration or capability.

## Released compatibility remains unchanged

Declaration versions v1-v10 and their released pairings continue to mean exactly what their pinned
compatibility profiles define. Product/System Readiness v1 publication does not retrofit any of
these consumers.

In particular:

- Ticket Specification v1-v4 remain immutable;
- declaration schemas v1-v10 remain immutable;
- existing Repository Documentation, Development Workflow, Technology Baseline, web/deployment,
  Contract-first Delivery, Repository Environments, and Repository Localization pairings remain
  unchanged; and
- a repository that does not adopt declaration v11 keeps its existing behavior.

## Declaration v11 supported pairing

Declaration v11 is additive. Its core supported pairing selects:

| Capability | Version |
| --- | --- |
| Ticket Specification | v5 |
| Development Workflow | v8 |
| Repository Documentation | v2 |
| Technology Baseline | v1 |
| Contract-first Delivery | v1 |
| Product/System Readiness | v1 |

The web pairing additionally selects Web Application Baseline v3 and Deployment Environments v1,
with Repository Localization v1 represented in the compatibility profile where applicable.

Repository Standards v9.3.0 qualifies these pairings for explicit release-pinned adoption. The
`status: supported` transition means that the portable contract set has passed its release and
conformance gate; it does not migrate a consumer and does not imply that an arbitrary consumer's
active writers, validators, or provider automation are compatible. The activation metadata remains
fail-closed and requires compatible Ticket Specification v5 and Product/System Readiness v1
automation before migration. Web consumers retain the additional qualified Web v3 requirements.

## Product/System Readiness compatibility boundary

Product/System Readiness applicability is not inferred from the Repository Standards declaration,
Repository Profile, Repository Documentation Profile, web profile, or deployment profile. The
Repository Standards declaration selects the capability version; `.product-readiness.yml` authors
whether that capability is `required` or `not-applicable` for the repository and defines its
Subjects when required.

Ticket Specification v5 owns Product-/Release-Epic Increment Targets. The repository sidecar owns
long-term Subject Targets. Neither target is derived from the other.

Provider automation MUST preserve the following boundaries:

```text
authored intent != derived readiness
target != candidate
target != assessed
target != established
deployment != operational proof
PROD != TRL 9
product stage != TRL
```

## Ticket Specification compatibility

### v1-v4

Ticket Specification v1-v4 keep their released semantics. v4 adds Contract-first Delivery metadata
and remains the ticket contract for declaration v9/v10 consumers. Publication of v5 does not add a
Product Increment section to v1-v4 tickets.

### v5

Ticket Specification v5 incorporates v4 and adds Product-/Release-Epic readiness increment intent.
Every v5 ticket has a `product_increment` value; it is normally `null`. A non-null increment is
allowed only for an Epic and carries authored Product Stage, stable Subject binding, and Increment
Readiness Target plus an exact assessment reference when qualifying completion.

Candidate, Assessed, Established, Preservation, Requalification, current, and actual readiness are
not authored ticket fields. A readiness-targeted Epic cannot complete successfully without derived
assessment evidence meeting its target.

## Product Stage compatibility

Product Stage and TRL are orthogonal across all Product/System Readiness integrations. `mvp` may
reach TRL 9 for its defined scope; `production` implies no TRL. Migration tooling MUST NOT infer one
dimension from the other.

## Security compatibility boundary

TRL is not a security classification. A consumer or provider MUST NOT infer `secure`, `low risk`,
`security approved`, or `low criticality` from TRL 9. Security/risk/exposure/data/criticality gates
remain independent even when technical security evidence contributes to readiness qualification.

## Migration

Changing declaration schema or selected standard versions is an explicit reviewed repository
migration. Declaration v11 is available from Repository Standards v9.3.0 and MUST be pinned to an
immutable release identity. Follow:

- `docs/repository-contract-v11-migration.md`;
- `docs/ticket-standard-v5-migration.md`; and
- `docs/reference/product-system-readiness.md`.

A failed proposed migration does not invalidate the previously pinned declaration when the previous
contract remains unchanged and conformant.

## Provider compatibility

Repository Standards remains the portable source of normative contracts. Jenkins and Maintenance
may implement compatible validators and evaluators, but are provider implementations rather than
prerequisites for interpreting the standard.

A repository MUST NOT migrate to a newer declaration when active writing/enforcement automation
cannot implement its selected contract. For declaration v11 this includes Product/System Readiness
sidecar validation, Ticket Specification v5 parsing/writing, authored-versus-derived separation,
and fail-closed Epic completion semantics. Productive evidence evaluation/gate activation is a
separate provider capability and is not activated merely by publication of Repository Standards
v9.3.0.

## Published-artifact immutability

Tests protect released standards, schemas, compatibility profiles, generated adapters/templates,
and reference declarations by Git blob SHA or equivalent regression assertions. New contract
versions are introduced as new files. Existing released files MUST NOT be edited to add fields,
pairings, or semantics.

## Failure behavior

Validation fails rather than guessing when, among other cases:

- a declaration/standard pairing is unsupported;
- a required contract field is missing;
- a v11 repository omits the Product/System Readiness selection;
- Product/System Readiness applicability is inferred instead of authored;
- a readiness declaration contains unknown or derived/current readiness fields;
- a Product-/Release-Epic attempts `Status/Done` without qualifying evidence;
- Product Stage is used to manufacture a TRL;
- deployment or PROD presence is used as operational proof; or
- consumer automation is incompatible with the selected contract set.

## Deprecation

A compatibility path may be deprecated only after known consumers have migrated and a replacement
has passed Canary validation. Removal requires a documented migration window and a new release.
