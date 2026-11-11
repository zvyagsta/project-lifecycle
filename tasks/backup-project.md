# backup-project — private backup

**When:** the configured end-of-day checkpoint or a direct backup request, and only after the user configured a private repository.

**Input:** `private_backup` in local settings.

**Steps**
1. Update the context and run the link check.
2. Review the change list; exclude credentials and the configured exclusions.
3. Commit, push, and verify that the remote branch contains the new commit.

Full sequence: [private-backup.md](../references/private-backup.md).

**Result:** a verified remote commit, or an exact report of why the backup is only local.

**Done when:** the remote branch contains the new commit.

**Do not:** create a repository, change visibility or overwrite remote history without the user's request.
