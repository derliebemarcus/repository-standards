# Product/System Readiness v1

## Status and scope

Product/System Readiness v1 defines a provider-neutral, evidence-based readiness model for a concrete software product or operated system. It adapts the NASA Technology Readiness Level (TRL) scale 1 through 9 to software products and operated systems while preserving the essential progression from principles and concepts through proof, integration, qualification, and successful operational use.

This standard defines normative semantics only. Executable schemas, evaluators, Repository Standards declaration integration, Ticket Specification fields, and provider-specific CI or deployment implementation are outside this versioned Design Contract and belong to follow-up contracts.

The TRL scale is ordinal, not metric. A consumer MAY compare ordered levels, for example `TRL 8 >= TRL 7`, but MUST NOT add, average, interpolate, or interpret a difference between levels as a quantity of effort, time, risk, cost, or remaining work.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174. Lowercase occurrences of words such as "must", "should", and "may" are non-normative.

## Source of truth and contract identity

The normative source for Product/System Readiness v1 is this document:

`standards/product-system-readiness/v1/standard.md`

A qualification, downstream Test Contract, or implementation that claims conformance to this Design Contract MUST bind this artifact to an immutable or reproducible revision. A mutable branch name or ticket description alone MUST NOT be the frozen Design Contract identity.

No machine-readable Product/System Readiness schema is normative in v1 at the publication of this Design Contract. A later Test Contract MAY add schemas and executable fixtures only when they preserve the semantics defined here.

Consumers MUST adopt Product/System Readiness explicitly through a subsequently released compatible Repository Standards contract. The existence of this document MUST NOT silently reinterpret an existing repository or a consumer pinned to an earlier released declaration.

## NASA alignment

This standard is aligned with the nine-level NASA Technology Readiness model and with the software-specific guidance and success criteria in NASA NPR 7123.1D Appendix E. It adapts mission/flight terminology to general software products and operated systems; NASA documents remain external reference material and do not replace this standard's normative software criteria.

Primary references verified for this Design Contract are:

- NASA, *Technology Readiness Levels*: <https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/>
- NASA NPR 7123.1D, Appendix E, *Technology Readiness Levels*: <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_&page_name=AppendixE>

Where a NASA source and this adaptation use different domain terminology, a Product/System Readiness assessment MUST apply this standard to the software subject while preserving the ordered intent of the NASA scale.

## Core terminology

### Readiness Subject

A **Readiness Subject** is the concrete entity whose technical readiness is being assessed. Product/System Readiness v1 initially permits exactly these subject kinds:

- `product`: a bounded software product delivered for use; and
- `system`: a bounded software-intensive or infrastructure system that is operated as a system.

A repository is not automatically a Readiness Subject. One repository MAY contain zero, one, or multiple Readiness Subjects. One Readiness Subject MAY also depend on content from multiple repositories.

Each applicable subject MUST have a stable **Subject Identity** that:

- unambiguously distinguishes it from every other subject in the assessment domain;
- remains stable across ordinary source revisions, releases, and deployments;
- is not merely a mutable branch, environment URL, artifact tag, or repository profile; and
- permits historical assessments to remain attributable after later revisions exist.

When a repository contains multiple products or systems, each subject MUST be assessed independently. Automation MUST NOT synthesize one repository-wide TRL by taking a minimum, maximum, average, or other aggregation unless a future separately governed standard explicitly defines a distinct aggregate subject.

Libraries, standards, design systems, shared tooling, frameworks, and similar repositories are not automatically `product` or `system` subjects. They MAY be `not-applicable`, or they MAY identify a distinct product/system subject when one genuinely exists. An infrastructure repository MAY identify a `system` subject when it represents a bounded system that is actually operated.

### Applicability

Applicability is an authored governance decision, not a consequence of repository profile, documentation profile, programming language, deployment topology, or the existence of a web URL.

An adoption MUST state whether Product/System Readiness is:

- `required`; or
- `not-applicable`.

`not-applicable` MUST include a non-empty rationale. A repository profile such as `application`, `library`, or `infrastructure` MUST NOT by itself determine applicability.

A consumer MUST NOT use `not-applicable` merely because evidence is missing or because the current readiness would be lower than a target.

### Product Stage

A **Product Stage** describes scope or lifecycle positioning, for example `concept`, `prototype`, `mvp`, `beta`, or `production`. Product Stage and TRL are orthogonal dimensions.

A Product Stage MUST NOT be translated mechanically to a TRL, and a TRL MUST NOT be used to infer Product Stage. In particular:

- `mvp` MUST NOT cap readiness;
- `production` MUST NOT imply TRL 8 or TRL 9; and
- a deliberately limited MVP MAY establish TRL 9 for its defined scope when every cumulative criterion through TRL 9 is satisfied.

