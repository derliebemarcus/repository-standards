# Story Point estimation

## Purpose

This reference summarizes the canonical Story Point estimation model introduced by Ticket
Specification v3 and preserved by its released successor specifications. The originating normative
source is `standards/ticket-specification/v3/standard.md`; a consumer's selected Ticket Specification
remains authoritative when it incorporates or evolves that model. This page is explanatory and MUST
NOT override a released standard or machine-readable profile.

## Estimation dimensions

Story Points are a relative, holistic assessment of:

- **effort** — the amount of coherent work required to reach the acceptance criteria;
- **complexity** — the number and difficulty of interacting concepts, components, or constraints;
- **risk** — the likelihood and consequence of implementation, integration, operational, or
  validation failure; and
- **uncertainty** — how much of the solution, integration surface, or validation path is not yet
  fully known.

No single dimension determines the estimate. Story Points are not hours, person-days, calendar
duration, staffing levels, file counts, task counts, or lines of code.

## Canonical anchors

| Story Points | Canonical anchor |
| ---: | --- |
| **1** | Very small, clearly bounded change with a known solution and negligible uncertainty and risk. |
| **2** | Small change with few affected concerns and low integration effort, risk, and uncertainty. |
| **3** | Normal change with multiple coherent steps or moderate integration and manageable complexity, risk, and uncertainty. |
| **5** | Larger coherent change spanning multiple components or layers, or carrying material complexity, risk, or uncertainty. |
| **8** | Large but still responsibly deliverable as one ticket; typically cross-cutting and/or carrying substantial complexity, risk, or uncertainty. |
| **13** | Exceptional estimate indicating work that is normally too large or too uncertain for a single Ready ticket. |

Choose the nearest anchor for the complete ticket outcome, not a mathematical sum of separate
dimensions.

## Interpreting the anchors

A change that touches many files can still be small when the work is repetitive, well understood,
low-risk, and easy to validate. Conversely, a very small code diff can justify a larger estimate when
integration behavior, operational impact, uncertainty, or validation risk is substantial.

The estimate should therefore reflect the complete declared scope, acceptance criteria, integration
surface, validation burden, operational consequences, and unresolved uncertainty.

## Split boundary

Tickets above eight Story Points should normally be split before entering `Status/Ready`.

`Estimate/13` is an exception value. Retaining it requires:

1. documented justification; and
2. explicit consideration of whether the work can be split into independently valuable or
   independently verifiable tickets.

The justification should explain why keeping the work together is clearer or safer than the
available split alternatives.

## Versioning and adoption

These anchors were introduced by Ticket Specification v3. They also apply to later Ticket
Specification versions that normatively incorporate the v3 estimation model, including the published
v4 and v5 successors.

Repositories pinned to Ticket Specification v1 or v2 retain their released estimation semantics.
Existing historical estimates MUST NOT be rewritten solely because a repository adopts a later
Ticket Specification.

Tooling and AI agents MUST resolve the ticket profile selected by the consumer's supported Repository
Standards pairing. For a v3 consumer the machine-readable source is
`profiles/ticket-specification-v3.json`; later consumers use their selected successor profile, such as
`profiles/ticket-specification-v5.json` for declaration v11.
