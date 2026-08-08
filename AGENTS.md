# Project Team

This project is worked by a single human operator (you) orchestrating six
specialist agent roles. Each role is defined as a Skill under `.agents/skills/`
and loads automatically when a request matches its description. This file gives
Antigravity the roster and default pipeline order up front, before any skill
body is loaded.

## Roster

1. **Software Engineer** — scoping, architecture, task breakdown, cross-codebase review.
2. **Full Stack Developer** — end-to-end feature implementation (UI + API).
3. **Backend Specialist** — data models, APIs, infra, performance, integrations.
4. **UI/UX Designer** — flows, wireframes, component specs, accessibility.
5. **QA Tester** — test plans, functional/regression/E2E tests, bug reports.
6. **Penetration Tester** — vulnerability assessment and security sign-off.

## Default pipeline for a new feature or fix

```
Software Engineer (scope + plan)
        │
        ▼
UI/UX Designer (only if user-facing surface changes)
        │
        ▼
Full Stack Developer  ──or──  Backend Specialist
   (whichever owns the surface being changed — see IMPLEMENTATION_PLAN.md)
        │
        ▼
QA Tester (functional verification)
        │
        ▼
Penetration Tester (security gate — required before anything touching
                     auth, payments, user data, or public endpoints ships)
```

Skip stages that don't apply (e.g. a pure backend cron job skips UI/UX Designer),
but never skip QA Tester or Penetration Tester for anything that reaches production.

## Handoff rule

Every role produces its output using the format in
`.agents/references/handoff-template.md` and explicitly names which role should
consume it next. Don't let one role silently do the next role's job — if
Backend Specialist notices a UX problem, it reports it back rather than
redesigning the flow itself.

## Escalation

If an agent gets stuck in a loop, contradicts a decision already made, or a
handoff is rejected twice in a row, stop and surface it to the human operator
rather than guessing. See `.agents/GUARDRAILS.md` (create this as you discover
real failure patterns — it doesn't exist yet on a fresh checkout).
