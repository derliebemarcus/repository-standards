# Ticket Specification v1

## Status and scope

This standard defines the organization-wide contract for Forgejo tickets. It covers ticket
metadata, description structure, ticket families, readiness, estimation, validation, relations,
impact assessment, migration, and AI-assisted authoring.

It applies to new tickets and to tickets changed after adoption. Migration rules distinguish
between open and closed legacy tickets.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences of words such as "must", "should", and "may" are non-normative.
Normative obligations MUST use the capitalized BCP 14 forms.

## Source of truth

The normative source is this document. The machine-readable representation is
`profiles/ticket-specification-v1.json`, validated by
`schemas/ticket-specification-v1.schema.json`. Reference templates and the AI authoring adapter
MUST be generated from the machine-readable representation and MUST NOT become separately
maintained policy copies.

Consumers MUST pin a released standard version. They MUST NOT load an unversioned branch as their
policy source during each operation.

## Ticket metadata

### Title

A ticket title MUST describe one concrete outcome or problem. It MUST be understandable without
opening the ticket and MUST NOT use an implementation status as its title.

### Assignee

A ticket MUST have exactly one assignee. When no assignee is supplied, automation MUST assign
`marcus`.

### Label categories

A ticket MUST have:

- exactly one `Kind/*` label;
- exactly one `Priority/*` label;
- exactly one `Status/*` label;
- at least one `Area/*` label.

Multiple `Area/*` labels MAY be used when the work crosses component boundaries. Labels outside
these categories MAY be used when they do not contradict the required categories.

When no priority is supplied, automation MUST assign `Priority/Low`. When no status is supplied,
automation MUST assign `Status/Backlog`.

The supported priority order is:

1. `Priority/Critical`;
2. `Priority/High`;
3. `Priority/Normal`;
4. `Priority/Low`.

`Priority/Medium` MUST NOT be assigned because it duplicates `Priority/Normal`.

### Estimate

Forgejo does not provide a native Story Point field. Relative estimates MUST therefore use exactly
one exclusive label from this sequence:

- `Estimate/1`;
- `Estimate/2`;
- `Estimate/3`;
- `Estimate/5`;
- `Estimate/8`;
- `Estimate/13`.

An implementable leaf ticket in `Status/Ready` MUST have exactly one `Estimate/*` label. An Epic
MUST NOT have an `Estimate/*` label. The assignee MUST review the estimate before the ticket enters
`Status/Ready`.

Story Points MUST represent relative effort, complexity, risk, and uncertainty. They MUST NOT be
interpreted as hours or person-days. A ticket estimated above eight Story Points SHOULD be split
before it enters `Status/Ready`. Retaining `Estimate/13` requires a documented justification.

## Ticket families and kinds

Ticket family, `Kind/*` label, and branch prefix are separate concepts. A family defines the
description template. The `Kind/*` label preserves the nature of the work.

| Ticket family | Allowed kind labels |
| --- | --- |
| Epic | `Kind/Epic` |
| Story | `Kind/Feature`, `Kind/Enhancement`, `Kind/Refactoring`, `Kind/Maintenance`, `Kind/Research` |
| Bug | `Kind/Bug` |
| Security | `Kind/Security` |
| Documentation | `Kind/Documentation` |
| Testing | `Kind/Testing` |

A ticket MUST use exactly one family and exactly one compatible `Kind/*` label.

### Epic

An Epic groups outcomes delivered through child tickets. It MUST define the target outcome,
boundaries, success measures, and child structure. It MUST NOT contain a direct Story Point
estimate.

### Story

Feature, Enhancement, Refactoring, Maintenance, and Research use the Story family. They retain
distinct kind labels and branch prefixes.

A Story MUST provide kind-specific details:

- Feature: user or system value, new behavior, interfaces, normal cases, and error cases;
- Enhancement: current behavior, deficiency, desired improvement, and unchanged guarantees;
- Refactoring: technical debt, behavior that remains unchanged, and measurable quality target;
- Maintenance: maintenance reason, affected assets, and operational risk;
- Research: research question, assumptions, method, evaluation criteria, timebox, evidence, and
  expected decision artifact.

### Bug

