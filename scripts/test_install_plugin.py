#!/usr/bin/env python3
"""Dependency-free regression tests for installer filesystem boundaries."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import install_plugin


class InstallerSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        preferred_tmp = os.environ.get("DEV_TEAM_SKILLS_TEST_TMP")
        if preferred_tmp is None:
            preferred_tmp = str(Path(__file__).resolve().parents[1])
        self.temporary = tempfile.TemporaryDirectory(dir=preferred_tmp)
        self.root = Path(self.temporary.name)
        self.source = self.root / "bundle"
        (self.source / "rules").mkdir(parents=True)
        (self.source / "skills" / "feature-pipeline").mkdir(parents=True)
        (self.source / "agents").mkdir(parents=True)
        self.write_manifest("dev-team-skills")
        (self.source / "rules" / "team-policy.md").write_text("policy", encoding="utf-8")
        (self.source / "skills" / "feature-pipeline" / "SKILL.md").write_text(
            "skill", encoding="utf-8"
        )
        (self.source / "agents" / "qa-tester.md").write_text("qa", encoding="utf-8")
        (self.source / "agents" / "penetration-tester.md").write_text(
            "security", encoding="utf-8"
        )
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_manifest(self, name: str) -> None:
        (self.source / "plugin.json").write_text(
            json.dumps({"name": name}), encoding="utf-8"
        )

    def run_install(self, apply: bool = True) -> int:
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return install_plugin.install(self.source, self.workspace, apply)

    def test_installs_once_and_refuses_overwrite(self) -> None:
        self.assertEqual(self.run_install(), 0)
        self.assertEqual(self.run_install(), 2)
        self.assertTrue(
            (self.workspace / ".agents" / "plugins" / "dev-team-skills").is_dir()
        )

    def test_rejects_manifest_path_traversal(self) -> None:
        self.write_manifest("../../escaped")
        self.assertEqual(self.run_install(), 1)
        self.assertFalse((self.root / "escaped").exists())

    def test_rejects_linked_source_entry(self) -> None:
        target = self.root / "outside-secret.txt"
        target.write_text("do not copy", encoding="utf-8")
        link = self.source / "linked-secret.txt"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertEqual(self.run_install(), 1)
        self.assertFalse((self.workspace / ".agents").exists())

    def test_rejects_linked_agents_path_without_outside_write(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        agents = self.workspace / ".agents"
        try:
            agents.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlink creation unavailable: {exc}")
        self.assertEqual(self.run_install(), 3)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
