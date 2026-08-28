# Contract-first Delivery v1

## Status and scope

Contract-first Delivery v1 defines a provider-neutral delivery contract for changes whose correctness depends on an explicit contract before implementation. It standardizes four ordered work products:

1. Design Contract;
2. Test Contract;
3. Implementation; and
4. Conformance Evidence.

The terms are domain-neutral. A Design Contract MAY be a UI design, API description, persistent-data schema, protocol/interface contract, architecture decision or deployment/promotion contract. A Test Contract is the executable or otherwise reproducible qualification contract derived from the Design Contract. Conformance Evidence records execution of fixed contract revisions against an exact implementation revision and, where applicable, an exact deployed artifact.

This standard does not require one Forgejo ticket per work product. Multiple work products MAY be produced within one ticket when ordering, qualification and immutable revision identity remain independently verifiable.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences of words such as "must", "should" and "may" are non-normative.

## Source of truth

The normative source is this document. The complete machine-readable representation is `profiles/contract-first-delivery-v1.json`. Conformance evidence is represented by `schemas/contract-first-evidence-v1.schema.json`.

Consumers MUST pin a released version. Publication MUST NOT silently reinterpret consumers pinned to earlier Repository Standards declarations.

## Applicability

Every ticket governed by a Repository Standards declaration that selects this standard MUST make an explicit applicability decision:

- `required`; or
- `not-applicable`.

`not-applicable` MUST include a non-empty rationale explaining why contract-first ordering adds no meaningful correctness or auditability value.

Changes to externally observable behavior SHOULD default to `required`. This includes, as applicable:

- user interfaces and user journeys;
- public or consumer-facing APIs;
- persistent data models and migrations;
- integration interfaces and protocols;
- deployment, environment and promotion semantics; and
- other externally observable behavior whose expected outcome can be described independently of its implementation.

A domain-specific standard MAY strengthen this default to a MUST and MAY define narrowly scoped exceptions.

## Work-product model

### Design Contract

A Design Contract defines the normative intended behavior, structure or interface before implementation. It MUST identify a reproducible normative source and MUST be independently reviewable from the implementation it governs.

Examples include:

- Penpot frames plus the declared Design System decision for a UI;
- an OpenAPI description for a REST interface;
- a database schema and migration contract;
- an interface or protocol specification for an integration;
- an ADR plus architecture contract for a material architecture decision; or
- an environment and immutable-promotion contract for deployment behavior.

A derived rendering, screenshot or generated fixture MUST NOT silently replace the normative Design Contract from which it was derived.

### Test Contract

A Test Contract translates the Design Contract into assertions and reproducible qualification conditions before implementation begins. It MUST be qualified independently from whether the not-yet-implemented product currently conforms.

Before an implementation may become Ready, every required Test Contract MUST establish, as applicable:

- the assertions and pass/fail semantics;
- fixtures, data and runtime states;
- execution environment and deterministic parameters such as viewport, browser, fonts or protocol versions;
- provenance back to the Design Contract revision;
- an executable or otherwise reproducible harness;
- at least one controlled negative case demonstrating that a relevant contract violation is detected; and
- fail-closed behavior when required inputs, provenance or assertions are missing.

A required Test Contract MUST NOT use `skip`, `xfail`, implicit baseline acceptance, unbounded or materially over-broad tolerances, or an equivalent masking mechanism to hide missing implementation or contract violations.

Test Contract qualification MUST NOT require the future implementation to pass. A repository MAY execute the Test Contract against controlled fixtures, known-bad examples or a contract harness so that the contract itself can be qualified while the product remains unimplemented.

### Implementation

Implementation begins only from a qualified and frozen Contract Set. The implementation MUST NOT redefine the expected outcome merely because the current code differs from the Design or Test Contract.

An implementation work item governed by `required` applicability MUST reference the exact Design Contract and Test Contract artifacts it implements before it enters `Status/Ready`. The frozen references MUST be immutable or reproducibly revision-bound.

### Conformance Evidence

Conformance Evidence is point-in-time verification. It MUST execute or evaluate fixed Design and Test Contract revisions against an exact Implementation revision. Where runtime behavior is part of the contract, the evidence MUST additionally identify the exact deployed artifact or deployed revision and target environment.

Evidence generation MUST NOT modify, accept, regenerate as authoritative, widen or otherwise change the Design Contract, Test Contract, assertions, baselines or tolerances merely to make the evaluated implementation conform.

If a contract needs to change, the contract change MUST occur as a new contract revision before evidence is regenerated. The implementation MUST then be requalified against that new revision.

Conformance Evidence SHOULD be retained as a Verification / Evidence artifact under Repository Documentation when that standard is adopted. It MAY be retained in CI or another artifact system rather than committed to Git when provenance and retention remain auditable.

## Work-item and artifact identity

A work item and its contract artifact are distinct concepts. Mutable ticket text MUST NOT be treated as the sole immutable identity of a Design or Test Contract.

A planning-time dependency reference MAY be unresolved before the implementation reaches `Status/Ready`. An unresolved reference MUST identify a governing work item and MUST NOT claim an artifact revision or digest that does not yet exist. This permits the complete delivery graph to be planned before upstream contract artifacts are finished.

