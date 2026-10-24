---
trigger: always_on
description: Core authority, evidence, safety, and escalation rules for the dev-team-skills plugin.
---

# Dev Team Policy

@[Agent guardrails](../GUARDRAILS.md)

Use only `ready-for-next-stage`, `blocked`, and `needs-human-decision` for
pipeline state. Require QA and risk-proportionate Penetration Tester review for
every production-bound code or configuration change. Human approval is required
for release, external writes, destructive operations, access-control changes,
and risk acceptance.
