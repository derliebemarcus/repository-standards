# Ticket-based Development Workflow v8

## Status and normative language

Development Workflow v8 supersedes v7 only for repositories that explicitly adopt version 8. Development Workflow v1 through v7 remain immutable for repositories pinned to those versions.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174.

Development Workflow v8 requires Ticket Specification v4, Repository Documentation v2 and Contract-first Delivery v1. It uses Repository Standards declaration schema v9.

## Incorporated Development Workflow v7 requirements

Except where this document adds Contract-first lifecycle enforcement, every normative requirement of Development Workflow v7 remains in force. This includes all incorporated v6 requirements, pull-request supersession, logical required-gate identity, provider-specific required-check mapping, and `pull_request_target` trust-boundary requirements.

## Contract-first lifecycle enforcement

For a ticket whose `delivery.applicability` is `not-applicable`, the inherited workflow applies unchanged after the applicability rationale has been validated.

For `delivery.applicability=required`, the workflow MUST enforce the Contract-first Delivery v1 graph and Ticket Specification v4 metadata.

### Pre-write validation

Before creating or changing a Contract-first ticket, automation MUST validate:

- the selected delivery model and role;
- applicability and any required rationale;
- consistency between direct blockers and referenced upstream contract work items;
- the syntactic validity of resolved contract artifact references; and
- whether the requested lifecycle state is compatible with the current graph.

A ticket MAY exist before upstream contract artifacts are complete. Before `Status/Ready`, an unresolved upstream reference MAY identify only the governing work item. Such a reference MUST be resolved to an exact artifact revision or digest before the Ready transition can succeed.

### Design-to-Test gate

A required Test Contract MUST NOT enter an implementable state until its governing Design Contract revisions are resolved and the Design Contract work is complete.

Completion of a Test Contract MUST mean qualification of the test contract itself. The gate MUST be able to validate the harness, assertions, fixtures/states, deterministic parameters, provenance, controlled negative case and fail-closed behavior without requiring the future product implementation to be conformant.

A Test Contract that masks the absent implementation using `skip`, `xfail`, implicit baseline acceptance, unbounded/materially over-broad tolerances or an equivalent mechanism MUST fail qualification.

### Implementation Ready gate and freeze

`Status/Ready` is the mandatory freeze boundary for implementation work.

Before an implementation ticket may enter `Status/Ready`, automation MUST establish that:

1. every required Design Contract work item is `Status/Done` and closed when represented as a separate ticket;
2. every required Design Contract reference resolves to an exact artifact revision or digest;
3. every required Test Contract work item is `Status/Done` and closed when represented as a separate ticket;
4. every required Test Contract has passed Test Contract qualification;
5. every required Test Contract reference resolves to an exact artifact revision or digest; and
6. the exact resulting Contract Set is recorded in the implementation ticket metadata.

The transition MUST fail closed when any condition cannot be established.

Once the transition succeeds, the exact Design and Test Contract revisions form the frozen Contract Set for that implementation. Merely editing a mutable ticket body MUST NOT be treated as preserving the same Contract Set unless the immutable artifact identities are unchanged.

### In Progress gate

An implementation MUST NOT enter or remain validly in `Status/In Progress` when its frozen Contract Set is incomplete, unresolved or stale.

Before allowing the transition to `Status/In Progress`, automation MUST revalidate that every frozen contract identity still corresponds to the qualified contract set selected at Ready.

### Contract invalidation

If a frozen Design Contract changes, its dependent Test Contract qualification becomes stale and every downstream implementation/evidence qualification that depends on the old contract set MUST be treated as stale for the new design.

If a frozen Test Contract changes, downstream implementation qualification and evidence MUST be treated as stale for the new test contract.

If the Implementation revision changes, evidence for the previous implementation revision MUST NOT satisfy the Definition of Done for the new revision.

When staleness is detected, automation MUST:

- prevent forward status transitions that rely on stale qualification;
- prevent merge or Done decisions that rely on stale qualification;
- require explicit requalification and a newly frozen Contract Set; and
- preserve historical evidence rather than rewriting it.

Automation SHOULD move a stale Ready/In-Progress ticket to `Status/Blocked`. Where the provider cannot perform that transition atomically, the enforcement gate MUST still fail closed until requalification completes.

