# plan-period — plan for a day, week or other period

**When:** «план на сегодня», «план недели», a plan for a custom period.

**Input:** current context, the previous review, open decisions, the user's priorities; roles and time zone from local settings.

**Steps**
1. Write the plan in Markdown first; it is the working source. Keep it short: objective, priority outcomes with «done when» for each, dependencies, decisions needed and by whom, what moves to the next period, limits of the executor's actions. Rules: [reviews.md](../references/reviews.md).
2. Write plainly: no internal jargon; expand abbreviations at first use; when two identifiers name the same item, show both; time without measurement is «не измерено»; a plan is not a result.
3. Copy `assets/report-style/plan.html` to the period's archive folder as `<name>.draft.html`. Move the Markdown text into its blocks, delete unused blocks, repeat the ones you need. Use the roles from settings unless the project's own rules allow personal names.
4. Build with [build-page](build-page.md): `python scripts/build_page.py <draft> <name>.html --md <name>.md --layout <screenshots folder>`.
5. Move the previous Markdown and HTML pair to the archive; give the user the path and ask whether to open it.

**Result:** a Markdown and HTML pair in the period folder; the draft in its archive.

**Done when:** the build passes, the page and the Markdown say the same, and the active context links the new plan.

**Do not:** start the plan's tasks; present planned time as actual; open or publish the page without the user's answer.
