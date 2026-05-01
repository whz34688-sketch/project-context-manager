# Example: Resume Existing Project

User:

```text
Use $project-context-manager to continue this project.
```

Expected agent workflow:

1. Select the current workspace as project root.
2. Run `scripts/validate_context.py --root <project-root>`.
3. If files are valid, read only:
   - `PROJECT_STATE.md`
   - `NEXT_TASK.md`
4. Do not read the full `TASK_LOG.md` unless debugging, recovering, or resolving a conflict.
5. Confirm the current task from `NEXT_TASK.md`.
6. Execute the next action.
7. At the end, append meaningful progress to `TASK_LOG.md`, update `NEXT_TASK.md`, update `PROJECT_STATE.md` only if project truth changed, then validate again.
