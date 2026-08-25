# Methods and models

This page explains why Repository Standards uses Diátaxis, arc42-lite, C4, and MADR and how their
roles fit together. It is **non-normative**. Binding requirements are defined by the selected
[Repository Documentation Standard](../../standards/repository-documentation/v2/standard.md).

## How the models fit together

The models solve different problems:

- **Diátaxis** organizes the wider documentation set by the reader's information task.
- **arc42-lite** structures architecture-specific information inside that wider set.
- **C4** provides architecture views and diagrams at useful levels of abstraction.
- **MADR** structures durable Architecture Decision Records.

Diátaxis and arc42 are therefore not competing models. In an illustrative repository layout they may
appear together like this:

```text
docs/
├── tutorials/        # Diátaxis
├── how-to/           # Diátaxis
├── explanation/      # Diátaxis
├── reference/        # Diátaxis
├── architecture/     # arc42-lite + C4
├── decisions/        # MADR
├── operations/       # operational procedures
└── verification/     # point-in-time evidence
```

This is an example, not a mandatory directory tree unless a selected profile or declaration makes a
specific path mandatory.

## Diátaxis

### What is it?

Diátaxis is a documentation framework that distinguishes four primary documentation modes:
Tutorials, How-to Guides, Reference, and Explanation. Its key contribution is to organize material by
what the reader is trying to achieve rather than by source-code layout or authoring convenience.

### What problem does it solve?

Documentation often becomes difficult to use when learning material, task instructions, factual
lookup, and conceptual explanation are mixed together. Diátaxis provides a vocabulary for separating
those information needs while still allowing the pages to link to one another.

### How does Repository Standards use it?

Repository Documentation v2 adopts the four Diátaxis information tasks as explicit document types:

- Tutorials support guided learning.
- How-to Guides support task completion.
- Reference supports precise lookup.
- Explanation supports understanding.

Repository Standards extends the overall documentation model with Architecture, Decision / ADR,
Operations / Runbook, Verification / Evidence, and Index / Navigation because those information tasks
need explicit treatment in engineering repositories.

### What does it explicitly not mean here?

Diátaxis does not require four particular directory names, nor does it prohibit a carefully designed
page from containing more than one information task. It also does not replace architecture,
operations, or evidence models. Classification is based primarily on the reader's information need,
not on document length or format.

### Further information

- Official Diátaxis documentation: https://diataxis.fr/
- Official introduction: https://diataxis.fr/start-here/

## arc42-lite

### What is it?

arc42 is a template and organization model for communicating software architecture. It provides a
structured set of concerns including context, constraints, building blocks, runtime, deployment,
cross-cutting concepts, architecture decisions, quality requirements, risks, and terminology.

`arc42-lite` is the Repository Standards name for the pragmatic subset needed to keep those concerns
coherent without requiring every repository to reproduce the complete arc42 template mechanically.

### What problem does it solve?

Architecture documentation tends to drift when context, runtime behavior, deployment, constraints,
and quality concerns are documented as disconnected fragments. arc42 provides a stable conceptual
structure in which those concerns can be related.

### How does Repository Standards use it?

Repository Documentation v2 requires architecture content to cover the relevant architecture
information tasks: context and boundaries, constraints, building blocks, runtime and deployment,
cross-cutting concepts, quality requirements, risks and technical debt, terminology, and references
to relevant ADRs.

The `arc42-lite` declaration tells readers and tooling which architecture convention is in use. It
does not add an independent second architecture standard.

### What does it explicitly not mean here?

`arc42-lite` does **not** mean that every arc42 chapter must exist as a separate file or heading. It
does not justify placeholder sections for concerns that are irrelevant to the repository. The
normative Repository Documentation version defines which information tasks must be satisfied.

### Further information

- Official arc42 site: https://arc42.org/
- Official arc42 documentation: https://docs.arc42.org/home/

## C4

### What is it?

The C4 model is a hierarchy of software-architecture abstractions:

1. **System Context** — the system, its users, and external systems around it.
2. **Container** — deployable or runtime units such as applications, services, databases, or other
   major technology boundaries.
3. **Component** — significant components within a container.
4. **Code** — implementation-level structures where that detail is useful.

### What problem does it solve?

Architecture diagrams become hard to interpret when different levels of abstraction are mixed or
left implicit. C4 gives diagrams a recognizable scope and vocabulary so a reader can tell which
question a view is answering.

### How does Repository Standards use it?

Repository Documentation v2 uses C4 as a view model inside architecture documentation:

- System Context **should** be present when external people or systems matter to understanding the
  system boundary.
- Container **should** be present when multiple deployable or runtime units matter to understanding
  the architecture.
- Component and Code views are optional and may be added when they materially improve understanding.

Text diagrams or another repository-supported rendering mechanism may express those views; the
information communicated by the view is more important than producing a particular drawing format.

### What does it explicitly not mean here?

A repository does not need all four C4 levels. C4 is not a requirement to draw diagrams for their own
sake, and it does not replace the prose, constraints, quality concerns, runtime descriptions, or ADRs
that make architecture understandable.

### Further information

- Official C4 model: https://c4model.com/

## MADR

### What is it?

MADR is a Markdown-oriented template and convention for Architecture Decision Records. An ADR
preserves an architecturally significant decision together with enough context and consequences to
understand why it was made.

### What problem does it solve?

A current architecture view tells readers what the system is. It often cannot explain why a
significant choice was made, what alternatives existed, or what consequences were accepted. ADRs
preserve that decision history without forcing the current architecture document to become a
chronological log.

### How does Repository Standards use it?

Repository Standards uses MADR-compatible records, normally under `docs/decisions/`. Repository
Documentation v2 requires the decision record to make at least these concepts clear:

- Status;
- Context / Problem;
- Decision;
- Consequences; and
- traceable supersession when a later ADR replaces a decision.

Accepted ADR content should remain historically stable. A changed decision is normally captured by a
new ADR, with status/supersession metadata connecting the records.

### What does it explicitly not mean here?

MADR is not the architecture documentation itself. An ADR directory cannot replace a coherent current
architecture description. Repository Standards also does not require every optional field or section
that any MADR template version offers when the normative standard does not require it.

### Further information

- Official MADR project and specification: https://adr.github.io/madr/

## Practical composition

A useful documentation flow is often:

1. an **Index** tells the reader where to start;
2. Diátaxis pages serve learning, task, lookup, and understanding needs;
3. **Architecture** provides the current structural model using arc42-lite and useful C4 views;
4. **ADRs** explain significant architectural choices over time;
5. **Runbooks** make operational procedures safe and repeatable; and
6. **Verification / Evidence** records bounded proof without pretending to be current Reference.

These layers should link to one another, but each should retain a clear authority and information
task.
