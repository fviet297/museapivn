"""Upgrade must merge upstream into the local branch, never overwrite local commits.
Standard library only; compiles the helpers from app.py without importing FastAPI or the engine."""
import ast
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "app.py"
HELPERS = {"_git", "_git_error", "_is_in_local_history", "_merge_upstream"}
tree = ast.parse(SOURCE.read_bytes(), filename=str(SOURCE))
module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in HELPERS],
                    type_ignores=[])


class FakeHTTPException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def run(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def commit_file(repo, name, content, message):
    Path(repo, name).write_text(content, encoding="utf-8")
    run(repo, "add", name)
    run(repo, "commit", "-m", message)
    return run(repo, "rev-parse", "HEAD")


def init_repo(path):
    run(path, "init", "-b", "main")
    run(path, "config", "user.name", "test")
    run(path, "config", "user.email", "test@example.com")


class UpgradeMergeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.upstream = os.path.join(self.tmp.name, "upstream")
        self.fork = os.path.join(self.tmp.name, "fork")
        os.makedirs(self.upstream)
        init_repo(self.upstream)
        commit_file(self.upstream, "ui.txt", "标题\n\n按钮\n", "base")
        commit_file(self.upstream, "core.txt", "v1\n", "core v1")
        run(self.tmp.name, "clone", "-q", self.upstream, self.fork)
        run(self.fork, "config", "user.name", "test")
        run(self.fork, "config", "user.email", "test@example.com")
        commit_file(self.fork, "ui.txt", "Tiêu đề\n\nNút\n", "Việt hoá")
        self.ns = {"os": os, "BASE_DIR": self.fork, "HTTPException": FakeHTTPException,
                   "UPSTREAM_REF": "refs/remotes/upstream/main"}
        exec(compile(module, str(SOURCE), "exec"), self.ns)

    def tearDown(self):
        self.tmp.cleanup()

    def test_upstream_base_already_in_fork_is_not_an_update(self):
        upstream_head = run(self.upstream, "rev-parse", "--short", "HEAD")
        self.assertTrue(self.ns["_is_in_local_history"](upstream_head))

    def test_new_upstream_commit_is_an_update(self):
        new_sha = commit_file(self.upstream, "core.txt", "v2\n", "core v2")
        self.assertFalse(self.ns["_is_in_local_history"](new_sha[:7]))

    def test_merge_keeps_translation_and_brings_new_feature(self):
        new_sha = commit_file(self.upstream, "core.txt", "v2\n", "core v2")
        self.ns["_merge_upstream"](self.upstream)
        self.assertEqual(Path(self.fork, "ui.txt").read_text(encoding="utf-8"), "Tiêu đề\n\nNút\n")
        self.assertEqual(Path(self.fork, "core.txt").read_text(encoding="utf-8"), "v2\n")
        self.assertTrue(self.ns["_is_in_local_history"](new_sha))

    def test_conflict_aborts_and_keeps_current_code(self):
        commit_file(self.upstream, "ui.txt", "新标题\n\n按钮\n", "upstream edits translated line")
        head_before = run(self.fork, "rev-parse", "HEAD")
        with self.assertRaises(FakeHTTPException) as ctx:
            self.ns["_merge_upstream"](self.upstream)
        self.assertEqual(ctx.exception.status_code, 409)
        self.assertIn("ui.txt", ctx.exception.detail)
        self.assertEqual(run(self.fork, "rev-parse", "HEAD"), head_before)
        self.assertFalse(os.path.exists(os.path.join(self.fork, ".git", "MERGE_HEAD")))
        self.assertEqual(Path(self.fork, "ui.txt").read_text(encoding="utf-8"), "Tiêu đề\n\nNút\n")

    def test_fetch_failure_raises_without_touching_code(self):
        head_before = run(self.fork, "rev-parse", "HEAD")
        with self.assertRaises(FakeHTTPException) as ctx:
            self.ns["_merge_upstream"](os.path.join(self.tmp.name, "missing"))
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertEqual(run(self.fork, "rev-parse", "HEAD"), head_before)


if __name__ == "__main__":
    unittest.main()
