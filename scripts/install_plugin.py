#!/usr/bin/env python3
"""Safely install the bundled plugin into an Antigravity IDE workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugin"


def is_link_or_junction(path: Path) -> bool:
    """Return true for links and Windows junctions without following them."""
    return path.is_symlink() or (
        hasattr(path, "is_junction") and path.is_junction()
    )


def reject_linked_tree(root: Path) -> None:
    """Reject a bundle containing filesystem indirection."""
    if is_link_or_junction(root):
        raise ValueError(f"plugin source cannot be a link or junction: {root}")
    for path in root.rglob("*"):
        if is_link_or_junction(path):
            raise ValueError(
                f"plugin source contains a link or junction: {path.relative_to(root)}"
            )


def source_name(source: Path) -> str:
    manifest = source / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    name = data.get("name")
    if not isinstance(name, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", name
    ):
        raise ValueError(
            "plugin/plugin.json name must be one lowercase hyphenated path component"
        )
    return name


def ensure_contained(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} resolves outside the workspace: {resolved}") from exc
    return resolved


def install(source: Path, workspace_arg: Path, apply: bool) -> int:
    try:
        reject_linked_tree(source)
        name = source_name(source)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Invalid plugin source: {exc}", file=sys.stderr)
        return 1

    workspace = workspace_arg.resolve()
    if not workspace.is_dir():
        print(f"Workspace does not exist: {workspace}", file=sys.stderr)
        return 1

    plugins = workspace / ".agents" / "plugins"
    current = workspace
    for component in (".agents", "plugins"):
        current /= component
        if is_link_or_junction(current):
            print(
                f"Refusing installation through a link or junction: {current}",
                file=sys.stderr,
            )
            return 3

    try:
        projected_plugins = ensure_contained(plugins, workspace, "Plugin directory")
        destination = ensure_contained(
            projected_plugins / name, workspace, "Plugin destination"
        )
    except ValueError as exc:
        print(f"Refusing installation: {exc}", file=sys.stderr)
        return 3

    files = sorted(path.relative_to(source) for path in source.rglob("*") if path.is_file())
    required = {
        Path("plugin.json"),
        Path("rules/team-policy.md"),
        Path("skills/feature-pipeline/SKILL.md"),
        Path("agents/qa-tester.md"),
        Path("agents/penetration-tester.md"),
    }
    missing = sorted(required - set(files))
    if missing:
        print(f"Plugin source is incomplete: {missing}", file=sys.stderr)
        return 1

    print(f"Source: {source}")
    print(f"Destination: {destination}")
    print(f"Files: {len(files)}")
    if destination.exists() or is_link_or_junction(destination):
        print(
            "Refusing to overwrite an existing plugin. Remove or back it up explicitly first.",
            file=sys.stderr,
        )
        return 2
    if not apply:
        print("Dry run only. Re-run with --apply to install.")
        return 0

    try:
        plugins.mkdir(parents=True, exist_ok=True)
        for path in (workspace / ".agents", plugins):
            if is_link_or_junction(path):
                raise ValueError(f"installation path became a link or junction: {path}")
        resolved_plugins = ensure_contained(plugins, workspace, "Plugin directory")
        destination = ensure_contained(
            resolved_plugins / name, workspace, "Plugin destination"
        )
    except (OSError, ValueError) as exc:
        print(
            f"Refusing installation: {exc}",
            file=sys.stderr,
        )
        return 3

    if destination.exists() or is_link_or_junction(destination):
        print(
            "Refusing to overwrite an existing plugin. Remove or back it up explicitly first.",
            file=sys.stderr,
        )
        return 2

    staging = destination.parent / f".{name}.install-{uuid.uuid4().hex}"
    try:
        shutil.copytree(source, staging, symlinks=True)
        reject_linked_tree(staging)
        os.replace(staging, destination)
    except Exception:
        if staging.exists() and not is_link_or_junction(staging):
            shutil.rmtree(staging)
        raise
    print(f"Installed {name}. Restart or refresh Antigravity Customizations.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install dev-team-skills into a workspace without overwriting files."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="target Antigravity workspace root; defaults to the current directory",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the installation; without this flag the command is a dry run",
    )
    args = parser.parse_args()
    return install(SOURCE, args.workspace, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
