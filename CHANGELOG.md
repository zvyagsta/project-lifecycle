# Changelog

Versions follow `MAJOR.MINOR.PATCH`. A new MAJOR version may change how work is done and is applied only with the user's consent. MINOR adds tasks, templates, or checks without changing existing behavior. PATCH fixes text and bugs. The version is the same in `SKILL.md` and `.claude-plugin/plugin.json`; `tests/run_checks.py` checks this.

## 1.1.0

- Added the `analytical-note` task for a source-backed answer to a project question. It uses the Minto pyramid by default, separates published behavior, local observations, inferences and unknowns, and checks the requested reading format.
- Keep personal data local during analytical research. The public package and release metadata may identify only the creator's public GitHub account; local checks and an explicit approval of the reviewed update precede publication.
- Added Codex alongside Claude and zvyagsta in the README contributors list. Existing plan, review and report behavior is unchanged.

## 1.0.0

- **Changed approval workflow:** present a designed HTML report and infographic before requesting approval. Keep the text draft internal; export only the approved HTML version to the project's accepted formats. This replaces text-draft approval before layout, so installation requires consent for a major version.
- Added reusable report-content rules: progress against the plan, a self-contained explanation of purpose and value for any kind of work, useful measures only, and brief next steps from the current plan. Preserve uncertainty and distinguish planned targets from completed results.
- Preserve accepted content during narrow corrections; retain prior versions and check exported text and layout.
- Show full clickable local paths in user-facing file links. Keep real project paths out of public skill files.
- Keep approved final documents, the current period plan and active prompt visible after release; archive working materials and older versions without deletion, update links and verify retained files.
- Added a publication procedure with local validation, private-data review before staging and again on the exact staged diff, author/committer/tagger metadata review before push, version consistency and remote verification. Project data and private denylists remain outside the public package.
- Updated README, task instructions, shared workflow, design references and synthetic review cases to the same approval and archive rules. Existing export formats and design assets are unchanged.

## 0.2.0

- Named repeatable tasks in `tasks/`: `start-project`, `resume-project`, `update-skill`, `plan-period`, `review-period`, `report-period`, `update-context`, `intake-material`, `record-decision`, `build-page`, `backup-project`, `close-workstream`, `close-project`.
- Plan page: `assets/report-style/plan.html` and `plan.css` in the same design system as the report.
- `scripts/build_page.py`: one offline HTML file with embedded fonts; checks placeholders, links, text against Markdown, and layout at 1280 and 400 px.
- Updates: Claude Code plugin marketplace (`.claude-plugin/`), Codex metadata (`agents/openai.yaml`), `scripts/update_skill.py` for git clones and submodules (`check` with `--interval-days`, `apply` with `--origin` and `--allow-major`; the new version's own tests gate the update), monthly schedule examples and update modes in `references/updates.md`, install prompt in README.
- `scripts/audit.py`: shared `missing_target` link check used by `link_findings` and `build_page.py`.
- Local configuration example: `skill_updates`.

## 0.1.0

- First public version: workflow, lifecycle and review rules, starter files, report and infographic style, private backup, read-only checks.
