# Web Application Baseline v3

## Status and scope

Web Application Baseline v3 supersedes v2 only for repositories that explicitly adopt v3. It
incorporates every normative requirement of Web Application Baseline v2 except where this document
explicitly replaces the v1/v2 canonical-route model with the multilingual route model below.

The standard remains opt-in through a compatible Repository Standards declaration. Existing v1 and
v2 consumers remain unchanged.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174.

## Source of truth

The normative source is this document together with `standards/web-application-baseline/v2/standard.md`
and, transitively, `standards/web-application-baseline/v1/standard.md`, except for the route
requirements explicitly superseded below. The complete machine-readable representation is
`profiles/web-application-baseline-v3.json`.

Web Application Baseline v3 requires Contract-first Delivery v1, Ticket Specification v4,
Development Workflow v8, and Repository Localization v1.

## Superseded canonical-route model

The v1 requirement that `/impressum`, `/datenschutz`, and `/barrierefreiheit` themselves are the
canonical static routes is superseded by this section. All other v1 requirements for those pages,
including unauthenticated access, global navigation, shared application design, accessibility,
content ownership, and artifact provenance, remain in force for their v3 language-prefixed forms.

## Canonical multilingual route model

A canonical user-facing content route MUST begin with exactly one supported lowercase ISO 639-1
language code and MUST use the form:

```text
/<language>/<stable-route-id>
```

The language code MUST be declared by Repository Localization v1 and MUST be a current ISO 639-1
alpha-2 identifier. Uppercase codes, regional tags such as `de-CH`, unknown two-letter strings, and
undeclared ISO 639-1 codes MUST NOT be accepted as canonical language namespaces.

The URL language namespace identifies the content language. Route identifiers are stable semantic
identifiers and MUST NOT be localized merely because the content language changes.

The required baseline route identifiers are:

- `impressum`;
- `datenschutz`;
- `barrierefreiheit`.

For every declared supported language, an adopting website MUST therefore provide:

```text
/<language>/impressum
/<language>/datenschutz
/<language>/barrierefreiheit
```

For example, a German/English consumer provides `/de/datenschutz` and `/en/datenschutz`. It does not
use `/en/privacy` as the canonical representation of that baseline route.

Localized aliases such as `/en/privacy` MAY exist for compatibility or usability. An alias MUST NOT
be advertised as canonical and MUST either redirect to the stable canonical route in the same
language or otherwise expose the stable route as its canonical destination.

## Scope of the language namespace

The language-prefix requirement applies to canonical user-facing content routes. It MUST NOT by
itself require language prefixes for APIs, health endpoints, machine-only callbacks, static assets,
or other non-content technical endpoints.

A consumer MAY define additional stable user-facing route identifiers. When it does, the same
language namespace and stable-identifier rules SHOULD be applied consistently across the public
content surface.

## Repository Localization declaration

A v3 web consumer MUST provide Repository Localization v1 at `.repository-localization.yml`.
The declaration MUST identify:

- one non-empty set of supported ISO 639-1 language codes; and
- exactly one default language that is a member of that set.

The declaration is repository-owned and versioned with the application. Supported languages MUST
NOT be guessed from existing routes, browser preferences, deployment geography, or design artifacts.

An undeclared language MUST NOT silently receive content in another language under the undeclared
language URL.

## Root and language negotiation

The unprefixed root `/` is not a canonical content-language representation under v3. It MUST redirect
to exactly one declared supported language root.

A consumer MAY use request-language negotiation to select that target when the selected language is
supported. When no supported preference can be selected deterministically, the consumer MUST redirect
to the declared default language.

Negotiation MUST NOT cause an unsupported or malformed language namespace to serve default-language
content while preserving the unsupported namespace in the URL.

Unprefixed legacy content routes such as `/datenschutz` MAY redirect to a language-prefixed canonical
route. They MUST NOT remain independent canonical representations after v3 adoption.

## Navigation and language switching

Global navigation and footer links MUST preserve the current language when linking to another
localized user-facing route, unless the interaction itself is explicitly a language change.

A language switch SHOULD preserve the current stable route identifier when an equivalent target
exists. For `impressum`, `datenschutz`, and `barrierefreiheit`, every supported language has an
equivalent target by definition, so the language switch MUST preserve the route identifier.

Language-switch controls MUST be operable and understandable under the repository's normal
accessibility gates. A language name or code MUST NOT rely on color, iconography, or flag imagery
alone to convey the selected language.

## Document language and language changes

The rendered document's `html[lang]` value MUST identify the language actually delivered by the
canonical route. The value MAY be a more specific valid BCP 47 language tag, such as `de-CH`, when
the delivered content requires regional metadata, but the canonical URL namespace remains the
corresponding ISO 639-1 code such as `/de/`.

Material passages in another language MUST use appropriate language semantics where required by the
repository's accessibility target. URL language alone MUST NOT be treated as sufficient accessibility
evidence.

## Canonical and alternate-language relationships

For publicly indexable content, each language-specific page MUST identify its own canonical URL.
Equivalent localized pages MUST expose consistent alternate-language relationships using valid
`hreflang` values. An `x-default` alternate MAY identify the root or another neutral fallback when
that matches the consumer's actual navigation behavior.

A localized alias MUST NOT create a competing canonical identity for the same language and semantic
route.

## Contract-first route conformance

All Web Application Baseline v2 Contract-first Delivery requirements remain in force. For UI changes
that affect localized routing, language negotiation, language switching, navigation, rendered
language, or localized page states, the Design Contract and Test Contract MUST identify the relevant
language state in addition to the other applicable v2 dimensions.

The Test Contract MUST cover enough language states to demonstrate that:

- the declared default language and supported-language set are honored;
- required baseline routes exist for every supported language;
- unsupported language namespaces fail closed rather than silently falling back in place;
- language switching preserves the semantic route where required;
- `html[lang]`, canonical identity, and alternate-language relationships match the delivered state;
  and
- technical non-content endpoints are not accidentally rewritten solely by the multilingual route
  contract.

Consumer-specific language fixtures, translations, route implementations, and SEO metadata remain
consumer-owned. Shared automation MAY validate the portable route and declaration invariants.

## Artifact provenance and required pages

The v1 artifact-provenance rules continue to apply to the language-prefixed baseline pages. Where v1
refers to `/impressum`, `/datenschutz`, and `/barrierefreiheit`, v3 applies that obligation to every
corresponding `/<language>/<stable-route-id>` canonical page.

The legal/editorial content remains project-specific. This standard MUST NOT invent missing operator,
privacy, accessibility, jurisdiction, or translation facts.

## Consumer activation

A repository MUST NOT activate Web Application Baseline v3 until:

- a compatible Repository Standards declaration selecting v3 is adopted;
- `.repository-localization.yml` satisfies Repository Localization v1;
- selected Contract-first and web-conformance automation can enforce the v3 routing and language
  invariants fail closed; and
- the repository has an explicit migration plan for any previously canonical unprefixed routes.

Publication of v3 MUST NOT modify or reinterpret Web Application Baseline v1 or v2 consumers.