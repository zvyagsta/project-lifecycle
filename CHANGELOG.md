# Changelog

Versions follow `MAJOR.MINOR.PATCH`. A new MAJOR version may change how work is done and is applied only with the user's consent. MINOR adds tasks, templates, or checks without changing existing behavior. PATCH fixes text and bugs. The version is the same in `SKILL.md` and `.claude-plugin/plugin.json`; `tests/run_checks.py` checks this.

## 0.2.0

- Named repeatable tasks in `tasks/`: `start-project`, `resume-project`, `update-skill`, `plan-period`, `review-period`, `report-period`, `update-context`, `intake-material`, `record-decision`, `build-page`, `backup-project`, `close-workstream`, `close-project`.
- Plan page: `assets/report-style/plan.html` and `plan.css` in the same design system as the report.
- `scripts/build_page.py`: one offline HTML file with embedded fonts; checks placeholders, links, text against Markdown, and layout at 1280 and 400 px.
- Updates: Claude Code plugin marketplace (`.claude-plugin/`), Codex metadata (`agents/openai.yaml`), `scripts/update_skill.py` for git clones and submodules (`check` with `--interval-days`, `apply` with `--origin` and `--allow-major`; the new version's own tests gate the update), monthly schedule examples and update modes in `references/updates.md`, install prompt in README.
- `scripts/audit.py`: shared `missing_target` link check used by `link_findings` and `build_page.py`.
- Local configuration example: `skill_updates`.

## 0.1.0

- First public version: workflow, lifecycle and review rules, starter files, report and infographic style, private backup, read-only checks.
