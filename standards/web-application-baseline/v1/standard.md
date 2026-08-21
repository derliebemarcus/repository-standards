# Web Application Baseline v1

## Status and scope

This standard defines the minimum delivery baseline for organization-owned user-facing websites and
web applications that explicitly adopt it. It does not apply automatically to third-party
operational products such as Forgejo, Jenkins, or SonarQube.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174. Lowercase occurrences are non-normative.

The standard defines required static informational pages, navigation and visual integration,
accessibility-statement structure, and public build/release provenance. It does not replace legal
review and MUST NOT be interpreted as proof that application-specific legal text is complete.

## Required static pages

An adopting website MUST provide these stable internal routes:

- `/impressum` for the imprint/provider information;
- `/datenschutz` for the privacy information;
- `/barrierefreiheit` for the accessibility statement.

The routes MUST be reachable without authentication and MUST return the normal successful page
representation for the deployed website. Redirects MAY be used only when the canonical destination
remains the required route visible to the user.

The three destinations MUST be linked from the website's global footer or equivalent persistent
global navigation. They are internal destinations and MUST open in the same browsing context.

The pages are static informational pages: their legal/editorial content MUST NOT depend on a user
account, personalization, or mutable application state. They MAY be rendered through the same
application framework and shell as other pages.

## Legal-content ownership

The owning application MUST provide project-specific content appropriate to its operator,
processing activities, jurisdiction, and current functionality. Structural validation of this
standard MUST NOT claim legal compliance or invent missing legal facts.

A consumer MUST update the affected page in the same change when functionality, operator data,
processing behavior, accessibility status, or another fact makes existing page content inaccurate.

## Visual and interaction integration

The required pages MUST use the same design language and application shell as the primary website.
At minimum this includes the applicable typography, color system, spacing, responsive behavior,
navigation, footer, focus treatment, and component conventions.

When the repository declares `decision: use` for `siczb/design-system`, the required pages MUST use
the same active Design System integration as the rest of the website. When the repository declares
`decision: do-not-use`, the pages MUST use the repository's own shared website design rather than a
separate legal-page theme.

A consumer MUST NOT satisfy this standard by attaching visually unrelated standalone HTML pages to
an otherwise styled application.

The required pages MUST satisfy the same accessibility quality gates as the rest of the website.
Responsive behavior, keyboard operation, focus visibility, semantic structure, and text contrast
MUST be covered by the consumer's applicable quality checks.

## Accessibility statement minimum structure

`/barrierefreiheit` MUST identify:

- the website or application covered by the statement;
- the applicable accessibility target and current conformance status;
- known limitations or a statement that no known limitations are currently recorded;
- available alternatives or workarounds for material known limitations where applicable;
- a feedback/contact path for accessibility barriers;
- the statement preparation date or last review date.

Jurisdiction-specific enforcement, arbitration, supervisory, or statutory wording MUST be included
when applicable to the consumer, but this standard MUST NOT invent or hard-code a jurisdiction for
all consumers.

## Artifact provenance

Public provenance MUST be derived from metadata embedded in or bound immutably to the built
artifact. Deployment automation MUST NOT reconstruct public provenance from the currently checked
out branch, a later repository state, or environment name.

Every web artifact has exactly one release state:

- `non-release`;
- `release-candidate`;
- `release`.

The release state is independent of the runtime environment.

The canonical provenance fields are:

- `commit`: short Git commit SHA for the built source revision;
- `build_number`: build-system identifier of the artifact-producing build;
- `build_time`: artifact build time represented as ISO-8601 with an explicit timezone;
- `release_version`: complete release identifier when the artifact is a release candidate or final
  release.

The full internal provenance record MAY contain additional fields. Public rendering MUST expose only
the fields required below and MUST NOT expose secrets, credentials, internal filesystem paths, or
other operationally sensitive metadata.

## Public provenance rendering

The global footer of `/impressum`, `/datenschutz`, and `/barrierefreiheit` MUST render provenance
according to the artifact release state.

| Artifact release state | Required public footer content |
| --- | --- |
| `non-release` | Commit · Build number · Build time |
| `release-candidate` | Release version · Build number · Build time |
| `release` | Release version |

For `non-release`, `commit`, `build_number`, and `build_time` MUST be present. `release_version` MUST
NOT be presented as if the artifact were released.

For `release-candidate`, `release_version`, `build_number`, and `build_time` MUST be present. The
release version MUST preserve the complete release-candidate identifier, including the RC suffix.

For `release`, `release_version` MUST be present. Commit, build number, and build time MUST NOT be
rendered in the public footer, even when they remain available internally for audit or rollback.

The human-readable build time MAY be localized, but the markup MUST also contain an ISO-8601 value
with timezone, for example through an HTML `time` element with a `datetime` attribute.

A short commit SHA SHOULD use the repository's normal unambiguous abbreviation length and MUST
identify exactly the source revision bound to the artifact.

## Release-version semantics

Artifact Provenance v1 release versions MUST use semantic versioning. A final release MUST use the
form `X.Y.Z`, and a release candidate MUST use the complete form `X.Y.Z-rc.N`. SemVer build metadata
MAY be appended. A final release MUST NOT be inferred merely from a branch name or environment.

The build pipeline is authoritative for artifact release state. A deployment to DEV or STAGE MUST
NOT transform a non-release artifact into a release candidate, and deployment to PROD MUST NOT
transform an unreleased artifact into a release.

## Validation contract

For an adopting deployable website, contract failures MUST block the applicable release/deployment
gate.

Validation MUST check at least:

- the three canonical routes exist and are reachable without authentication;
- all three are reachable through internal same-context global navigation;
- all three use the website's normal application shell/design integration;
- the accessibility statement contains the required structural information;
- the pages are included in the normal accessibility quality checks;
- exactly one artifact release state is present;
- required provenance fields exist for that state and public rendering matches the state matrix;
- build time is machine-readable with timezone when it is publicly required;
- final-release public rendering omits commit, build number, and build time.

Visual-integration validation MAY use component/shell assertions, visual regression, or another
repeatable consumer-specific mechanism. A generic validator MUST NOT declare design consistency
solely from route existence.

## Consumer adoption

Adoption MUST be explicit through a released repository declaration schema that lists
`web-application-baseline: v1`. Consumers MUST remain pinned until an explicit migration is made.

Runtime enforcement and build metadata generation are implementation responsibilities of the
consumer CI/CD contract and `siczb/maintenance`, not this standards repository.