### Target

A **Target** is authored intent. It MAY express:

- a long-term Product/System Target; or
- an Increment Target for a concrete Product-/Release-Epic or equivalent bounded increment.

A Target MUST be one TRL from 1 through 9. A Target is not evidence and MUST NOT be treated as Candidate, Assessed, or Established readiness.

A long-term Product/System Target MUST NOT by itself block an intermediate release whose explicit Increment Target is lower. When a Product-/Release-Epic declares an Increment Target as an exit target, successful completion MUST establish an assessment meeting or exceeding that target, or MUST record an explicit exception through the applicable governance mechanism. Product Stage MUST NOT generate that target implicitly.

### Candidate

**Candidate Readiness** is the highest level an evaluator calculates as potentially satisfiable from the evidence currently presented before final qualification decisions are applied. Candidate Readiness is derived and MUST NOT be an authoritative authored field.

Candidate Readiness MAY be useful for diagnostics, but it MUST NOT satisfy a release, lifecycle, or governance gate that requires Assessed or Established readiness.

### Assessed

**Assessed Readiness** is the qualified result for one exact assessment context: Subject Identity, relevant source revision, artifact identity where applicable, contract set, qualification context, and evidence set.

Assessed Readiness MUST be derived from evidence. A consumer MUST NOT author an authoritative current TRL directly.

### Established

**Established Readiness** is a historical readiness state created when a qualified assessment establishes a level for a specific Subject/revision/artifact/context and the establishment evidence is retained. Established Readiness is derived historical state, not a mutable author-entered current field.

A later revision MUST NOT erase or rewrite the fact that an earlier revision established a level. Whether a later revision preserves that level is a separate evidence-based decision.

### Unassessed

`unassessed` means that no defensible current readiness result has been established for the applicable assessment context. It MUST NOT be treated as TRL 0 and MUST NOT extend the NASA scale. The TRL scale remains exactly 1 through 9.

A missing, incomplete, stale, mismatched, or unknown evidence set MAY result in `unassessed` or in a lower evidence-supported TRL. Automation MUST NOT substitute TRL 1 merely because the current state is unknown.

## Authored and derived information

A conforming implementation MUST preserve the following ownership boundary:

| Information | Normative source type |
| --- | --- |
| applicability | authored/declarative |
| readiness subject kind | authored/declarative |
| subject identity | authored/declarative |
| long-term target | authored/declarative |
| increment target | authored/declarative |
| product stage, when used | authored/declarative |
| candidate TRL | derived |
| assessed TRL | evidence-derived |
| established TRL | evidence-derived historical state |
| preservation result | evidence-derived |
| requalification requirement/result | evidence/change-impact-derived |

An authored declaration MAY claim intended scope, target, context, or equivalence for evaluation. Such a claim MUST NOT become sufficient evidence merely because it is present in a declaration.

## Cumulative and fail-closed assessment rule

TRL exit criteria are cumulative.

To assess or establish TRL `N`, every mandatory criterion for TRL 1 through `N` MUST be satisfied by valid evidence for the applicable subject and assessment context. A higher-level artifact or test MAY satisfy a lower-level criterion only when its provenance and content explicitly demonstrate that criterion; satisfaction MUST NOT be inferred solely from the existence of higher-level evidence.

The following rules are mandatory:

```text
missing evidence != pass
unknown != satisfied
claim != evidence
runtime environment name != readiness evidence
deployment != operational proof
PROD != TRL 9
```

When a mandatory criterion cannot be proven, evaluation MUST fail closed for that criterion and for every higher level whose cumulative establishment depends on it. The result MAY still be a lower TRL when every criterion through that lower level is satisfied.

## Evidence classes

Evidence MAY come from different tools and stores, but the assessment MUST be able to classify evidence by the capability it proves. Product/System Readiness v1 recognizes at least these conceptual evidence classes:

- research and principle evidence;
- concept, architecture, requirement, and feasibility evidence;
- proof-of-concept and analytical evidence;
- integration and controlled-test evidence;
- relevant/representative-environment evidence;
- realistic-problem and prototype-demonstration evidence;
- operationally relevant demonstration evidence;
- final-system verification and qualification evidence;
- immutable artifact/release and deployment evidence where applicable;
- security, accessibility, operations, and documentation qualification evidence where independently applicable; and
- successful operational-use evidence.

Evidence class names are conceptual in this Design Contract. The executable representation belongs to the downstream Test Contract.

## TRL 1 through 9

### TRL 1 - principles and problem basis observed

**Purpose:** establish that the subject rests on understood principles relevant to a defined problem rather than on an unsupported implementation idea.

**Software interpretation:** the problem/domain basis, relevant technical or scientific principles, and assumptions underlying the prospective software capability are understood and reviewable.

