# Contract-first Delivery reference

## Purpose

Contract-first Delivery v1 makes the sequence from intended behavior to implementation evidence
explicit and machine-checkable:

```text
Design Contract
      ↓
Test Contract + qualification
      ↓
resolved/frozen Contract Set at Ready
      ↓
Implementation
      ↓
deployment where runtime evidence is required
      ↓
Conformance Evidence
      ↓
Done
```

The normative source is `standards/contract-first-delivery/v1/standard.md`. This document explains
the operational model without replacing the standard.

## Work products

### Design Contract

The Design Contract defines the observable behavior or presentation before implementation. Depending
on the domain it can describe UI screens/states, APIs, persistent data, integrations, deployment
behavior, or another externally observable contract.

For web UI work the normative visual source SHOULD remain the declared design source, for example
Penpot. Exported screenshots are derived test artifacts, not independent design truth.

### Test Contract

The Test Contract translates the Design Contract into executable or reproducible assertions,
fixtures/states, rendering parameters, provenance, and failure behavior.

Qualification of the Test Contract answers whether the contract itself is deterministic,
reproducible, capable of detecting controlled non-conformance, and fail-closed. It does **not**
require the future implementation to pass before implementation begins.

### Implementation

Implementation is performed against the Contract Set frozen at `Status/Ready`. A planned
implementation may exist earlier and reference unfinished Design/Test Contract work items. Before
Ready those references must resolve to stable artifact locators plus exact revisions and/or digests.

### Conformance Evidence

Evidence records the result for exact Design Contract, Test Contract, implementation, and—where
runtime behavior applies—deployed artifact revisions. Evidence must not mutate the contracts it
evaluates.

## DEV timing

A DEV runtime is **not** a prerequisite for defining the Design Contract or Test Contract.

For a web application the recommended sequence is:

1. create/resolve the Design Contract;
2. derive and qualify the Test Contract;
3. provision DEV in parallel when needed;
4. freeze exact Contract revisions at `Status/Ready`;
5. implement;
6. deploy the exact implementation revision/artifact to DEV;
7. execute live functional, accessibility/reflow, and visual conformance as applicable;
8. retain revision-bound Evidence;
9. complete the implementation.

A DEV environment therefore SHOULD be reliably deployable by the time implementation starts and
MUST exist before any required conformance class claims evidence against a running application.

A repository MUST NOT invent runtime evidence when no qualifying runtime exists. Non-runtime
unit/contract validation may still run earlier.

## Web conformance classes

The web-conformance model introduced with Web Application Baseline v2 remains in force for later Web
Application Baseline versions that normatively incorporate v2, including v3. The selected Web
Application Baseline is authoritative for any additional or superseding requirements.

| Class | Primary question |
| --- | --- |
| Functional | Does the deployed UI behave and expose state/copy/navigation as contracted? |
| Accessibility | Are semantics, keyboard/focus, WCAG-relevant behavior, and accessibility assertions conformant? |
| Reflow/responsive | Does the UI remain usable and conformant across required viewport/reflow conditions? |
| Live runtime | Is the tested UI the actual deployed revision/artifact under the declared runtime conditions? |
| Visual | Does visible presentation conform to the normative design source within bounded tolerances? |

Visual comparison MUST NOT substitute for accessibility, functional, or reflow validation.

For v3 consumers, localized routing, language negotiation, language switching, rendered language,
and localized page states add the language dimensions required by Web Application Baseline v3.

## Penpot and visual evidence

For Penpot-backed UI work, a Design Contract SHOULD identify at least the relevant
project/file/page/frame or screen, state/variant, viewport, and design-source revision/provenance that
can be resolved by the consumer environment.

A visual Test Contract SHOULD identify deterministic rendering parameters, runtime state/fixture,
navigation, screenshot target, comparison method, and bounded tolerances.

Expected/actual/diff images are evidence artifacts. A baseline image derived from Penpot remains
subordinate to the normative Penpot source and must retain provenance back to it.

## Invalidation

Contract-first Delivery uses downstream invalidation rather than historical rewriting:

- Design Contract change → Test Contract qualification, implementation qualification, and Evidence
  become stale.
- Test Contract change → implementation qualification and Evidence become stale.
- Implementation/deployed revision change → previous Evidence does not qualify the new revision.

The affected work must be requalified. Historical Evidence is retained as point-in-time evidence.

## Provider-neutral gates

Development Workflow v8 defines three logical gate identities:

- `contract-graph`
- `test-contract-qualification`
- `contract-conformance`

Provider integrations map these logical gates to concrete Jenkins/Forgejo/GitHub checks. Repository
Standards does not prescribe a Maintenance implementation API.

## Maintenance integration

Maintenance may provide reusable runners for browser orchestration, deployed-revision verification,
Penpot provenance, deterministic rendering, image diff, and evidence retention. Consumer repositories
remain responsible for product-specific navigation, fixtures/states, selectors, copy, assertions,
and Design/Test Contract mappings.

Declaration generations that select Contract-first Delivery remain fail-closed until the consumer's
actual ticket/lifecycle/CI integration can enforce the selected Contract-first requirements. A newer
Repository Standards release does not activate those provider capabilities implicitly.
