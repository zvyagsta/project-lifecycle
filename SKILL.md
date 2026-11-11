---
name: project-lifecycle
description: "Start or maintain a project workspace through named repeatable tasks: context, incoming materials, decisions, period plans and reviews with designed plan and report pages, private backups, skill updates, and closure. Use for a new workspace or an ongoing project; do not infer authorization to publish or send files. Триггеры: «начни проект», «продолжаю с другого устройства», «план на сегодня», «план недели», «итоги дня», «итоги недели», «отчёт за день», «инфографика», «запиши решение», «прислали материал», «обнови контекст», «сохрани копию», «обнови скилл», «закрываем направление»."
metadata:
  version: 0.2.0
---

# Project lifecycle

Read [WORKFLOW.md](WORKFLOW.md) before working. It is the single, tool-neutral instruction for this method. Project-specific facts live only in the project's local context and settings, never in this skill.

## Repeatable tasks

Pick the task that matches the request and follow its file. Each task file has the same parts: when, input, steps, result, done when, do not. A task starts only on the user's request; finishing one task does not start the next.

| Task | What it does | Typical request |
|---|---|---|
| [start-project](tasks/start-project.md) | Set up a project in an empty folder | «начни проект» |
| [resume-project](tasks/resume-project.md) | Continue on another device or after a break | «продолжаю с другого устройства» |
| [update-skill](tasks/update-skill.md) | Check and apply a new version of this skill | «обнови скилл», monthly check |
| [plan-period](tasks/plan-period.md) | Plan for a day, week or period: Markdown and a plan page | «план на сегодня» |
| [review-period](tasks/review-period.md) | Internal review of a period with evidence | «итоги дня» |
| [report-period](tasks/report-period.md) | Report and infographic for other readers, after approval | «отчёт за день» |
| [update-context](tasks/update-context.md) | Record a substantive iteration and check links | after any result |
| [intake-material](tasks/intake-material.md) | Store an incoming original once and record it | «прислали файл» |
| [record-decision](tasks/record-decision.md) | Record a decision with date, role and basis | «записываем решение» |
| [build-page](tasks/build-page.md) | Build one offline HTML page with checks | inside plans and reviews |
| [backup-project](tasks/backup-project.md) | Private backup with remote verification | «сохрани копию» |
| [close-workstream](tasks/close-workstream.md) | Close one workstream with acceptance evidence | «закрываем направление» |
| [close-project](tasks/close-project.md) | Close the whole project | «закрываем проект» |

## References

[start-project.md](references/start-project.md) — empty workspace. [portability.md](references/portability.md) — another environment or device. [updates.md](references/updates.md) — installing and updating this skill. [reviews.md](references/reviews.md) — plans and reviews. [report-style.md](references/report-style.md) — report, infographic and plan pages. [private-backup.md](references/private-backup.md) — private backups. [lifecycle.md](references/lifecycle.md) — states of materials, results, decisions and closure. Use only the references relevant to the request.

The core workflow is independent of a particular model or tool. Optional project instruction files are short pointers to the same workflow; they are not required to start a project.
