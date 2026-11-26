# Editing and publishing the reusable skill

Use this procedure when the user asks to change this skill itself. Installing an already published version is a different operation: see [updates.md](updates.md). A request to edit locally does not by itself authorize a push.

1. Identify the installed copy, its source repository and any pinned project copy. Check repository status and upstream state. Preserve unrelated local changes; update the copy actually used by the agent before publishing. Do not update project submodule pointers or commit a private project as an incidental part of a skill release.
2. Extract reusable rules from the user's request. Write them in neutral terms. No personal data or project materials may be transmitted to an external destination or enter the reusable package, including filenames, examples, generated files, commit messages and release metadata. The creator's public GitHub account may be named for attribution; do not add any other personal identifier. Keep project names, people, companies, paths, domains, object identifiers, operational numbers, schedules, source materials and private examples out of the reusable package. Retain only public package metadata and clearly synthetic examples. Keep private review notes and denylists outside this repository.
3. Edit the narrowest relevant instructions and reconcile all entry points that describe the same behavior. Update README and CHANGELOG with the new behavior and migration impact. Keep the version in SKILL.md and plugin.json equal to the newest changelog version. Use the package's version policy: changed default behavior requires a MAJOR release, which the updater must not install silently.
4. Before staging, run the package checks, style checks and public-data audit locally with a private denylist. Do not upload the package or private inputs to an external scanning service. Check links and walk through realistic synthetic cases, including the approval boundary and archive behavior. Also review filenames, generated files and binary additions; a text scan cannot establish that the entire package is safe.
5. Stage only the intended package files. Review the exact staged diff again for private content, consistency and unrelated changes. Confirm that private inputs, screenshots, audit notes and denylists are absent from the staged file list. Check the intended Git author, committer and tagger identities before creating release objects; do not rely on a workstation default. Use the repository's established public identity, or ask if none is established. A failing audit or unresolved finding blocks publication; a scanner passing is not a substitute for reading the diff.
6. Show the exact reviewed changes and check results to the user, then wait for their explicit approval to publish this version. Preparing an update is not publication approval. Commit and push only after that approval. Before pushing, inspect the actual commit and annotated-tag metadata as well as their contents; a clean tree audit does not cover author, committer or tagger fields. Do not force-push without explicit authorization, including when correcting an already published release. Verify that the remote branch contains the intended commit, and distinguish a verified remote update from a local-only commit. If changes are needed after the review, repeat the relevant checks on the new staged content before sending it.

Typical local checks, from the skill repository:

```text
python tests/run_checks.py
python tests/check_style.py
python scripts/audit.py public . --denylist <private-denylist-outside-repository>
git diff --check
git diff --cached --stat
git diff --cached
```

The publication authorization applies to this reusable package, not to the user's project materials. Report the installed version, the published commit or branch status, the checks actually run, and any separate project copy that remains pinned.
