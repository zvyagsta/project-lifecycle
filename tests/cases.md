# Edge cases for a project lifecycle skill

These are behavioral dry runs. A pass means the prototype instructions lead to the expected decision; it is not an autonomous-agent benchmark.

| Case | Input | Expected decision | Dry-run result |
|---|---|---|---|
| Empty folder | A user has only a clean project folder and asks to start a project. | Ask for missing essentials, then create a minimal context on request; do not require old files. | Pass: WORKFLOW.md and start-project.md specify this; initializer tested. |
| Shared incoming | A source document arrives in workstream A; workstream B later needs it. | Keep one canonical original in A, link from B, record findings in each context. | Pass: WORKFLOW.md and lifecycle.md specify this. |
| File without delivery | A report is generated and approved, with no evidence it was sent. | Mark approved; keep delivery unconfirmed. | Pass: WORKFLOW.md and lifecycle.md separate states. |
| Stale handoff | A dated chat handoff says workstream A is active; current context says B is active. | Read B as current; identify the handoff as a dated snapshot and surface the conflict. | Pass: WORKFLOW.md specifies this. |
| Partial closure | One deliverable is accepted, but integration and handover remain open. | Close only the accepted workstream; keep project active. | Pass: WORKFLOW.md and lifecycle.md specify this. |
| Unconfirmed meeting | A period plan lists a meeting, but there is no record it happened. | Review says meeting was planned; does not count it as completed. | Pass: reviews.md plan/review rules. |
| Overlapping periods | A two-week review already counted an outcome; a monthly review includes the same dates. | Summarize with a link, avoid double counting. | Pass: reviews.md period boundaries. |
| Public leakage | A reusable template contains a private name, email, path, or internal URL. | Block release; remove the value from the public package, keep it in local configuration. | Partial: audit.py detects denylisted terms and common patterns; human review remains necessary. |
| New computer | A user starts a project in a fresh workspace at another path. | Resolve the new context locally; prior project material is optional. | Checked as a behavioral dry run; path resolution is checked with a fresh synthetic workspace in `run_checks.py`. |
| Existing context | Setup is run again after the user filled `project_context.md`. | Keep the existing file byte for byte. | Checked in `run_checks.py`. |
| Backup not configured | A user starts in an empty folder and ends the day. | Do not create a repository or upload files. | Pass: WORKFLOW.md and private-backup.md require explicit local configuration. |
| Private backup with archives | The user configured a private repository and authorized end-of-day backup. | Check context and links, include retained archives, exclude configured files and credentials, push, verify remote commit. | Behavioral case; remote access depends on the host and user account. |
| Backup upload fails | A local commit succeeds but the push fails. | Report that the backup is only local; retry after access is restored. | Pass: WORKFLOW.md and private-backup.md distinguish commit from verified remote backup. |
| Named task | The user asks «план на сегодня». | Follow `tasks/plan-period.md`: Markdown first, plan page built and checked, path given, the page not opened without consent, the plan's tasks not started. | Checked in `run_checks.py`: every task is listed in SKILL.md and has the common parts; behavior is a dry run. |
| Plan page offline | A plan page is opened on a device without internet access. | Fonts and styles are embedded; the page renders the same. | Checked in `run_checks.py`: the build inlines styles and fonts. |
| Update available | The installed copy is behind the repository. | `update_skill.py check` reports both versions and the changelog; mode `notify` applies only on consent. | Checked in `run_checks.py` with a synthetic repository. |
| Update with local edits | The managed copy was edited locally. | Refuse the update and keep the installed version. | Checked in `run_checks.py`. |
| Major update | A new MAJOR version is published. | Wait for the user's consent (`--allow-major`). | Checked in `run_checks.py`. |
| Broken update | The new version fails the skill's tests. | Return to the previous commit and report. | Checked in `run_checks.py`. |
| Pinned project copy | A project keeps the skill as a submodule; the user installed a newer version. | Work by the installed version, report the difference, update the project copy only on request. | Behavioral case: WORKFLOW.md, updates.md and update-skill.md specify this. |
| Project name in the public skill | A private project name appears in a skill file. | `audit.py public --denylist <private file>` fails; the term is removed before publishing; the denylist stays in the private project. | Checked in `run_checks.py` with a synthetic term. |

## Report and publication review cases

These cases use synthetic situations. They are manual instruction walkthroughs, not claims of autonomous execution.

| Case | Input | Expected decision | Review result |
|---|---|---|---|
| Work without tests | A coordination period resolved a dependency; no testing took place. | Explain why coordination was needed, the confirmed decision and its consequence; do not invent tests or hours. | Pass: reports.md content rules apply to any work. |
| First report preview | The user requests a report and infographic, with no approved text draft. | Prepare and check both HTML previews; keep their status unapproved; wait before final export. | Pass: report-period.md separates preview and export. |
| Narrow correction | The user accepts the content except for the next-steps block. | Preserve the other sections; revise that block from the current plan and retain the earlier version. | Pass: reports.md protects accepted content. |
| Later plan | The report covers a closed period; the user asks to add today's plan. | Label the plan's period and target; do not count the new plan as work completed in the report period. | Pass: reports.md requires explicit plan period and status. |
| Activity count | A source lists many actions but the count does not explain an outcome. | Omit the count from the external report; retain evidence internally where useful. | Pass: reports.md filters measures by reader value. |
| Cleanup after export | The folder contains approved exports, a current plan pair, a prompt, drafts and older exports. | Keep the final exports, plan pair and prompt; archive the rest without deletion; fix moved links and verify retained files. | Pass: report-period.md and reports.md cover the retained set and move checks. |
| Unapproved plan | A report is approved, while the active plan is still a proposal. | Keep the active plan with its real status; report approval does not approve the plan. | Pass: reports.md states the exception explicitly. |
| Full-path link | The user needs to locate a delivered local file. | Show its resolved absolute path as the clickable label; do not copy that path into a public template. | Pass: workflow and reports.md separate local communication from public assets. |
| Private release note | A reusable change is sound, but its release note contains a real client detail. | Remove the private detail before staging; audit and read the staged diff again before an authorized push. | Pass: publishing.md uses two distinct review points; automated scanning remains incomplete. |

## Executable checks

`python tests/run_checks.py` checks the public-data scanner, local Markdown-link scanner, fresh workspace configuration, and this package. It deliberately uses synthetic people, paths, and domains.
