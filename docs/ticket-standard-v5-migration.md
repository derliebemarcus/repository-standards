# Ticket Specification v5 migration

Ticket Specification v5 is an explicit opt-in successor to v4. Existing v1-v4 consumers remain
valid and MUST NOT be rewritten merely because v5 artifacts exist.

## Preconditions

Adopt v5 only when the repository also adopts the compatible Repository Standards declaration that
selects Product/System Readiness v1 and when the writer/validator tooling understands v5.

Before migration:

1. keep the current released declaration valid;
2. decide Product/System Readiness applicability explicitly;
3. create and validate `.product-readiness.yml`;
4. identify stable Product/System Subject Identities when applicability is `required`;
5. decide which open Epics are genuinely Product-/Release-Epic increments; and
6. ensure ticket-writing automation can preserve Product Stage/Target as authored intent and keep
   Candidate/Assessed/Established/Preservation/Requalification derived.

## Ticket migration

Every v5 ticket contains a `## Product increment` section. Ordinary tickets and Epics that do not
represent a readiness increment use:

```yaml
product_increment: null
```

An open Product-/Release-Epic may adopt a non-null increment through a reviewed ticket change:

```yaml
product_increment:
  kind: release
  subject_identity: "product:example-service"
  stage: mvp
  readiness_target: 9
  assessment: null
```

Do not infer Product Stage or targets from old labels, milestones, releases, environments, deployed
state, repository profile, or historical ticket text. Do not synthesize historical assessments.

## Completion migration boundary

A readiness-targeted Epic must not be migrated directly to a completed v5 representation unless an
exact qualifying assessment exists and the derived Assessed Readiness meets or exceeds the authored
target. Otherwise keep the Epic active, remove the intended target through normal reviewed
governance, or remain on the previously pinned Ticket Specification.

`mvp` does not cap readiness. A deliberately bounded MVP may target and establish TRL 9 when the
Product/System Readiness v1 evidence is complete, including successful intended operational use.
`production` does not imply a TRL.

## Compatibility

Ticket Specification v1-v4 are immutable. Migration to v5 does not modify their schemas, profiles,
templates, adapters, or historical tickets. The compatible Repository Standards v11 pairings are
`supported` beginning with immutable Repository Standards release v9.3.0. Adoption remains explicit:
a consumer MUST pin v9.3.0 or a later release that preserves the pairing and qualify compatible v5
writer/validator automation before migrating.
