# Project Lifecycle

A reusable skill for starting and running projects with readable context, traceable decisions, organized materials, period plans and reviews, handoffs, and closure. It starts in an empty project folder; prior files or chat history are optional.

## Use

Install this folder as a skill in an agent that supports `SKILL.md`, using that agent's installation instructions. The method itself is in [WORKFLOW.md](WORKFLOW.md). The agent can read it directly if its host does not load skills automatically.

Ask the agent to start a project. It should gather the missing essentials and create the first context only when requested. The optional initializer previews a minimal folder setup without writing anything:

```text
python scripts/init_project.py <project-folder>
python scripts/init_project.py <project-folder> --apply
```

`--agent codex` or `--agent claude` adds a short project instruction file pointing to the same workflow. These files contain no separate version of the rules.

The [report style](references/report-style.md) includes A4 and horizontal templates, a shared color system, Bitter and Golos Text fonts, and optional SVG icons. Project-specific text, people, addresses, credentials, and source materials belong in the local project, outside this skill.

## Checks

```text
python tests/run_checks.py
python tests/check_style.py
python scripts/audit.py public .
```

The public-data scan catches common patterns; review the package yourself before publishing. The optional scripts use Python 3.11 or newer. The Markdown workflow and templates do not need Python.

The skill's code and templates are licensed under MIT. The bundled fonts remain under SIL OFL 1.1; see [font notices](assets/report-style/FONT-LICENSES.md).
