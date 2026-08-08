# Dev Team Skills for Antigravity

A six-role virtual dev team — Software Engineer, Full Stack Developer, Backend
Specialist, UI/UX Designer, QA Tester, and Penetration Tester — implemented as
Antigravity Skills, so a solo developer can orchestrate work the way a small
software company would: scoped, handed off between specialists, tested, and
security-reviewed before it ships.

This README covers installation and day-to-day usage. For the reasoning
behind the design (division of responsibility, phased rollout, why the
handoff format exists), see `IMPLEMENTATION_PLAN.md`.

## What's included

```
your-project/
├── AGENTS.md                          # team roster + default pipeline order
└── .agents/
    ├── skills/
    │   ├── software-engineer/SKILL.md
    │   ├── full-stack-developer/SKILL.md
    │   ├── backend-specialist/SKILL.md
    │   ├── ui-ux-designer/SKILL.md
    │   ├── qa-tester/SKILL.md
    │   └── penetration-tester/SKILL.md
    ├── workflows/
    │   └── feature-pipeline.md        # chains all six roles end to end
    └── references/
        └── handoff-template.md        # shared artifact format between roles
```

## Requirements

- [Antigravity](https://antigravity.google) installed.
- A project folder to open as an Antigravity workspace (Antigravity is
  project-centric — it needs a folder selected to scope file/tool access).

## Install

### Option A — Per project (recommended default)

Unzip so `AGENTS.md` and `.agents/` sit directly at your project root:

```
your-project/
├── AGENTS.md
├── .agents/
├── src/
├── package.json
└── ...
```

Commit these to version control. They're project configuration, not personal
preference — if you ever bring on a collaborator, they inherit the same
pipeline automatically.

### Option B — Global (available in every project)

Copy individual role folders into Antigravity's global skills directory:

```
~/.gemini/config/skills/<role>/SKILL.md
```

Good for roles whose logic barely changes between projects — `qa-tester` and
`penetration-tester` are the best candidates, since good testing and security
habits are largely stack-agnostic. Keep stack-specific roles
(`full-stack-developer`, `backend-specialist`) project-local so they can
reference your actual frameworks and conventions.

You can mix both: global for the stack-agnostic roles, project-local for the
rest.

## First-time setup checklist

- [ ] Files placed correctly (`AGENTS.md` at project root, or role folders
      under `~/.gemini/config/skills/`).
- [ ] Open the project in Antigravity and check **Agent Manager** — all
      installed skills should be listed by name + description.
- [ ] Open each `SKILL.md` and replace generic framework/tooling references
      with your actual stack (e.g. your real frontend framework, ORM, test
      runner, CI system, security scanning tools).
- [ ] Smoke-test one role in isolation with an unambiguous request (e.g. "review
      this endpoint for injection risk" should load `penetration-tester` only).
- [ ] Run one small real task through the full pipeline before trusting it on
      anything bigger.

## Using it day to day

You generally don't need to name a role — Antigravity matches your request
against each skill's `description` and loads the right one automatically.

| You say... | What loads |
|---|---|
| "I want to add a settings page with dark mode" | Software Engineer scopes it, routes onward |
| "How should this component look and behave?" | UI/UX Designer |
| "Build the API for saving user preferences" | Backend Specialist |
| "Wire up this form to the backend" | Full Stack Developer |
| "Write test cases for the signup flow" | QA Tester |
| "Check this login flow for vulnerabilities" | Penetration Tester |

**To run the full chain** (scope → design → build → verify → security gate),
say something like:

> "Run the feature pipeline for adding a contact form."

This follows `.agents/workflows/feature-pipeline.md` and pauses for your
approval between stages rather than running end to end unattended.

## How handoffs work

Every role produces its output in the shared format defined in
`.agents/references/handoff-template.md`: context, deliverable, acceptance
criteria, open questions, and a status (`ready-for-next-stage`, `blocked`, or
`needs-human-decision`). This means the next role never has to re-derive
context — and you can audit the full chain of a feature after the fact by
reading the handoffs in order.

## Customizing for your stack

The shipped `SKILL.md` files assume a generic web app. Before relying on them:

1. Replace framework/tooling mentions in `full-stack-developer` and
   `backend-specialist` with your real ones (React/Next.js, your ORM, your
   API conventions, etc.).
2. Update `qa-tester` with your actual test runner and CI command.
3. Update `penetration-tester` with any security tooling you already use
   (dependency scanners, SAST tools) so it references real commands instead
   of generic checklist items.

## Fixing problems

**A skill doesn't trigger when it should** — sharpen its `description` field
in the frontmatter. That field is the only thing Antigravity's router sees
before deciding to load the skill, so add the actual phrasing you used that
failed to trigger it.

**A role asks for context a previous stage already had** — the handoff from
the producing role is incomplete. Fix that role's `SKILL.md` output format,
not the prompt you're sending to the consuming role.

**An agent loops or stalls** — create `.agents/GUARDRAILS.md` (referenced by
all six skills but not included by default) and document the specific
failure pattern as you hit it. Treat it as a living file, not a one-time setup
step.

**Two roles overlap or step on each other** — check the division-of-labor
table in `IMPLEMENTATION_PLAN.md`. Each `SKILL.md` also has a "what you do
NOT do" section; if two roles both claim the same task, tighten those
sections rather than letting the pipeline sort it out at runtime.

## Files reference

| File | Purpose |
|---|---|
| `IMPLEMENTATION_PLAN.md` | Design rationale, phased rollout, division of responsibility |
| `AGENTS.md` | Team roster and default pipeline order (read by Antigravity at session start) |
| `.agents/skills/*/SKILL.md` | Individual role definitions |
| `.agents/workflows/feature-pipeline.md` | Chained end-to-end workflow |
| `.agents/references/handoff-template.md` | Shared artifact format between roles |
| `.agents/GUARDRAILS.md` | *(not included — create as you discover real failure patterns)* |