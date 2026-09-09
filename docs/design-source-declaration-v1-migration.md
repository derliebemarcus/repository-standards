# Design Source Declaration v1 migration

Design Source Declaration v1 is additive repository metadata. It does not change a repository's `.repository-standards.yml` version and it does not modify Web Application Baseline v2 in place.

## Preconditions

Before adopting the sidecar in a consumer repository:

1. use a Repository Standards release that includes Design Source Declaration v1;
2. identify the actual normative design project from authoritative design-platform state;
3. verify the stable Penpot team UUID and project UUID rather than deriving them from display names;
4. determine whether `penpot-rpc` is an established automation interface for that repository/environment; and
5. confirm that existing Design Contracts, if any, point to the same provider/project.

An ambiguous project mapping is a migration blocker. Do not guess.

## Adoption

Add `.repository-design-source.yml` to the consumer repository:

```yaml
version: 1
source:
  provider: penpot
  team:
    id: "<verified-team-uuid>"
    name: "siczb"
  project:
    id: "<verified-project-uuid>"
    name: "<display-name>"
automation:
  interface: penpot-rpc
```

Omit `automation` when no automation interface is intentionally declared. Do not place credentials or session material in the file.

Validate with the released reference validator:

```text
python3 tools/design_source.py .repository-design-source.yml
```

## Staged rollout

Use one real Web Application Baseline consumer as a Canary before broad adoption. Qualification should establish that:

- repository metadata resolves the intended Penpot project by ID;
- AI/tooling discovery honors the sidecar instead of name heuristics;
- existing/new Design Contracts preserve provider/project consistency;
- absence of Penpot-RPC in an execution environment does not invalidate the source; and
- malformed or contradictory declarations fail closed.

After the Canary succeeds, independent consumer migrations may proceed in parallel through their normal protected PR/main paths.

## Rollback

Because the contract is additive, rollback is the repository-owned removal of `.repository-design-source.yml` in a governed change. Removing the sidecar returns the repository to an undeclared design-source state; it does not change the repository's standards pin or erase existing Design Contract provenance.
