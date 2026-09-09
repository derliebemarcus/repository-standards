# Design Source Declaration v1

## Status and scope

Design Source Declaration v1 defines a repository-owned, versioned declaration for the primary normative design source of a repository. Its canonical declaration path is `.repository-design-source.yml`.

The declaration is metadata for deterministic design-source discovery. It MUST NOT contain credentials or secrets and MUST NOT implicitly alter `.repository-standards.yml`, Web Application Baseline adoption, Design System adoption, deployment automation, or the content of a Design Contract.

Capitalized requirement keywords are interpreted according to BCP 14, consisting of RFC 2119 and RFC 8174.

## Canonical declaration

The v1 declaration has this shape:

```yaml
version: 1
source:
  provider: penpot
  team:
    id: "11111111-1111-4111-8111-111111111111"
    name: "siczb"
  project:
    id: "22222222-2222-4222-8222-222222222222"
    name: "example-web"
automation:
  interface: penpot-rpc
```

The root MUST contain `version` and `source`. It MAY contain `automation`. No other root fields are valid in v1.

`version` MUST be the integer `1`.

The declaration is intentionally singular: the `source` object is the repository's primary normative design source. A repository requiring multiple independently authoritative design sources MUST use a future contract version that defines their precedence and roles rather than inventing additional v1 fields.

## Design source identity

`source` MUST contain exactly:

- `provider`;
- `team`; and
- `project`.

Design Source Declaration v1 supports the provider identifier `penpot`. A consumer MUST fail closed on an unknown provider instead of treating an arbitrary provider string as compatible.

For `provider: penpot`, both `team.id` and `project.id` MUST be stable Penpot UUID identifiers. Human-readable `name` fields MAY be provided for `team` and `project`, but a name MUST NOT be used as the normative identity and MUST NOT substitute for an ID.

A consumer MUST resolve Penpot resources by the declared IDs. It MUST NOT select a team or project solely because its display name resembles a repository name, organization name, ticket title, URL fragment, prior prompt, or remembered project.

`team` and `project` MUST each contain `id` and MAY contain `name`. No other fields are valid in v1.

## Automation interface

`automation` is optional. When present, it MUST contain exactly one field, `interface`.

Design Source Declaration v1 recognizes `penpot-rpc` as an optional automation interface for a Penpot source. The automation interface describes an available interaction capability; it is not the normative design source and it does not replace the Penpot team/project identity.

A repository MAY declare a valid Penpot source without declaring any automation interface. A consumer MUST NOT reject an otherwise valid Penpot design source merely because `penpot-rpc` is unavailable in the current execution environment.

When `automation.interface: penpot-rpc` is declared, the source provider MUST be `penpot`. Unknown automation-interface identifiers MUST fail closed.

The portable Web Application Baseline and Contract-first Delivery standards MUST NOT require ChatGPT, MCP, RPC, or another concrete client/runtime merely because this optional metadata exists.

## Relationship to Web Design Contracts

The repository declaration provides stable project-level discovery context. It does not freeze a particular screen, component, state, file, page, frame, or design revision.

A revisions-bound Web Design Contract remains responsible for the concrete design artifact identity required by Web Application Baseline v2, including the relevant file/page/frame/component or equivalent, state, responsive variant, interaction semantics, accessibility-relevant intent, and immutable/reproducible contract revision.

When a Design Contract uses the repository's declared primary design source, its provider and project identity MUST match the repository declaration. A consumer that can validate both artifacts MUST fail closed on a provider or project mismatch rather than silently switching design sources.

A Design Contract MAY refine the repository-level declaration with more specific Penpot identities. Such refinement MUST NOT redefine the repository's primary team/project mapping implicitly.

## Repository ownership and versioning

The declaration MUST live in the repository whose design source it describes and MUST be version-controlled with that repository.

The declaration is independently versioned from `.repository-standards.yml`. Adding, changing, or removing `.repository-design-source.yml` MUST NOT rewrite the repository's standards version or silently migrate another standards contract.

Consumers MUST read the declaration from the repository revision relevant to the operation being performed. A consumer MUST NOT combine a design-source declaration from one revision with repository metadata from another revision while claiming one atomic repository snapshot.

A missing sidecar means the repository has no design source declared under this contract. It is distinct from an invalid sidecar.

## Consumer behavior

A conforming consumer MUST:

- distinguish a missing sidecar from an invalid sidecar;
- reject unsupported contract versions;
- reject unknown root, source, team, project, and automation fields;
- reject unknown providers and automation interfaces;
- reject missing or malformed normative Penpot UUIDs;
- treat names only as display metadata;
- use the declared design source before attempting heuristic discovery;
- fail closed when a referenced Design Contract conflicts with the declared provider or project; and
- keep credentials and session material outside the declaration.

An AI agent SHOULD resolve `.repository-design-source.yml` before searching for a design project. It MUST NOT create or choose a replacement project merely because the declared source is temporarily inaccessible. Inaccessibility is an execution/tooling condition, not evidence that the repository mapping is obsolete.

## Security

The sidecar is not a secret store. Credentials, access tokens, API keys, session identifiers, cookies, passwords, RPC connection secrets, or equivalent authentication material MUST NOT be included.

The schema and reference validator reject unknown fields so common credential-bearing additions cannot be silently accepted. Provider authentication remains an implementation/environment responsibility.

## Compatibility

Design Source Declaration v1 is additive metadata targeted for publication with the Repository Standards v9.2.0 release line. Existing repositories and existing `.repository-standards.yml` declarations remain valid without it.

Web Application Baseline v2 remains provider-neutral and immutable. Its existing requirement for a stable Design Contract source is not changed in place; this sidecar supplies optional repository-level discovery metadata that compatible consumers may use.

Publication of this contract MUST NOT migrate existing repositories automatically. A future incompatible metadata shape, provider model, or multi-source model MUST use a new Design Source Declaration contract version. A consumer that does not support the declared version MUST fail closed.
