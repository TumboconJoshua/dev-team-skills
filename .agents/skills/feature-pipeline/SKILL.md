---
name: feature-pipeline
description: Coordinates a feature or fix from scope through design, implementation, QA, security review, and human release approval. Use when asked to run the feature pipeline, ship a feature end to end, or coordinate specialist roles for production-bound work.
---

# Feature Pipeline

Coordinate the role skills without absorbing their specialist work. Read
`../../GUARDRAILS.md` and use `../../references/handoff-template.md` at every
stage.

## Workflow

1. **Scope — Software Engineer**
   - Define outcome, non-goals, acceptance criteria, implementation owner, and
     `low` or `elevated` risk.
   - Require a threat model for elevated work.
   - Stop for a human decision when scope changes authority or has unresolved
     product choices.
2. **Design — UI/UX Designer when applicable**
   - Specify user flow, applicable states, WCAG 2.2 AA behavior, and data needs.
   - Skip and record the reason when behavior is not user-facing.
3. **Build — Full Stack Developer or Backend Specialist**
   - Use the owner selected during scope.
   - Discover the project's commands and conventions before editing.
   - Provide implementation and rollback evidence proportionate to risk.
4. **Verify — QA Tester**
   - Map evidence to each acceptance criterion and run risk-based regression checks.
   - On failure, return to the implementation owner.
5. **Security — Penetration Tester for every production-bound change**
   - Use a focused review for low-risk work and a full threat-informed review for
     elevated work.
   - Verify applicable trust boundaries, dependencies, configuration, threat
     model, and remediation evidence.
   - Block unresolved findings unless the human accepts the risk with owner and
     expiry.
6. **Release — Human operator**
   - Review the chain, rollback plan, and accepted risk.
   - Never deploy, publish, or merge without user authorization.

## State and retry rules

Use only `ready-for-next-stage`, `blocked`, and `needs-human-decision`.
Stop immediately on the latter two. Allow a maximum of 2 implementation attempts
for the same blocking reason; after attempt 2, return `needs-human-decision`.
Record skipped stages and reasons. Save only sanitized local evidence.

## Hand off to

Hand off to the role named by the current stage, or the human operator at a stop
or release point.
