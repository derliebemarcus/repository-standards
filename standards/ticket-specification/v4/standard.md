# Ticket Specification v4

## Status and scope

Ticket Specification v4 is the successor to Ticket Specification v3. It normatively incorporates every requirement of Ticket Specification v3, including the v2 lifecycle and v1 ticket contract, unless this document explicitly adds or supersedes a requirement.

This version adds machine-readable Contract-first Delivery metadata. Ticket families, label categories, Story Point anchors, completion/reopen semantics, relation headings and branch-prefix mappings remain unchanged.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174.

## Source of truth

The normative source is this document together with the requirements incorporated from `standards/ticket-specification/v3/standard.md`. The complete machine-readable representation is `profiles/ticket-specification-v4.json`, validated by `schemas/ticket-specification-v4.schema.json`.

Consumers MUST pin a released version. Adoption of v4 MUST be explicit and MUST use a Repository Standards declaration that also selects Contract-first Delivery v1 and a compatible Development Workflow version.

## Incorporated Ticket Specification v3 requirements

Except where this document adds delivery metadata and readiness constraints, every normative requirement of Ticket Specification v3 remains in force. In particular, v4 preserves:

- the mandatory assignee and Area/Kind/Priority/Status label cardinalities;
- the canonical `state=closed` plus `Status/Done` completion representation;
- the existing ticket families and description sections;
- the canonical `Blocked by` dependency relation;
- the Story Point values and v3 estimation anchors; and
- all branch-prefix mappings.

## Delivery contract metadata

Every v4 ticket MUST carry a machine-readable `delivery` object with:

- `model: contract-first-v1`;
- an explicit `applicability` of `required` or `not-applicable`;
- a `rationale` when applicability is `not-applicable`;
- a delivery `role` when applicability is `required`;
- Design Contract references;
- Test Contract references; and
- Conformance Evidence references where evidence exists.

Allowed delivery roles are:

- `design-contract`;
- `test-contract`;
- `implementation`; and
- `conformance-evidence`.

The role identifies the ticket's primary workflow role. It does not imply that every work product needs a separate ticket. A small implementation ticket MAY contain Design and Test Contract artifacts produced earlier within the same work item when their independent revisions and qualification order remain verifiable.

## Canonical ticket-body representation

Forgejo has no native structured field for this contract. When ticket metadata is serialized in a Forgejo description, v4 MUST use a `## Delivery contract` section containing exactly one fenced YAML document whose root key is `delivery`.

Example for a Ready implementation:

```yaml
delivery:
  model: contract-first-v1
  applicability: required
  rationale: null
  role: implementation
  design_contracts:
    - work_item: "#42"
      artifact:
        type: penpot
        locator: "project/file/page/frame:C214"
        revision: "design-revision"
  test_contracts:
    - work_item: "#53"
      artifact:
        type: git
        locator: "tests/contracts/C214.yml"
        revision: "commit-sha"
  evidence: []
```

Example for a planned implementation whose blockers exist but whose artifacts are not yet resolved:

```yaml
delivery:
  model: contract-first-v1
  applicability: required
  rationale: null
  role: implementation
  design_contracts:
    - work_item: "#42"
      artifact: null
  test_contracts:
    - work_item: "#53"
      artifact: null
  evidence: []
```

This unresolved form is valid only before the applicable lifecycle gate requires exact artifact identity. It MUST NOT be used to enter `Status/Ready` or to produce Conformance Evidence.

Example for a non-applicable ticket:

```yaml
delivery:
  model: contract-first-v1
  applicability: not-applicable
  rationale: "Documentation-only correction; no executable or externally observable behavior changes."
  role: null
  design_contracts: []
  test_contracts: []
  evidence: []
```

Automation MUST treat the parsed object, not labels inferred from it, as the source of truth. Labels MAY be derived for visualization but MUST NOT replace this contract.

## Applicability

Applicability semantics are defined by Contract-first Delivery v1 and MAY be strengthened by another selected domain standard.

For `not-applicable`:

