# Product/System Readiness

Product/System Readiness v1 is the provider-neutral readiness model for concrete software products
and operated systems. The normative Design Contract is
`standards/product-system-readiness/v1/standard.md`; this page explains the repository and ticket
integration supplied by Ticket #60.

## Frozen governing contracts

The implementation is governed by the immutable Design Contract:

```text
artifact: standards/product-system-readiness/v1/standard.md
revision: fa10d783440c4a798f3fe5b6fa55ac6166ce77da
blob:     2729a92f5a35091b0ca28b7eda361007fa7b0c6f
```

and the qualified Test Contract:

```text
artifact: profiles/product-system-readiness-test-contract-v1.json
revision: a8fa9519a97f188d5918aee79d5203f3f8deb25d
blob:     bd96ed63fb0d0774ba856d6d39abff17eb6516c1
```

The Test Contract remains unchanged. Its oracle is a qualification harness, not the productive
Maintenance/Jenkins readiness evaluator.

## Authority model

The contract intentionally separates authored intent from evidence-derived state:

| Concept | Authority |
| --- | --- |
| Applicability | Authored in `.product-readiness.yml` |
| Subject kind | Authored in `.product-readiness.yml` |
| Subject Identity | Authored in `.product-readiness.yml` |
| Long-term Product/System Target | Authored in `.product-readiness.yml` |
| Product-/Release-Epic Increment Target | Authored in Ticket Specification v5 |
| Product Stage | Authored in Ticket Specification v5 for an increment |
| Candidate | Derived from evidence |
| Assessed | Derived from evidence |
| Established | Derived from evidence |
| Preservation | Derived from evidence |
| Requalification | Derived from evidence |

The core invariants are therefore:

```text
authored intent != derived readiness
target != candidate
target != assessed
target != established
deployment != operational proof
PROD != TRL 9
product stage != TRL
```

A ticket, repository profile, documentation profile, environment name, deployment, or Product Stage
MUST NOT manufacture authoritative current readiness.

## Repository declaration

A repository that adopts Product/System Readiness v1 uses the repository-owned sidecar:

```text
.product-readiness.yml
```

The versioned validation contract is:

- `schemas/product-system-readiness-declaration-v1.schema.json`;
- `profiles/product-system-readiness-declaration-v1.json`; and
- `tools/product_system_readiness.py`.

The declaration is fail closed. Unknown fields are rejected. A `required` declaration needs at
least one Product/System Subject and every Subject needs a stable identity and long-term target from
TRL 1 through 9. A `not-applicable` declaration needs a non-empty rationale and declares no
Subjects.

Example product declaration:

```yaml
schema: product-system-readiness-intent-v1
applicability: required
rationale: null
subjects:
  - kind: product
    identity: product:example-service
    long_term_target: 9
```

Example shared library declaration:

```yaml
schema: product-system-readiness-intent-v1
applicability: not-applicable
rationale: "Shared library only; no bounded product or operated system subject is declared."
subjects: []
```

Subject kinds are exactly `product` and `system`. The stable identity format is
`<kind>:<stable-id>`, for example `product:example-service` or `system:edge-routing`. Branch names,
environment names, mutable URLs, artifact tags, and repository profiles are not stable Subject
Identities. When a repository declares multiple Subjects, each remains independent; there is no
repository-wide TRL aggregation.

Applicability is authored. It is never inferred solely from a Repository Profile, Repository
Documentation Profile, web/application classification, or infrastructure classification. An
infrastructure repository may legitimately declare an operated `system` Subject; a library may
legitimately declare `not-applicable` with rationale.

## Ticket Specification v5

Ticket Specification v5 incorporates v4 and adds one `## Product increment` YAML section to every
ticket. Non-targeted tickets use:

```yaml
product_increment: null
```

A Product-/Release-Epic may instead declare:

