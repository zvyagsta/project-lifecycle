# Install and use in another environment

Install this reusable skill as a folder where the chosen skill-aware agent can read `SKILL.md` and its supporting files. The skill contains no project context, source documents, code, credentials, or participant data. Model-specific loading and permissions belong to the host program and must be checked there.

Open a chat in an empty project folder and ask the agent to start a project using this skill. The skill asks for the missing essentials and, on a direct setup request, creates a minimal local context. If the project has prior history, the user may provide it; otherwise the history section starts empty. No earlier workspace is required.

The optional `scripts/init_project.py` previews or creates starter files without overwriting existing files. The generated context is a blank template; fill it from the user's project answers before treating it as current context.

If the user wants a local configuration, create `.project-lifecycle/config.json` from the example asset with paths relative to the new project root. Run `python scripts/audit.py project <project-dir>` after creating the entrypoints. The check cannot establish that external services work or that the context is complete.

The reusable report design is optional and can be copied into the new project's report tooling. Keep project-specific text and participant details in the local project, outside the public skill. Publication or synchronization is a separate user-authorized action.
