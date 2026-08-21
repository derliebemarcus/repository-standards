# Security Policy

Repository Standards Public Core is designed to contain no credentials, private keys, tokens, private operational details, or organization-specific control files. The deterministic export performs fail-closed checks on the fully assembled distribution before it can qualify for publication.

## Reporting a security issue

Do **not** put secrets, credentials, private infrastructure details, or non-public vulnerability information into a public GitHub Issue.

If GitHub private vulnerability reporting is available for this repository, use that private channel for security-sensitive reports. If no private GitHub reporting channel is available, do not disclose sensitive details publicly; use a non-public contact method published by the repository owner on GitHub.

For a security-related documentation or contract problem that contains no sensitive information, a normal GitHub Issue is acceptable.

## Scope

Relevant reports include:

- a secret, credential, private key, or token present in the generated Public Core;
- an unintended private hostname, URL, credential value, or operational detail;
- a path-traversal, symlink-escape, or destination-escape defect in Public Core assembly;
- a way for excluded Forgejo/Jenkins control files or organization-specific integrations to enter the Public Core;
- a validation path that fails open when the export should be rejected.

Security fixes are implemented and qualified in the canonical Forgejo repository before a corrected Public Core is republished. GitHub remains a distribution target rather than an independent writable source.
