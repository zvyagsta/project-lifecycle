# start-project — start a project

**When:** an empty folder, or the user asks to start or set up a project.

**Input:** purpose, desired result, first work item, review rhythm if the user wants one. Ask only for what is missing.

**Steps**
1. If `project_context.md` exists, this is not a new project: switch to [resume-project](resume-project.md).
2. Preview the starter files: `python scripts/init_project.py <folder>`. Create them with `--apply` only on the user's request.
3. Fill `project_context.md` from the user's answers. For a new project the history section says «Пока нет».
4. If the user wants local settings, create `.project-lifecycle/config.json` from `assets/project.local.example.json`, then run `python scripts/audit.py project <folder>`.

**Result:** `PROJECT_WORKFLOW.md`, `project_context.md`, optional agent pointers and local settings.

**Done when:** the context names purpose, success criteria, current stage and next step; `audit.py project` passes when settings exist.

**Do not:** invent past stages, approvals or deliveries; overwrite an existing context. Details — [start-project.md](../references/start-project.md).
