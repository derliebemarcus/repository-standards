# Branching models

## Repository bootstrap decision

Every repository bootstrap asks whether a `develop` branch is used. The answer selects one
versioned model in `.repository-standards.yml`.

The branching semantics are unchanged between Development Workflow v2 and v3. The workflow version
instead identifies which Ticket Specification and repository-declaration schema are compatible with
those semantics.

## Single model

`main` is both integration and release branch.

```text
ticket branch -> pull request -> main
```

Regular branches start from `main` and pull requests target `main`.

## Integration model

`develop` is the integration branch and `main` is the release branch.

```text
ticket branch -> pull request -> develop
develop -> manual release pull request -> main
```

Regular branches start from and return to `develop`. Release promotion is manually created and
manually merged. `main` and `develop` use equivalent protection and quality gates.

## Jenkins discovery

Normal Jenkins Multibranch Pipeline projects use:

```regex
^(main|develop|PR-[0-9]+)$
```

The filter is valid for both models and both currently supported workflow contract sets.

## Hotfix

A Hotfix starts from `main`, returns to `main`, and is then reintegrated into `develop` when the
integration model is active.

## Compatible workflow versions

- Declaration schema v1 + Ticket Specification v1 uses Development Workflow v2.
- Declaration schema v2 + Ticket Specification v2 uses Development Workflow v3.

Development Workflow v3 normatively incorporates the unchanged branching, release, protection,
Hotfix, and manual-main-build requirements of v2 while adding the Ticket Specification v2 lifecycle
integration contract.

See `docs/reference/compatibility.md` for the machine-readable pairing boundary.