**Exit criteria:**

- **R1.1** The problem, need, or domain phenomenon relevant to the Readiness Subject MUST be explicitly described.
- **R1.2** The technical, scientific, mathematical, operational, or software principles on which the proposed capability depends MUST be identified and supported by traceable research, analysis, observation, or established engineering knowledge.
- **R1.3** Material assumptions, unknowns, and limitations at this level MUST be recorded so that later feasibility claims can be tested against them.
- **R1.4** The evidence supporting R1.1 through R1.3 MUST be independently reviewable and attributable to a source or analysis; an unsupported assertion MUST NOT satisfy TRL 1.

**Required evidence classes:** research/principle evidence and reviewable problem/assumption documentation.

### TRL 2 - product/system concept and application formulated

**Purpose:** turn principles into a coherent proposed application or system concept.

**Software interpretation:** intended users/actors or system consumers, scope, application, candidate architecture/algorithmic approach, and critical feasibility assumptions are formulated, but critical functionality is not yet proven.

**Exit criteria:**

- **R2.1** The intended application, users/actors or system consumers, scope boundaries, and expected value or system outcome MUST be defined.
- **R2.2** A candidate product/system concept MUST identify the major software responsibilities, architecture or algorithmic approach, and interfaces needed to realize the intended application at a level sufficient for feasibility reasoning.
- **R2.3** Critical functions, characteristics, dependencies, and assumptions whose failure would invalidate the concept MUST be identified.
- **R2.4** Feasibility and expected benefit MUST be supported by documented analysis, modelling, synthetic exploration, or equivalent reviewable evidence; the concept MUST NOT rely only on aspiration.

**Required evidence classes:** concept/architecture/requirement evidence and analytical or synthetic feasibility evidence.

### TRL 3 - critical functionality proven in proof of concept

**Purpose:** prove the critical technical idea before claiming an integrated product/system.

**Software interpretation:** critical functions or characteristics are demonstrated analytically and experimentally in a limited, not-yet-integrated proof of concept.

**Exit criteria:**

- **R3.1** Each critical function or characteristic selected for proof MUST have measurable success conditions derived from the concept and identified risks.
- **R3.2** Analytical expectations or predictions for the proof MUST be recorded before the result is interpreted.
- **R3.3** Executable proof-of-concept software, a representative executable model, or an equivalent experimental implementation MUST exercise the selected critical functionality.
- **R3.4** Controlled experimental results MUST meet the declared success conditions and MUST be traceable to the proof implementation and inputs.
- **R3.5** Missing integration, scale, environment fidelity, and other limitations MUST be recorded. A non-integrated proof MUST NOT be represented as an integrated system demonstration.

**Required evidence classes:** proof-of-concept, analytical, controlled-test, and limitation evidence.

### TRL 4 - critical components integrated and validated in a controlled context

**Purpose:** demonstrate that the critical software components and interfaces work together.

**Software interpretation:** functionality-critical components are integrated, interfaces/interoperability are exercised, and the integrated subset is validated in a controlled test context.

**Exit criteria:**

- **R4.1** Functionality-critical components required for the assessed concept MUST be integrated sufficiently to exercise their interactions.
- **R4.2** Critical interfaces, protocols, data exchanges, and interoperability behavior MUST be validated using controlled and reproducible tests.
- **R4.3** Characteristics of the later relevant/representative environment that can materially affect behavior MUST be identified, and expected behavior or performance in those characteristics MUST be predicted or bounded.
- **R4.4** Test results MUST demonstrate agreement with the declared functional and technical expectations for the integrated subset.
- **R4.5** The architecture and interface description MUST be sufficiently current to trace the tested components and interactions to the product/system concept.

**Required evidence classes:** architecture/interface evidence, integration tests, controlled validation, and environment/performance prediction evidence.

### TRL 5 - integrated system validated in a relevant environment

**Purpose:** show that an end-to-end integrated system behaves as expected under conditions materially representative of intended use.

**Software interpretation:** essential end-to-end elements are implemented and interfaced with real surrounding systems or qualified equivalents, and are validated in a relevant environment whose fidelity is explicitly characterized.

**Exit criteria:**

- **R5.1** The essential end-to-end path of the subject MUST be integrated across the software elements and external dependencies necessary to demonstrate the intended behavior.
- **R5.2** External systems, hardware, data, services, or integrations used for validation MUST be actual dependencies or documented qualified equivalents whose relevant behavioral constraints are identified.
- **R5.3** The Relevant Environment MUST be defined by behavioral characteristics that can affect correctness, performance, reliability, security-relevant behavior, or operability. An environment name alone MUST NOT satisfy this criterion.
- **R5.4** End-to-end tests in that environment MUST satisfy declared functional and applicable non-functional expectations for the tested scope.
- **R5.5** Remaining fidelity gaps, scaling assumptions, and expected differences from the intended operational environment MUST be documented and MUST NOT invalidate the demonstrated result.

