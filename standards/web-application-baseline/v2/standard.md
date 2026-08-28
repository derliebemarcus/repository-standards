# Web Application Baseline v2

## Status and scope

Web Application Baseline v2 supersedes v1 only for repositories that explicitly adopt v2. It incorporates every normative requirement of Web Application Baseline v1 and adds Contract-first Delivery requirements for user-visible web frontend changes.

The standard remains opt-in through the Repository Standards declaration. Once adopted, its requirements are mandatory for the covered web application.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174.

## Source of truth

The normative source is this document together with `standards/web-application-baseline/v1/standard.md`. The complete machine-readable representation is `profiles/web-application-baseline-v2.json`.

Web Application Baseline v2 requires Contract-first Delivery v1, Ticket Specification v4 and a compatible Development Workflow.

## Incorporated v1 requirements

All Web Application Baseline v1 requirements remain in force, including:

- the canonical static routes `/impressum`, `/datenschutz` and `/barrierefreiheit`;
- global same-context navigation and shared application shell;
- the Design System decision;
- accessibility statement requirements;
- public artifact-provenance presentation by release state; and
- blocking validation.

## UI-impact applicability

A ticket that changes user-visible web UI behavior, presentation, navigation, responsive behavior, interactive state, user-visible copy tied to a UI state, or another externally observable frontend characteristic MUST use:

```yaml
delivery:
  model: contract-first-v1
  applicability: required
```

A repository MAY define narrowly scoped exceptions for generated/vendor content or emergency recovery paths only when the exception is explicit, reviewable and does not weaken user-facing quality gates by default.

A documentation-only correction outside executable UI behavior MAY use `not-applicable` with the Ticket Specification v4 rationale requirement.

## Web Design Contract

For a required UI change, the Design Contract MUST identify the normative design source appropriate to the repository. A UI Design Contract MUST include, as applicable:

- design provider/source and stable project/file/page/frame or equivalent identity;
- the relevant screen or component identity;
- the UI state or states being specified;
- viewport, breakpoint or responsive variant;
- user-visible copy when it is design-normative;
- interaction and navigation expectations;
- relationship to the repository's declared Design System decision; and
- accessibility-relevant semantics or behavior that belong to the design intent.

Penpot is a supported example of a normative design source, not a mandatory provider. A repository MAY use another declared, reproducible source.

An exported image or screenshot baseline derived from Penpot or another design source is a Test Contract artifact. It MUST NOT become an independent normative design truth merely because the visual test consumes it.

## Web Test Contract

The Test Contract MUST be defined and qualified before the implementation enters `Status/Ready`.

For each covered UI state, it MUST define the applicable test dimensions, including:

- route/navigation needed to reach the state;
- deterministic fixture/data/runtime state;
- viewport and responsive conditions;
- browser/runtime identity where material;
- fonts and rendering inputs where visual determinism depends on them;
- selectors or stable semantic anchors owned by the consumer;
- required assertions;
- provenance back to the exact Design Contract revision;
- visual baseline identity and configured tolerance when visual comparison applies; and
- expected failure behavior.

The Test Contract MUST be qualifiable without requiring the not-yet-implemented UI to pass. A controlled negative case MUST demonstrate that a materially relevant mismatch is detected.

Visual baselines MUST use a controlled review lifecycle. Baseline creation or update MUST be distinguishable from conformance execution and MUST NOT occur implicitly in the evidence run.

## Conformance classes

Web UI conformance consists of distinct classes. A repository MUST NOT treat one class as a universal substitute for the others.

### Functional conformance

Functional conformance validates observable behavior such as navigation, state transitions, interaction, content/state relationships and consumer-owned assertions.

### Accessibility conformance

Accessibility conformance validates applicable semantic, keyboard, focus, name/role/value and other accessibility requirements. Automated accessibility checks MUST be combined with any additional test technique needed for the selected contract; visual equality MUST NOT be treated as accessibility evidence.

### Reflow and responsive conformance

Reflow/responsive conformance validates layout adaptation, content availability and interaction usability at required viewport/breakpoint conditions. A screenshot at one viewport MUST NOT substitute for reflow qualification across required responsive states.

### Live-runtime conformance

Where a deployed DEV or equivalent canonical pre-production runtime is part of the delivery model, live-runtime conformance MUST execute against the actually deployed immutable revision/artifact rather than silently starting a different local build.

The evidence MUST fail closed when the expected source/artifact revision cannot be matched to the deployed runtime.

### Visual conformance

When the Design Contract contains normative visual presentation, visual conformance MUST compare deterministic actual rendering with a derived and provenance-bound expected baseline or another repeatable representation of the normative source.

Visual comparison MUST produce sufficient failure evidence to diagnose a mismatch. For image-diff techniques this SHOULD include expected, actual and diff artifacts.

Tolerance MUST be explicit, bounded and justified by rendering determinism. A tolerance MUST NOT be widened merely to accept an implementation that conflicts with the Design Contract.

## Required class selection

For a user-visible UI change, the Test Contract MUST explicitly classify each of the following as `required` or `not-applicable` with rationale:

- functional;
- accessibility;
- reflow-responsive;
- live-runtime; and
- visual.

Functional and accessibility conformance SHOULD normally be required for interactive UI changes. Reflow SHOULD normally be required for responsive web applications. Live-runtime SHOULD normally be required when the repository has a canonical DEV environment. Visual SHOULD normally be required when a normative visual design source exists.

Another domain standard or repository policy MAY strengthen these SHOULD defaults to MUST.

## Evidence

Conformance Evidence for a covered UI change MUST bind:

- exact Design Contract revision(s);
- exact Test Contract revision(s);
- exact implementation/source revision;
- immutable build/artifact identity when available;
- target runtime and deployed revision for live-runtime evidence;
- browser and version when material;
- viewport and device-scale/render parameters where material;
- execution time and result; and
- relevant reports, traces, screenshots and diffs.

The evidence MUST preserve the separation between Test Contract and implementation. Failed evidence MUST NOT mutate the Contract Set, baseline or tolerance in the same qualification step.

## Responsibility boundary

The repository/consumer owns product-specific navigation, fixtures, selectors, copy, state setup and assertions.

Shared automation MAY own generic browser provisioning, deterministic rendering, design-source provenance, image diff, report/artifact handling, immutable revision verification and CI orchestration.

Web Application Baseline v2 is provider-neutral. It MUST NOT require a particular Jenkins shared-library method, Penpot integration implementation or browser-runner API by name.

## Accessibility and WCAG boundary

This standard establishes engineering evidence and does not make a legal-compliance claim. Repositories MUST continue to apply their declared accessibility target and jurisdiction-specific obligations independently.

Visual conformance MUST NOT replace semantic accessibility, keyboard/focus, reflow or other WCAG-relevant validation.

## Consumer activation boundary

A repository MUST NOT activate Web Application Baseline v2 until its selected automation can enforce the required Contract-first lifecycle and selected web conformance classes fail closed.

Concrete shared Live-/Visual-Conformance capabilities SHOULD become the default implementation only after they have demonstrated reproducibility and portability across independent consumers. Until that qualification is complete, this standard defines the target contract without asserting that a particular implementation is already mandatory.
