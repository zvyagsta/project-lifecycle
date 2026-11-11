# Plans and reviews

Configure each cadence as a period and a trigger: for example daily on request, weekly on Friday, monthly at month end, or a custom two-week span. Store the time zone and the first day of the week. A schedule preference guides what to prepare when invoked; it does not itself create a background automation.

## Plan

State the period, objective, up to a few priority outcomes, dependencies, known commitments, and what needs a decision. Mark a meeting as planned until evidence confirms it happened. Separate work the agent may do from actions requiring approval or access.

Write the plan in Markdown first; it stays the working source. When the plan is read on screen, build the reading page from `assets/report-style/plan.html` with `scripts/build_page.py`, following [plan-period](../tasks/plan-period.md). The page shows the main point, what already exists, ordered steps with their state, decision cards, a dependency chain, who decides what, what moves to the next period, time, and the executor's limits. Planned time is not actual time; without measurement write «не измерено».

## Review

State the period and evidence cutoff. Separate completed outcomes, work still in progress, decisions, unresolved questions, external deliveries, and next period's priorities. Link internal evidence. Use the project's approved external format when making a version for others. Do not infer completion from an earlier plan or delivery from an output file.

## Period boundaries

Use the configured time zone and explicit inclusive start/end dates. If periods overlap or evidence arrived later than the event, record the event date and the date it became known. Do not count the same outcome twice in a cumulative review; a later review may summarize earlier work with a link.
