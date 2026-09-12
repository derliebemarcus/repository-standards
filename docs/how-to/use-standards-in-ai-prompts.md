# Use repository standards in AI prompts

## Principle

Do not copy complete standards into project prompts. Copied policy becomes an uncontrolled fork.
Use three layers instead:

1. released normative standards in `siczb/repository-standards`;
2. versioned/generated AI adapters under `reference/ai/`; and
3. a short project bootstrap instruction that loads the repository's pinned declaration and adapter.

## Repository declaration

A repository adopting Repository Standards stores `.repository-standards.yml`. Its declaration
version, selected standards, and branching model form one compatibility contract. An AI agent MUST
validate the whole pairing and MUST NOT infer adoption merely because a standard or adapter exists.

For Product/System Readiness v1, declaration v11 is the additive integration boundary. The v11
pairings are candidate until their separate release/conformance qualification is complete; an agent
MUST NOT migrate a consumer to them before they are released as supported.

When a released compatible declaration selects Product/System Readiness v1, applicability is still
not derived from `.repository-standards.yml`, repository profile, documentation profile, web profile,
or deployment profile. The repository-owned `.product-readiness.yml` is authoritative for:

- applicability;
- Product/System Subject kind;
- stable Subject Identity; and
- long-term Product/System Readiness Target.

## Ticket Specification v5

For Ticket Specification v5, the agent MUST load `reference/ai/ticket-authoring-v5.md` and preserve
the generated `## Product increment` section. Non-targeted tickets use
`product_increment: null`. Only a Product-/Release-Epic deliberately declares a non-null increment.

The following are authored intent:

- Product Stage;
- Increment Readiness Target; and
- Subject Identity binding.

The following remain evidence-derived and MUST NOT be authored as authoritative ticket metadata:
Candidate, Assessed, Established, Preservation, Requalification, current readiness, and actual
readiness.

An AI agent MUST preserve these boundaries:

```text
authored intent != derived readiness
target != candidate
target != assessed
target != established
deployment != operational proof
PROD != TRL 9
product stage != TRL
```

An `mvp` may target and establish TRL 9 for its deliberately bounded scope when the complete
evidence supports it. `production` implies no TRL. The agent MUST NOT infer either dimension from
the other.

Before setting a readiness-targeted Product-/Release-Epic to `Status/Done`, the agent MUST require
an exact qualifying assessment reference, verify that it binds to the same Subject Identity, and
verify that the evidence-derived Assessed Readiness meets or exceeds the authored target. Missing,
stale, mismatched, or insufficient evidence fails closed.

Product/System Readiness is not a security classification. The agent MUST NOT infer security
approval, low risk, low criticality, or similar security/risk state from TRL.

## Bootstrap instruction

A project prompt should contain only the loading and enforcement contract:

```text
Before any ticket or repository write, read `.repository-standards.yml`, validate its complete
released contract set, load the declared standards and matching AI adapter from
`siczb/repository-standards`, and validate the proposed change. Load repository-owned sidecars
required by that contract set. Do not reconstruct rules from memory or an older conversation. Do
not invent missing facts or derive authored intent from unrelated repository state. Apply defaults,
validation, lifecycle rules, and required reconciliation exactly as defined by the loaded adapter.
```

Repository-specific operational instructions MAY be added after this bootstrap. They MUST NOT
weaken or duplicate the standard.

## Agent write flow

An AI agent should:

1. read `.repository-standards.yml`;
2. validate the complete pairing against the released compatibility profile;
3. resolve the selected released standard artifacts;
4. load required repository-owned sidecars;
5. determine the selected Ticket Specification version;
6. load `reference/ai/ticket-authoring-v<major>.md`;
7. select the ticket family and generated template;
8. collect only available facts and mark material unknowns explicitly;
9. author only fields owned by the selected contracts;
10. validate the complete proposal before writing;
11. write through a standard-aware interface; and
12. trigger required reconciliation and provider checks after the write.

For Product/System Readiness v1, step 4 includes `.product-readiness.yml`. The agent MUST keep
multiple Subjects independent and MUST NOT calculate a repository-wide TRL.

## Updating prompts and migrations

The bootstrap normally stays unchanged because declaration and adapter selection are version-aware.
When a repository changes declaration or pinned standard versions, update the declaration through a
reviewed migration and re-run its contract checks.

For Product/System Readiness adoption, follow `docs/repository-contract-v11-migration.md` and
`docs/ticket-standard-v5-migration.md`. Do not synthesize historical Product Stage, targets,
assessments, or readiness state during migration.

Long-lived prompt text SHOULD NOT hard-code a Ticket Specification, Development Workflow,
Repository Documentation, Product/System Readiness, Web Application Baseline, or Deployment
Environments version unless the prompt is intentionally bound to that exact released contract set.
