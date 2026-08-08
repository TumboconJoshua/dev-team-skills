# Workflow: feature-pipeline

Trigger phrase: "run the feature pipeline for <description>" or "ship <feature>
end to end".

Chains the team roster in `AGENTS.md` for a single feature request, stage by
stage, pausing for human approval between stages.

## Steps

1. **Scope** — Invoke Software Engineer skill on the raw request. Output: a
   handoff artifact (see `.agents/references/handoff-template.md`) with the
   plan, task breakdown, and which downstream roles are needed.
   → Pause. Human approves scope before continuing.

2. **Design** (skip if the Software Engineer handoff marks no user-facing
   surface changed) — Invoke UI/UX Designer skill with the scope handoff as
   input. Output: flow/component spec handoff.

3. **Build** — Invoke Full Stack Developer skill (or Backend Specialist skill
   if the scope handoff says backend-only) with the scope + design handoffs as
   input. Output: implementation handoff, including a diff/PR summary.

4. **Verify** — Invoke QA Tester skill with the implementation handoff as
   input. Output: test results handoff. If tests fail, loop back to step 3
   with the failure list attached — do not proceed to step 5 on a failing
   build.

5. **Security gate** — Required if the change touches auth, payments, user
   data, file uploads, or any public-facing endpoint; optional otherwise but
   recommended. Invoke Penetration Tester skill with the implementation +
   verify handoffs as input. Output: findings handoff with severity ratings.
   Anything rated High/Critical blocks merge and loops back to step 3.

6. **Ship** — Human operator reviews the final chain of handoff artifacts and
   merges/deploys. This step is intentionally not delegated to an agent.

## Notes

- Each stage's handoff artifact should be saved (e.g. under `.agents/runs/<date>-<feature>/`)
  so the whole chain is auditable later, not just held in conversation context.
- If any stage returns `status: blocked` or `needs-human-decision`, the workflow
  halts there rather than continuing with guesses.
