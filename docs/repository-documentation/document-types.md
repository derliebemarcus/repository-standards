# Document types

This page explains the Repository Documentation v2 document types in practical terms. It is
**non-normative**. The authoritative requirements are in the
[Repository Documentation Standard v2](../../standards/repository-documentation/v2/standard.md#document-type-quality-criteria).

The central rule is simple: judge a document by the information task it performs. Length is not a
quality criterion. A compact index or evidence record can be complete; a long page can still fail if
it does not answer the reader's actual need.

## Tutorial

**Use when:** a reader needs to learn by completing a guided, dependable exercise.

A strong tutorial has a clear learning objective, meaningful prerequisites, an intentional sequence,
and an observable working end state. It avoids turning into an encyclopedic reference while the
reader is still trying to learn the path.

**Common misuse:** a list of commands without a learning objective, or a reference page padded with
steps and called a tutorial.

Normative criteria: [Tutorial](../../standards/repository-documentation/v2/standard.md#tutorial).

## How-to Guide

**Use when:** a reader already understands the domain sufficiently and needs to accomplish a concrete
task.

A strong how-to states the goal and prerequisites, gives actionable steps, identifies the expected
result, and explains how to verify success. Background material should be linked rather than allowed
to obscure the task.

**Common misuse:** using a how-to as the permanent home for exhaustive configuration facts, or giving
steps without an expected result or verification.

Normative criteria: [How-to Guide](../../standards/repository-documentation/v2/standard.md#how-to-guide).

## Reference

**Use when:** a reader needs precise lookup of durable facts about a current contract, interface,
configuration, or system state.

A strong reference defines its scope and authority boundary, is precise and sufficiently complete
within that scope, and minimizes narrative distraction. It should be obvious which facts are defined
there and which are not.

**Common misuse:** copying a one-time build result into a reference page and presenting it as a
permanently current fact. Point-in-time proof belongs to Verification / Evidence.

Normative criteria: [Reference](../../standards/repository-documentation/v2/standard.md#reference).

## Explanation

**Use when:** a reader needs to understand context, motivation, relationships, limits, alternatives,
or trade-offs.

A strong explanation connects concepts rather than merely enumerating them. It may explore why a
choice exists, where it stops applying, and what alternatives were considered.

**Common misuse:** treating explanatory prose under `docs/` as if it could add or override a binding
requirement. Normative authority remains with the selected versioned artifact under `standards/`.

Normative criteria: [Explanation](../../standards/repository-documentation/v2/standard.md#explanation).

## Architecture

**Use when:** a reader needs a coherent current model of durable system structure, boundaries,
relationships, constraints, deployment, and quality-relevant concerns.

Repository Standards uses an arc42-lite structure and C4 views where useful. Architecture should
cover relevant context and boundaries, constraints, building blocks, runtime and deployment
relationships, cross-cutting concepts, quality requirements, risks, technical debt, terminology, and
links to the ADRs that explain significant choices.

**Common misuse:** making the ADR directory the only architecture description, or producing every C4
level regardless of whether it communicates useful information.

Normative criteria: [Architecture](../../standards/repository-documentation/v2/standard.md#architecture).
See also [Methods and models](methods-and-models.md).

## Decision / ADR

**Use when:** an architecturally significant decision and its rationale need a durable historical
record.

A strong ADR makes Status, Context / Problem, Decision, and Consequences explicit. When a decision is
replaced, the supersession path should let a reader reconstruct the decision history without
rewriting the accepted historical record.

**Common misuse:** silently editing an accepted ADR to describe a later decision, or using ADRs as a
substitute for a current architecture overview.

Normative criteria: [Decision / ADR](../../standards/repository-documentation/v2/standard.md#decision--adr).

## Operations / Runbook

**Use when:** an operational action must be executed safely and repeatably, especially where failure
can affect availability, security, data, or recovery.

A strong runbook combines goal, prerequisites, safe execution conditions, concrete steps,
verification, failure handling, stop conditions, and rollback or recovery. Not every operational
procedure needs elaborate recovery text, but risk-relevant boundaries must be explicit.

**Common misuse:** treating a production-impacting procedure as an ordinary how-to while omitting
stop conditions or recovery behavior.

Normative criteria: [Operations / Runbook](../../standards/repository-documentation/v2/standard.md#operations--runbook).

## Verification / Evidence

**Use when:** the purpose is to preserve proof that a state, claim, build, release, test, audit, or
other subject was examined under identifiable conditions.

Verification is a separate **evidence class**. It is not ordinary Reference documentation. A useful
evidence record identifies what was checked, the relevant revision/version/PR/build/release, when it
was checked, how it was checked, the result, where the evidence came from, any available artifacts or
reproduction steps, and the limits of the result.

Evidence is naturally point-in-time. Keeping historical evidence is useful and conformant, but its
navigation and labeling must prevent readers from confusing it with current system documentation.
For example:

- `Build #42 passed the release qualification for commit abc123 on 2026-08-25` is evidence.
- `The release pipeline requires these gates` is current Reference or Architecture, depending on
  scope.
- `To rerun the release qualification safely` is a How-to or Runbook, depending on operational risk.

A verification record can be extremely short when the entire information task is one clear,
traceable proof. Length does not make it incomplete.

**Common misuse:** a `verification.md` page saying only “works” without scope, identity, method, or
result provenance; or an old green-build record presented as proof that the current head remains
green.

Normative criteria: [Verification / Evidence](../../standards/repository-documentation/v2/standard.md#verification--evidence).

## Index / Navigation

**Use when:** a reader needs orientation, entry points, and clarity about where authority lives.

A strong index stays concise, exposes relevant routes into the documentation set, and avoids
becoming a second copy of the content it links to. Where current docs, historical evidence,
standards, and explanatory guidance coexist, the index should make those authority boundaries clear.

**Common misuse:** judging an index by word count, or turning it into duplicated detail that drifts
from its authoritative pages.

Normative criteria: [Index / Navigation](../../standards/repository-documentation/v2/standard.md#index--navigation).

## Boundaries that matter

### Tutorial vs. How-to

Both can contain steps. A Tutorial optimizes for learning; a How-to optimizes for completing work.
The reader's information task, not the presence of numbered steps, determines the type.

### How-to vs. Runbook

Both can be procedural. A Runbook adds the operational safety model needed when failure or continued
execution can materially affect a live environment, data, security, availability, or recovery.

### Reference vs. Verification

Reference states durable current facts within an authority boundary. Verification records that
something was checked at a particular time or revision under stated conditions. Evidence can support
a reference claim but does not become permanently current merely because the check once passed.

### Explanation vs. normative Standard

Explanation helps a reader understand. A versioned Standard defines binding obligations. Guidance
under `docs/` cannot silently create new requirements.

### Architecture vs. ADR

Architecture is the coherent current system view. ADRs are the historical chain of significant
choices and rationale. They should link to one another rather than replace one another.

### Index vs. content page

An index can be complete with a handful of links. A content page must provide the substance its
information task requires. A heading-only or fragmentary content page is therefore not rescued by
being short or by being labeled an index when it is actually expected to explain, instruct, or
describe something.

### Current documentation vs. historical evidence

Current documentation is maintained to describe the present contract or system. Historical evidence
is retained to demonstrate what was observed for a bounded revision or time. Both can remain useful,
but their authority and validity windows must be distinguishable.
