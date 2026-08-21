# Ticket-based Development Workflow v1

## Source of truth

Every implementation starts from a ticket. The complete ticket description and all comments MUST be read before work begins. The latest explicit requirement wins when statements conflict.

## Ticket state

The ticket MUST be marked in progress when the implementation branch is created. It MUST remain in progress until the implementation is merged and verified. It may be marked done only after the branch is closed and all acceptance criteria are satisfied.

## Branch names

Ticket branches use one of these forms:

```text
<type>/<ticket-number>-<ticket-title-slug>
<type>/<repository>-<ticket-number>-<ticket-title-slug>
```

The repository-qualified form uses the exact repository name containing the ticket. Slugs are lowercase ASCII with hyphens and no spaces.

Type prefixes are `feature`, `enhancement`, `bugfix`, `hotfix`, `refactoring`, `maintenance`, `documentation`, `security`, `test`, and `research`.

## Pull requests

A ticket-linked pull request title MUST start with `#<ticket-number>`. It is ready for review by default. Draft status is used only when explicitly requested or when the pull request intentionally communicates incomplete work.

The pull request MUST describe:

- the implemented scope;
- acceptance-criteria coverage;
- validation performed;
- documentation impact;
- security, compatibility, release, and deployment impact where applicable.

## Documentation impact declaration

Every pull request MUST choose exactly one outcome:

1. affected documentation was updated in the same pull request; or
2. no documentation update is required, with a concrete explanation.

The declaration MUST consider all repository-owned documentation. It MUST NOT be satisfied by changing an unrelated Markdown file.

## Forgejo automation

Forgejo is the leading source-control and automation system. Active Forgejo Actions workflows MUST be stored in `.forgejo/workflows/`. Executable workflow files MUST NOT remain in `.github/workflows/`.

The `.github/` directory MAY contain non-executable compatibility metadata needed by mirrors or external consumers. GitHub-specific or historical one-shot automation MUST be ported, removed, or archived outside the active Forgejo workflow path.

Forgejo workflows MUST use Forgejo events, API semantics, and `FORGEJO_*` context where applicable. Referenced actions MUST use fully qualified trusted URLs. Workflow runtime dependencies MUST be declared explicitly, and workflows intended for organization runners MUST support ARM64.

## Definition of Done

Work is done only when:

- all current ticket requirements and acceptance criteria are implemented;
- tests, static checks, contracts, and required external checks pass;
- the complete `docs/` tree was assessed and affected documents were updated;
- architecture changes are reflected in architecture documentation;
- durable decisions are recorded or superseded through ADRs;
- configuration, compatibility, installation, upgrade, release, deployment, and operations guidance is current;
- no known placeholder, temporary bypass, or undocumented manual step remains;
- the pull request is merged and the resulting main-branch build is successful where applicable.

## Review and merge

Review MUST assess correctness, maintainability, tests, documentation, security, compatibility, and operational safety. Passing automation does not replace review of semantic documentation drift.

Automated dependency pull requests without a project ticket MAY be exempt from ticket naming, but they remain subject to repository checks and documentation-impact assessment.