```yaml
product_increment:
  kind: release
  subject_identity: "product:example-service"
  stage: mvp
  readiness_target: 9
  assessment: null
```

The `subject_identity` binds the increment to exactly one Subject in `.product-readiness.yml`.
`readiness_target` is the authored target for this Epic only; it is separate from the Subject's
long-term target. Automation MUST NOT copy or infer one from the other.

Product Stage and TRL are orthogonal. In particular:

- an `mvp` may target and establish TRL 9 for its deliberately bounded scope;
- `production` implies no TRL;
- a Product Stage never sets a TRL or target; and
- a target never sets a Product Stage.

An MVP can therefore reach TRL 9 when its intentionally limited scope is fully qualified through the
cumulative criteria and the actual subject has been proven by successful intended operational use.
The fact that later scope is planned does not make the qualified MVP incomplete for its declared
boundary.

## Epic completion contract

A Product-/Release-Epic with a Readiness Target cannot successfully complete as `Status/Done`
without an exact `assessment` artifact reference. The referenced assessment must:

1. bind to the same Subject Identity;
2. be valid for the exact evaluated revision/artifact/context; and
3. derive an Assessed Readiness equal to or above the authored Increment Target.

Missing, stale, mismatched, unassessed, or insufficient evidence fails completion closed. The target
may instead be changed through the normal reviewed ticket-governance process before completion.
Completion never causes the target to be rewritten and never manufactures an assessment.

Ticket #60 supplies this machine-checkable contract and repository-local validation surface. The
productive Maintenance/Jenkins evidence evaluator and organization-wide gate activation remain a
separate provider implementation.

## Assessment semantics

TRL remains the ordinal NASA-aligned scale 1 through 9. `unassessed` means that no qualifying
current assessment exists; it is not TRL 0. Every level is cumulative.

The important operational boundary remains:

```text
TRL 8 = actual final system fully qualified for intended operation
TRL 9 = that actual system proven by successful real operational use
```

A production-equivalent qualification context can support TRL 8 without an environment named PROD.
Conversely, a PROD URL, deployment, health check, smoke test, brief reachability, or synthetic-only
workload cannot establish TRL 9. TRL 9 requires subject-appropriate real operational use and the
full evidence defined by the governing Design/Test Contracts.

After establishment, ordinary changes use Preservation evidence. A material change that crosses an
evidence validity boundary requires Requalification. Historical readiness remains attached to the
revision for which it was established and is never rewritten.

## Security boundary

Product/System Readiness is not a security, risk, exposure, data, or criticality classification.
None of these implications is valid:

```text
TRL 9 => secure
TRL 9 => low risk
TRL 9 => security approved
TRL 9 => low criticality
```

Technical security evidence may contribute to readiness qualification where applicable, but it does
not replace the independent security-governance process or security gates.

## Adoption and compatibility

Repository Standards declaration v11 is the additive adoption boundary for Ticket Specification v5
and Product/System Readiness v1. The v11 pairings in
`profiles/repository-standards-compatibility-v10.json` are intentionally `candidate` until the
separate release/conformance qualification is complete. Existing declaration versions and Ticket
Specification v1-v4 consumers remain unchanged.

Adoption is explicit and opt in. Publishing these artifacts does not silently add Product/System
Readiness to an older consumer, infer applicability, or activate provider-side gates. See
`docs/repository-contract-v11-migration.md` and `docs/ticket-standard-v5-migration.md`.

## Related contracts

- `standards/contract-first-delivery/v1/standard.md` defines revision-bound Design/Test/Implementation
  and Conformance Evidence.
- `standards/deployment-environments/v2/standard.md` remains authoritative for artifact release state,
  runtime environments, promotion, PROD, and rollback.
- `standards/repository-environments/v1/standard.md` defines human-web URLs; those URLs are not
  readiness evidence.
- `standards/ticket-specification/v5/standard.md` defines Product-/Release-Epic increment intent and
  completion semantics.