A Bug MUST describe environment, reproducible steps, expected behavior, actual behavior, and
available evidence. It MUST define a regression test or a concrete alternative validation method.

### Security

A Security ticket MUST describe the affected asset, attack surface or trust boundary, threat or
vulnerability, affected versions, impact, mitigation, and validation. Public tickets MUST NOT
contain secrets, personal data, or unnecessarily exploitable detail.

### Documentation

A Documentation ticket MUST identify the audience, affected source of truth, required corrections
or additions, examples, links, and validation method.

### Testing

A Testing ticket MUST identify the coverage gap, risk, test level, assertions, fixtures or data,
and determinism requirements.

### Hotfix

Hotfix is not a ticket family. It is an expedited delivery path normally used by a
`Kind/Bug` or `Kind/Security` ticket with `Priority/Critical`.

A Hotfix MUST retain normal test, documentation, security, compatibility, rollout, verification,
and rollback requirements. It MUST use the `hotfix/` branch prefix and the hotfix integration rules
defined by Ticket-based Development Workflow v2.

## Required ticket description

Every ticket MUST contain the following headings in this order. A non-applicable section MUST
remain present and MUST state why it does not apply.

```markdown
## Context

## Goal

## Scope

### In scope

### Out of scope

### Affected components

## Requirements

## Acceptance criteria

## Work-type details

## Relations

### Parent

### Blocked by

### Blocks

### Related

## Validation

### Tests or research validation

### Documentation

## Impact assessment

### Security

### Compatibility

### Deployment

## Estimate
```

### Context and goal

`Context` MUST explain the current situation and reason for the ticket. `Goal` MUST define the
observable outcome rather than merely naming implementation activity.

### Scope and boundaries

`In scope` MUST list concrete deliverables. `Out of scope` MUST list explicit non-goals.
`Affected components` MUST identify repositories, modules, interfaces, data, operations, or user
journeys affected by the work.

Discoveries outside the declared scope MUST become linked follow-up tickets. A material scope
change MUST be documented before implementation continues and MAY require re-estimation.

### Requirements and acceptance criteria

Requirements MUST use BCP 14 terminology when they are normative. Acceptance criteria MUST be
observable, testable, and sufficient to decide whether the ticket is complete.

### Work-type details

`Work-type details` MUST contain the family- and kind-specific information required by this
standard.

## Relations and dependency synchronization

Relations MUST use explicit ticket references. Local `#123`, repository-qualified
`repository#123`, fully qualified `owner/repository#123`, and canonical Forgejo issue URLs MAY be
used when unambiguous.

`### Blocked by` is the canonical direct-dependency declaration consumed by
`workboard_forgejo_issue_dependency_sync`.

Each direct blocker MUST appear as a standalone list item or reference line immediately below
`### Blocked by`. Explanatory prose MUST NOT appear between direct blocker references. Use `None`
when there are no direct blockers.

`Parent`, `Blocks`, and `Related` MUST NOT be interpreted as direct blockers. Closed tickets MAY be
used in any relation and MUST remain visible during relation migration and reconciliation.

Dependency declarations MUST NOT contain self-dependencies or cycles. After a ticket is created or
its direct blockers change, automation MUST reconcile the affected ticket with `STATE=all`.

## Definition of Ready

A ticket MAY enter `Status/Ready` only when all applicable conditions are satisfied:

- exactly one assignee is assigned;
- exactly one `Kind/*`, `Priority/*`, and `Status/*` label is assigned;
- at least one `Area/*` label is assigned;
- the title, context, goal, scope, requirements, and acceptance criteria are complete;
- family- and kind-specific details are complete;
- parent and dependency relations are explicit;
- direct blockers are resolved;
- the test or research-validation strategy is explicit;
- documentation impact is explicit;
- security, compatibility, and deployment impact are classified;
- no required impact remains `Not yet determined`;
- no unresolved question prevents implementation;
- an implementable leaf ticket has an assignee-reviewed `Estimate/*` label;
- an Epic has no `Estimate/*` label.

A ticket failing these conditions MUST remain in `Status/Backlog`, `Status/Need More Info`, or
`Status/Blocked`, as appropriate.

## Validation requirements

