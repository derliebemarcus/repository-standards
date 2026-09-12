# Ticket Specification v5

## Status and scope

Ticket Specification v5 is the additive successor to Ticket Specification v4. It normatively
incorporates every Ticket Specification v4 requirement unless this document explicitly adds a
requirement. Ticket Specification v1 through v4 remain immutable.

v5 adds machine-readable Product-/Release-Epic increment metadata for Product/System Readiness
v1. It does not make readiness an authored current-state field and does not implement the
provider-side Product/System Readiness evaluator.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174.

## Source of truth

The normative source is this document together with the requirements incorporated from
`standards/ticket-specification/v4/standard.md`. The complete machine-readable representation is
`profiles/ticket-specification-v5.json`, validated by
`schemas/ticket-specification-v5.schema.json`.

Consumers MUST pin a released version. Adoption of v5 MUST be explicit and MUST use a compatible
Repository Standards declaration that also selects Product/System Readiness v1, Contract-first
Delivery v1, and the compatible Development Workflow version.

## Incorporated Ticket Specification v4 requirements

Every v4 requirement remains in force, including label cardinalities, Story Point anchors,
lifecycle state, ticket families, relation headings, Contract-first Delivery metadata, exact
contract references at readiness boundaries, and Conformance Evidence requirements.

## Product increment metadata

Every v5 ticket MUST carry a `product_increment` value. It MUST be `null` unless the ticket is a
Product-/Release-Epic that deliberately declares a bounded readiness increment. A non-null value
MUST contain exactly:

- `kind`: `product` or `release`;
- `subject_identity`: the stable Readiness Subject Identity from the adopted
  `.product-readiness.yml` declaration;
- `stage`: a non-empty authored Product Stage;
- `readiness_target`: an authored TRL target from 1 through 9; and
- `assessment`: either `null` before qualifying evidence exists, or an exact immutable/reproducible
  artifact reference to the assessment used for completion.

Presence of this object declares a Product-/Release-Epic increment. It does not assert current
readiness.

The canonical ticket-body representation is a `## Product increment` section containing exactly
one fenced YAML document whose root key is `product_increment`.

Example:

```yaml
product_increment:
  kind: release
  subject_identity: "product:example-service"
  stage: mvp
  readiness_target: 9
  assessment: null
```

Tickets without such an increment use:

```yaml
product_increment: null
```

## Authored versus derived authority

The following v5 fields are authored intent:

- Product Stage;
- Increment Readiness Target; and
- the Subject Identity binding that selects the declared Product/System Readiness Subject.

Candidate, Assessed, Established, Preservation, and Requalification readiness remain derived.
The ticket body MUST NOT introduce an authoritative current or actual TRL field. An assessment
artifact reference is evidence provenance, not an authored assessment result.

`Target = authored intent` and `Assessment = derived result` are independent invariants.

## Product Stage and TRL

Product Stage and TRL are orthogonal. Automation MUST NOT derive either dimension from the other.
In particular:

- `mvp` MUST NOT cap or prevent TRL 9;
- `production` MUST NOT imply any TRL;
- a Product Stage MUST NOT automatically set an Increment Target; and
- an Increment Target MUST NOT automatically set a Product Stage.

A deliberately bounded MVP MAY establish TRL 9 when the exact defined scope satisfies every
cumulative Product/System Readiness v1 criterion through TRL 9, including successful operational
use.

## Long-term versus increment target

The long-term Product/System Target is declared in `.product-readiness.yml`. The
`product_increment.readiness_target` belongs to one Product-/Release-Epic and is independent.
Automation MUST NOT copy, infer, aggregate, or otherwise manufacture one target from the other.

A lower Increment Target MAY be valid while the long-term target is higher. Multiple Readiness
Subjects in one repository remain independent; a ticket MUST bind to exactly one Subject Identity
and MUST NOT use a repository-wide aggregated TRL.

## Completion contract

For a Product-/Release-Epic with non-null `product_increment`, successful `Status/Done` completion
MUST have a non-null exact `assessment` artifact reference. The referenced assessment MUST bind to
the same Subject Identity and its evidence-derived Assessed Readiness MUST meet or exceed
`readiness_target`.

Missing, invalid, stale, mismatched, unassessed, or insufficient evidence MUST fail completion
closed. A target MAY instead be changed through the normal reviewed ticket-governance process
before completion. Closing the ticket MUST NOT cause automation to lower or rewrite the target,
invent an assessment, or infer readiness from Product Stage, deployment, environment name, or
PROD presence.

The schema can require the exact assessment reference at `Status/Done`; semantic evaluation of the
referenced assessment is a separate machine-checkable contract. Provider-specific evidence
collection and productive Maintenance/Jenkins evaluation remain outside Ticket Specification v5.

## Security boundary

Product/System Readiness is not a security, risk, exposure, data, or criticality classification.
Neither Ticket Specification v5 nor a Product/System Readiness assessment may infer any of the
following solely from TRL:

```text
TRL 9 => secure
TRL 9 => low risk
TRL 9 => security approved
TRL 9 => low criticality
```

Security evidence may contribute to readiness qualification when independently applicable, but it
MUST NOT replace the separate security-governance process or independent security gates.

## AI-assisted authoring

An AI agent operating on a v5 repository MUST load the released v5 adapter before creating,
changing, classifying, estimating, reopening, or closing a ticket.

The agent MUST keep Product Stage and targets authored and readiness results derived. It MUST NOT
write candidate, assessed, established, current, or actual readiness into a ticket as authoritative
metadata. Before completing a readiness-targeted Epic it MUST obtain the exact qualifying
assessment reference and verify that the derived assessment meets the declared target.

## Compatibility and migration

Ticket Specification v1 through v4 remain immutable for pinned consumers. v5 is an explicit
opt-in adoption boundary. Existing tickets MUST NOT be retrospectively assigned Product Stage,
Increment Targets, assessment results, or readiness history during migration.

Open Product-/Release-Epics may adopt `product_increment` only through a reviewed update. Other
migrated v5 tickets use `product_increment: null`. Existing consumers that remain pinned to v1-v4
continue to use their released contracts without Product/System Readiness reinterpretation.
