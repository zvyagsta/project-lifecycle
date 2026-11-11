# Project Lifecycle

A skill that helps an AI agent run a project for you. The agent keeps the project's memory in plain files: what the project is for, where it stands, what was decided and why, which materials arrived. It writes plans and reviews, builds readable pages from them and closes the work when it is accepted.

The same files work with Claude Code, Codex and any agent that reads `SKILL.md`. You can switch agents or devices, and the next session picks up from the files rather than from a chat history.

The skill holds no project data. Everything about your project stays in your project folder.

## How the agent behaves

- It starts a task only when you ask for it. Finishing one task does not start the next.
- It does not send, publish or push anything without a separate request.
- It records a decision only when someone made one. A proposal or a discussion stays a proposal.
- It counts work as done only when there is evidence: a file, a message, a confirmed result. A plan is not evidence.
- It keeps earlier versions of results and never overwrites history.

## Tasks

Repeatable work is split into 13 named tasks. You ask in your own words, and the agent picks the task and follows its file in [tasks/](tasks/). The examples are in Russian, as in the skill's triggers; an agent understands the same request in English.

**Start and continue**

| Task | What the agent does | Example request |
|---|---|---|
| [start-project](tasks/start-project.md) | Asks for the purpose, the expected result and the first piece of work, then creates the project context in an empty folder. | «начни проект» — start a project |
| [resume-project](tasks/resume-project.md) | On a new device, after a fresh clone or in a new chat, reads the context and tells you where the work stands. Changes no files. | «продолжаю с другого устройства» — I'm continuing on another device |
| [update-skill](tasks/update-skill.md) | Checks for a new version of this skill and installs it if the new version's tests pass. Asks before a major version. | «обнови скилл» — update the skill |

**Everyday work**

| Task | What the agent does | Example request |
|---|---|---|
| [update-context](tasks/update-context.md) | After a result, a decision, a meeting or a new material, writes down what changed, why, what is still open and the next step. Checks the links. | runs after each result |
| [intake-material](tasks/intake-material.md) | Stores an incoming recording, transcript, document or table once, with its source and date, and notes whether anyone has reviewed it. | «прислали файл» — a file came in |
| [record-decision](tasks/record-decision.md) | Records a decision with its date, who made it and on what basis. | «записываем решение» — record the decision |
| [backup-project](tasks/backup-project.md) | Commits the project to a private repository you set up and checks that GitHub received the commit. Off until you configure it. | «сохрани копию» — save a copy |

**Plans and reports**

| Task | What the agent does | Example request |
|---|---|---|
| [plan-period](tasks/plan-period.md) | Writes a plan for a day, a week or another period in Markdown, then builds it into an HTML page. | «план на сегодня» — plan for today |
| [review-period](tasks/review-period.md) | Writes an internal review of the period with a link to evidence for each completed item. | «итоги дня» — results of the day |
| [report-period](tasks/report-period.md) | Prepares a report and an infographic for a manager or a team. Builds the files after you approve the text; sending them is a separate step. | «отчёт за день» — daily report |
| [build-page](tasks/build-page.md) | Turns a draft into one HTML file that opens offline, with fonts and styles inside, and checks links, text and layout at desktop and phone width. | used by plans and reviews |

**Closing**

| Task | What the agent does | Example request |
|---|---|---|
| [close-workstream](tasks/close-workstream.md) | Closes one line of work after its result is accepted and records the acceptance and the open follow-ups. | «закрываем направление» — close this workstream |
| [close-project](tasks/close-project.md) | Closes the project: final results, handover, open obligations, who supports what. | «закрываем проект» — close the project |

The full method behind the tasks is in [WORKFLOW.md](WORKFLOW.md). An agent that does not load skills automatically can read it directly.

## Install

### Claude Code

```text
/plugin install project-lifecycle --marketplace zvyagsta/project-lifecycle
```

This works in one step on Claude Code 2.1.275 or later. Then turn on updates: `/plugin` → `Marketplaces` → `project-lifecycle` → `Enable auto-update`. Third-party marketplaces start with updates off.

