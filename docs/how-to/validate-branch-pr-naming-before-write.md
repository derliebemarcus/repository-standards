# Validate branch and pull-request naming before write

This procedure applies to AI agents and automation operating on repositories whose selected
Development Workflow requires the pre-write branch and pull-request validation model introduced in
Development Workflow v4 and preserved by later workflow versions that incorporate it.

Always resolve the workflow version from the repository's complete released compatibility pairing.
Do not assume that the newest published Development Workflow applies to an older pinned consumer.

## Branch creation

Before calling a Forgejo branch mutation:

1. read the target repository's `.repository-standards.yml`;
2. validate the complete declaration against the matching released declaration schema and
   compatibility profile;
3. load the released Development Workflow profile selected by that declaration;
4. load the compatible Ticket Specification profile identified by the selected contract set;
5. read the referenced ticket and determine its single `Kind/*` label;
6. derive the regular prefix from the Ticket Specification `branch_prefixes` mapping, or establish
   that the explicit Hotfix path is being used;
7. validate branch form, ticket number, repository qualification, slug, source branch, and branching
   model; and
8. issue the Forgejo branch write only after every validation succeeds.

Do not use remembered aliases or normalize an invalid prefix silently. For example, if the planned
name is `fix/123-example`, report that `fix` is undeclared and derive `bugfix` only when the ticket is
actually `Kind/Bug` and the regular path is intended.

## Ticket-linked pull-request creation

Before calling a Forgejo pull-request mutation:

1. repeat the released declaration/profile resolution above;
2. validate the already existing head branch against the released contract;
3. require a title in the form `#<ticket-number> <summary>`;
4. require the title ticket number to equal the ticket number encoded in the head branch;
5. validate repository qualification when the branch names another repository;
6. validate the target branch against the selected branching model or explicit Hotfix path; and
7. issue the Forgejo pull-request write only after every validation succeeds.

## Fail-closed behavior

When required metadata or a released contract cannot be resolved, stop before the mutation. Do not
create a temporary branch or pull request to let a later Forgejo Action determine whether the name
was valid.

The post-write Forgejo naming check remains mandatory where configured. It is defense in depth and
must evaluate semantics equivalent to the released contract; it is not a substitute for pre-write
validation.

## Examples

For ticket `#123` with `Kind/Bug`:

```text
bugfix/123-example-bug       valid regular-prefix candidate
fix/123-example-bug          reject before Forgejo write
hotfix/123-example-bug       reject unless the explicit Hotfix path applies
```

For the valid regular branch, a ticket-linked pull-request title can be:

```text
#123 Fix example bug
```

These must be rejected before the pull-request write:

```text
#124 Fix example bug          ticket number differs from branch
#123                          summary missing
```
