# Design Source Declaration

Design Source Declaration provides repository-owned discovery metadata for a repository's primary
normative design source. The normative v1 contract is defined in
[`standards/design-source-declaration/v1/standard.md`](../../standards/design-source-declaration/v1/standard.md).

## Why this is separate metadata

`.repository-standards.yml` selects portable standards versions. `.repository-design-source.yml`
identifies the repository-specific design project used by those standards. Keeping them separate
avoids changing a repository's standards pin merely because a Penpot project is renamed or rebound.

The declaration also separates **design authority** from **tooling capability**:

- `source.provider`, `source.team.id`, and `source.project.id` identify the normative design source;
- optional names improve human readability but are not identifiers;
- `automation.interface` advertises a usable interaction path such as `penpot-rpc`, but does not
  become design authority.

## Penpot example

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

Use real Penpot UUIDs in consumer repositories. Do not copy the example IDs as operational values.

## Design Contract boundary

The repository sidecar answers: **Which design project is authoritative for this repository?**

The Design Contract answers: **Which exact design artifact and revision governs this delivery item?**

For a Web Application Baseline that requires Contract-first design binding, the Design Contract
identifies the relevant file/page/frame/component or equivalent, UI state, responsive variant,
interaction semantics, accessibility-relevant intent, and revision required by the selected web
contract. Provider and project must remain consistent with the repository-level declaration.

This model was introduced for Web Application Baseline v2 and remains applicable to v3, which
incorporates the v2 Contract-first requirements while adding localization-specific dimensions. The
selected released Web Application Baseline remains authoritative.

## AI and automation behavior

Agents should resolve and validate `.repository-design-source.yml` before searching design tooling.
This removes repository-name heuristics from the normal path and makes the intended Penpot project
discoverable from version-controlled repository state.

If `penpot-rpc` is declared but unavailable to the current client, that is a tooling limitation. It
does not invalidate the Penpot source and must not cause an agent to silently select or create
another project.

## Security

Never place tokens, cookies, credentials, session identifiers, RPC connection secrets, or other
authentication material in the sidecar. Authentication remains environment-owned.