### Pull-request gate

A ticket-linked implementation pull request with required applicability MUST be rejected as non-conforming when:

- the ticket has no valid frozen Contract Set;
- a referenced Contract revision is stale or unresolved;
- required upstream contract work has reopened or is otherwise no longer complete;
- the pull request changes the Test Contract, Design Contract or visual baseline that is supposed to qualify the same implementation without representing that as explicit contract evolution; or
- required Contract-first metadata cannot be resolved fail closed.

A pull request MAY contain a legitimate contract revision plus downstream implementation only when the full ordering remains independently verifiable and the resulting new Contract Set is qualified and frozen before implementation qualification. Tooling MUST NOT infer valid ordering merely from final file contents in one commit.

### Definition of Done and evidence gate

A required implementation MUST NOT become `Status/Done` until valid Conformance Evidence exists for:

- the exact frozen Design Contract revisions;
- the exact frozen Test Contract revisions;
- the exact implementation/source revision being completed; and
- where runtime behavior applies, the exact deployed artifact/revision and environment.

Evidence MUST validate against `schemas/contract-first-evidence-v1.schema.json` or an explicitly compatible representation and MUST preserve the Contract-first prohibition on contract mutation during evidence generation.

A failed conformance run MUST NOT be repaired by silently adjusting assertions, baselines or tolerances inside the evidence step. Such changes are Test Contract evolution and trigger requalification.

## Logical quality gates

The Contract-first lifecycle introduces logical engineering outcomes, not provider-specific status strings. At minimum, implementations SHOULD expose logical gates equivalent to:

- `contract-graph` — applicability, role, dependencies and contract identities are coherent;
- `test-contract-qualification` — the Test Contract itself is qualified independently from product conformance; and
- `contract-conformance` — the exact implementation has valid Conformance Evidence against its frozen Contract Set.

These logical identities MUST follow the provider-mapping rules inherited from Development Workflow v7. A Forgejo/Gitea or GitHub adapter MUST map them to concrete producible status/check identities without changing their semantics.

## Branch and dependency automation

`Blocked by` remains the canonical direct dependency relation. Dependency-sync tooling SHOULD derive blockers from separate Design/Test Contract work items and SHOULD expose Contract-first role/applicability data to Workboard or equivalent visualization.

Derived labels MAY improve visualization but MUST NOT become the source of truth for delivery role or applicability.

## AI behavior

An AI agent MUST resolve the pinned Repository Standards declaration and load the matching v8 workflow and v4 ticket adapters before writes.

For required implementation work it MUST perform the following order:

1. resolve/create the Design Contract;
2. resolve/create and qualify the Test Contract;
3. resolve exact artifact revisions and establish `Status/Ready`/freeze;
4. implement;
5. qualify the exact implementation/deployed artifact as applicable;
6. record Conformance Evidence; and
7. only then complete the implementation.

The agent MUST NOT bypass sequencing by marking upstream tickets Done without evidence, by changing a contract in an evidence step, or by selecting `not-applicable` solely to remove a blocker.

## Repository declaration schema v9

Development Workflow v8 uses Repository Standards declaration schema v9. A core v9 declaration selects:

- Ticket Specification v4;
- Development Workflow v8;
- Repository Documentation v2;
- Technology Baseline v1; and
- Contract-first Delivery v1.

A web v9 declaration additionally selects Web Application Baseline v2 and Deployment Environments v1.

The normal Jenkins Multibranch Pipeline filter remains:

```regex
^(main|develop|PR-[0-9]+)$
```

## Compatibility and implementation boundary

Publishing this workflow does not migrate existing consumers. Before a repository adopts Development Workflow v8, all automation that creates/updates ticket metadata, controls Ready/In-Progress/Done transitions, validates pull requests, synchronizes dependencies, or evaluates evidence MUST support v4/v8 Contract-first semantics fail closed.

Repository Standards defines logical semantics, not one specific Jenkins shared-library API. Concrete Maintenance capabilities MAY implement web Live-/Visual-Conformance, but they become a mandatory consumer mechanism only after their separate compatibility/consumer qualification is complete.
