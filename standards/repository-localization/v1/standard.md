# Repository Localization v1

## Status and scope

Repository Localization v1 defines repository-owned language metadata for applications that need a
stable, machine-readable set of supported content languages and one deterministic default language.
It is introduced for Web Application Baseline v3 but is independently versioned.

The canonical declaration path is `.repository-localization.yml`.

## Normative language

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and
RFC 8174.

## Source of truth

The normative source is this document. The machine-readable representation is
`profiles/repository-localization-v1.json`, and declaration shape is defined by
`schemas/repository-localization-v1.schema.json`.

## Declaration shape

The declaration MUST have exactly this logical shape:

```yaml
version: 1
web-application-baseline: v3
default-language: de
supported-languages:
  - de
  - en
```

The root MUST contain exactly:

- `version` with value `1`;
- `web-application-baseline` with value `v3`;
- `default-language` with one lowercase ISO 639-1 language code; and
- `supported-languages` with a non-empty unique list of lowercase ISO 639-1 language codes.

Unknown fields MUST fail validation.

## Language identity

Every language identifier in the declaration MUST be a valid ISO 639-1 alpha-2 code in lowercase.
A syntactically two-letter value that is not assigned by ISO 639-1 MUST be rejected. Uppercase,
mixed-case, three-letter, private-use, and regional BCP 47 identifiers MUST be rejected by this
contract.

The declaration controls the canonical URL language namespace, not the complete locale model. A
consumer MAY use a more specific BCP 47 tag such as `de-CH` internally for formatting, collation,
translation selection, or `html[lang]`, provided the canonical URL namespace remains the declared
ISO 639-1 code such as `de`.

## Supported and default languages

`supported-languages` MUST contain at least one entry and MUST NOT contain duplicates.

`default-language` MUST occur exactly once in `supported-languages`.

The order of `supported-languages` MAY be used for deterministic presentation, but MUST NOT override
`default-language` as the fallback language.

A repository MUST NOT infer supported languages from route discovery, file names, browser language,
deployment location, translation catalogs, or design sources when this declaration is present.

## Relationship to Web Application Baseline v3

A consumer adopting Web Application Baseline v3 MUST adopt Repository Localization v1.

Each `supported-languages` value becomes a permitted canonical language namespace for user-facing
content routes. A language that is valid ISO 639-1 but absent from the declaration remains unsupported
for that consumer and MUST NOT receive another language's content under its own namespace.

The default language supplies the deterministic fallback required by the WAB v3 root redirect when
request-language negotiation does not select another declared supported language.

## Responsibility and content boundary

This contract declares language identity only. It MUST NOT be treated as evidence that translations
exist, are complete, are legally accurate, or have been reviewed.

Consumer repositories remain responsible for translation content, locale-specific formatting,
regional variants, language-switch UI, SEO relationships, accessibility semantics, and validation of
actual rendered routes.

## Security and privacy

The declaration MUST NOT contain credentials, user preferences, geolocation rules, personal data, or
runtime request state. Language negotiation based on a request is runtime behavior and remains outside
this static repository metadata contract.

## Compatibility and migration

Repository Localization v1 is opt-in and additive for repositories not using WAB v3. Publishing this
contract MUST NOT alter existing WAB v1/v2 consumers.

A repository migrating to WAB v3 MUST materialize and validate `.repository-localization.yml` before
activating the compatible Repository Standards declaration. Missing or invalid metadata MUST fail
closed rather than being synthesized from the application.