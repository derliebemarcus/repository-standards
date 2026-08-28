# Repository Environments v1

## Status and scope

Repository Environments v1 defines a repository-owned, versioned declaration for human-web environment URLs. Its canonical declaration path is `.repository-environments.yml`.

This contract is metadata for discovery and navigation. It MUST NOT contain credentials or secrets and MUST NOT implicitly alter deployment automation, branch policy, or the repository's `.repository-standards.yml` pin.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174.

## Canonical declaration

The v1 declaration has this shape:

```yaml
version: 1
deployment-environments: v2
environments:
  DEV:
    url: "https://dev.example.invalid/"
  STAGING:
    url: "https://staging.example.invalid/"
  PROD:
    url: "https://example.invalid/"
```

The root MUST contain exactly:

- `version`, with integer value `1`;
- `deployment-environments`, with string value `v2`; and
- `environments`, a mapping.

`deployment-environments: v2` selects the canonical environment vocabulary defined by Deployment Environments v2 for this metadata document. It MUST NOT be interpreted as an implicit migration of an independently pinned repository declaration or deployment pipeline.

## Environment mapping

`environments` MAY contain only these keys:

1. `DEV`;
2. `STAGING`;
3. `PROD`.

At least one environment MUST be present when the sidecar exists. Repositories without a human-web environment SHOULD omit `.repository-environments.yml` entirely rather than publish an empty declaration.

Each present environment MUST be an object containing exactly one field, `url`.

A missing environment key means that no human-web URL is declared for that environment. Absence is valid and is distinct from an invalid present environment.

A present environment with a missing `url`, an empty URL, an invalid URL, or an additional unknown field is invalid. Consumers MUST fail closed rather than silently dropping that entry.

## URL contract

Every `url` MUST:

- be a non-empty absolute URI using `http` or `https`;
- contain a host;
- contain no URL userinfo, username, password, token, or other credential material;
- contain no fragment; and
- be the concrete repository-owned human-web target for that environment.

The contract does not require a trailing slash and does not prescribe a hostname convention.

A consumer MUST NOT infer or synthesize an environment URL from repository names, environment names, organization names, DNS conventions, project fixtures, or another centrally maintained project-to-URL table.

## Repository ownership and versioning

The declaration MUST live in the repository whose environments it describes and MUST be version-controlled with that repository.

The declaration is independently versioned from `.repository-standards.yml`. Adding, changing, or removing `.repository-environments.yml` MUST NOT rewrite the repository's standards version or change deployment policy unless a separate governed change does so explicitly.

Consumers MUST read the declaration from the repository's authoritative branch for the use case being served. A consumer MUST NOT combine an environment declaration from one revision with repository metadata from another revision while claiming one atomic inventory snapshot.

## Consumer behavior

A conforming consumer MUST:

- distinguish a missing sidecar from an invalid sidecar;
- distinguish a missing environment from an invalid environment entry;
- reject unknown root keys and unknown environment keys;
- reject unsupported contract versions;
- validate URLs before exposing them as navigation targets;
- preserve canonical environment ordering `DEV`, `STAGING`, `PROD`; and
- fail closed on malformed or incompatible metadata.

A missing sidecar means the repository has no declared human-web environments under this contract. It does not mean the repository should be omitted from a repository inventory.

## Security

The sidecar is not a secret store. Credentials, bearer tokens, API keys, URL userinfo, or other secret material MUST NOT be included. A validator that detects credential-bearing URL userinfo MUST reject the declaration.

## Compatibility

Repository Environments v1 is additive metadata. Existing repositories and existing `.repository-standards.yml` declarations remain valid without it. Publication of this contract MUST NOT migrate existing consumers automatically.

A future incompatible metadata shape MUST use a new Repository Environments contract version. A consumer that does not support the declared version MUST fail closed.
