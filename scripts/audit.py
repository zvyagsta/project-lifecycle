"""Small read-only checks for a project-lifecycle skill package and context links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt", ".toml", ".html", ".css", ".svg"}
PRIVATE_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "Windows absolute path": re.compile(r"\b[A-Z]:\\(?:[^\s\"'<>|]+)", re.I),
    "private network address": re.compile(r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"),
    "non-public URL": re.compile(r"https?://[^\s)\]<>\"']+", re.I),
}
LINK = re.compile(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)")


def public_findings(root: Path, denylist: list[str]) -> list[str]:
    findings: list[str] = []
    if not root.is_dir():
        return [f"missing directory: {root}"]
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        rel = path.relative_to(root)
        content = path.read_text(encoding="utf-8", errors="replace")
        for term in denylist:
            if term.casefold() in str(rel).casefold() or term.casefold() in content.casefold():
                findings.append(f"{rel}: private term from denylist")
        for label, pattern in PRIVATE_PATTERNS.items():
            for match in pattern.finditer(content):
                if label == "non-public URL":
                    host = match.group().split("/")[2].split(":")[0].lower()
                    if not (host.endswith(".local") or host.endswith(".internal") or "." not in host):
                        continue
                line = content.count("\n", 0, match.start()) + 1
                findings.append(f"{rel}:{line}: {label}")
    return sorted(set(findings))


def link_findings(project: Path, contexts: list[Path]) -> list[str]:
    findings: list[str] = []
    for item in contexts:
        path = item if item.is_absolute() else project / item
        if not path.is_file():
            findings.append(f"missing context: {path}")
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for match in LINK.finditer(content):
            target = unquote(match.group(1).strip("<>").split("#", 1)[0])
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            if not (path.parent / target).exists():
                line = content.count("\n", 0, match.start()) + 1
                findings.append(f"{path}:{line}: missing link target {target}")
    return findings


def project_findings(project: Path) -> list[str]:
    """Check that a workspace can resolve its local configuration."""
    root = project.resolve()
    config_path = root / ".project-lifecycle" / "config.json"
    if not config_path.is_file():
        return [f"missing local configuration: {config_path}"]
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid local configuration: {error}"]
    findings: list[str] = []
    entrypoints = config.get("entrypoints")
    paths = config.get("paths")
    if not isinstance(entrypoints, list) or not entrypoints or not all(isinstance(x, str) for x in entrypoints):
        findings.append("entrypoints must be a nonempty list of relative paths")
        entrypoints = []
    if not isinstance(paths, dict) or not all(isinstance(x, str) for x in paths.values()):
        findings.append("paths must map names to relative paths")
        paths = {}
    targets: list[tuple[str, str]] = [("entrypoint", x) for x in entrypoints]
    targets.extend((name, value) for name, value in paths.items())
    for label, value in targets:
        candidate = Path(value)
        if candidate.is_absolute() or not (root / candidate).resolve().is_relative_to(root):
            findings.append(f"{label}: path must stay inside project: {value}")
        elif not (root / candidate).exists():
            findings.append(f"{label}: missing path: {value}")
    safe_contexts = [Path(x) for x in entrypoints if Path(x).suffix.lower() == ".md"
                     and not Path(x).is_absolute() and (root / x).resolve().is_relative_to(root)]
    findings.extend(link_findings(root, safe_contexts))
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    pub = sub.add_parser("public", help="scan text files for likely private data")
    pub.add_argument("package", type=Path)
    pub.add_argument("--denylist", type=Path, help="local file with one private term per line")
    links = sub.add_parser("links", help="check local Markdown links in context files")
    links.add_argument("project", type=Path)
    links.add_argument("contexts", nargs="+", type=Path)
    project = sub.add_parser("project", help="check a workspace's local configuration")
    project.add_argument("project", type=Path)
    args = parser.parse_args()
    if args.mode == "public":
        terms: list[str] = []
        if args.denylist:
            if not args.denylist.is_file():
                parser.error("denylist file does not exist")
            terms = [line.strip() for line in args.denylist.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.lstrip().startswith("#")]
        found = public_findings(args.package, terms)
    elif args.mode == "links":
        found = link_findings(args.project, args.contexts)
    else:
        found = project_findings(args.project)
    for item in found:
        print(item)
    if found:
        print(f"FAIL: {len(found)} finding(s)")
        return 1
    print("PASS: no findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
