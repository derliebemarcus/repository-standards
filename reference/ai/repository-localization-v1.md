# Repository Localization v1 AI adapter

When a repository adopts Web Application Baseline v3, the agent MUST resolve the released
Repository Localization v1 contract and `.repository-localization.yml` before reasoning about
canonical content-language routes.

The agent MUST NOT infer supported languages from existing routes, translation files, browser
preferences, deployment geography, or design artifacts.

For v1:

- `version` is exactly `1`;
- `web-application-baseline` is exactly `v3`;
- `supported-languages` is a non-empty unique list of lowercase ISO 639-1 codes;
- `default-language` is exactly one member of `supported-languages`;
- unknown fields or unassigned/invalid ISO 639-1 codes fail closed.

Canonical user-facing content routes under WAB v3 use
`/<ISO-639-1>/<stable-route-id>`. The required stable route IDs are `impressum`, `datenschutz`, and
`barrierefreiheit` in every supported language. The agent MUST NOT localize these canonical route
IDs. A localized alias such as `/en/privacy` MAY exist only as a non-canonical route pointing to the
stable canonical `/en/datenschutz` representation.

The root `/` redirects to a declared supported language. Request-language negotiation MAY select a
supported language; otherwise the declared default language is the deterministic fallback.
Unsupported namespaces MUST NOT silently serve another language in place.

Regional BCP 47 metadata such as `de-CH` MAY be used inside the application or in `html[lang]`, but
MUST NOT replace the ISO 639-1 URL namespace.