A resolved contract reference MUST identify:

- the contract artifact type;
- a stable locator for the artifact;
- an immutable or reproducible revision and/or integrity digest; and
- the governing work item where one exists.

Every unresolved reference required by an implementation MUST become a resolved contract reference before the implementation may enter `Status/Ready`. Conformance Evidence MUST use resolved references only.

A contract artifact MAY be repository content, a versioned external design source, a generated-but-integrity-bound package, or another reproducible source. The resolved reference MUST be sufficient to determine later exactly which contract revision governed the implementation.

## Contract graph and ordering

For `required` applicability, the canonical dependency order is:

```text
Design Contract
      |
      v
Test Contract
      |
      v
Implementation
      |
      v
Conformance Evidence
```

A Test Contract MUST NOT be considered complete until every Design Contract revision it derives from is identified and qualified.

An Implementation MUST NOT enter `Status/Ready` until every required Design and Test Contract work item is complete, every required Test Contract is qualified, and every required contract artifact reference resolves to an exact revision.

Conformance Evidence MUST NOT satisfy the Definition of Done for an implementation unless it references the exact frozen Contract Set and the exact implementation revision being completed.

## Ready freeze

`Status/Ready` is the contract-freeze boundary for an implementation.

When an implementation enters `Status/Ready`, its referenced Design and Test Contract revisions form the frozen Contract Set. Automation MUST record or validate those exact revision-bound references before allowing the transition.

`Status/In Progress` MUST NOT be reachable while the required Contract Set is incomplete, unresolved or stale.

The freeze does not prohibit legitimate contract evolution. It prohibits silently changing the expected contract underneath an implementation that was declared Ready.

## Invalidation and requalification

A change to a frozen upstream contract invalidates downstream qualification:

```text
Design Contract changed
        |
        v
Test Contract review/qualification stale
        |
        v
Implementation qualification stale
        |
        v
Conformance Evidence invalid for the new contract
```

A Test Contract change invalidates implementation qualification and prior evidence for the changed contract set. An Implementation change invalidates evidence for the previous implementation revision.

Automation MUST fail closed when a Ready or In-Progress implementation references a contract revision that is no longer the qualified revision intended for that work. It MUST prevent forward lifecycle transitions and merge/Done decisions that rely on stale qualification. It SHOULD move the affected work item to `Status/Blocked` or an equivalent non-implementable state until the new Contract Set is explicitly qualified and frozen.

Requalification MUST create or select explicit new revisions; it MUST NOT overwrite historical evidence so that old and new contract sets become indistinguishable.

## Evidence provenance

Conformance Evidence MUST identify, as applicable:

- consumer or repository;
- ticket and pull request where applicable;
- every Design Contract artifact locator and revision/digest;
- every Test Contract artifact locator and revision/digest;
- source/Implementation revision;
- build or immutable artifact identity;
- runtime environment and deployed revision where runtime qualification applies;
- execution method and runner/tool identity;
- deterministic execution parameters required to reproduce the result;
- execution time;
- result;
- result artifacts such as reports, traces, screenshots or diffs; and
- limitations or validity boundaries.

Evidence MUST be invalidated for a different implementation revision, a different frozen Contract Set, or a materially different runtime target unless the evidence contract explicitly proves those dimensions equivalent.

## Validation and enforcement

A conforming implementation SHOULD enforce this lifecycle at multiple boundaries:

1. ticket authoring and applicability classification;
2. contract-graph validation;
3. lifecycle transition validation for `Status/Ready` and `Status/In Progress`;
4. branch/pull-request validation for implementation work; and
5. Definition-of-Done/evidence validation.

The normative contract is provider-neutral. Jenkins, Forgejo, Workboard, Maintenance or another tool MAY implement the gates, but a repository MUST NOT depend on a provider-specific function name to interpret this standard.

## AI-assisted delivery

An AI agent operating on a repository that adopts this standard MUST resolve the repository's pinned contract before making lifecycle, implementation or evidence writes.

For `required` applicability, the agent MUST:

1. create or identify the Design Contract and, before implementation becomes Ready, resolve its exact artifact revision;
2. create or identify and qualify the Test Contract against that Design Contract and resolve its exact artifact revision;
3. freeze the exact Contract Set at `Status/Ready` before implementation begins;
4. implement without weakening the frozen contract;
5. qualify the exact implementation and deployed artifact where applicable; and
6. record Conformance Evidence bound to the exact revisions.

The agent MUST NOT repair a failed conformance result by silently changing the governing contract, assertion, baseline or tolerance. Such a change is contract evolution and requires a new revision plus downstream requalification.

## Implementation and rollout boundary

Repository Standards defines the portable contract. Consumer automation owns enforcement. A repository MUST NOT activate a declaration containing Contract-first Delivery v1 until its ticket/lifecycle/CI integrations can enforce the applicable transition and evidence rules fail closed.

A domain-specific technical capability MAY become a required implementation mechanism only after its compatibility and reproducibility have been separately qualified. Publication of this standard alone does not mandate one specific browser runner, design provider, CI platform or artifact store.
