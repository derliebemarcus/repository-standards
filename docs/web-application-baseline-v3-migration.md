# Web Application Baseline v3 migration

## Purpose

Web Application Baseline v3 changes the canonical location of user-facing content routes. It is an
explicit migration, not a reinterpretation of WAB v2.

WAB v1/v2 remain immutable and keep `/impressum`, `/datenschutz`, and `/barrierefreiheit` as their
canonical routes. WAB v3 uses `/<ISO-639-1>/<stable-route-id>`.

## Preconditions

Before adopting v3, a repository must:

1. use a released Repository Standards package containing Declaration v10, WAB v3, and Repository
   Localization v1;
2. materialize `.repository-localization.yml` with verified supported languages and one default;
3. ensure the three baseline pages have accurate content in every declared supported language;
4. define redirects or another explicit disposition for previously canonical unprefixed routes;
5. qualify language routing, switching, accessibility, canonical URLs, and `hreflang` under the
   repository's Contract-first Test Contract; and
6. ensure selected CI/runtime enforcement can fail closed on declaration and deployed-revision
   mismatches.

## Canonical route migration

For a German/English consumer:

```text
v2 canonical             v3 canonical
/impressum                /de/impressum, /en/impressum
/datenschutz              /de/datenschutz, /en/datenschutz
/barrierefreiheit         /de/barrierefreiheit, /en/barrierefreiheit
```

The route IDs remain stable across languages. Do not migrate `/en/datenschutz` to `/en/privacy` as
the canonical route. A localized alias may redirect to the stable canonical route.

## Root and legacy routes

`/` becomes a language-selection redirect. It may select a supported request language and otherwise
falls back to the declared default language.

Legacy unprefixed content routes may redirect to a selected language-prefixed route. They cease to be
canonical after v3 activation. An unsupported namespace such as `/zz/datenschutz` must not serve the
default language while preserving `/zz/` in the URL.

## Repository Localization v1

Example:

```yaml
version: 1
web-application-baseline: v3
default-language: de
supported-languages:
  - de
  - en
```

Validate before activation:

```text
python tools/repository_localization.py .repository-localization.yml
```

Supported languages are repository-owned facts. Do not infer them from routes, translation files,
Penpot frames, browser preferences, or deployment geography.

## Declaration v10

Declaration v9 remains pinned to WAB v2. WAB v3 adoption uses a compatible Declaration v10 web
pairing. The core v10 pairing remains available for non-web repositories and does not require the
localization sidecar.

A WAB v3 consumer must not activate the v10 web pairing unless Repository Localization v1 validates
and the consumer can enforce the selected Contract-first/web conformance classes.

## SEO and accessibility migration

For publicly indexable variants:

- make each language-specific URL self-canonical;
- emit consistent `hreflang` relationships for equivalent variants;
- use `x-default` only when it represents actual neutral/root fallback behavior;
- make `html[lang]` match delivered content; and
- expose accessible language-switch controls and language semantics for material foreign-language
  passages.

## Technical routes

Do not blanket-prefix APIs, health checks, callbacks, or assets. WAB v3's prefix obligation applies
to canonical user-facing content routes.

## Rollback

Rollback restores the previous released declaration and WAB pairing together with its route
contract. Do not create a mixed state in which Declaration v9 is interpreted with v3 routes or
Declaration v10 web is used without valid Repository Localization v1 metadata.

## Pull-request qualification note

The final pull-request revision must be qualified by the repository's configured required checks
under their provider-specific pull-request identities before merge. A manually dispatched validation
run is supplemental evidence and does not substitute for a required `pull_request` check context.