### Codex and other agents

Clone the repository into a permanent folder, for example `~/.agents/project-lifecycle`, and link it from the agent's skills folder (for Codex: `~/.codex/skills/project-lifecycle`). To get updates, run `python ~/.agents/project-lifecycle/scripts/update_skill.py apply` once a month, by hand or from a scheduled task. Commands for Windows Task Scheduler and cron are in [references/updates.md](references/updates.md).

### Let the agent install it

Copy this prompt to the agent. If you do not need automatic updates, the first paragraph is enough.

```text
Install the project-lifecycle skill from https://github.com/zvyagsta/project-lifecycle for the current user. In Claude Code, add the marketplace zvyagsta/project-lifecycle and install the plugin project-lifecycle@project-lifecycle in user scope. In Codex and other Agent Skills clients, install the repository folder as a personal skill. Check that the skill is available.

Keep the repository as the update source in the way that suits this client. In Claude Code, use the added marketplace and turn on its built-in auto-update; if only the user can switch it, give one final step: /plugin → Marketplaces → project-lifecycle → Enable auto-update. Do not create a separate scheduled task for Claude Code.

If the client cannot update a marketplace, keep a managed git clone in a permanent folder of the user and connect the skill from it with a folder link where the client and the operating system allow it; otherwise copy it and keep the previous copy. Create a permanent local task "project-lifecycle update" on the 1st of each month at 10:00 local time that runs: python <clone>/scripts/update_skill.py apply. The script updates fast-forward only, runs the skill's tests, keeps the installed version on any failure, and waits for consent before a new major version. Report the result in one short summary.

After setup, run python <clone>/scripts/update_skill.py check once. If the client supports neither marketplace auto-update nor local scheduled tasks, install the skill and report this limitation.
```

## Updates

The update script changes nothing unless every check passes: the copy has no local edits, it comes from this repository, the new version continues the installed one, and the new version's tests pass. If the tests fail, it returns to the previous version. A new major version (1.0, 2.0) waits for your consent, because it may change how the agent works.

A project can also keep its own pinned copy of the skill as a git submodule, so a fresh clone works right away. That copy changes only when you ask. Details: [references/updates.md](references/updates.md). Version history: [CHANGELOG.md](CHANGELOG.md). To hear about new versions without an agent, use `Watch` → `Custom` → `Releases` on this page.

## Start a project

Open an empty folder and ask the agent to start a project. It asks only for what it does not know yet and does not invent the project's history. To set up the folders without an agent, use the initializer. The first command shows what it would create; the second creates it:

```text
python scripts/init_project.py <project-folder>
python scripts/init_project.py <project-folder> --apply
```

`--agent codex` or `--agent claude` also adds a short instruction file for that agent. It only points to the same method and holds no rules of its own.

## Pages and reports

The skill includes templates for an A4 report, a horizontal infographic and a plan page. They share one color system, the Bitter and Golos Text fonts and optional SVG icons. `scripts/build_page.py` builds a plan or review into a single HTML file that opens without internet. Rules: [references/report-style.md](references/report-style.md).

## Private backup

The agent can save the whole project, archives included, to a private GitHub repository you choose: at the end of the day or on request. This is off until you set it up for a project, and the repository name stays in your project settings. Details: [references/private-backup.md](references/private-backup.md).

## Checks

```text
python tests/run_checks.py
python tests/check_style.py
python scripts/audit.py public . --denylist <file with your private terms>
```

The last command searches the skill for private data before you publish a fork or a change. It finds e-mail addresses, Windows paths, private network addresses and links to non-public sites, plus the terms from your denylist. Keep the denylist in your private project, never in this repository, and look through the files yourself before publishing.

The scripts need Python 3.11 or newer. The method and the templates work without Python.

## License

Code and templates: MIT. Bundled fonts: SIL OFL 1.1, see [assets/report-style/FONT-LICENSES.md](assets/report-style/FONT-LICENSES.md).
