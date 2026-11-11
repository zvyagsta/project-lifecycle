# build-page — build a reading page

**When:** inside [plan-period](plan-period.md) and [review-period](review-period.md), or whenever a Markdown material needs a designed HTML page for reading.

**Input:** a draft HTML that keeps `@import url("design.css");` (and `plan.css` for plans) in its style; the Markdown source.

**Steps**
1. `python scripts/build_page.py <draft.html> <out.html> --md <source.md> --layout <screenshots folder>`.
2. The script embeds the styles and fonts into one offline file and checks placeholders, local links, words that differ from the Markdown, and horizontal scroll at 1280 and 400 px. The layout check needs Playwright and Chrome or Edge; without them it is skipped with a message.
3. Look at the screenshots once, fix what is visible, rebuild once.

**Result:** one self-contained HTML file.

**Done when:** the script exits with code 0 and the word differences are only labels.

**Do not:** add colors or fonts outside `design.css`; load fonts or scripts from the internet; publish the page. Style rules: [report-style.md](../references/report-style.md).
