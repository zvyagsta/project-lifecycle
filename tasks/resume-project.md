# resume-project — continue on another device or after a break

**When:** a new computer, a fresh clone, a new chat, or «продолжаю с другого устройства».

**Input:** the project folder or repository; the skill installed for the user, the project copy of the skill, or both.

**Steps**
1. Clone with the skill copy: `git clone --recurse-submodules <project>`; after a plain clone run `git submodule update --init --recursive`.
2. Find the skill. The version installed for the user is the working one; the project copy is the pinned fallback. If both exist and their versions differ, say so and offer [update-skill](update-skill.md).
3. Read the entrypoints from `.project-lifecycle/config.json`, then the active workstream context.
4. Run `python scripts/audit.py project <folder>` and the project's own link check.
5. Report purpose, active stage, latest confirmed result, open questions and next step, naming the files read.

**Result:** a short status in chat; no files changed.

**Done when:** paths resolve on this device and the next step is clear.

**Do not:** treat an old chat summary or handoff note as current status; start the next task without the user's request.
