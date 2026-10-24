# Delivery Risk Matrix

Classify the change before implementation.

## Low risk

Use `low` when the change has limited blast radius and does not affect a sensitive
trust boundary, public API, user or regulated data, dependencies, migrations, or
infrastructure. Production-bound low-risk changes still require QA and a focused
Penetration Tester review.

## Elevated risk

Use `elevated` when the change affects authentication, authorization, sessions,
payments, secrets, personal or regulated data, uploads, dependency or CI trust,
infrastructure security, migrations with material recovery risk, or a new or
materially changed public endpoint.

Elevated work requires a threat model before implementation, risk-based QA, a full
threat-informed security review, rollback or recovery evidence, and human release
approval.

When classification is uncertain, choose `elevated` or return
`needs-human-decision`; do not silently weaken a gate.
