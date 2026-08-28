# Repository Standards v9 migration

## Scope

Repository Standards v9 is the adoption boundary for Contract-first Delivery v1.

It combines:

- Ticket Specification v4;
- Development Workflow v8;
- Repository Documentation v2;
- Technology Baseline v1;
- Contract-first Delivery v1;
- Web Application Baseline v2 for web consumers; and
- Deployment Environments v1 for web consumers.

Repository Standards v8 remains immutable. Migration is explicit; publishing v9 does not change a v8 consumer.

## Preconditions

A repository MUST NOT activate declaration schema v9 until its actual ticket/lifecycle/CI integrations can enforce the selected Contract-first requirements fail-closed.

Before migration, verify:

1. the current declaration is valid and its current pairing remains green;
2. Ticket Specification v4 metadata can be created/read without destroying existing ticket content;
3. direct dependency handling can preserve the Design → Test → Implementation → Evidence graph where separate tickets are used;
4. required Contract references can be resolved to immutable/revisioned artifacts at `Status/Ready`;
5. Test Contract qualification can execute controlled negative cases and fail closed;
6. required conformance can bind Evidence to exact implementation revisions/artifacts;
7. stale Contract/Evidence states block forward lifecycle transitions and merge as required;
8. historical Evidence can be retained without being rewritten; and
9. provider-specific checks can map the logical gates `contract-graph`, `test-contract-qualification`, and `contract-conformance`.

For web applications additionally verify that required runtime and visual capabilities are consumer-qualified before enabling them.

## DEV readiness for web consumers

DEV does **not** need to exist before Design Contract or Test Contract authoring.

Recommended timing:

- Design/Test Contract work can start without DEV.
- DEV provisioning SHOULD happen in parallel and SHOULD be reliably deployable before implementation work begins.
- The exact implementation revision/artifact MUST be deployed before any required live-runtime, accessibility/reflow-on-runtime, or visual conformance Evidence is produced.
- `Status/Done` MUST NOT be reached while required runtime Evidence is absent or bound to another revision.

This avoids making infrastructure a prerequisite for specification while still preventing synthetic or stale UI evidence.

## Declaration migration

### Core, single branch

Use `reference/repository-standards-v9.single.yml`.

### Core, integration branch

Use `reference/repository-standards-v9.integration.yml`.

### Web, single branch

Use `reference/repository-standards-v9.web.single.yml`.

### Web, integration branch

Use `reference/repository-standards-v9.web.integration.yml`.

Do not combine v9 declaration schema with older Ticket/Workflow pairings. Unsupported combinations fail closed.

## Ticket migration

Ticket Specification v4 adds one mandatory structured `## Delivery contract` block.

For existing open tickets, classify Contract-first applicability based on actual scope. Do not blanket-mark tickets `not-applicable` merely to complete migration.

For applicable work:

- select the primary role;
- reference governing Design/Test Contract work;
- allow unresolved references only before Ready and only when a real `work_item` is identified;
- resolve exact artifacts before Ready;
- retain Evidence references after qualification.

Historical closed v1-v3 tickets do not need to be rewritten solely to look like v4 tickets. Migration tooling MUST NOT invent historical Contract artifacts or Evidence.

## Workflow migration

Development Workflow v8 preserves v7 behavior and adds Contract-first lifecycle gates.

The important transition boundary is `Status/Ready`:

- applicable implementation work may be planned earlier;
- all required Design/Test Contract work must be completed/qualified;
- all required Contract references must resolve to exact artifact identities;
- the resulting Contract Set is frozen;
- a later Contract change invalidates downstream qualification and must be handled explicitly.

Provider automation SHOULD move affected implementation work to `Status/Blocked` when a safe transition exists after invalidation.

## Web migration

Web Application Baseline v2 makes Contract-first Delivery required for user-visible UI impact and separates functional, accessibility, reflow/responsive, live-runtime, and visual conformance.

For Penpot-backed visual work:

- Penpot/design-source provenance remains normative;
- baseline screenshots are derived test artifacts;
- expected/actual/diff artifacts retain provenance;
- tolerances are bounded and reviewable;
- visual testing does not replace functional/accessibility/reflow testing.

## Rollout sequence

Recommended rollout:

1. deploy/update consumer tooling while the repository remains on v8;
2. run v9 validators in observation or non-authoritative qualification mode where safe;
3. qualify controlled positive and negative cases;
4. verify stale-contract and mismatched-revision failures;
5. verify web runtime/Penpot capabilities where applicable;
6. atomically change `.repository-standards.yml` to a canonical v9 declaration;
7. run all required checks against that exact revision;
8. merge only after v9 checks are green; and
9. qualify the target branch after merge.

## Rollback

If v9 activation fails before merge, retain the previous v8 declaration unchanged and fix the migration tooling or contracts on the feature branch.

Do not weaken Contract-first rules simply to make activation pass.

After v9 has been merged, reverting to v8 is an explicit standards downgrade and must be treated as a governed compatibility change rather than silently rewriting v9 ticket/evidence history.

## Maintenance relationship

Maintenance may implement reusable adapters/runners for the normative logical gates, including live DEV and Penpot visual conformance. Repository Standards defines required semantics and evidence; Maintenance implements automation.

Consumer readiness must be proven before v9 activation. The existence of a Maintenance capability alone is not evidence that a consumer is correctly wired to it.