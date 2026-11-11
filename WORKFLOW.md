# Project workflow — common instructions

This file is the portable method. It works in a clean, empty project folder as well as an established project. The project context supplies facts when one exists; this file supplies the workflow. Prior folders, code, and chat history are never prerequisites.

## Start or continue

1. If the folder is empty and no `project_context.md` exists, treat this as a new project. Ask only for missing essentials: purpose, desired result, immediate work, and any review rhythm the user wants. If the user already gave them, proceed. Create the initial structure and context only when asked to start or set up the project. Record unknowns instead of inventing history.
2. If `project_context.md` exists, read it and the local rules. Identify the purpose, active stage, latest confirmed result, open questions, and next step. Name the files used. If the folder contains other project files but no context, inspect what is available and ask where the current facts are; do not assume the project is new.
3. Follow the user's current request. A question, doubt, or correction first needs an answer and reasons; it is not automatically an instruction to edit files.
4. Match the request to a named task in `tasks/` (listed in `SKILL.md`) and follow its steps. If no task fits, use the rules below.
5. If local settings enable skill update checks (`skill_updates`), check once per configured interval at the start of work and report the result in one line; apply an update only as the configured mode allows. A project copy of the skill stays pinned until the user asks to update it.

## Work with materials and results

- Classify each statement as confirmed fact, decision, plan, proposal, or unknown. A file's existence does not prove approval, delivery, deployment, or completion.
- Preserve each incoming original once. Record its source role, receipt date, review status, and canonical path. Other workstreams link to it.
- Keep internal evidence and source links with the work. Record review, approval, and external delivery as separate events, each with its own evidence.
- Preserve superseded versions and point current navigation to the new result. Treat dated handoff notes and prior plans as snapshots; current context takes precedence, and conflicts should be surfaced.
- After an authorized substantive change, update the active context with what changed, why, what remains open, and the next action. Update the project overview only when the whole project changes. Check local links.

## Plans, reviews, and closure

- Use the user's chosen cadence, time zone, and period boundaries. A schedule preference does not create an automation. Count completed work from evidence, not from plans.
- Keep a period plan short: objective, priority outcomes, dependencies, decisions needed. A review separates completed work, work in progress, decisions, unknowns, delivery, and next steps.
- Close a workstream when acceptance evidence and remaining handoff are recorded. Close the whole project only after project-level acceptance, open obligations, ownership, and archive locations are resolved.

## Optional private backup

- A GitHub repository is an optional project-specific store, not a prerequisite for this workflow. Configure its owner, repository, visibility, exclusions, and backup triggers only on the user's request. Keep these values in the local project, not in this public skill.
- When the user has authorized a continuing backup cadence, run it at the configured end-of-day checkpoint or on a direct backup request. This is a workflow trigger, not a background schedule. Update the context and check links first; then review changed files, exclude credentials and user-excluded material, commit, push, and verify that the remote received the commit. Preserve project archives unless the user excludes them.
- If the remote is not private, access is unclear, a sensitive file is staged, or the push fails, stop the upload and report the exact state. Never describe a local commit as a completed backup. Follow [private-backup.md](references/private-backup.md) for the detailed sequence.

## Communication and authorization

Write briefly: one conclusion, then up to three steps when useful. Use plain language. Create or edit files, settings, automations, and external destinations only on the user's direct request; perform the requested scope. Propose additional changes in words first. Do not send or publish without separate authorization.

For details, use the relevant files in `references/` when available. A copied `PROJECT_WORKFLOW.md` in a project must remain usable even without those references; the rules above are sufficient to continue safely.
