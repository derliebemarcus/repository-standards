# Repository contract v11 migration

Repository declaration v11 is the additive adoption boundary for Product/System Readiness v1 and
Ticket Specification v5. It does not alter declaration v1-v10 or their released compatibility
pairings.

## Release boundary

The v11 pairings in `profiles/repository-standards-compatibility-v10.json` are `supported` beginning
with immutable Repository Standards release v9.3.0. This releases the portable contract set; it does
not migrate any repository automatically and it does not assert that an arbitrary consumer's active
writers, validators, or provider automation are compatible.

A consumer MUST pin Repository Standards v9.3.0 or a later release that preserves this pairing and
MUST NOT migrate to v11 until its active writers/validators implement Ticket Specification v5 and
Product/System Readiness v1. Productive Maintenance/Jenkins readiness assessment and gate activation
remain a separate provider capability.

## Selected standards

The core v11 pairing selects:

```yaml
version: 11
standards:
  ticket-specification: v5
  development-workflow: v8
  repository-documentation: v2
  technology-baseline: v1
  contract-first-delivery: v1
  product-system-readiness: v1
```

The web pairing additionally selects Web Application Baseline v3 and Deployment Environments v1.
Product/System Readiness applicability remains independent of those profiles and is authored only
through `.product-readiness.yml`.

## Migration procedure

1. Pin an immutable Repository Standards release at or after v9.3.0 that advertises the v11 pairing.
2. Keep the repository's existing declaration and pinned standards unchanged until all following
   migration prerequisites are satisfied.
3. Decide Product/System Readiness applicability explicitly.
4. Add `.product-readiness.yml` and validate it against the v1 declaration contract.
5. If applicability is `required`, declare one or more stable `product`/`system` Subjects and their
   long-term TRL targets independently.
6. Upgrade ticket writers/parsers to Ticket Specification v5 and its generated adapter/templates.
7. Add `product_increment: null` to v5 tickets unless an Epic deliberately declares a Product- or
   Release-Increment Target.
8. Verify active automation preserves authored-versus-derived separation and fail-closed Epic
   completion semantics.
9. Validate the whole v11 declaration against the released compatibility profile.
10. Only then switch `.repository-standards.yml` to v11 through the repository's normal reviewed
    change process.

Do not infer applicability from repository profile, documentation profile, environment names, or
whether the repository deploys software. Do not infer Subject Identity, Product Stage, targets, or
current readiness from historical repository state.

## Semantic boundaries

Migration MUST preserve:

```text
authored intent != derived readiness
target != candidate
target != assessed
target != established
deployment != operational proof
PROD != TRL 9
product stage != TRL
```

An MVP may establish TRL 9 for its deliberately bounded scope when the full cumulative qualification
and successful real operational use are evidenced. TRL 9 does not imply security approval, low risk,
low exposure, low criticality, or any other independent governance classification.

## Rollback

Before adoption is committed, migration failure leaves the prior released declaration authoritative.
After adoption, rollback is a deliberate reviewed declaration migration; do not delete or rewrite
historical readiness evidence to simulate that the v11 contract never applied.

## Provider boundary

The portable repository contract defines declaration, Ticket Specification, and completion
semantics. Productive Maintenance/Jenkins evidence collection, assessment execution, and gate
activation are provider responsibilities and are not introduced by declaration publication alone.
