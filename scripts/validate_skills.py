#!/usr/bin/env python3
"""Validate this repository's Agent Skills package without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
FIXTURES = ROOT / ".agents" / "tests" / "skill-cases.json"
CANONICAL_STATUSES = {
    "ready-for-next-stage",
    "blocked",
    "needs-human-decision",
}
REQUIRED_FILES = (
    '.agents/GUARDRAILS.md',
    "AGENTS.md",
    "README.md",
    "IMPLEMENTATION_PLAN.md",
    ".agents/references/handoff-template.md",
    ".agents/skills/feature-pipeline/SKILL.md",
    ".agents/tests/skill-cases.json",
)


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", "node_modules"}
    return [
        path
        for path in ROOT.rglob("*.md")
        if not ignored.intersection(path.relative_to(ROOT).parts)
    ]


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    values: dict[str, str] = {}
    current: str | None = None
    folded = False
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            current = match.group(1)
            raw = (match.group(2) or "").strip()
            folded = raw in {">", "|", ">-", "|-"}
            values[current] = "" if folded else raw.strip("\"'")
        elif current and folded and (line.startswith(" ") or not line.strip()):
            values[current] = f"{values[current]} {line.strip()}".strip()
    return values


def validate_skills(errors: list[str]) -> set[str]:
    if not SKILLS_DIR.is_dir():
        errors.append("missing .agents/skills directory")
        return set()

    names: set[str] = set()
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        relative = skill_file.relative_to(ROOT)
        try:
            metadata = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{relative}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "").strip()
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{relative}: invalid skill name {name!r}")
        if name != skill_file.parent.name:
            errors.append(f"{relative}: name must match directory {skill_file.parent.name!r}")
        if not description or len(description) > 1024:
            errors.append(f"{relative}: description must contain 1-1024 characters")
        if name in names:
            errors.append(f"{relative}: duplicate skill name {name!r}")
        names.add(name)

    for directory in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        if not (directory / "SKILL.md").is_file():
            errors.append(f"{directory.relative_to(ROOT)}: missing SKILL.md")
    return names


def validate_markdown_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    fence_pattern = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
    for source in markdown_files():
        text = fence_pattern.sub("", source.read_text(encoding="utf-8"))
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and ">" in target:
                target = target[1 : target.index(">")]
            else:
                target = target.split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (ROOT / target.lstrip("/")) if target.startswith("/") else (source.parent / target)
            if not resolved.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: broken internal link {raw_target!r}"
                )


def validate_repository_rules(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    legacy = ROOT / ".agents" / "workflows"
    if legacy.exists():
        active_files = [path for path in legacy.rglob("*") if path.is_file()]
        for path in active_files:
            errors.append(f"legacy workflow must be migrated: {path.relative_to(ROOT)}")

    documents = {path: path.read_text(encoding="utf-8") for path in markdown_files()}
    for path, text in documents.items():
        if re.search(r"RFC\s*7807", text, re.IGNORECASE):
            errors.append(f"{path.relative_to(ROOT)}: use RFC 9457 instead of RFC 7807")

    handoff = ROOT / ".agents" / "references" / "handoff-template.md"
    if handoff.is_file():
        text = handoff.read_text(encoding="utf-8")
        missing = sorted(status for status in CANONICAL_STATUSES if status not in text)
        if missing:
            errors.append(f"{handoff.relative_to(ROOT)}: missing statuses {', '.join(missing)}")

    noncanonical = re.compile(
        r"(?:verification\s+status|security\s+status|mark\s+status|status\s+(?:as|is)|status\s*[:=])"
        r"[^\n]{0,50}`(passed|failed|cleared)`",
        re.IGNORECASE,
    )
    for path, text in documents.items():
        for match in noncanonical.finditer(text):
            errors.append(
                f"{path.relative_to(ROOT)}: non-canonical handoff status {match.group(1)!r}"
            )

    pipeline = ROOT / ".agents" / "skills" / "feature-pipeline" / "SKILL.md"
    if pipeline.is_file():
        text = pipeline.read_text(encoding="utf-8")
        retry_ceiling = re.search(
            r"(?:maximum|max(?:imum)?\s+of|ceiling(?:\s+of)?)\s*(?:two|2)\s+"
            r"(?:implementation\s+)?(?:attempts?|retries)",
            text,
            re.IGNORECASE,
        )
        if not retry_ceiling:
            errors.append(
                f"{pipeline.relative_to(ROOT)}: must state a maximum of 2 implementation attempts"
            )

    workflows_dir = ROOT / ".github" / "workflows"
    if workflows_dir.is_dir():
        for workflow in workflows_dir.glob("*.y*ml"):
            text = workflow.read_text(encoding="utf-8")
            actions = re.findall(r"^\s*-?\s*uses:\s*([^\s#]+)", text, re.MULTILINE)
            for action in actions:
                if not re.fullmatch(r"[^@\s]+@[0-9a-fA-F]{40}", action):
                    errors.append(
                        f"{workflow.relative_to(ROOT)}: pin action {action!r} to a full commit SHA"
                    )
            if any(action.startswith("actions/checkout@") for action in actions):
                if not re.search(r"persist-credentials:\s*false", text):
                    errors.append(
                        f"{workflow.relative_to(ROOT)}: checkout must disable persisted credentials"
                    )


def validate_fixtures(errors: list[str], skill_names: set[str]) -> None:
    if not FIXTURES.is_file():
        return
    try:
        data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"{FIXTURES.relative_to(ROOT)}: invalid JSON: {exc}")
        return

    if data.get("version") != 1:
        errors.append(f"{FIXTURES.relative_to(ROOT)}: version must be 1")
    routing = data.get("routing_cases")
    workflows = data.get("workflow_cases")
    if not isinstance(routing, list) or not routing:
        errors.append(f"{FIXTURES.relative_to(ROOT)}: routing_cases must be a non-empty list")
        routing = []
    if not isinstance(workflows, list) or not workflows:
        errors.append(f"{FIXTURES.relative_to(ROOT)}: workflow_cases must be a non-empty list")
        workflows = []

    ids: set[str] = set()
    coverage = {name: {True: False, False: False} for name in skill_names}
    for index, case in enumerate(routing):
        location = f"routing_cases[{index}]"
        required = {"id", "prompt", "target_skill", "should_match"}
        missing = required - case.keys() if isinstance(case, dict) else required
        if missing:
            errors.append(f"{location}: missing {', '.join(sorted(missing))}")
            continue
        if case["id"] in ids:
            errors.append(f"{location}: duplicate id {case['id']!r}")
        ids.add(case["id"])
        target = case["target_skill"]
        if target not in skill_names:
            errors.append(f"{location}: unknown target_skill {target!r}")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            errors.append(f"{location}: prompt must be a non-empty string")
        if not isinstance(case["should_match"], bool):
            errors.append(f"{location}: should_match must be boolean")
        elif target in coverage:
            coverage[target][case["should_match"]] = True

    for skill, kinds in sorted(coverage.items()):
        if not kinds[True] or not kinds[False]:
            errors.append(f"routing_cases: {skill!r} needs positive and negative cases")

    saw_retry_ceiling = False
    observed_workflows: dict[str, dict[str, object]] = {}
    for index, case in enumerate(workflows):
        location = f"workflow_cases[{index}]"
        required = {
            "id",
            "stage",
            "outcome",
            "attempt",
            "expected_status",
            "expected_next_role",
        }
        missing = required - case.keys() if isinstance(case, dict) else required
        if missing:
            errors.append(f"{location}: missing {', '.join(sorted(missing))}")
            continue
        if case["id"] in ids:
            errors.append(f"{location}: duplicate id {case['id']!r}")
        ids.add(case["id"])
        observed_workflows[case["id"]] = case
        if case["expected_status"] not in CANONICAL_STATUSES:
            errors.append(f"{location}: invalid expected_status {case['expected_status']!r}")
        attempt = case["attempt"]
        if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 0 or attempt > 2:
            errors.append(f"{location}: attempt must be an integer from 0 through 2")
        if attempt == 2 and case["expected_status"] == "needs-human-decision":
            saw_retry_ceiling = True
        for field in ("id", "stage", "outcome", "expected_next_role"):
            if not isinstance(case[field], str) or not case[field].strip():
                errors.append(f"{location}: {field} must be a non-empty string")
    if workflows and not saw_retry_ceiling:
        errors.append("workflow_cases: must cover escalation at the second failed attempt")

    required_workflows = {
        "qa-pass-security-required": {
            "stage": "qa-tester",
            "condition": "production-bound-elevated-risk",
            "expected_status": "ready-for-next-stage",
            "expected_next_role": "penetration-tester",
        },
        "qa-second-failure-escalates": {
            "attempt": 2,
            "expected_status": "needs-human-decision",
            "expected_next_role": "human-operator",
        },
        "qa-pass-low-risk-security-review": {
            "stage": "qa-tester",
            "condition": "production-bound-low-risk",
            "expected_status": "ready-for-next-stage",
            "expected_next_role": "penetration-tester",
        },
        "security-blocks-release": {
            "stage": "penetration-tester",
            "condition": "unresolved-security-finding",
            "expected_status": "blocked",
            "expected_next_role": "implementing-role",
        },
        "external-action-needs-approval": {
            "stage": "feature-pipeline",
            "condition": "external-write",
            "expected_status": "needs-human-decision",
            "expected_next_role": "human-operator",
        },
    }
    for case_id, expected in required_workflows.items():
        case = observed_workflows.get(case_id)
        if case is None:
            errors.append(f"workflow_cases: missing required case {case_id!r}")
            continue
        for field, value in expected.items():
            if case.get(field) != value:
                errors.append(
                    f"workflow_cases: {case_id!r} must set {field} to {value!r}"
                )


def main() -> int:
    errors: list[str] = []
    skill_names = validate_skills(errors)
    validate_markdown_links(errors)
    validate_repository_rules(errors)
    validate_fixtures(errors, skill_names)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validation passed for {len(skill_names)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
