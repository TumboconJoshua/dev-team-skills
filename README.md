# Dev Team Skills for Antigravity

A project-scoped, seven-skill package that gives a solo developer a disciplined
software delivery team: six specialist roles plus an end-to-end feature pipeline.

The package uses current Agent Skills, explicit role handoffs, risk-based QA and
security gates, and a dependency-free repository validator.

## Included

```text
your-project/
|-- AGENTS.md
|-- .agents/
|   |-- GUARDRAILS.md
|   |-- references/handoff-template.md
|   |-- skills/
|   |   |-- software-engineer/SKILL.md
|   |   |-- ui-ux-designer/SKILL.md
|   |   |-- full-stack-developer/SKILL.md
|   |   |-- backend-specialist/SKILL.md
|   |   |-- qa-tester/SKILL.md
|   |   |-- penetration-tester/SKILL.md
|   |   `-- feature-pipeline/SKILL.md
|   `-- tests/skill-cases.json
|-- scripts/validate_skills.py
`-- .github/workflows/validate.yml
```

## Install

Copy `AGENTS.md`, `README.md`, `IMPLEMENTATION_PLAN.md`, the complete
`.agents/` directory, and the validation files to the target project root.
Install the package atomically: roles depend on shared project policy and the
handoff contract, so copying one role globally is unsupported.

Open the project in Antigravity, confirm seven skills are discoverable, and run:

```shell
python scripts/validate_skills.py
```

The dependency-free validator checks frontmatter, names, internal links, required
files, obsolete workflow layout, statuses, retry termination, and fixtures.

## Use

| Request | Skill |
|---|---|
| Scope a feature, refactor, or cross-cutting fix | `software-engineer` |
| Specify a screen, flow, component, or accessibility behavior | `ui-ux-designer` |
| Build a small-to-medium UI and API feature | `full-stack-developer` |
| Change data models, APIs, jobs, performance, or integrations | `backend-specialist` |
| Test an implementation or reproduce a defect | `qa-tester` |
| Assess an authorized security-sensitive change | `penetration-tester` |
| Coordinate production-bound work end to end | `feature-pipeline` |

Invoke the complete chain with:

> Run the feature pipeline for adding a contact form.

The pipeline pauses for human authority or a material decision. Deployment,
publishing, destructive operations, and risk acceptance remain human-approved.

## Delivery model

1. Software Engineer defines scope, risk, criteria, and ownership.
2. UI/UX Designer contributes only when user-facing behavior changes.
3. Full Stack Developer or Backend Specialist implements according to ownership.
4. QA Tester verifies every production-bound code or configuration change.
5. Penetration Tester reviews every production-bound change, with depth
   proportionate to risk.
6. The human operator approves release.

Direct, well-scoped work may start at the owning role, but cannot bypass applicable
QA, security, or human-approval gates.

## Risk gates

- **Low:** documentation, tests, internal refactors, or isolated changes without a
  new trust boundary, public API, user data, dependency, migration, or infrastructure
  impact. QA and security review remain required but may be narrowly focused for
  production-bound code or configuration.
- **Elevated:** authentication, authorization, sessions, payments, secrets, PII or
  other user data, uploads, dependencies or CI, infrastructure security, or a new
  or materially changed public endpoint. Threat modeling and security review are
  mandatory.

Every security finding must be fixed, shown not applicable with evidence, or
accepted by the human with an owner and expiry.

## Handoffs

Every role uses `.agents/references/handoff-template.md`. Workflow states are:

- `ready-for-next-stage`
- `blocked`
- `needs-human-decision`

Handoffs include criterion results, exact evidence, risk, attempt count, findings,
and the next owner. After two failures for the same reason, the pipeline stops for
a human decision.

Optional evidence belongs under `.agents/runs/<run-id>/`. That directory is ignored
because logs and payloads may contain sensitive information.

## Adapt and maintain

Roles discover the target repository's manifests, lockfiles, CI, commands,
conventions, and architecture before acting. Frameworks named in skills are examples,
not defaults. Put persistent stack-specific context in the target project's
`AGENTS.md` or project rules.

`AGENTS.md` and `.agents/GUARDRAILS.md` define instruction precedence, untrusted
content handling, least privilege, secret handling, approvals, truthful evidence,
and loop termination.

- Update descriptions when real prompts route incorrectly.
- Add positive and negative cases to `.agents/tests/skill-cases.json`.
- Run the validator before each merge.
- Smoke-test Antigravity routing after description changes; fixtures cannot prove
  model routing behavior.

See `IMPLEMENTATION_PLAN.md` for architecture and ownership decisions.
