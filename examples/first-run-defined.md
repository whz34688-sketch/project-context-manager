# Example: First Run With Defined Project

User:

```text
Use $project-context-manager to manage this project context. I want to build a Chrome extension that collects useful AI tools from web pages. The first version should save title, URL, tags, and notes locally.
```

Expected agent workflow:

1. Select the current workspace as project root.
2. Run `scripts/validate_context.py --root <project-root>`.
3. See that no context files exist.
4. Classify as Defined Mode because goal, deliverable, and first direction are identifiable.
5. Run `scripts/init_context.py --root <project-root> --mode defined --project-name "Chrome AI tool collector" --project-description "Build an MVP Chrome extension that saves AI tool pages locally" --current-task "Create the MVP project plan and first implementation step"`.
6. Edit `PROJECT_STATE.md` and `NEXT_TASK.md` with the confirmed project details.
7. Run validation again.
8. Start implementation or planning.
