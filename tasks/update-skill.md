# update-skill — check and apply a new version of this skill

**When:** the monthly check, the user asks «обнови скилл», or [resume-project](resume-project.md) finds two different versions.

**Input:** the skill copy to update — a git clone installed for the user, or the project copy (git submodule); the mode from `skill_updates` in local settings: `notify`, `auto-minor` or `pinned`.

**Steps**
1. Mode `pinned`: stop unless the user asked directly.
2. `python scripts/update_skill.py check --repo <copy> --interval-days 30` (without `--interval-days` on a direct request) shows the installed and available versions and the changelog. Exit code 2 means an update is available.
3. Mode `notify`: tell the user what changed and apply only on consent. Mode `auto-minor`: apply MINOR and PATCH updates; a MAJOR update always needs consent.
4. `python scripts/update_skill.py apply --repo <copy>`; add `--allow-major` only with consent, `--origin <url>` for a fork. The script updates fast-forward only, runs the new version's tests and returns to the previous commit if they fail.
5. For a project copy, the project now shows a changed skill pointer. Commit it only on the user's request, with the version in the message.
6. A plugin install in Claude Code updates through the marketplace's auto-update instead; see [updates.md](../references/updates.md).

**Result:** the copy is on the new version, or the user knows an update is waiting and why it was not applied.

**Done when:** the script printed «up to date» or «updated to X»; a refusal is reported with its reason.

**Do not:** update a copy with local changes, force a merge, or create a scheduled task without the user's request.