**Required evidence classes:** end-to-end integration, relevant-environment characterization, representative dependency/data evidence, test results, and fidelity-gap evidence.

### TRL 6 - high-fidelity prototype demonstrated on realistic problems

**Purpose:** demonstrate engineering feasibility at realistic scale and problem complexity.

**Software interpretation:** a high-fidelity system prototype exercises the critical functionality on realistic, production-scale or otherwise full-scale representative problems and is sufficiently integrated with its surrounding ecosystem to demonstrate engineering feasibility.

**Exit criteria:**

- **R6.1** A high-fidelity prototype MUST implement every critical function needed to resolve the material technical feasibility questions for the defined scope.
- **R6.2** Demonstration inputs, workloads, data volumes, concurrency, topology, or problem sizes MUST be realistic for the material engineering constraints being qualified.
- **R6.3** The prototype MUST be integrated with actual surrounding systems or qualified equivalents to the degree necessary to demonstrate end-to-end engineering feasibility.
- **R6.4** Material scaling, performance, resource, failure, recovery, and integration constraints identified for the intended use MUST be exercised or otherwise explicitly qualified.
- **R6.5** Results MUST demonstrate engineering feasibility against declared expectations and MUST identify residual gaps between the prototype and the intended operational system.

**Required evidence classes:** high-fidelity prototype evidence, realistic workload/problem evidence, integration evidence, performance/failure/recovery evidence, and documented results.

### TRL 7 - system prototype demonstrated under operationally relevant conditions

**Purpose:** demonstrate a nearly complete prototype under conditions representative of actual operation.

**Software interpretation:** the system prototype contains the key functionality for the defined scope, is integrated with operationally relevant surrounding systems, and is demonstrated through representative operational scenarios.

**Exit criteria:**

- **R7.1** The system prototype MUST contain all key functionality required to demonstrate the defined scope as a coherent system rather than only isolated critical functions.
- **R7.2** The demonstration context MUST reproduce or explicitly qualify the material operational constraints of the intended environment, including applicable hardware, runtime, infrastructure, database, integration, security-configuration, data, and workload behavior.
- **R7.3** Representative operational scenarios MUST include normal operation and material failure/recovery or degraded-mode scenarios applicable to the subject.
- **R7.4** Demonstration results MUST satisfy declared operationally relevant success conditions; residual defects and limitations MUST be known and MUST NOT invalidate the demonstrated operational feasibility.
- **R7.5** The evidence MUST identify the exact prototype revision/configuration and all material differences from the final intended system configuration.

**Required evidence classes:** operationally relevant prototype demonstration, scenario evidence, context-fidelity evidence, defect/limitation evidence, and exact revision/configuration provenance.

### TRL 8 - actual final system completed and qualified for intended operation

**Purpose:** establish that the actual system for the defined scope is complete in its final configuration and has passed complete qualification for its intended operating context.

**Software interpretation:** the actual release or deployable system, not merely a prototype, is fully implemented for the defined scope, fully integrated, and verified and validated in a Qualification Context proven adequate for the intended operational environment/platform. Successful real-world use is not yet required.

**Exit criteria:**

- **R8.1** The actual final system for the defined scope MUST be complete and MUST have an immutable or reproducibly revision-bound artifact identity where an artifact exists. Artifact release state MUST be identified where Deployment Environments v2 or an equivalent release contract applies.
- **R8.2** The final configuration relevant to behavior MUST be identified, including applicable runtime, database, infrastructure, platform, integration, data, security configuration, and externally supplied configuration characteristics.
- **R8.3** The Qualification Context MUST be proven adequate for the intended operation through evidence comparing its material characteristics with the intended operational context. A self-authored `production_equivalent: true`, an environment name, or an unqualified equivalence claim MUST NOT satisfy this criterion.
- **R8.4** Complete verification and validation for the final system and scope MUST pass against the applicable requirements and frozen Design/Test Contracts, including representative functional, performance, capacity, failure/recovery, deployment, rollback, migration, and interoperability behavior where those dimensions apply.
- **R8.5** Independently applicable technical qualification gates for security behavior/configuration, accessibility, operations/observability, and required documentation MUST have valid evidence where those controls are part of the intended system qualification. Passing TRL 8 MUST NOT itself be interpreted as a security approval, accessibility certification, risk classification, or regulatory approval.
- **R8.6** User, operator, maintenance, support, recovery, and training documentation required for the intended operation MUST be complete enough to operate and sustain the final system for the defined scope.
- **R8.7** Known limitations and accepted residual defects MUST be documented and MUST NOT contradict a mandatory intended-operation requirement or an applicable independent gate.

