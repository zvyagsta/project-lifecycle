"""Prepare a fresh project workspace without overwriting existing files."""

from __future__ import annotations

import argparse
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
COMMON = {
    "PROJECT_WORKFLOW.md": SKILL / "WORKFLOW.md",
    "project_context.md": SKILL / "assets" / "starter" / "project_context.md",
}
AGENT_FILES = {
    "codex": {"AGENTS.md": SKILL / "assets" / "starter" / "AGENTS.md"},
    "claude": {"CLAUDE.md": SKILL / "assets" / "starter" / "CLAUDE.md"},
}


def file_plan(agents: list[str]) -> dict[str, Path]:
    plan = dict(COMMON)
    for agent in agents:
        plan.update(AGENT_FILES[agent])
    return plan


def prepare(target: Path, agents: list[str], apply: bool) -> list[str]:
    plan = file_plan(agents)
    messages: list[str] = []
    for name, source in plan.items():
        destination = target / name
        if destination.exists():
            messages.append(f"KEEP {destination}")
            continue
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
            messages.append(f"CREATE {destination}")
        else:
            messages.append(f"WOULD CREATE {destination}")
    return messages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="new or existing project folder")
    parser.add_argument("--agent", action="append", choices=sorted(AGENT_FILES),
                        help="optional project instruction file; repeat for multiple agents")
    parser.add_argument("--apply", action="store_true", help="create missing files")
    args = parser.parse_args()
    agents = list(dict.fromkeys(args.agent or []))
    for message in prepare(args.project_dir.resolve(), agents, args.apply):
        print(message)
    if not args.apply:
        print("Preview only. Add --apply to create missing files.")


if __name__ == "__main__":
    main()
