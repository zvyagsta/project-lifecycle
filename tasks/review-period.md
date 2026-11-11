# review-period — internal review of a day, week or other period

**When:** «итоги дня», «итоги недели», the end of a period, or before the next plan.

**Input:** the period's plan, files changed in the period, the active context, recorded decisions and deliveries.

**Steps**
1. State the period and the evidence cutoff in the configured time zone.
2. For each planned item: status (done, partly, not started, moved), link to the result and how it was checked, time or «не измерено», what remains and whom it depends on.
3. List decisions with date and basis, unresolved questions, external deliveries with evidence, and the next period's priorities.
4. For a reading page, build it like a plan page with [build-page](build-page.md).

**Result:** an internal review with links to evidence.

**Done when:** every completed item has evidence and nothing is counted twice across periods.

**Do not:** infer completion from the plan or delivery from a generated file. Rules: [reviews.md](../references/reviews.md).