**Required evidence classes:** final artifact/configuration evidence, Qualification Context evidence, complete V&V/conformance evidence, applicable security/accessibility/operations/documentation evidence, deployment/rollback evidence where applicable, and residual-limitation evidence.

TRL 8 MUST NOT require an environment literally named `PROD`. A final system MAY establish TRL 8 in DEV, STAGING, a dedicated qualification environment, a test rig, or another context when R8.1 through R8.7 and every lower criterion are actually satisfied. Conversely, the existence of PROD MUST NOT establish TRL 8 when qualification is incomplete.

### TRL 9 - actual system proven by successful operational use

**Purpose:** establish that the actual system has succeeded in real intended operation.

**Software interpretation:** the actual Product/System Subject has been operated in its intended real context with real operational actors, workload, integrations, and outcomes, and the retained evidence demonstrates successful operation rather than only deployment or qualification.

**Exit criteria:**

- **R9.1** The operationally used system MUST be traceable to the Readiness Subject and to the final qualified artifact/revision/configuration lineage. A different artifact or materially different configuration MUST NOT inherit operational proof automatically.
- **R9.2** Real operational use MUST have occurred in the intended operational context with actual operational actors, traffic, workload, data, integrations, or mission/business/service use as applicable. Synthetic tests, a smoke test, health check, deployment success, or brief reachability alone MUST NOT satisfy this criterion.
- **R9.3** Before the operational result is accepted, the assessment MUST define evidence sufficiency appropriate to the subject's operating model, including a justified observation boundary such as representative scenarios, transaction/workload volume, operating cycles, elapsed service exposure, or mission phases. There is no universal minimum duration, but a few minutes of existence MUST NOT be treated as representative solely because no failure was observed.
- **R9.4** Operational results MUST satisfy declared success conditions for the intended scope and MUST include enough evidence to evaluate correctness and the critical operational characteristics on which the readiness claim depends.
- **R9.5** Material incidents, failures, defects, recovery events, and limitations observed during the qualifying operational boundary MUST be included in the assessment. An unresolved condition that invalidates the declared success criteria MUST prevent TRL 9 establishment.
- **R9.6** Sustaining operational ownership/support appropriate to the subject MUST exist, and the operational evidence MUST remain traceable through deployment/artifact lineage, telemetry or logs, business/mission outcomes, incident records, or equivalent auditable records.

**Required evidence classes:** operational deployment lineage, real-use evidence, predeclared sufficiency boundary, operational success results, incident/limitation evidence, and sustaining-support evidence.

A PROD URL, a successful PROD deployment, a successful smoke test, or short-lived reachability MUST NOT establish TRL 9 by itself.

## Qualification Context and Qualification Environment

A **Qualification Context** is the complete evidence-bound context in which readiness criteria are evaluated. A **Qualification Environment** is a runtime environment used as part of that context. The environment name is metadata, not proof of fidelity.

For criteria that require relevant, operationally relevant, or final-system qualification, evidence MUST identify the material dimensions whose fidelity can affect the result. As applicable, this includes:

- exact source revision and final release/artifact identity;
- final application/system configuration;
- runtime, operating system, container, database, infrastructure, network, and platform behavior;
- production-equivalent security configuration and trust relationships relevant to the tested behavior;
- real integrations or qualified equivalents;
- representative data, workload, concurrency, capacity, and performance characteristics;
- deployment, migration, restart, recovery, and rollback behavior;
- representative normal, degraded, and failure scenarios;
- complete verification and validation applicable to the level; and
- required security, accessibility, operations, observability, and documentation gates.

An equivalence claim MUST identify both the intended context and the qualification context, the compared dimensions, known differences, and evidence that each material difference does not invalidate the criterion being supported. A boolean or label asserting equivalence MUST NOT substitute for that evidence.

Examples of valid semantics include:

```text
DEV only, not representative
-> environment name provides no TRL 8 evidence

DEV only, final system with fully evidenced production-equivalent qualification context
-> TRL 8 can be established if all cumulative criteria pass

DEV + production-equivalent STAGING
-> TRL 8 can be established in STAGING if all cumulative criteria pass

PROD exists, final-system qualification incomplete
-> PROD does not establish TRL 8
```

## Evidence provenance and validity

Every evidence item used to satisfy a readiness criterion MUST have enough provenance to establish its applicability. The evidence model MUST be capable of binding, as applicable:

