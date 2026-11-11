# Optional report design

The assets in `assets/report-style/` preserve the reusable typography and layout of a report and a horizontal infographic. They contain no project examples. Copy the whole folder into a project's report tooling only when the user requests designed output.

- `design.css`: shared colors, sizes, and font roles. Bitter is used for headings and large numbers; Golos Text for body text and labels. The design uses a white sheet, dark blue text, indigo for confirmed progress, amber for waiting or uncertainty, and a rare red accent for a break or problem.
- `plan.html` and `plan.css`: a screen page for plans and internal reviews — a white sheet with ordered steps, state chips, decision cards and a dependency chain. Indigo marks done or ordered work; amber marks what waits for a decision or for the owner's action. `plan.css` has no colors of its own. Build one offline file with `scripts/build_page.py` ([build-page](../tasks/build-page.md)).
- `report.html`: A4 report template. `infographic.html`: horizontal companion template. Replace every `{{PLACEHOLDER}}` with approved, HTML-escaped project text. Fill repeatable sections/cards/steps with HTML using the existing classes. Leave `design.css` and `fonts/` beside the HTML so the templates work offline.
- `fonts/`: four WOFF2 files for Cyrillic and Latin subsets. See `FONT-LICENSES.md` for copyright and license details.
- `icons/`: optional line icons for findings, decisions, waiting, risks, research, and milestones. Read [icons.md](../assets/report-style/icons.md) before choosing one; omit an icon when none fits. The templates work without icons.

The report's purpose, audience, period, and approval gate come from the local project. Do not assume every project needs a two-page daily report or a JPEG. If text does not fit, shorten it with the user's approval when meaning changes; do not silently shrink type. Keep internal source notes separate from a shareable report. A rendered file is not evidence it was sent.

When generating a report, first make a source-backed draft, then use the project's approval rule. Review the final layout at its intended size. The template does not itself publish, send, or schedule anything.