- `rationale` MUST be non-empty;
- `role` MUST be null; and
- contract/evidence arrays MUST be empty.

For `required`:

- `role` MUST be one allowed delivery role; and
- `rationale` MAY be null or contain additional explanation.

An agent MUST NOT choose `not-applicable` solely to avoid contract work, failing tests or a lifecycle gate.

## Contract references

Before `Status/Ready`, a Design or Test Contract dependency MAY be represented as an unresolved reference containing:

- a non-empty `work_item`; and
- `artifact: null`.

An unresolved reference MUST NOT invent or predict a revision/digest. It exists only to express planned graph structure while upstream contract work is incomplete.

A resolved Design or Test Contract reference MUST contain an `artifact` with:

- a non-empty `type`;
- a stable non-empty `locator`; and
- at least one of `revision` or `digest`.

For a resolved reference, `work_item` MAY be null when no separate work item exists. If a governing ticket exists, the reference SHOULD identify it.

A mutable issue number or issue body alone MUST NOT satisfy the immutable artifact identity requirement at a freeze or evidence boundary.

## Role-specific dependency semantics

A `test-contract` ticket with `required` applicability MUST identify the Design Contract revision or revisions from which it derives before the Test Contract itself is Ready or complete.

An `implementation` ticket with `required` applicability MAY initially identify upstream contract work by unresolved work-item reference. It MUST identify every governing Design Contract and Test Contract artifact revision before it enters `Status/Ready`.

A `conformance-evidence` ticket with `required` applicability MUST identify resolved Design and Test Contract revisions being evaluated before it becomes Ready or complete. Evidence itself MAY be a CI artifact rather than a dedicated ticket; the delivery role exists for work where evidence production or review is intentionally tracked as a separate item.

`Blocked by` remains the canonical work-item dependency relation. Contract references do not replace ticket dependencies where separate upstream work items exist. Automation SHOULD reconcile the Contract-first graph with direct ticket dependencies so an implementation cannot be Ready while a required upstream contract ticket remains incomplete.

## Definition of Ready interaction

The inherited Definition of Ready is strengthened for `delivery.applicability=required`.

An implementation ticket MUST NOT enter `Status/Ready` until:

- required Design Contract work items are complete;
- required Design Contract artifact revisions are resolved;
- required Test Contract work items are complete;
- required Test Contracts are qualified according to Contract-first Delivery v1; and
- all references required to form the frozen Contract Set are present and exact.

The Development Workflow defines the transition gate and freeze mechanics. Ticket Specification v4 defines the canonical metadata consumed by that gate.

## Completion and evidence

`Status/Done` retains its v3 meaning. For an implementation with `required` applicability, applicable Definition-of-Done requirements additionally require valid Conformance Evidence bound to the frozen Contract Set and exact implementation revision.

Evidence references in a ticket MUST identify a reproducible evidence artifact using the resolved artifact-reference identity rules. Closing a ticket MUST NOT cause automation to invent evidence or rewrite historical contract references.

## AI-assisted authoring

An AI agent operating on a v4 repository MUST load the released v4 adapter before creating, changing, classifying, estimating, reopening or closing a ticket.

The agent MUST make applicability explicit. For `required` work, it MUST set the primary delivery role, preserve exact contract references once resolved, and respect the Contract-first ordering. It MAY create implementation work early with unresolved upstream work-item references, but it MUST NOT move that implementation to Ready or In Progress while upstream contract work is incomplete, unresolved or stale.

When a frozen Contract Set changes, the agent MUST treat the implementation as requiring requalification rather than editing references as if the old evidence remained valid.

## Compatibility and migration

Ticket Specification v1 through v3 remain immutable for pinned consumers. v4 is a new adoption boundary because it adds mandatory ticket metadata and strengthens readiness for required Contract-first work.

Migration MUST NOT fabricate delivery history for completed legacy tickets. Open tickets migrated to v4 MUST receive an explicit applicability decision before their next lifecycle transition. Tickets already in implementation MAY require deterministic migration handling rather than retrospective claims that upstream contracts existed when they did not.
