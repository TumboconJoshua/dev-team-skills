# Handoff Artifact Template

Use this contract for every stage. Keep it self-contained, redact secrets and
unnecessary personal data, and never claim evidence that was not produced.

```markdown
## Handoff: <short title>

**From:** <role>
**To:** <next role or Human operator>
**Status:** <ready-for-next-stage | blocked | needs-human-decision>
**Risk:** <low | elevated>
**Attempt:** <0 | 1 | 2>
**Run ID:** <stable identifier, if available>
**Related:** <ticket, branch, commit SHA, and/or paths>

### Context
<request, purpose, scope, constraints, and non-goals>

### Deliverable
<role-specific result, decisions, changed surfaces, and file links>

### Acceptance criteria
- [ ] <criterion ID>: <measurable outcome> — <PASS | FAIL | NOT-RUN>

### Verification evidence
- Command or check: <exact command or manual check>
- Result: <exit code and outcome, or not run with reason>
- Environment: <relevant runtime, OS, browser, or target>

### Security and release
- Threat model required: <yes/no + reason>
- Security review required: <yes/no + reason>
- Rollback/post-deploy plan required: <yes/no + reason>
- Sensitive data redacted: <yes/no>
- Findings: <fixed, not applicable with evidence, human-accepted with owner/expiry, or none>

### Risks and open questions
<risk, assumption, unresolved decision, or None>

### Next action
<named owner, required action, and blocking finding IDs>
```

## Contract

- `ready-for-next-stage` means this role's required work and checks passed.
- `blocked` means a concrete dependency or failed gate needs a named owner.
- `needs-human-decision` means authorization, risk acceptance, or a material
  choice is required.
- Failed QA or security gates use `blocked`; successful gates use
  `ready-for-next-stage`.
- Keep stable finding IDs. Close findings only after re-verification, a documented
  not-applicable rationale, or human risk acceptance with an owner and expiry.
- After attempt 2 fails for the same reason, stop with `needs-human-decision`.
- If no artifact policy exists, keep only minimal redacted evidence and do not
  commit raw logs or payloads.
