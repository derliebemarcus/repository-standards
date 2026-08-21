# Ticket Specification v3 migration

## Purpose

Ticket Specification v3 adds canonical semantic anchors for the existing Story Point values `1, 2, 3, 5, 8, 13`. It retains Ticket Specification v2 lifecycle semantics and all other incorporated Ticket Specification v1/v2 requirements.

Migration is explicit. Publishing v3 does not change repositories pinned to Ticket Specification v1 or v2.

## What changes

A v3 consumer estimates Story Points using a holistic assessment of:

- effort;
- complexity;
- risk; and
- uncertainty.

The canonical anchors are:

| Story Points | Anchor |
| ---: | --- |
| 1 | Very small, clearly bounded; known solution; negligible uncertainty and risk. |
| 2 | Small; few affected concerns; low integration effort, risk, and uncertainty. |
| 3 | Normal; multiple coherent steps or moderate integration; manageable complexity, risk, and uncertainty. |
| 5 | Larger coherent change; multiple components/layers or material complexity, risk, or uncertainty. |
| 8 | Large but still responsibly deliverable as one ticket; cross-cutting and/or substantial complexity, risk, or uncertainty. |
| 13 | Exceptional; normally too large or too uncertain for one Ready ticket. |

Story Points are not time. Hours, person-days, calendar duration, staffing, file counts, task counts, lines of code, or any other single mechanical proxy must not be used to derive them.

`Estimate/13` remains exceptional. It requires documented justification and explicit consideration of splitting. Tickets above eight Story Points should normally be split before `Status/Ready`.

## What does not change

- The supported Story Point values are unchanged.
- Existing `Estimate/*` labels remain syntactically valid.
- `Status/Done` and the v2 Forgejo lifecycle invariant are unchanged.
- Ticket families, required sections, direct dependency handling, readiness, validation, and impact assessment are unchanged.
- Historical ticket estimates are not automatically rewritten.

## Required contract pairing

Ticket Specification v3 is adopted through Repository Standards declaration schema v5 together with Development Workflow v5:

```yaml
version: 5
standards:
  ticket-specification: v3
  development-workflow: v5
  repository-documentation: v1
```

Web repositories may additionally retain Web Application Baseline v1 and Deployment Environments v1 as the supported paired extension.

Development Workflow v5 preserves Development Workflow v4 behavior and changes only the released version coupling required for Ticket Specification v3 adoption.

## Migration procedure

1. Ensure every ticket-writing automation can resolve and load Ticket Specification v3.
2. Ensure estimation automation consumes `profiles/ticket-specification-v3.json` rather than maintaining private anchors.
3. Ensure branch and pull-request writers support Development Workflow v5 and continue to perform the inherited fail-closed pre-write validation.
4. Change `.repository-standards.yml` to declaration schema v5 using the appropriate released reference declaration.
5. Validate the complete declaration pairing before writing tickets, branches, or pull requests.
6. Apply v3 anchors to new estimates and future legitimate re-estimation decisions.

## Existing tickets

Migration must not become a historical re-estimation exercise. Existing estimates remain unchanged unless a normal material scope, risk, integration, validation, or uncertainty change independently requires re-estimation.

Completed-ticket history and historical evidence must not be invented or rewritten solely because the repository adopts v3.

## Rollback

If a consumer cannot safely use v3/v5, do not partially mix versions. Restore the previous complete supported declaration pairing and its released adapters/profiles. Unsupported pairings must fail closed rather than being coerced.