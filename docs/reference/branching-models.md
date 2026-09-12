# Branching models

## Repository bootstrap decision

Every repository bootstrap decides whether a `develop` branch is used. The answer selects one
versioned branching model in `.repository-standards.yml` through a supported repository-declaration
pairing.

Branching semantics are versioned by Development Workflow. A consumer must resolve the workflow
version from its complete compatibility pairing instead of assuming that the newest published
workflow applies to every repository.

## Single model

`main` is both integration and release branch.

```text
ticket branch -> pull request -> main
```

Regular ticket branches start from `main` and pull requests target `main`, subject to the selected
Development Workflow and Ticket Specification contracts.

## Integration model

`develop` is the integration branch and `main` is the release branch.

```text
ticket branch -> pull request -> develop
develop -> manual release pull request -> main
```

Regular ticket branches start from and return to `develop`. Release promotion to `main` follows the
selected workflow contract. Protected delivery branches use their required quality gates according
to that contract.

## Jenkins discovery

Normal Jenkins Multibranch Pipeline projects use:

```regex
^(main|develop|PR-[0-9]+)$
```

The filter is retained by the released workflow/declaration pairings that specify it. Jenkins is an
implementation provider; the portable branching semantics remain defined by the selected Development
Workflow.

## Hotfix

A Hotfix starts from `main`, returns to `main`, and is reintegrated into `develop` when the
integration model is active, according to the selected workflow's Hotfix requirements.

## Compatibility and workflow evolution

The current additive compatibility matrix is:

`profiles/repository-standards-compatibility-v10.json`

It preserves all released declaration/workflow pairings through declaration v11. The latest supported
v11 pairing selects Development Workflow v8. Earlier consumers continue to use the workflow version
selected by their immutable declaration pairing; publication of v8 did not rewrite v1-v10 consumers.

Development Workflow evolved additively across the released pairings. Later versions add lifecycle,
quality-gate, supersession, and Contract-first Delivery semantics without making documentation
statements about an older pairing authoritative for a newer one.

For exact combinations, always use the compatibility profile rather than maintaining a second manual
list here. See `docs/reference/compatibility.md`.

## Provider status identities

Logical required checks are part of the portable workflow contract where defined. Concrete status
identities are provider adapters. For example, Forgejo/Gitea Actions may include the event in the
concrete check identity, while GitHub has different status-check identity semantics.

A provider-specific status name must not be treated as the normative workflow requirement itself.
Changes to provider event models or check names therefore require coordinated adapter/protection
updates without silently changing the selected Development Workflow contract.
