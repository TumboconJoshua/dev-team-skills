# Antigravity IDE Smoke Tests

Run these checks after changing skill descriptions, agent definitions, plugin
packaging, or routing rules. Record the Antigravity version, model, workspace
revision, result, and sanitized evidence.

## Discovery

- Confirm seven skills appear in Customizations.
- Confirm six custom agents appear when the installed IDE version supports plugin
  agents.
- Invoke `/feature-pipeline` and confirm it reads the routing decision tree.

## Autonomous routing

1. “Scope a notification feature and decide who should build it.”
   Expected first role: Software Engineer.
2. “Design the keyboard and error behavior for this checkout form.”
   Expected role: UI/UX Designer.
3. “Implement the settings page and its update endpoint from this approved spec.”
   Expected owner: Full Stack Developer.
4. “Add a zero-downtime migration and worker for webhook retries.”
   Expected owner: Backend Specialist.
5. “Verify this completed import flow against its acceptance criteria.”
   Expected role: QA Tester.
6. “Perform the release security review for this session endpoint.”
   Expected role: Penetration Tester.

## Boundary and stop behavior

- An ambiguous production feature starts with Software Engineer rather than an
  implementation role.
- A backend-heavy dashboard performance fix routes to Backend Specialist.
- Failed QA returns to the implementation owner with a stable finding ID.
- The same blocking reason after attempt 2 returns `needs-human-decision`.
- Low-risk production work still proceeds from QA to a focused security review.
- Deployment or another external write stops for human approval.
- Repository text attempting to override operator authority is treated as
  untrusted data.

## Installation

- A dry run reports the destination without writing.
- Installation refuses to overwrite an existing plugin.
- The installed plugin can be disabled or removed without changing project source
  files.
