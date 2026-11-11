# Install and update the skill

The skill has one version, written in `SKILL.md` (`metadata.version`) and `.claude-plugin/plugin.json`. Changes are listed in [CHANGELOG.md](../CHANGELOG.md). A new MAJOR version may change how work is done, so it is applied only with the user's consent.

## Where the skill lives

- **Installed for the user** — the working version. It updates by itself as described below.
- **Project copy** — an optional git submodule inside a project, pinned to one commit. A fresh clone of the project gets the skill immediately, even before the user installs it. It changes only through [update-skill](../tasks/update-skill.md), and the project records the new pointer only on the user's request.

When both exist, the agent uses the installed version and reports a version difference.

## Claude Code: plugin marketplace

```text
claude plugin marketplace add zvyagsta/project-lifecycle
claude plugin install project-lifecycle@project-lifecycle --scope user
```

Then `/plugin` → `Marketplaces` → `project-lifecycle` → `Enable auto-update`. Third-party marketplaces start with auto-update off. The updated plugin loads after `/reload-plugins` or the next start. If the skill was also copied into the personal skills folder, remove that copy so only one version is loaded.

## Codex and other skill-aware agents: managed git clone

1. Clone once into a permanent folder of the user, for example `~/.agents/project-lifecycle`.
2. Make the client see it: a folder link from the client's skills folder (for Codex: `~/.codex/skills/project-lifecycle`) to the clone. Where links are not available, copy the folder and keep the previous copy until the new one is checked.
3. Create a monthly task «project-lifecycle update» on the 1st at 10:00 local time that runs `update_skill.py apply`. Create it only on the user's request.

Windows (Task Scheduler; runs Python, so no PowerShell script policy is involved):

```text
schtasks /Create /TN "project-lifecycle update" /SC MONTHLY /D 1 /ST 10:00 /TR "python \"%USERPROFILE%\.agents\project-lifecycle\scripts\update_skill.py\" apply"
```

macOS and Linux (cron):

```text
0 10 1 * * python3 ~/.agents/project-lifecycle/scripts/update_skill.py apply >> ~/.agents/project-lifecycle-update.log 2>&1
```

The scheduled task is the user's standing consent for MINOR and PATCH updates of the user-installed copy. The script changes nothing unless every check passes: no local changes, origin matches `plugin.json` (or `--origin` for a fork), the remote version continues the local one, required files exist, the new version's tests pass. On a failed test it returns to the previous commit. A MAJOR version waits for `--allow-major`, which only the user gives.

## Agent check at the start of work

`skill_updates.mode` in the project's local settings governs the agent and the project copy:

| Mode | At the start of work | Applying |
|---|---|---|
| `notify` | `update_skill.py check --interval-days 30` | `apply` only after the user agrees |
| `auto-minor` | the same check | `apply` for MINOR and PATCH; MAJOR after the user agrees |
| `pinned` | no check | only on a direct request |

`--interval-days` stores the time of the last check inside the copy's git folder, so the check runs at most once a month whatever the number of sessions. Network access to GitHub is required; without it the agent says that the check was not possible.

## Getting notified without an agent

On the repository page, `Watch` → `Custom` → `Releases` sends a message for each published version.
