# Repository Environments v1 AI adapter

Before reading or writing repository environment URLs, use the released Repository Environments v1 contract and Deployment Environments v2 vocabulary. Do not infer rules from repository names, DNS conventions, design fixtures, prompt history, or a central project list.

Canonical declaration path: `.repository-environments.yml`.

Canonical machine-readable environment order: `DEV`, `STAGING`, `PROD`.

`STAGE` is invalid in Repository Environments v1. `STAG` is UI-only and must not be persisted.

A missing sidecar means no human-web environments are declared under this contract. A missing environment key is valid. A present environment entry with a missing, empty, malformed, credential-bearing, or fragmented URL is invalid and must fail closed.

URLs must be concrete repository-owned absolute HTTP(S) human-web targets. Do not synthesize URLs and do not add MCP/API endpoints when the intended use is human navigation.

The sidecar is additive metadata. Its `deployment-environments: v2` field selects the v2 environment vocabulary for the sidecar and does not migrate `.repository-standards.yml` or deployment automation.

Validate supported declarations with `tools/repository_environments.py` or an implementation conforming to `schemas/repository-environments-v1.schema.json` plus the normative URL constraints.
