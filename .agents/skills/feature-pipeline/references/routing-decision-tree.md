# Routing Decision Tree

Choose one implementation owner. Add design, QA, and security stages separately.

1. If the request is ambiguous, architectural, cross-cutting, or needs task
   decomposition, start with Software Engineer.
2. If user behavior, navigation, layout, interaction states, or accessibility
   changes, route through UI/UX Designer before implementation.
3. If implementation spans both UI and server/API code and is small to medium,
   assign Full Stack Developer.
4. If the work is backend-only or dominated by schema, migrations, jobs,
   infrastructure, reliability, performance, or integrations, assign Backend
   Specialist.
5. After production-bound code or configuration changes, always route through QA
   Tester and then Penetration Tester.
6. Route authorization, risk acceptance, destructive actions, external writes,
   and release approval to the human operator.

When two implementation roles appear plausible, choose the role that owns the
highest-risk changed boundary. Do not assign both roles to edit the same files
concurrently.
