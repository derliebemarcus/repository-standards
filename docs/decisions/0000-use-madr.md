# Use MADR-compatible Architecture Decision Records

- Status: accepted
- Date: 2026-07-13

## Context

Repository standards require durable decisions to remain understandable after their implementation tickets and pull requests are closed.

## Decision drivers

- decisions must remain versioned with the standards;
- changed decisions must be traceable;
- records must be readable without specialized tooling.

## Considered options

- ticket comments only;
- mutable architecture documentation only;
- MADR-compatible ADR files.

## Decision

Use MADR-compatible ADR files below `docs/decisions/` with stable numeric filenames. Accepted records are superseded rather than rewritten.

## Rationale

ADRs preserve context, alternatives, consequences, and supersession history while remaining plain Markdown.

## Consequences

Durable decisions require an ADR. Routine implementation details remain in tickets and code documentation.

## Risks

The ADR index can drift unless validation checks referenced files.

## References

- `siczb/repository-standards#1`
