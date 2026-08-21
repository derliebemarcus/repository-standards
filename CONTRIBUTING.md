# Contributing to Repository Standards

Thank you for helping improve Repository Standards. The GitHub repository is a generated public distribution of a canonical Forgejo repository, so the contribution model intentionally differs from a normal GitHub-first project.

## Contributions are issue-only on GitHub

Use **GitHub Issues** to propose external changes. Choose the template that best matches the request:

- **Bug Report** for behavior that contradicts a published contract or for defects in public tools/reference assets;
- **Standard Change Proposal** for a new or changed normative requirement;
- **Documentation Proposal** for public documentation, examples, or explanatory material.

Provide enough evidence to evaluate the proposal without relying on private infrastructure or credentials.

## GitHub pull requests are not accepted

**Do not open a GitHub pull request. GitHub PRs are not reviewed or merged.**

This is intentional: Forgejo is the single source of truth, and the GitHub repository is regenerated from an explicit Public Core allowlist. Accepting changes directly on GitHub would create a second writable source and break that governance model.

If you already prepared a patch, open the appropriate GitHub Issue and describe the intended change there. A maintainer can use that proposal during canonical implementation.

## What happens after an issue is filed?

The normal path is:

```text
GitHub Issue
→ technical/domain evaluation
→ canonical ticket and implementation in Forgejo when accepted
→ normal Forgejo review and qualification
→ deterministic Public Core export
→ later GitHub republication
```

An accepted GitHub Issue does not bypass the canonical ticket, review, compatibility, security, or test requirements.

## Standard changes

For a normative change, state:

- the problem being solved;
- the affected standard or contract family;
- the proposed requirement or semantic change;
- compatibility impact for existing pinned consumers;
- migration implications, if any;
- alternatives considered.

Published versions are immutable. A proposal that changes existing obligations or incompatible semantics normally requires a new versioned contract boundary rather than modification of a published version.

## Documentation changes

Documentation proposals should identify the target audience, the unclear or missing material, and the intended outcome. Public documentation must remain understandable without access to private infrastructure.

## Security-sensitive material

Do not include credentials, tokens, private keys, private host details, or non-public vulnerability information in a public GitHub Issue. See `SECURITY.md` before reporting a security-sensitive problem.

## License of contributions

Repository Standards Public Core is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). Contributions that are intentionally submitted for inclusion in the work are handled under the contribution terms of Apache License 2.0 unless explicitly designated otherwise as described by that license. No additional or dual license is introduced by this contribution process.
