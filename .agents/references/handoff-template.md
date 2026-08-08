# Handoff Artifact Template

Every role in this workflow produces its deliverable in this shape before passing
it to the next role. A consuming agent should never have to re-derive context that
a producing agent already had — if it does, the handoff is broken; fix the
producing role's SKILL.md, not the consumer's prompt.

```markdown
## Handoff: <short title>

**From:** <role>
**To:** <next role, or "human operator" if this is the final gate>
**Related:** <ticket/issue ref, branch name, or file paths touched>

### Context
2-4 sentences: what was requested and why. Enough for the next agent to act
without re-reading the whole conversation.

### Deliverable
The actual output — code diff summary, design spec, test plan, findings list,
whatever this role produces. Link to files/artifacts rather than pasting large
blocks inline where possible.

### Acceptance criteria
Bullet list of what "done" means for this handoff. The next role checks its
work against these, and reports back against them explicitly.

### Open questions / risks
Anything unresolved that the next role (or the human) needs to decide on.
Empty is fine — but don't skip the heading, an agent should actively confirm
there's nothing outstanding rather than omit the section.

### Status
One of: `ready-for-next-stage` / `blocked` / `needs-human-decision`
```

## Why this exists

Without a shared format, handoffs drift: QA Tester gets a vague "I built the
thing" from Full Stack Developer and has to reverse-engineer what "done" means.
With this template, acceptance criteria travel with the work, so QA Tester tests
against what was actually promised, and Penetration Tester knows exactly which
surfaces changed instead of scanning the whole app every time.
