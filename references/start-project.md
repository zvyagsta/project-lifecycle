# Start a project workspace

An empty folder is a normal starting point. Ask only for missing essentials: project purpose, desired result, first work item, and preferred review rhythm if relevant. Do not require old files, code, chats, or a handoff summary. If the user already gave enough information, do not delay setup with repeated questions.

When the user requests setup, use the starter assets as a small default structure. Copy `WORKFLOW.md` from the skill to the new project root as `PROJECT_WORKFLOW.md`. Add `assets/starter/AGENTS.md` or `CLAUDE.md` only when those instruction formats are useful in the chosen environment; they are pointers to the one common file. Adapt names and folders to the project's actual work. Keep project-wide context short: purpose, success criteria, current stage, decisions, open questions, and next step. For a genuinely new project, say that past stages do not yet exist. For an ongoing project, accept any history the user provides and mark its source.

For a repeatable setup, run `python scripts/init_project.py <new-project-folder>` to preview the minimal files, then add `--apply` only after the user requests creation. The script creates missing files and never overwrites an existing context. Optional `--agent codex` and `--agent claude` add project instruction pointers. Fill `project_context.md` from the user's answers; the generated template is not a completed project brief.

Create an active workstream context only when there is a distinct stream to manage. Keep incoming originals, working files, approved outputs, and superseded versions separate. Do not invent completed stages, agreement, or delivery. Build code only when the user requests it.

The entry files contain no separate rules to maintain. Change shared behavior in the local `PROJECT_WORKFLOW.md`; change project facts in `project_context.md`. Local participants and addresses belong only in the new project's files, never in this skill.
