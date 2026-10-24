#!/usr/bin/env python3
"""Synchronize the committed Antigravity plugin from canonical workspace sources."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"
MIRRORS = (
    (ROOT / ".agents" / "skills", PLUGIN / "skills"),
    (ROOT / ".agents" / "agents", PLUGIN / "agents"),
    (ROOT / ".agents" / "references", PLUGIN / "references"),
)
FILES = ((ROOT / ".agents" / "GUARDRAILS.md", PLUGIN / "GUARDRAILS.md"),)


def is_link_or_junction(path: Path) -> bool:
    return path.is_symlink() or (
        hasattr(path, "is_junction") and path.is_junction()
    )


def linked_entries(directory: Path) -> list[Path]:
    entries = [directory] if is_link_or_junction(directory) else []
    entries.extend(path for path in directory.rglob("*") if is_link_or_junction(path))
    return entries


def escapes_repository(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
    except ValueError:
        return True
    return False


def relative_files(directory: Path) -> set[Path]:
    return {
        path.relative_to(directory)
        for path in directory.rglob("*")
        if path.is_file()
    }


def differences() -> list[str]:
    problems: list[str] = []
    if is_link_or_junction(PLUGIN) or escapes_repository(PLUGIN):
        problems.append("unsafe plugin root link, junction, or external resolution")
    for source, destination in MIRRORS:
        if escapes_repository(source):
            problems.append(
                f"source root resolves outside repository: {source.relative_to(ROOT)}"
            )
        if destination.exists() and escapes_repository(destination):
            problems.append(
                f"plugin root resolves outside repository: {destination.relative_to(ROOT)}"
            )
        for linked in linked_entries(source):
            problems.append(f"unsafe source link or junction: {linked.relative_to(ROOT)}")
        if destination.exists():
            for linked in linked_entries(destination):
                problems.append(
                    f"unsafe plugin link or junction: {linked.relative_to(ROOT)}"
                )
        expected = relative_files(source)
        actual = relative_files(destination) if destination.is_dir() else set()
        for relative in sorted(expected - actual):
            problems.append(f"missing plugin file: {destination.relative_to(ROOT) / relative}")
        for relative in sorted(actual - expected):
            problems.append(f"stale plugin file: {destination.relative_to(ROOT) / relative}")
        for relative in sorted(expected & actual):
            if (source / relative).read_bytes() != (destination / relative).read_bytes():
                problems.append(f"out-of-sync plugin file: {destination.relative_to(ROOT) / relative}")
    for source, destination in FILES:
        if is_link_or_junction(source):
            problems.append(f"unsafe source link or junction: {source.relative_to(ROOT)}")
        if is_link_or_junction(destination):
            problems.append(
                f"unsafe plugin link or junction: {destination.relative_to(ROOT)}"
            )
        if not destination.is_file():
            problems.append(f"missing plugin file: {destination.relative_to(ROOT)}")
        elif source.read_bytes() != destination.read_bytes():
            problems.append(f"out-of-sync plugin file: {destination.relative_to(ROOT)}")
    return problems


def synchronize() -> None:
    unsafe = []
    if is_link_or_junction(PLUGIN) or escapes_repository(PLUGIN):
        unsafe.append(PLUGIN)
    for source, destination in MIRRORS:
        unsafe.extend(path for path in (source, destination) if escapes_repository(path))
        unsafe.extend(linked_entries(source))
        if destination.exists():
            unsafe.extend(linked_entries(destination))
    for source, destination in FILES:
        unsafe.extend(path for path in (source, destination) if is_link_or_junction(path))
    if unsafe:
        formatted = ", ".join(str(path.relative_to(ROOT)) for path in unsafe)
        raise ValueError(f"refusing to synchronize through links or junctions: {formatted}")

    for source, destination in MIRRORS:
        destination.mkdir(parents=True, exist_ok=True)
        for relative in sorted(relative_files(source)):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
    for source, destination in FILES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync or verify the committed Antigravity plugin mirror."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without changing files",
    )
    args = parser.parse_args()

    if not args.check:
        synchronize()
    problems = differences()
    if problems:
        print("Plugin synchronization failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        if not args.check:
            print("Remove stale generated files explicitly, then run again.", file=sys.stderr)
        return 1
    print("Plugin mirror is synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
