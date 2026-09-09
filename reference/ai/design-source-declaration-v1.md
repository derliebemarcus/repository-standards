# Design Source Declaration v1 AI adapter

Before searching for, selecting, or creating a design project for a repository, an AI agent SHOULD check for `.repository-design-source.yml` in the authoritative repository revision.

If the sidecar exists, the agent MUST validate it as Design Source Declaration v1 before using any design tooling. An invalid sidecar is a blocker; the agent MUST NOT bypass it by guessing a project from repository names, prior prompts, remembered URLs, or similar display names.

For `provider: penpot`, resolve the declared Penpot team and project by `team.id` and `project.id`. `team.name` and `project.name`, when present, are display metadata only.

If `automation.interface: penpot-rpc` is present and that capability is available in the execution environment, the agent MAY use it to interact with the declared Penpot project. `penpot-rpc` is an automation interface, not the normative design source. If the interface is unavailable, the Penpot declaration remains valid; report the tooling limitation instead of selecting another project.

When creating or qualifying a Web Design Contract, preserve the repository-level provider/project identity and add the concrete file/page/frame/component or equivalent identity, state, responsive variant, and design revision required by the Web Application Baseline. A provider or project mismatch between the Design Contract and `.repository-design-source.yml` MUST fail closed.

Never place Penpot credentials, tokens, cookies, session IDs, RPC secrets, or other authentication material in `.repository-design-source.yml`.

A missing sidecar means no Design Source Declaration v1 mapping exists. It does not authorize automatic project creation. Use repository policy and explicit task context to determine the next step.
