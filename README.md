# Project Context Manager

Project Context Manager is an AI-agent workflow for long-running projects.
It keeps project memory in files instead of relying on a long conversation.

The skill is packaged for Codex, but the workflow is useful for any agent that can read and write project files.

Repository:

https://github.com/whz34688-sketch/project-context-manager

## What Problem It Solves

Long AI-agent projects often break down when the conversation gets long or when work moves to a new thread.

Common symptoms:

- The agent forgets prior requirements.
- The user rewrites the same handoff prompt again and again.
- The next thread does not know what was already tried.
- Project decisions are trapped in chat history.
- The user is not sure whether the handoff prompt is complete.

This skill moves project memory into three files in the project root:

- `PROJECT_STATE.md`: current project truth.
- `NEXT_TASK.md`: current task and resume pointer.
- `TASK_LOG.md`: historical progress log.

## How It Works

The agent follows a fixed workflow:

1. Validate whether the three context files exist.
2. If none exist, determine whether the project is Defined or Exploratory.
3. Initialize missing files with `scripts/init_context.py`.
4. Read `PROJECT_STATE.md` and `NEXT_TASK.md` before doing work.
5. Avoid reading full history unless needed.
6. Execute the task.
7. Update context files after meaningful progress.
8. Validate structure with `scripts/validate_context.py`.

## File Structure

```text
project-context-manager/
  README.md
  SKILL.md
  LICENSE
  agents/
    openai.yaml
  templates/
    PROJECT_STATE.template.md
    NEXT_TASK.template.md
    TASK_LOG.template.md
  scripts/
    init_context.py
    validate_context.py
  examples/
    first-run-defined.md
    first-run-exploratory.md
    resume-existing-project.md
```

## First Run Prompt

Use this inside a project folder:

```text
Use $project-context-manager to manage this project context. I want to build a small browser extension that saves useful AI tools from web pages. Start with an MVP.
```

If the project is unclear, use:

```text
Use $project-context-manager to help me clarify this project first. I want to build an AI project, but I do not know the exact form yet.
```

## Resume Prompt

In a later thread, inside the same project folder:

```text
Use $project-context-manager to continue this project.
```

The agent should read `PROJECT_STATE.md` and `NEXT_TASK.md`, then continue from the recorded next action.

## Scripts

Initialize context files:

```bash
python scripts/init_context.py --root /path/to/project --mode defined --project-name "my-project" --project-description "Build an MVP" --current-task "Create the initial plan"
```

Validate context files:

```bash
python scripts/validate_context.py --root /path/to/project
```

Use `--strict` when you want remaining `TBD` placeholders to fail validation:

```bash
python scripts/validate_context.py --root /path/to/project --strict
```

## Design Principle

Use code for repeatable mechanical work. Use the agent only for semantic project understanding.

Good code-owned tasks:

- Create the three files.
- Preserve stable file headings.
- Check whether required sections exist.

Good agent-owned tasks:

- Understand what the user wants.
- Decide whether the project is Defined or Exploratory.
- Summarize project truth.
- Update decisions and next actions.

## License

MIT
