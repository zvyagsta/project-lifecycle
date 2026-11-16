# Optional report design

The assets in `assets/report-style/` preserve the reusable typography and layout of a report and a horizontal infographic. They contain no project examples. Copy the whole folder into a project's report tooling only when the user requests designed output.

- `design.css`: shared colors, sizes, and font roles. Bitter is used for headings and large numbers; Golos Text for body text and labels. The design uses a white sheet, dark blue text, indigo for confirmed progress, amber for waiting or uncertainty, and a rare red accent for a break or problem.
- `plan.html` and `plan.css`: a screen page for plans and internal reviews — a white sheet with ordered steps, state chips, decision cards and a dependency chain. Indigo marks done or ordered work; amber marks what waits for a decision or for the owner's action. `plan.css` has no colors of its own. Build one offline file with `scripts/build_page.py` ([build-page](../tasks/build-page.md)).
- `report.html`: A4 report template. `infographic.html`: horizontal companion template. Replace every `{{PLACEHOLDER}}` with HTML-escaped project text: source-backed text for previews, approved text for final exports. Fill repeatable sections/cards/steps with HTML using the existing classes. Leave `design.css` and `fonts/` beside the HTML so the templates work offline.
- `fonts/`: four WOFF2 files for Cyrillic and Latin subsets. See `FONT-LICENSES.md` for copyright and license details.
- `icons/`: optional line icons for findings, decisions, waiting, risks, research, and milestones. Read [icons.md](../assets/report-style/icons.md) before choosing one; omit an icon when none fits. The templates work without icons.

The report's purpose, audience, period and accepted export formats come from the local project. Show designed HTML before requesting approval; export the approved version afterward, unless the user explicitly specifies another workflow. Follow [reports.md](reports.md) for content and release rules. Do not assume every project needs a two-page daily report or a JPEG. If text does not fit, shorten it with the user's approval when meaning changes; do not silently shrink type. Keep internal source notes separate from a shareable report. A rendered file is not evidence it was sent.

When generating a report, keep the source-backed draft internal and present the report and infographic as HTML previews together. Review the final layout at its intended size. The template does not itself publish, send, or schedule anything.
