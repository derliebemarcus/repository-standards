# Design System decision contract

Repository Documentation Ruleset **1.2.0** introduces the Design System decision contract for repositories with a relevant user-facing UI. Earlier declared `1.x` rulesets are not retroactively subject to this requirement; migration to `1.2.0` is explicit.

UI repositories document their architecture decision in `.design-system-consumer.json`. This contract records the decision and adoption state, not duplicated package versions.

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

`active` requires real Design System dependencies in the referenced manifest. `planned` represents an accepted architecture decision before persistent package adoption. `blocked` additionally requires `trackingIssue` for the technical prerequisite.

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

A `do-not-use` decision is conformant when it is explicit, documented and consistent with the package manifest. It must not be treated as a failed or incomplete Design System migration.

## Migration to ruleset 1.2.0

A UI repository migrates by changing `documentation.ruleset_version` in `.repository-documentation.yml` to `1.2.0` in the same change that adds `.design-system-consumer.json` and the referenced human-readable documentation. This keeps the new normative requirement atomic and prevents a transient non-conformant state.

Non-UI repositories may move to ruleset `1.2.0` without a Design System consumer declaration. The `siczb/design-system` provider repository is also exempt from the consumer declaration.

## Authority

Package versions belong to the package manifest and lockfile. `.design-system-consumer.json` must not duplicate them. The contract schema is `schemas/design-system-consumer-v1.schema.json`; the normative requirement is part of Repository Documentation Standard v1 from ruleset `1.2.0` onward.
