# Implementation Plan: Antigravity Development Team

## Goal

Provide a small, auditable delivery team for a solo operator without pretending
that role separation replaces human authority. The package is installed as one
project-scoped unit and uses Agent Skills for both specialist work and orchestration.

## Architecture decisions

### ADR-001: Skills for procedures, custom agents for isolated roles

The end-to-end pipeline is a standard skill at
`.agents/skills/feature-pipeline/SKILL.md`. Six custom-agent definitions provide
isolated role contexts and least-privilege tool lists where the target IDE supports
them. Legacy `.agents/workflows/` files are not supported.

### ADR-002: Atomic project installation

For source-mode development of this repository, keep `AGENTS.md` and the complete
`.agents/` tree together. Do not copy individual role skills globally because
they depend on shared guardrails and references.

For target projects, install the generated `plugin/` bundle instead of copying
repository documentation. The safe installer writes it under
`.agents/plugins/dev-team-skills/`, rejects links and path escapes, and refuses
overwrite.

### ADR-002a: Canonical workspace source plus verified plugin mirror

`.agents/skills/`, `.agents/agents/`, and shared references are the editable
source. `scripts/sync_plugin.py` creates the committed Antigravity plugin mirror.
Validation fails on missing, stale, or changed mirrored files so the two forms
cannot silently drift.

### ADR-003: One state machine

Every role emits exactly one workflow status:

- `ready-for-next-stage`
- `blocked`
- `needs-human-decision`

PASS/FAIL results and security dispositions are evidence, not extra workflow states.
Blocked and human-decision states halt orchestration.

### ADR-004: Risk-based gates

QA and authorized security review are mandatory for production-bound code and
configuration. Elevated changes also require threat modeling before implementation.
Low-risk work receives a focused security review rather than skipping the gate.

Elevated surfaces include authentication, authorization, sessions, payments,
secrets, PII or regulated data, uploads, dependency and CI trust, infrastructure
security, and new or materially changed public endpoints.

### ADR-005: Human-controlled side effects

The agent team can analyze, design, implement, and verify within the approved
workspace. Deployment, publishing, destructive operations, external communications,
access-control changes, and risk acceptance require human authorization.

### ADR-006: Stack discovery over framework assumptions

Each implementation role inspects manifests, lockfiles, CI, commands, tests, and
existing patterns before acting. Named frameworks and tools are examples. The target
project remains the source of truth.

## Role ownership

| Role | Owns | Does not own |
|---|---|---|
| Software Engineer | Scope, architecture, risk, acceptance criteria, task routing | Non-trivial implementation |
| UI/UX Designer | User flows, applicable UI states, WCAG 2.2 AA specs | Production code or backend design |
| Full Stack Developer | Small-to-medium UI/API implementation | Deep infrastructure or independent visual direction |
| Backend Specialist | Data, APIs, migrations, jobs, integrations, operations | Frontend presentation |
| QA Tester | Risk-based verification, evidence, reproducible defects | Production fixes or risk acceptance |
| Penetration Tester | Authorized threat-informed security verification | Feature correctness or self-remediation |
| Human operator | Material decisions, approvals, accepted risk, release | None delegated by default |

## Pipeline

1. **Scope:** define outcome, non-goals, risk, criteria, and owner.
2. **Design:** run only for changed user-facing behavior.
3. **Build:** use Full Stack Developer or Backend Specialist ownership.
4. **Verify:** map every criterion to evidence and relevant regression checks.
5. **Security:** run for every production-bound change with depth proportionate to
   risk, and close every finding by fix, evidence-backed not-applicable disposition,
   or human risk acceptance.
6. **Release:** human reviews evidence, rollback plan, and remaining accepted risk.

When native custom agents are available, the coordinator delegates each stage to
the matching definition under `.agents/agents/`. QA and security definitions lack
editing and command tools; the coordinator executes their approved, non-destructive
checks and returns exact output for independent assessment. Skill-only execution
is the compatibility fallback.

A rejected handoff returns to its owner. The same blocking reason gets a maximum of
two implementation attempts; a second failure becomes `needs-human-decision`.

## Handoff requirements

The shared template records:

- source and next role;
- status, risk, attempt, and run identifier;
- measurable acceptance criteria and outcomes;
- exact commands, exit codes, environment, and sanitized evidence;
- threat-model, security-review, rollback, and release requirements;
- stable findings and their dispositions;
- unresolved decisions and next action.

Optional evidence is local under `.agents/runs/` and ignored by default. Never store
secrets, session tokens, raw PII, or full production payloads.

## Validation

`scripts/validate_skills.py` is a standard-library check run locally and in GitHub
Actions. It verifies:

- skill frontmatter, names, uniqueness, and description limits;
- required shared files and internal Markdown links;
- removal of legacy workflows;
- canonical statuses and the retry ceiling;
- absence of obsolete problem-details guidance;
- positive and negative routing fixtures for every skill;
- ambiguous boundary-routing fixtures and an Antigravity smoke-test checklist;
- workflow fixtures for success, failure, security blocking, escalation, and approval.
- plugin schema, native-agent definitions, and byte-for-byte distribution parity.
- installer traversal, overwrite, symlink, and junction protections.

Static checks do not prove semantic routing. After changing descriptions, manually
smoke-test representative prompts in Antigravity.

## Release checklist

1. Run `python -B scripts/validate_skills.py`.
2. Run `python -B scripts/sync_plugin.py --check`.
3. Exercise the installer dry run and refusal-to-overwrite behavior.
4. Review `git diff --check` and the complete diff.
5. Confirm no run artifacts, credentials, or personal data are staged.
6. Run `.agents/tests/antigravity-smoke-tests.md` in the supported IDE release.
7. Record any unrun checks or accepted risks before release.

## Deferred human decisions

- Choose and add a repository license before public reuse.
- Add semantic release/version metadata when the package has a release process.
- Pin or replace platform-specific guidance only after observing real project usage.