- Readiness Subject kind and stable Subject Identity;
- repository/consumer identity;
- source revision;
- immutable artifact identity or digest when an artifact exists;
- artifact release state when relevant;
- governing Design Contract and Test Contract artifacts/revisions;
- build and CI evidence;
- security evidence;
- accessibility evidence;
- deployment evidence;
- Qualification Environment and wider runtime/qualification context;
- operational-use evidence;
- tool, runner, and tool/runner version;
- execution parameters and material deterministic inputs;
- execution timestamp;
- result and pass/fail semantics;
- report, artifact, log, trace, or other result locators;
- limitations and known uncertainty; and
- explicit validity boundaries.

Evidence MUST be treated as invalid for a current claim when any dimension material to the criterion is missing, ambiguous, stale, or mismatched. Invalidation conditions include at least:

- different Subject Identity;
- a different relevant source revision without preservation/equivalence evidence;
- a different artifact or artifact lineage without explicit equivalence evidence;
- a changed or stale governing Contract Set;
- a materially different runtime or Qualification Context;
- a Fundamental Change;
- missing provenance required to establish applicability; or
- evidence outside its declared validity boundary.

Evidence MAY be reused across revisions, artifacts, or environments only when an explicit, criterion-specific equivalence argument proves that the changed dimensions are immaterial to the criterion or are adequately requalified. Reuse MUST NOT be inferred from similarity, shared source code, matching version labels, or environment names.

## Relationship to Contract-first Delivery

Contract-first Delivery and Product/System Readiness have different responsibilities:

```text
Contract-first Delivery
    -> produces qualified Design/Test/Implementation/Conformance Evidence

Product/System Readiness
    -> consumes suitable evidence to evaluate cumulative readiness criteria
```

A positive Contract-first Delivery result MAY satisfy one or more evidence requirements when its provenance and assertions match the readiness criterion. It MUST NOT automatically imply any TRL.

Product/System Readiness MUST NOT weaken, bypass, regenerate, or reinterpret a frozen Contract Set merely to obtain a higher readiness result. Contract-first invalidation and requalification rules remain in force independently.

## Relationship to Deployment Environments

When Deployment Environments v2 is applicable, it remains the source of truth for source revision, artifact release state, runtime environment vocabulary, immutable promotion, PROD semantics, and rollback artifact identity.

Product/System Readiness adds Qualification Context, readiness exit criteria, and Operational Evidence. It MUST NOT redefine deployment semantics.

In particular:

```text
Environment name != readiness evidence
deployment != operational proof
PROD != TRL 9
```

TRL 8 MAY be established without PROD when the final system is fully qualified for its intended operating context. TRL 9 requires successful actual operation of the subject and therefore cannot be established by artifact promotion or deployment evidence alone.

## Relationship to Repository Environments

Repository Environments v1 describes repository-owned human-web navigation URLs. A declared DEV, STAGING, or PROD URL is metadata only.

A URL MUST NOT be used as evidence of:

- qualification-context fidelity;
- successful deployment;
- actual productive operation;
- TRL 8; or
- TRL 9.

## Establishment, preservation, and requalification

Readiness evaluation has three explicit modes:

- `establishment`;
- `preservation`; and
- `requalification`.

### Establishment

**Establishment** is the first evidence-based establishment of a readiness level for a Subject/revision/artifact/context, or establishment of a higher level not previously established for that subject lineage.

Establishment MUST apply the cumulative criteria through the claimed level and MUST record the exact evidence/provenance set that established it.

### Preservation

**Preservation** evaluates whether an already established readiness level remains valid for a descendant revision or release after an ordinary change.

Preservation is not blind inheritance. To preserve established TRL `N`, evidence MUST demonstrate at least:

- exact lineage from the previously established subject/revision/artifact;
- an inventory of changes since the establishment or last valid preservation boundary;
- change-impact analysis against every readiness criterion and evidence validity boundary material to level `N`;
- identification of affected contracts, interfaces, configuration, runtime assumptions, trust boundaries, integrations, operational assumptions, and qualification dimensions;
- re-execution or replacement of evidence for every materially affected criterion;
- continued validity or explicitly proven equivalence for reused evidence; and
- absence of an unresolved Fundamental Change requiring requalification.

A routine feature, bug fix, documentation update, dependency update, or patch MAY preserve TRL 9 when the preservation evidence shows that established readiness remains valid. The change category alone MUST NOT prove preservation.

If preservation evidence is missing, inconclusive, stale, or shows that a material validity boundary was crossed, the prior level MUST NOT be carried forward as the current established state for the new revision.

### Fundamental Change

A **Fundamental Change** is a change that materially invalidates the representativeness of evidence on which established readiness depends and therefore requires explicit requalification rather than ordinary preservation.

A change-impact decision MUST evaluate at least these triggers:

