# Implementation Plan: Solo-Dev "Software Company" Workflow for Antigravity

## Goal

Turn Antigravity into a small virtual dev shop: one human (you) orchestrating six
specialist agent roles — Software Engineer, Full Stack Developer, Backend Specialist,
UI/UX Designer, QA Tester, and Penetration Tester — that hand work to each other
through defined artifacts instead of you re-explaining context every time.

This uses three Antigravity primitives together:

| Primitive | Role in this system |
|---|---|
| `AGENTS.md` | Project-root file defining the team roster, when each role is invoked, and the handoff order. Antigravity reads this at session start. |
| `SKILL.md` (per role, `.agents/skills/<role>/SKILL.md`) | Loaded on-demand when a request semantically matches its `description`. Contains the role's responsibilities, checklists, and output format. |
| `.agents/workflows/*.md` | Optional named macro-commands that chain roles in a fixed order for repeatable pipelines (e.g. "ship a feature"). |

## Folder layout (drop this at your project root)

```
your-project/
├── AGENTS.md
└── .agents/
    ├── skills/
    │   ├── software-engineer/SKILL.md
    │   ├── full-stack-developer/SKILL.md
    │   ├── backend-specialist/SKILL.md
    │   ├── ui-ux-designer/SKILL.md
    │   ├── qa-tester/SKILL.md
    │   └── penetration-tester/SKILL.md
    ├── workflows/
    │   └── feature-pipeline.md
    └── references/
        └── handoff-template.md
```

Skills placed under `.agents/skills/` are **project-scoped** — they only apply to this
repo. If you want a role available across every repo you touch (e.g. you always want
a penetration-tester skill on hand), copy that one folder into the **global** scope
instead: `~/.gemini/config/skills/<role>/`. Everything else about the file is identical.

## Phased rollout

### Phase 1 — Scaffold (today)
1. Copy the folder structure above into your project.
2. Commit `AGENTS.md`, `.agents/skills/`, `.agents/workflows/`, `.agents/references/`
   to version control — these are project config, not personal preference, so the
   team (even a future teammate) inherits the same pipeline.
3. Open the project in Antigravity and confirm it lists all six skills in Agent
   Manager (name + description only — bodies aren't loaded yet).

### Phase 2 — Smoke test each role in isolation
For each role, give a small, unambiguous request that should trigger only that skill
(e.g. "review this endpoint for SQL injection risk" → penetration-tester). Confirm:
- The correct skill loads (check Agent Manager's "skills equipped" indicator).
- The output matches the format defined in that SKILL.md.
- It does **not** silently do another role's job (e.g. QA Tester shouldn't also
  redesign the API — it should flag the issue and hand back).

### Phase 3 — Wire the handoff chain
1. Read `.agents/references/handoff-template.md` — this is the artifact format every
   role uses to pass work downstream (context, deliverable, open questions, acceptance
   criteria). Consistent handoffs are what make this feel like a real team instead of
   six disconnected prompts.
2. Run the `feature-pipeline` workflow (`.agents/workflows/feature-pipeline.md`) on
   one real, small feature end to end: Software Engineer (scope) → UI/UX Designer
   (if user-facing) → Full Stack Developer or Backend Specialist (build) → QA Tester
   (verify) → Penetration Tester (security gate before merge).
3. Where a handoff breaks (agent asks for context that was actually produced two
   steps earlier, or ignores acceptance criteria), fix the *producing* role's output
   format, not the consuming role's prompt — the artifact should be self-contained.

### Phase 4 — Add guardrails
Create `.agents/GUARDRAILS.md` (referenced by all six skills) documenting failure
patterns you actually hit: e.g. "Backend Specialist keeps proposing a new ORM instead
of using the existing one — reject and point back to `references/handoff-template.md`
acceptance criteria." Antigravity agents read this when they loop or stall, so treat
it as a living document, not a one-time file.

### Phase 5 — Tune triggering
Skills under-trigger more often than they over-trigger. If a role isn't loading when
it should, sharpen its `description` field (that's the *only* text the router sees
before deciding to load the skill) — add the specific phrases you actually used that
failed to trigger it, e.g. "...also use when the user says 'is this endpoint safe' or
'check for vulnerabilities', not just 'penetration test'."

### Phase 6 — Parallelize (optional, once the sequential pipeline is solid)
Antigravity supports concurrent agents on isolated workspace scopes (`@workspace_scope`).
Once handoffs are reliable, split independent workstreams — e.g. Full Stack Developer
on the feature branch while QA Tester writes tests against the previous stable branch —
and merge yourself. Don't parallelize before the sequential version works; concurrent
agents make broken handoffs much harder to debug.

## Division of responsibility (avoiding role overlap)

| Role | Owns | Does NOT own |
|---|---|---|
| Software Engineer | Scoping, architecture decisions, task breakdown, code review across the whole codebase | Hands-on feature implementation (delegates to Full Stack / Backend), pixel-level UI |
| Full Stack Developer | End-to-end feature implementation (UI + API + integration) for small/medium features | Deep backend infra (delegates to Backend Specialist), original visual design |
| Backend Specialist | Data models, APIs, performance, infra, third-party integrations | Frontend components, visual/UX decisions |
| UI/UX Designer | User flows, wireframes, component specs, accessibility, design tokens | Backend logic, database schema, security testing |
| QA Tester | Test plans, functional/regression/E2E test authoring, bug reports with repro steps | Fixing the bugs themselves, security-specific exploitation |
| Penetration Tester | Vulnerability assessment, exploit verification, security sign-off before release | Feature correctness testing (that's QA), fixing vulnerabilities (reports back to whoever owns that code) |

Every role's SKILL.md ends with a **"Hand off to"** section pointing at the next role
and the exact artifact to produce — this is what prevents scope creep between agents.

## What's in this package

- `AGENTS.md` — team roster + pipeline order Antigravity reads at session start.
- `.agents/skills/*/SKILL.md` — the six role definitions.
- `.agents/workflows/feature-pipeline.md` — example chained workflow.
- `.agents/references/handoff-template.md` — shared artifact format.

Next step after reviewing: adjust the checklists in each SKILL.md to match your
actual stack (the drafts assume a generic web app — swap in your real frameworks,
CI system, and security tooling).