Every ticket MUST make an explicit validation decision. When automated testing is not appropriate,
the ticket MUST document the reason and the alternative evidence.

The validation strategy SHOULD include the applicable levels:

- business logic: unit or component tests;
- APIs and integrations: contract or integration tests;
- user interfaces: component, accessibility, and end-to-end tests;
- Bugs: regression tests;
- data changes: migration, backward-compatibility, restart, and rollback tests;
- Security: positive and negative security tests;
- deployment changes: health, rollout, and rollback validation;
- Documentation: links, formatting, commands, and example validation.

### Research validation

Research succeeds by producing reliable decision evidence, not by confirming a preferred
hypothesis. A Research ticket MUST define:

- the research question;
- current knowledge and assumptions;
- evaluation criteria applied consistently to alternatives;
- method and evidence sources;
- a timebox;
- the expected result artifact;
- reproducibility requirements;
- limitations and remaining uncertainty;
- required follow-up tickets.

Persisted Research code MUST meet normal product test requirements. Disposable experimental code
MUST be marked non-production, MUST NOT enter production paths unintentionally, and MUST include
reproduction commands and inputs.

Research MUST have both a relative `Estimate/*` label and a concrete timebox before
`Status/Ready`.

## Documentation requirements

Every ticket MUST identify affected documentation or provide a concrete no-impact justification.

Documentation normally requires updates when work changes:

- public behavior or user journeys;
- APIs, events, CLI, or configuration;
- installation, upgrade, migration, or rollback;
- data models and persistence;
- architecture or durable decisions;
- deployment, operations, monitoring, or troubleshooting;
- security or compatibility expectations;
- release notes and examples.

Changing an unrelated Markdown file MUST NOT satisfy the documentation requirement.

## Impact assessment

Each of Security, Compatibility, and Deployment MUST use one classification:

- `No impact`;
- `Impact identified`;
- `Not yet determined`.

`Not yet determined` MAY be used in Backlog tickets but MUST block `Status/Ready`.

### Security

Security assessment MUST consider authentication, authorization, secrets, personal data, input
validation, trust boundaries, logging, dependency supply chain, and runtime privileges.

### Compatibility

Compatibility assessment MUST consider APIs, configuration, databases and files, events, CLI,
user interfaces, supported runtimes, and integrations. A breaking change MUST receive
`Compat/Breaking` and MUST provide a migration path.

### Deployment

Deployment assessment MUST consider artifacts and images, configuration and environment changes,
migrations, ordering, restarts, downtime, health checks, observability, rollout, and rollback.

## AI-assisted authoring

AI agents MUST determine the released standard version declared by the repository before creating,
changing, classifying, or closing a ticket. They MUST load the matching generated AI adapter and
MUST NOT reconstruct policy from memory or prior conversations.

Before a write, an AI agent MUST validate the proposed ticket against the machine-readable
contract. Missing factual content MUST NOT be invented. Unknown information MUST be marked
explicitly and MUST prevent `Status/Ready` where required.

A generic Forgejo issue API SHOULD be wrapped by a standard-aware operation that applies defaults,
renders the correct family template, validates metadata and sections, writes the ticket, and
triggers dependency reconciliation.

## Migration and legacy tickets

Migration MUST be staged:

1. publish and pin Ticket Specification v1;
2. update dependency parsing and enforcement consumers while retaining legacy headings;
3. inventory all tickets with `STATE=all`;
4. create a dry-run report containing original content, proposed metadata, proposed description,
   unresolved facts, relations, and before/after diffs;
5. migrate a Canary repository;
6. migrate open tickets completely;
7. migrate closed tickets conservatively;
8. reconcile dependencies in dry-run and apply modes;
9. enable audit, warning, and enforcement stages.

Open tickets MUST be migrated to the full current structure. Missing defaults MAY be applied, but
factual requirements, evidence, estimates, and impacts MUST NOT be invented.

Closed tickets MUST receive normalized assignees, label categories, and relations. Missing
historical evidence MUST be recorded as `Not recorded before Ticket Specification v1.` Closed
tickets MUST NOT receive invented tests, acceptance evidence, or Story Point estimates.

Migration tools MUST be idempotent, MUST archive original descriptions, and MUST provide a dry-run
mode before any organization-wide write.