- fundamental alteration of system architecture, execution model, decomposition, or critical interaction paths;
- a new or materially changed runtime platform, hardware platform, operating model, or infrastructure model;
- a new or materially changed Trust Boundary, identity/security architecture, or privilege model relevant to the subject;
- fundamental persistence, storage, consistency, or data-architecture change;
- new or materially changed critical operating assumptions, scale assumptions, failure modes, recovery model, or availability model;
- change to the identity or material scope of the Readiness Subject itself;
- fundamental change of the intended operating environment or critical external integrations; or
- any change that makes prior operational-use evidence materially non-representative of the new subject revision.

The presence of one of these trigger categories MUST cause an explicit impact evaluation. It requires requalification when the evidence validity boundary is materially crossed and cannot be proven preserved through bounded targeted re-evaluation.

A dependency update, ordinary feature, refactoring, configuration change, or routine platform patch MUST NOT automatically be classified as Fundamental Change solely because of its kind. Conversely, calling a change "maintenance" or "feature" MUST NOT exempt it when it actually crosses a fundamental validity boundary.

### Requalification

**Requalification** is explicit reassessment after a Fundamental Change or another invalidation that prevents preservation.

For revision B after an established revision A:

- A's historical establishment MUST remain valid for A;
- B MUST NOT silently inherit A's established readiness;
- B's current state MAY be `unassessed` until sufficient evidence is evaluated;
- B MAY assess at the highest lower level whose cumulative criteria remain valid for B; and
- B MAY re-establish the previous or a different level only from evidence valid for B.

Requalification MUST create a distinguishable new assessment/evidence boundary. It MUST NOT overwrite historical evidence to make old and new revisions indistinguishable.

## Historical readiness

Readiness history is append-only in meaning. If revision A established TRL 9 and revision B later requires requalification, the correct semantics are:

```text
revision A: established TRL 9
        |
        | fundamental change
        v
revision B: requalification required; current readiness derived from B evidence
```

The system MUST NOT rewrite history to claim that A never reached TRL 9. It also MUST NOT use A's historical TRL 9 label as proof that B is currently TRL 9.

## Product-/Release-Epic targets

This standard owns the semantics of readiness targets; a later Ticket Specification integration owns their concrete machine-readable placement.

A long-term Product/System Target expresses strategic intent for the subject. It MAY remain TRL 9 while intermediate increments target lower levels.

An Increment Target expresses the required readiness exit condition for one bounded Product-/Release-Epic or equivalent increment. When explicitly declared as an exit target, completion MUST have evidence-derived Assessed or Established readiness at or above that target for the defined increment/subject, or an explicit exception through the governing exception mechanism.

Examples:

```text
Product: Traincaster
long-term target: TRL 9

Increment: Traincaster MVP
increment target: TRL 8
```

No rule may infer `TRL 8` merely because the Product Stage is `mvp`. An MVP MAY explicitly target TRL 9.

## Risk, security, criticality, and compliance boundary

TRL is a technical readiness dimension. It is not a risk, exposure, security, safety, privacy, criticality, or regulatory classification.

The following implications are invalid and MUST NOT be made:

```text
high TRL => secure
high TRL => low risk
high TRL => low criticality
TRL 9 => security approved
```

Independent controls MAY depend on exposure, data classification, criticality, threat model, Trust Boundaries, change impact, safety considerations, or regulatory/organizational requirements. Those controls MAY contribute evidence to readiness criteria when technically relevant, but their governance remains independent.

If a mandatory security behavior or configuration is part of the intended final system qualification, missing evidence for that behavior prevents satisfaction of the affected TRL 8 qualification criterion. Separately, a system MAY have high established readiness while an independent security approval, risk acceptance, or compliance decision is missing or expired; the high TRL MUST NOT satisfy that independent gate.

## Decision cases

The following cases are normative interpretations of the rules above. The stated TRL is a ceiling or possibility only when every cumulative lower criterion is also satisfied.

