# Ticket Specification v3

## Status and scope

Ticket Specification v3 is the successor to Ticket Specification v2. It normatively incorporates all requirements of Ticket Specification v2, including all v1 requirements incorporated by v2, unless this document explicitly supersedes them. Ticket Specification v1 and v2 remain immutable and valid for consumers that continue to pin them.

This version adds canonical semantic anchors for Story Point estimation. It does not change the supported estimate values, ticket families, readiness rules, lifecycle contract, relation model, impact model, or completion/reopen semantics.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences of words such as "must", "should", and "may" are non-normative. Normative obligations MUST use the capitalized BCP 14 forms.

## Source of truth

The normative source is this document together with the requirements incorporated from `standards/ticket-specification/v2/standard.md` and, transitively, `standards/ticket-specification/v1/standard.md`.

The complete machine-readable representation is `profiles/ticket-specification-v3.json`, validated for ticket instances by `schemas/ticket-specification-v3.schema.json`. Reference templates and the v3 AI authoring adapter MUST be generated from the v3 machine-readable representation and MUST NOT become separately maintained policy copies.

Consumers MUST pin a released Ticket Specification version. Adoption of v3 MUST be explicit; publishing v3 MUST NOT silently change a consumer that remains pinned to v1 or v2.

## Incorporated Ticket Specification v2 requirements

Except where this document explicitly supersedes estimation guidance, every normative requirement of Ticket Specification v2 remains in force for Ticket Specification v3. This includes the canonical lifecycle pair `state=closed` plus `Status/Done`, reopen semantics, label cardinality, Definition of Ready, ticket families, required description structure, dependency synchronization, validation, impact assessment, and migration evidence rules.

## Estimation model

Story Points remain relative estimates. They MUST represent a holistic assessment of:

- effort;
- complexity;
- risk; and
- uncertainty.

No single dimension MUST determine the estimate by itself. Story Points MUST NOT be derived from or converted to hours, person-days, calendar duration, staffing levels, file counts, task counts, lines of code, or another mechanical proxy.

The supported estimate sequence remains:

- `Estimate/1`;
- `Estimate/2`;
- `Estimate/3`;
- `Estimate/5`;
- `Estimate/8`;
- `Estimate/13`.

An estimate expresses the overall relative size of the ticket compared with other tickets under the same estimation model. The anchors below are semantic reference points, not additive formulas or independent score bands.

## Canonical Story Point anchors

| Story Points | Canonical anchor |
| ---: | --- |
| **1** | Very small, clearly bounded change with a known solution and negligible uncertainty and risk. |
| **2** | Small change with few affected concerns and low integration effort, risk, and uncertainty. |
| **3** | Normal change with multiple coherent steps or moderate integration and manageable complexity, risk, and uncertainty. |
| **5** | Larger coherent change spanning multiple components or layers, or carrying material complexity, risk, or uncertainty. |
| **8** | Large but still responsibly deliverable as one ticket; typically cross-cutting and/or carrying substantial complexity, risk, or uncertainty. |
| **13** | Exceptional estimate indicating work that is normally too large or too uncertain for a single Ready ticket. Retaining it requires documented justification and explicit consideration of splitting. |

Automation and human estimators MUST use these anchors as comparative guidance. They MUST consider the complete ticket scope, acceptance criteria, integration surface, validation burden, operational impact, and unresolved uncertainty when selecting the nearest supported anchor.

A ticket MUST NOT be assigned a larger estimate merely because it touches many files when the change is mechanically repetitive and low-risk. A ticket MUST NOT be assigned a smaller estimate merely because its code diff is small when the work carries high uncertainty, integration complexity, operational risk, or difficult validation.

## Split boundary

The existing v1 split guidance remains in force: a ticket estimated above eight Story Points SHOULD be split before it enters `Status/Ready`.

`Estimate/13` is an explicit exception value, not a routine large-ticket category. Retaining `Estimate/13` MUST include a documented justification and MUST record that splitting was explicitly considered. The justification SHOULD explain why preserving the work as one coherent ticket is safer or clearer than the available split alternatives.

## Machine-readable estimation contract

The v3 machine-readable profile MUST expose:

- the shared estimation dimensions `effort`, `complexity`, `risk`, and `uncertainty`;
- the holistic relative-assessment rule;
- the prohibited mechanical proxies;
- one semantic anchor for each supported Story Point value;
- the split threshold of eight Story Points;
- the exceptional status of `Estimate/13`;
- the documented-justification requirement for `Estimate/13`; and
- the explicit split-consideration requirement for `Estimate/13`.

The v3 ticket schema MUST retain the v2 supported estimate values, Epic prohibition, Ready-leaf estimate requirement, research requirements, and lifecycle state/status invariants.

## AI-assisted estimation and authoring

An AI agent operating on a v3 repository MUST load the released v3 adapter before creating, changing, classifying, estimating, reopening, or closing a ticket.

When selecting or reviewing an estimate, the agent MUST apply the canonical v3 anchors and MUST NOT infer a time conversion. If material scope, risk, integration complexity, validation burden, or uncertainty changes, the ticket MAY require re-estimation before implementation continues.

The agent MUST preserve the existing rules against inventing missing factual content. Estimation uncertainty MUST be represented through the relative estimate and explicit ticket content rather than fabricated implementation facts.

## Compatibility with earlier Ticket Specification versions

Ticket Specification v1 and v2 remain immutable. Their existing estimation rules remain valid for consumers pinned to those versions. A v3 consumer MAY read historical v1/v2 estimates, but MUST NOT retroactively reinterpret or rewrite them solely to conform to the v3 anchors.

The supported Story Point values are unchanged, so existing `Estimate/*` labels remain syntactically compatible. The semantic anchors apply only after explicit v3 adoption.

## Migration from v2

Migration to v3 is a policy adoption, not a historical re-estimation exercise.

A repository adopting v3 MUST:

1. adopt a released Repository Standards declaration and Development Workflow pairing that explicitly supports Ticket Specification v3;
2. update ticket-authoring and estimation automation to load the v3 profile and adapter;
3. apply the v3 anchors to new estimates and to future re-estimation decisions; and
4. preserve existing estimates unless a normal material scope or uncertainty change independently requires re-estimation.

Migration MUST NOT invent retrospective estimates, rewrite completed-ticket history, or convert Story Points to elapsed time.