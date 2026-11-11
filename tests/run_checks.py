"""Exercise the package's checks, tasks, versions, page build and updater with synthetic fixtures."""

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import re
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit import link_findings, project_findings, public_findings  # noqa: E402
from init_project import prepare  # noqa: E402
import build_page  # noqa: E402
import update_skill  # noqa: E402
from update_skill import git  # noqa: E402


def check_version_and_tasks(package: Path) -> None:
    # The working tree is checked here, so plugin.json is read from disk, not from a commit.
    skill = (package / "SKILL.md").read_text(encoding="utf-8")
    skill_version = re.search(r"^\s+version:\s*([0-9.]+)\s*$", skill, re.M).group(1)
    plugin_version = json.loads((package / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    changelog = (package / "CHANGELOG.md").read_text(encoding="utf-8")
    changelog_version = re.search(r"^## ([0-9.]+)", changelog, re.M).group(1)
    assert skill_version == plugin_version == changelog_version, \
        f"versions differ: SKILL.md {skill_version}, plugin.json {plugin_version}, CHANGELOG {changelog_version}"
    listed = set(re.findall(r"\(tasks/([a-z-]+)\.md\)", skill))
    files = {p.stem for p in (package / "tasks").glob("*.md")}
    assert listed == files, f"SKILL.md tasks {sorted(listed ^ files)} do not match tasks/"
    for name in files:
        text = (package / "tasks" / f"{name}.md").read_text(encoding="utf-8")
        assert text.startswith(f"# {name} — "), f"task title must start with its name: {name}"
        for part in ("**When:**", "**Input:**", "**Result:**", "**Done when:**", "**Do not:**"):
            assert part in text, f"{name}: missing {part}"
    assert link_findings(package, [Path("SKILL.md")] + [Path("tasks") / f"{n}.md" for n in files]
                         + [Path("README.md"), Path("references") / "updates.md"]) == []


def check_build_page(root: Path) -> None:
    draft = root / "plan.draft.html"
    shutil.copyfile(build_page.DEFAULT_ASSETS / "plan.html", draft)
    page = build_page.build(draft, root / "plan.html", build_page.DEFAULT_ASSETS)
    assert "@import" not in page and "data:font/woff2;base64," in page and ".step-head" in page
    assert "<!--" not in page, "template notes must not reach the built page"
    assert build_page.broken_links('<a href="#x"></a><a href="https://example.org"></a><a href="absent.md"></a>',
                                   root) == ["absent.md"]


def fake_skill(path: Path, version: str, tests_pass: bool = True) -> None:
    (path / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (path / "tests").mkdir(exist_ok=True)
    (path / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"version": version, "repository": "https://example.org/skill"}), encoding="utf-8")
    (path / "SKILL.md").write_text(f"version {version}\n", encoding="utf-8")
    (path / "WORKFLOW.md").write_text("workflow\n", encoding="utf-8")
    (path / "CHANGELOG.md").write_text(f"# Changelog\n\n## {version}\n\n- change\n", encoding="utf-8")
    (path / "tests" / "run_checks.py").write_text("" if tests_pass else "raise SystemExit(1)\n", encoding="utf-8")


def commit(repo: Path, message: str) -> None:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=test", "-c", "user.email=test" + "@example.com", "commit", "-q", "-m", message)


def expect_refused(reason: str, *args, **kwargs) -> None:
    try:
        update_skill.run(*args, **kwargs)
    except update_skill.Refused:
        return
    raise AssertionError(reason)


def check_updater(root: Path) -> None:
    if os.environ.get(update_skill.UPDATING):
        print("SKIP updater fixture: running inside an update")
        return
    if shutil.which("git") is None:
        print("SKIP updater: git not found")
        return
    origin = root / "origin"
    origin.mkdir()
    git(origin, "init", "-q", "-b", "main")
    url = origin.as_posix()
    fake_skill(origin, "0.1.0")
    commit(origin, "0.1.0")
    git(root, "clone", "-q", url, "clone")
    clone = root / "clone"
    expect_refused("origin must match plugin.json unless --origin is given", "check", clone)
    assert update_skill.run("check", clone, origin=url) == 0
    assert update_skill.run("check", clone, origin=url, interval_days=30) == 0  # checked recently: no fetch
    fake_skill(origin, "0.2.0")
    commit(origin, "0.2.0")
    assert update_skill.run("check", clone, origin=url) == 2
    (clone / "WORKFLOW.md").write_text("local edit\n", encoding="utf-8")
    expect_refused("an update must be refused when the copy has local changes", "apply", clone, origin=url)
    git(clone, "checkout", "-q", "--", "WORKFLOW.md")
    assert update_skill.run("apply", clone, origin=url) == 0
    assert '"0.2.0"' in (clone / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    fake_skill(origin, "1.0.0")
    commit(origin, "1.0.0")
    expect_refused("a major update must wait for consent", "apply", clone, origin=url)
    before = git(clone, "rev-parse", "HEAD")
    fake_skill(origin, "1.0.1", tests_pass=False)
    commit(origin, "1.0.1 broken")
    expect_refused("a failing update must be rolled back", "apply", clone, origin=url, allow_major=True)
    assert git(clone, "rev-parse", "HEAD") == before, "rollback must return to the previous commit"
    for path in root.rglob("*"):  # git marks objects read-only; let the temporary folder be removed on Windows
        path.chmod(0o700)


def main() -> None:
    package = Path(__file__).resolve().parents[1]
    assert public_findings(package, ["Example" + "SecretToken"]) == [], "public package contains a private term"
    fixture_parent = (package / "tests").resolve()
    with TemporaryDirectory(dir=fixture_parent) as temp:
        root = Path(temp)
        assert root.resolve().is_relative_to(fixture_parent)
        (root / "public.md").write_text("# Public\n", encoding="utf-8")
        assert public_findings(root, []) == []
        contact = "person" + "@example.org"
        internal = "http:" + "//service.internal/x"
        (root / "private.md").write_text(
            "Contact " + contact + " at C:" + "\\\\Private\\\\Work or " + internal + "\n",
            encoding="utf-8",
        )
        findings = public_findings(root, [contact])
        assert any("email" in item for item in findings)
        assert any("Windows absolute path" in item for item in findings)
        assert any("non-public URL" in item for item in findings)
        assert any("denylist" in item for item in findings)
        context = root / "context.md"
        context.write_text("[exists](public.md) [missing](gone.md) [web](https:" + "//example.org)\n", encoding="utf-8")
        broken = link_findings(root, [Path("context.md")])
        assert len(broken) == 1 and "gone.md" in broken[0]
        (root / "gone.md").write_text("ok\n", encoding="utf-8")
        assert link_findings(root, [Path("context.md")]) == []
        fresh = root / "fresh-workspace-at-new-path"
        (fresh / ".project-lifecycle").mkdir(parents=True)
        (fresh / "workstreams" / "current").mkdir(parents=True)
        (fresh / "workstreams" / "current" / "incoming").mkdir()
        (fresh / "outputs").mkdir()
        (fresh / "archive").mkdir()
        (fresh / "AGENTS.md").write_text("Read [context](project_context.md).\n", encoding="utf-8")
        (fresh / "project_context.md").write_text(
            "Current [workstream](workstreams/current/project_context.md).\n", encoding="utf-8"
        )
        (fresh / "workstreams" / "current" / "project_context.md").write_text(
            "# Current\n", encoding="utf-8"
        )
        example = package / "assets" / "project.local.example.json"
        (fresh / ".project-lifecycle" / "config.json").write_bytes(example.read_bytes())
        assert project_findings(fresh) == [], "fresh workspace must resolve at a different path"
        (fresh / "project_context.md").unlink()
        assert any("missing path" in item for item in project_findings(fresh))
        empty = root / "empty-project"
        preview = prepare(empty, [], apply=False)
        assert all(line.startswith("WOULD CREATE") for line in preview)
        assert not empty.exists(), "preview must not create the project"
        created = prepare(empty, [], apply=True)
        assert len(created) == 2 and all(line.startswith("CREATE") for line in created)
        assert (empty / "PROJECT_WORKFLOW.md").is_file()
        context = empty / "project_context.md"
        context.write_text("# Existing context\n", encoding="utf-8")
        repeated = prepare(empty, [], apply=True)
        assert all(line.startswith("KEEP") for line in repeated)
        assert context.read_text(encoding="utf-8") == "# Existing context\n"
        optional = prepare(empty, ["codex", "claude"], apply=True)
        assert any(line.endswith("AGENTS.md") for line in optional)
        assert any(line.endswith("CLAUDE.md") for line in optional)
        assert "PROJECT_WORKFLOW.md" in (empty / "AGENTS.md").read_text(encoding="utf-8")
        assert "PROJECT_WORKFLOW.md" in (empty / "CLAUDE.md").read_text(encoding="utf-8")
        check_build_page(root)
        check_updater(root)
    check_version_and_tasks(package)
    print("PASS: public scan, links, empty-project setup, optional agent pointers, no overwrite, "
          "version and tasks, page build, updater")


if __name__ == "__main__":
    main()