| Case | Required interpretation |
| --- | --- |
| 1. Research proof of concept demonstrates a critical function but no integrated product exists. | TRL 3 MAY be established when R1-R3 pass. TRL 4 and above MUST NOT be claimed without the required integration evidence. |
| 2. Product prototype exists only in ordinary DEV. | `DEV` provides no automatic level. The result is the highest cumulative level its actual evidence supports; TRL 8 requires final-system qualification and cannot be inferred from DEV. |
| 3. Final product is qualified in a DEV environment that is fully proven production-equivalent for all material dimensions. | TRL 8 MAY be established without PROD when R1-R8 pass and the equivalence is evidenced. |
| 4. Final product is qualified in production-equivalent STAGING and PROD does not yet exist. | TRL 8 MAY be established when R1-R8 pass. PROD is not a prerequisite for TRL 8. |
| 5. An artifact is deployed to PROD without complete final-system qualification. | PROD does not establish TRL 8. Assessment remains at the highest lower cumulative level actually evidenced. |
| 6. A product is fully qualified, then deployed to PROD and passes only a smoke test. | TRL 8 MAY be established; TRL 9 MUST NOT be established until sufficient real operational-use evidence satisfies R9. |
| 7. A deliberately limited MVP is the first real version used successfully. | The MVP MAY establish TRL 9 for its defined scope when R1-R9 pass. MVP status neither lowers nor caps TRL. |
| 8. A TRL-9-established product receives an ordinary feature release. | TRL 9 MAY be preserved when the preservation evidence proves all material validity boundaries remain satisfied. It MUST NOT be inherited blindly. |
| 9. A TRL-9-established product undergoes a fundamental architecture change. | Historical TRL 9 remains true for the earlier revision. The changed revision requires requalification and MUST NOT inherit TRL 9 without new valid evidence. |
| 10. A library or design system has no independently operated Product/System Subject. | Product/System Readiness MAY be `not-applicable` with rationale. Repository type alone MUST NOT fabricate a subject. |
| 11. An infrastructure repository represents a bounded, continuously operated platform/system. | It MAY declare a `system` Readiness Subject and assess it normally; `infrastructure` profile neither requires nor forbids applicability. |
| 12. One repository contains multiple products or operated systems. | Each subject MUST have a separate stable identity and separate assessment/history. No repository-wide TRL is inferred. |
| 13. A repository declares a PROD URL but has no deployment or operational evidence. | The URL is navigation metadata and proves no TRL. If no other valid readiness evidence exists, the current state remains `unassessed`. |
| 14. Evidence belongs to an older source revision. | It is stale for the current claim unless preservation or criterion-specific equivalence proves continued validity. Evaluation MUST fail closed for unsupported affected criteria. |
| 15. Evidence belongs to a different artifact or environment. | It MUST NOT be reused automatically. Cross-artifact/context reuse requires explicit criterion-specific equivalence. |
| 16. A security-critical product has high technical readiness but a required security qualification is absent. | TRL MUST NOT substitute for the security gate. If the missing evidence is part of final-system technical qualification, R8 is unsatisfied for that current assessment; if it is a separate approval, readiness MAY remain established but release/operation remains independently blocked. |
| 17. Product long-term target is TRL 9 while the current Release-Epic target is TRL 8. | The increment MAY complete at TRL 8 when its target is satisfied; the long-term target does not automatically block it. |
| 18. An MVP explicitly targets TRL 9. | The target is valid. Completion requires evidence meeting TRL 9 or an explicit governed exception; `mvp` MUST NOT lower the target. |

## Validation obligations for downstream Test Contracts

A downstream executable Test Contract derived from this Design Contract MUST be able to prove at least:

- cumulative TRL 1 through 9 behavior;
- fail-closed handling of missing and unknown evidence;
- explicit applicability and stable subject identity;
- separation of authored Target/Stage from derived readiness;
- `unassessed` without introducing TRL 0;
- TRL 8 with adequate qualification both with and without an environment named PROD;
- rejection of PROD-only or URL-only readiness inflation;
- TRL 9 requiring sufficient real operational-use evidence;
- stale and cross-revision/artifact/context evidence rejection;
- establishment, preservation, Fundamental Change, and requalification state transitions;
- historical-readiness preservation across requalification;
- independent security/risk boundaries; and
- each decision case in this standard as a positive or controlled-negative fixture where applicable.

The Test Contract MUST NOT weaken these rules to fit a specific CI, issue tracker, deployment system, or evidence store.

## Compatibility and migration

Product/System Readiness v1 is an additive standard family. Existing released Repository Standards, schemas, declarations, ticket specifications, and consumer repositories remain unchanged and immutable.

Publication of this Design Contract alone MUST NOT:

- add fields to an existing released `.repository-standards.yml` schema;
- reinterpret a repository profile as readiness applicability;
- assign a guessed TRL to an existing product/system;
- rewrite historical tickets or releases;
- activate a readiness gate in Maintenance, Jenkins, Forgejo, Workboard, or another provider; or
- make Product/System Readiness mandatory for an existing consumer.

Adoption MUST occur only through a later explicit, released compatibility/declaration boundary with qualified machine-readable contracts and consumer enforcement. Migration MUST start from explicit subject/applicability/target decisions and available evidence. It MUST NOT invent historical readiness.

## Provider boundary

This standard defines outcomes and evidence semantics, not provider APIs. Jenkins, Forgejo, GitHub, Workboard, Maintenance, another CI system, or another evidence store MAY implement or surface the contract, but no provider-specific job, function, label, or URL is required to interpret Product/System Readiness v1.
