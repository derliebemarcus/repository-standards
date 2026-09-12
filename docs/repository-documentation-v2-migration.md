# Repository Documentation v2 migration

## Purpose

Repository Documentation v2 is the explicit adoption boundary for the document-type semantics added
for Repository Standards v8.0.0. It preserves Repository Documentation v1 as an immutable released
contract and does not apply v2 requirements retroactively.

The normative v2 specification is
[`standards/repository-documentation/v2/standard.md`](../standards/repository-documentation/v2/standard.md).
The explanatory guidance under [`docs/repository-documentation/`](repository-documentation/index.md)
is non-normative.

## What changes from v1 to v2?

v2 makes the information-task model operational rather than relying mainly on directory categories
and broad minimum-content requirements. It adds explicit normative semantics and purpose-specific
quality criteria for:

- Tutorial;
- How-to Guide;
- Reference;
- Explanation;
- Architecture;
- Decision / ADR;
- Operations / Runbook;
- Verification / Evidence; and
- Index / Navigation.

It also makes Verification / Evidence a distinct point-in-time evidence class and explicitly separates
it from durable current Reference, Architecture, and Operations documentation.

The v1 maintenance policy, architecture/ADR concepts, Design System decision requirement, bootstrap
principles, and objective validation approach are carried forward in v2.

## What existing documents do not need to change?

A repository that remains pinned to Repository Documentation v1 does not need to change anything
because v2 was published. Its v1 declaration, profile, schema, and requirements continue to apply.

Even when a repository chooses to migrate to v2, an existing document does not need rewriting merely
to become longer, to adopt a new directory name, or to copy normative wording. If the document
already fulfills the v2 information task for its type and remains correctly navigated and
maintained, it may remain unchanged.

## When is a short document still conformant?

A short document is conformant when it completely performs its information task.

Examples include:

- an Index that provides the necessary entry points and authority cues in a few lines;
- an Evidence record whose only purpose is to identify one build/revision, method, result, provenance,
  and validity boundary; or
- a compact Reference page whose narrow scope is completely and precisely covered.

v2 introduces no minimum word count, line count, heading count, or comparable editorial proxy.
Conversely, a heading-only or bullet-fragment content page is not complete when its information task
requires explanation, executable instructions, architecture substance, or operational safety detail.

## How are existing verification artifacts handled?

Historical verification artifacts may be retained. They do not need to be rewritten solely because
v2 names Verification / Evidence explicitly.

During migration, identify evidence that could reasonably be mistaken for current Reference,
Architecture, or Operations documentation. Correct navigation or labeling so that its bounded
revision/time and evidentiary role are clear. Add missing provenance, method, result identity, or
validity information when the artifact is expected to satisfy the v2 Verification / Evidence
criteria going forward.

Do not update an old evidence record to pretend that it proves the current state. Create new evidence
for a new revision, build, test, audit, or release.

## Must the existing `docs/` structure be rebuilt?

No. v2 document types describe information tasks, not mandatory directory names. Repositories may
retain an existing structure if document purposes, navigation, required profile content, and authority
boundaries remain clear.

A structure such as `docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/`,
`docs/architecture/`, `docs/decisions/`, `docs/operations/`, and `docs/verification/` is useful but is
not independently mandatory.

## Which requirements are new?

The breaking semantic additions are the v2 document-type definitions, their purpose-specific quality
criteria, the explicit distinctions between types, and the Verification / Evidence validity model.
A repository declaring v2 is expected to apply those semantics to documentation tasks that exist in
that repository.

The machine-readable v2 declaration schema itself deliberately remains small. Subjective editorial
quality is not converted into schema fields or automatic word-count checks.

## What can consumers adopt gradually?

Before changing the declaration, consumers may non-disruptively:

1. classify existing pages by information task;
2. improve navigation and authority cues;
3. separate current Reference from historical evidence;
4. add missing Verification provenance and validity boundaries to new evidence;
5. improve runbook stop/rollback/recovery content where operational risk requires it; and
6. align Architecture and ADR navigation with arc42-lite, C4, and MADR roles.

These preparatory improvements do not change the consumer's normative version. The binding migration
occurs only when the repository explicitly adopts a supported Repository Standards declaration pairing
that selects Repository Documentation v2. Declaration v8 was the original adoption boundary; later
supported pairings may preserve the same Repository Documentation v2 selection.

## Breaking vs. non-breaking changes

### Breaking contract change

Selecting Repository Documentation v2 is a breaking semantic migration because v2 adds obligations
that v1 consumers did not previously have. That is why v1 is not modified and why declaration v8 was
introduced as a separate original compatibility boundary.

### Non-breaking preparation

Improving a v1 consumer's documentation in ways that are already compatible with v1 — clearer
navigation, better architecture detail, more complete runbooks, or explicit evidence provenance — is
not itself a contract migration.

## Required declaration and compatibility boundary

A consumer that adopts Repository Documentation v2 must use a released Repository Standards pairing
that selects Repository Documentation v2 and is `supported` by the compatibility matrix pinned for
that consumer. The current additive compatibility reference is
`profiles/repository-standards-compatibility-v10.json`; it preserves the earlier supported pairings
and must be used instead of assuming that declaration v8 is the only valid adoption path.

Declaration v8 was the original Repository Documentation v2 adoption boundary. Its canonical
references remain immutable historical/released references:

- `reference/repository-standards-v8.single.yml`;
- `reference/repository-standards-v8.integration.yml`;
- `reference/repository-standards-v8.web.single.yml`; and
- `reference/repository-standards-v8.web.integration.yml`.

The original additive compatibility profile was
`profiles/repository-standards-compatibility-v7.json`. It remains immutable evidence of the initial
v8 pairing. Unsupported combinations still fail closed; in particular, the original negative
examples remain valid: declaration v7 must not be combined with Repository Documentation v2 and
declaration v8 must not be combined with Repository Documentation v1. Later declaration generations
must follow their own released compatibility pairings.

The corresponding `.repository-documentation.yml` declaration selects `standard_version: 2` and a
`2.x` ruleset such as `2.0.0`.

## Maintenance and CI boundary

Repository Standards defines the portable contract. Jenkins is one implementation and is not
required to interpret, adopt, or validate Repository Documentation v2 locally or in another CI
system.

Where a consumer depends on `siczb/maintenance` for blocking enforcement or migration writes, it
must not activate its selected Repository Standards pairing until a compatible Maintenance release
advertises and validates that pairing. This operational compatibility requirement does not make
Jenkins normative.

## Rollback

If a consumer migration cannot be qualified safely, restore its previously pinned repository and
documentation declarations. Do not modify v1 artifacts or compatibility profiles to make the failed
migration appear supported. Evidence produced during the attempted migration may be retained as
historical evidence when clearly labeled with its scope and result.
