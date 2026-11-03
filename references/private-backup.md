# Optional private GitHub backup

Use this only after the user chooses a repository and authorizes a backup cadence. Store the owner, repository, triggers, exclusions, and any organization policy in local project settings. Keep credentials in the host credential manager; do not write them into project files or this skill.

## Configure once for the project

1. Confirm the account and exact repository name. Create the repository as private only when directly requested. Verify its visibility before the first upload.
2. Record whether backup runs at the end of a working day, on request, or both. An end-of-day trigger runs only when an agent is working at that checkpoint; it does not create a scheduled task.
3. Confirm any excluded files or folders. Keep prior versions and project archives by default. Exclude credentials, keys, tokens, and user-excluded material. Large files may require Git LFS or another approved store; do not silently omit them.

## At each backup checkpoint

1. Finish the authorized work, update the active context, and run the project's link check. Record unresolved failures rather than claiming a clean handoff.
2. Review the change list and staged files. Check for secrets and unexpected content. If repository visibility or access cannot be verified, do not upload.
3. Commit the project state, push to the configured private repository, and verify the remote branch contains the new commit. Report the commit or the precise failure. A local commit alone is not a remote backup.

When two computers change the project, fetch and reconcile remote changes before pushing. Do not overwrite remote history to make a backup succeed. Keep a separate local copy until the remote state has been verified.
