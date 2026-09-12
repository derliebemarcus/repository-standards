# Design System decision contract

Repository Documentation v1 Ruleset **1.2.0** introduces the Design System decision contract for
repositories with a relevant user-facing UI. Earlier declared v1 rulesets are not retroactively
subject to this requirement; migration to `1.2.0` is explicit.

Repository Documentation v2 preserves this Design System decision concept. A v2 consumer therefore
follows its selected v2 contract and ruleset rather than treating the historical v1 Ruleset 1.2.0
migration procedure below as its own migration path.

UI repositories document their architecture decision in `.design-system-consumer.json`. This
contract records the decision and adoption state, not duplicated package versions.

## Use the Design System

```json
{
  "schemaVersion": 1,
  "consumerId": "example-app",
  "designSystem": "siczb/design-system",
  "decision": "use",
  "adoption": "active",
  "integration": "vite-react",
  "packageManifest": "frontend/package.json",
  "documentation": "docs/design-system.md",
  "rationale": "The product UI uses the shared interaction, accessibility and visual language provided by the Design System."
}
```

`active` requires real Design System dependencies in the referenced manifest. `planned` represents
an accepted architecture decision before persistent package adoption. `blocked` additionally requires
`trackingIssue` for the technical prerequisite.

## Do not use the Design System

```json
{
  "schemaVersion": 1,
  "consumerId": "specialized-ui",
  "designSystem": "siczb/design-system",
  "decision": "do-not-use",
  "integration": "specialized-runtime",
  "packageManifest": "package.json",
  "documentation": "docs/design-system.md",
  "rationale": "The UI runs in a constrained runtime whose rendering model is incompatible with the shared browser-oriented component packages."
}
```

A `do-not-use` decision is conformant when it is explicit, documented and consistent with the
package manifest. It must not be treated as a failed or incomplete Design System migration.

## Historical v1 migration to Ruleset 1.2.0

A Repository Documentation v1 UI repository migrates by changing
`documentation.ruleset_version` in `.repository-documentation.yml` to `1.2.0` in the same change
that adds `.design-system-consumer.json` and the referenced human-readable documentation. This keeps
the new normative requirement atomic and prevents a transient non-conformant state.

Non-UI v1 repositories may move to Ruleset `1.2.0` without a Design System consumer declaration. The
`siczb/design-system` provider repository is also exempt from the consumer declaration.

## Authority

Package versions belong to the package manifest and lockfile. `.design-system-consumer.json` must not
duplicate them. The contract schema is `schemas/design-system-consumer-v1.schema.json`; the decision
requirement originates in Repository Documentation v1 Ruleset `1.2.0` and is preserved by Repository
Documentation v2 according to its own normative contract.
