# Example: First Run With Exploratory Project

User:

```text
Use $project-context-manager. I want to build an AI project, but I am not sure what it should be yet.
```

Expected agent workflow:

1. Select the current workspace as project root.
2. Run `scripts/validate_context.py --root <project-root>`.
3. See that no context files exist.
4. Classify as Exploratory Mode because goal and deliverable are unclear.
5. Ask one to three intake questions, such as:
   - What problem do you want this project to solve?
   - Who is the first user?
   - What output would make the first version feel useful?
6. After the user answers, run `scripts/init_context.py` with `--mode exploratory`.
7. Write the clarified direction to `PROJECT_STATE.md`.
8. Write the next exploration step to `NEXT_TASK.md`.
9. Run validation again.
