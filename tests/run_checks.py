"""Exercise the package's read-only checks with synthetic fixtures."""

from pathlib import Path
from tempfile import TemporaryDirectory
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit import link_findings, project_findings, public_findings  # noqa: E402
from init_project import prepare  # noqa: E402


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
    print("PASS: public scan, links, empty-project setup, optional agent pointers, no overwrite")


if __name__ == "__main__":
    main()
