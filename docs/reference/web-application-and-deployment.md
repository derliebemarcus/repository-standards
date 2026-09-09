# Web Application and Deployment Interaction Model

## Purpose

Web Application Baseline and Deployment Environments are separate contracts with one shared
boundary: immutable artifact provenance. The web baseline defines what a website exposes to users;
the deployment standard defines how an artifact moves through runtime environments.

Published baseline and deployment versions remain immutable. Consumers select only explicitly
supported declaration pairings.

## Three independent dimensions

A deployment must retain three independent facts:

| Dimension | Examples | Meaning |
| --- | --- | --- |
| Source | `feature/*`, `develop`, `main`, tag/source revision | Where the build started |
| Artifact release state | `non-release`, `release-candidate`, `release` | What the built artifact is |
| Runtime environment | DEV, STAGE/STAGING, PROD | Where the existing artifact runs |

An environment never changes artifact release state. A branch name never proves that an artifact is
a final release.

## Default environment mapping

The default DEV source follows the selected Development Workflow branching model:

- `single`: `main` is the integration branch and default DEV source;
- `integration`: `develop` is the integration branch and default DEV source.

Preview or pull-request builds are build contexts and are not canonical shared environments.
Deployment Environments v1 uses optional `STAGE`; Deployment Environments v2 uses optional
`STAGING`. PROD accepts only an immutable final-release artifact.

## Artifact release states and public provenance

The artifact-producing pipeline creates one immutable provenance record. At minimum it identifies the
source commit, build number, build time, release state, and release version when applicable.

Web Application Baseline v1/v2 renders the state-appropriate public subset in the global footer of
`/impressum`, `/datenschutz`, and `/barrierefreiheit`:

| State | Public rendering |
| --- | --- |
| `non-release` | Commit · Build number · Build time |
| `release-candidate` | Release version · Build number · Build time |
| `release` | Release version |

Web Application Baseline v3 preserves the same provenance matrix but applies it to every canonical
language-prefixed form of the three stable route IDs.

## Web Application Baseline v3 multilingual routing

WAB v3 replaces only the v1/v2 canonical-route location. Canonical user-facing content uses:

```text
/<ISO-639-1>/<stable-route-id>
```

For example, a German/English consumer exposes:

```text
/de/impressum
/en/impressum
/de/datenschutz
/en/datenschutz
/de/barrierefreiheit
/en/barrierefreiheit
```

`impressum`, `datenschutz`, and `barrierefreiheit` are stable route identifiers. They are not
translated in canonical URLs. A localized alias such as `/en/privacy` may exist, but it is
non-canonical and points to `/en/datenschutz`.

A v3 consumer owns `.repository-localization.yml`, which declares the supported lowercase ISO 639-1
codes and exactly one default language. The root `/` redirects to a supported language; request
language negotiation may select a supported language, otherwise the declared default is used.
Unsupported namespaces do not silently receive another language's content in place.

The URL namespace remains ISO 639-1. More specific BCP 47 metadata such as `de-CH` may be used at
runtime or in `html[lang]` without changing `/de/` into a regional URL namespace.

For publicly indexable language variants, each variant has its own canonical URL and equivalent
variants expose consistent `hreflang` relationships. Language switching preserves the stable route
identifier where an equivalent target exists; this is mandatory for the three baseline routes.

The prefix contract applies to canonical user-facing content routes, not automatically to APIs,
health endpoints, callbacks, or static assets.

## Example: single branching model

A normal `main` build produces a `non-release` artifact unless the release process explicitly creates
a release candidate or final release. The artifact may be deployed to DEV.

A final release is an immutable artifact selected by the release process. Only that artifact may be
promoted to PROD. A later `main` commit does not retroactively change the deployed release identity.

## Example: integration branching model

A normal `develop` build produces a `non-release` artifact for DEV. The selected Development Workflow
controls release promotion from `develop` to `main`.

A release candidate may be deployed to DEV or an optional staging environment. A final release
artifact may be verified there and promoted unchanged to PROD.

## Rollback

Rollback selects a previously released immutable artifact. It does not rebuild historical branch
state. Consequently the public provenance shown after rollback is the provenance embedded in that
released artifact rather than metadata from the current repository head.

## Design and accessibility

The required static pages are part of the user-facing application, not a detached legal microsite.
They use the same application shell, design conventions, responsive behavior, and accessibility
quality gates as the rest of the website.

If `.design-system-consumer.json` declares `decision: use`, the pages use the same active Design
System integration. If the repository deliberately declares `decision: do-not-use`, the pages use
the repository's own shared application design.

WAB v3 additionally requires `html[lang]` to match the delivered language and requires normal
accessibility semantics for language switching and material passages in another language.

## Validation boundary

Repository Standards defines normative and machine-readable rules. `siczb/maintenance` owns shared
build metadata generation and may implement generic CI/deployment enforcement. A consumer must not
enable a newer declaration or WAB version until the selected enforcement is compatible and qualified.

For WAB v3, `.repository-localization.yml` must also validate before activation. Missing language
metadata must fail closed instead of being inferred from application routes.
