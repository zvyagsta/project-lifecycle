"""Check for and apply updates of a git-managed copy of this skill.

Usage:
    python scripts/update_skill.py check [--repo DIR] [--branch main] [--origin URL] [--interval-days N]
    python scripts/update_skill.py apply [--repo DIR] [--branch main] [--origin URL] [--allow-major]

DIR is a git clone or a git submodule of the skill (default: the folder this script belongs to).

check  fetches the remote branch and reports the installed and available versions with the
       changelog of the new version. It changes nothing in the skill. With --interval-days it does
       nothing when the last check was more recent (an agent's check at the start of work).
apply  is the user's consent to update, or the monthly scheduled task of a user-installed copy.
       It updates only when every safety condition holds:
         * the copy has no local changes;
         * origin is the expected repository (--origin, or the one named in .claude-plugin/plugin.json);
         * the remote version continues the local one (fast-forward only);
         * the remote version contains SKILL.md, WORKFLOW.md and .claude-plugin/plugin.json;
         * a new major version is applied only with --allow-major (it may change how work is done).
       After the update the new version's own tests (tests/run_*.py, tests/check_*.py) run; if any
       fails, the copy returns to the previous commit, which is printed.

Exit codes: 0 — up to date, checked recently or updated; 1 — refused or failed (the installed
version is kept); 2 — update available and not applied.
See references/updates.md for schedules and modes.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REQUIRED = ("SKILL.md", "WORKFLOW.md", ".claude-plugin/plugin.json")
STAMP = "project-lifecycle-last-check"
UPDATING = "PROJECT_LIFECYCLE_UPDATING"  # set while the updater runs tests; tests skip the updater fixture


class Refused(Exception):
    pass


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        raise Refused(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def normalize(url: str) -> str:
    url = url.strip().rstrip("/")
    return url[:-4] if url.endswith(".git") else url


def version_at(repo: Path, ref: str) -> tuple[str, str]:
    data = json.loads(git(repo, "show", f"{ref}:.claude-plugin/plugin.json"))
    return data.get("version", "0.0.0"), normalize(data.get("repository", ""))


def major(version: str) -> int:
    try:
        return int(version.split(".")[0])
    except ValueError:
        return 0


def changelog_section(repo: Path, ref: str, version: str) -> str:
    lines, keep = [], False
    for line in git(repo, "show", f"{ref}:CHANGELOG.md", check=False).splitlines():
        if line.startswith("## "):
            if keep:
                break
            keep = line[3:].strip() == version
        if keep:
            lines.append(line)
    return "\n".join(lines[:25]) or "(no changelog entry for this version)"


def stamp(repo: Path) -> Path:
    return Path(git(repo, "rev-parse", "--absolute-git-dir")) / STAMP


def checked_recently(repo: Path, days: int) -> bool:
    path = stamp(repo)
    return days > 0 and path.is_file() and time.time() - path.stat().st_mtime < days * 86400


def failed_test(repo: Path) -> str | None:
    env = {**os.environ, UPDATING: "1"}
    for test in sorted(repo.glob("tests/run_*.py")) + sorted(repo.glob("tests/check_*.py")):
        result = subprocess.run([sys.executable, "-I", str(test)], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", env=env)
        if result.returncode != 0:
            return f"{test.name}:\n{result.stdout}{result.stderr}"
    return None


def run(command: str, repo: Path, branch: str = "main", origin: str | None = None,
        allow_major: bool = False, interval_days: int = 0) -> int:
    if not (repo / ".git").exists():
        raise Refused(f"not a git clone or submodule: {repo}")
    if command == "check" and checked_recently(repo, interval_days):
        print("project-lifecycle: checked recently; next check later")
        return 0
    if git(repo, "status", "--porcelain"):
        raise Refused("the copy has local changes; nothing was changed")
    local_version, declared = version_at(repo, "HEAD")
    expected = normalize(origin) if origin else declared
    actual = normalize(git(repo, "remote", "get-url", "origin"))
    if not expected or actual != expected:
        raise Refused(f"origin {actual!r} is not the expected repository {expected!r}")

    remote = f"origin/{branch}"
    git(repo, "fetch", "--quiet", "origin", branch)
    stamp(repo).touch()
    head, target = git(repo, "rev-parse", "HEAD", remote).splitlines()
    if head == target:
        print(f"project-lifecycle {local_version}: up to date")
        return 0
    if git(repo, "merge-base", "HEAD", remote) != head:
        raise Refused("the remote version does not continue the local one; manual review needed")
    present = set(git(repo, "ls-tree", "-r", "--name-only", remote, "--", *REQUIRED).splitlines())
    if set(REQUIRED) - present:
        raise Refused(f"the remote version lacks {sorted(set(REQUIRED) - present)}")
    remote_version, _ = version_at(repo, remote)
    print(f"project-lifecycle: installed {local_version}, available {remote_version}")
    print(changelog_section(repo, remote, remote_version))

    if command == "check":
        return 2
    if major(remote_version) > major(local_version) and not allow_major:
        raise Refused(f"major update {local_version} → {remote_version} needs the user's consent (--allow-major)")
    git(repo, "reset", "--hard", "--quiet", target)  # fast-forward on a branch or a detached submodule
    failure = failed_test(repo)
    if failure:
        git(repo, "reset", "--hard", "--quiet", head)
        raise Refused(f"tests failed after the update; returned to {head[:7]}. {failure}")
    print(f"project-lifecycle: updated to {remote_version}; previous commit {head[:7]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check", "apply"))
    parser.add_argument("--repo", type=Path, default=SKILL, help="git clone or submodule of the skill")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--origin", help="expected repository URL (default: the one in plugin.json)")
    parser.add_argument("--allow-major", action="store_true", help="apply a new major version")
    parser.add_argument("--interval-days", type=int, default=0, help="check: skip if checked more recently")
    args = parser.parse_args()
    try:
        return run(args.command, args.repo.resolve(), args.branch, args.origin, args.allow_major, args.interval_days)
    except Refused as error:
        print(f"project-lifecycle: {error} The installed version is kept.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
