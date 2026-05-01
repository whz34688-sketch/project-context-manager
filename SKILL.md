---
name: project-context-manager
description: Use when an AI agent is managing a long-running, iterative, or multi-session project and must persist project state in PROJECT_STATE.md, NEXT_TASK.md, and TASK_LOG.md instead of relying on conversation history. Use for coding, writing, research, product, or exploratory projects that need reliable resume context across sessions; do not use for simple one-off tasks.
---

# Project Context Manager

This skill makes the project folder the source of truth. Conversation history is temporary; project state files are durable.

Resolve bundled resources relative to this `SKILL.md` file:

- `scripts/init_context.py`
- `scripts/validate_context.py`
- `templates/PROJECT_STATE.template.md`
- `templates/NEXT_TASK.template.md`
- `templates/TASK_LOG.template.md`

## Core Rule

For managed projects, always work from these files in the project root:

- `PROJECT_STATE.md`: current project truth.
- `NEXT_TASK.md`: active execution pointer.
- `TASK_LOG.md`: historical progress log.

Use code for deterministic work:

- Create missing state files with `scripts/init_context.py`.
- Check state file structure with `scripts/validate_context.py`.
- Do not hand-create the three files unless the script is unavailable.

Use agent judgment only for semantic work:

- Understanding the user's current goal.
- Choosing Defined vs Exploratory mode.
- Updating project-specific decisions, progress, and next actions.

## Execution Workflow

Follow this workflow whenever the skill is invoked.

Think of the workflow as a state machine:

1. Validate context files.
2. Choose one branch: First Run, Resume, Partial Repair, or Structure Repair.
3. Prepare `NEXT_TASK.md`.
4. Execute project work.
5. Update state files.
6. Validate again.

### 1. Select Project Root

Use the current workspace root unless the user explicitly names another project folder.

If the project root is ambiguous, ask one concise question for the path before changing files.

### 2. Run Context Validation

Run:

```bash
python scripts/validate_context.py --root <project-root>
```

Interpret the result:

- No core files exist: start the First Run workflow.
- Some core files are missing: run initialization to create only the missing files, then reconcile.
- All core files exist: start the Resume workflow.
- Files exist but validation reports structural errors: repair structure before continuing when safe; ask only if the correct repair is unclear.

### 3. First Run Workflow

Use this only when no core files exist.

Do not run initialization until the project is clear enough to write a useful first state.

First extract these fields from the user's message:

- Project goal: what the user wants to accomplish.
- Desired output: the artifact, product, report, codebase, document, or decision the project should produce.
- User plan: any steps, roadmap, or constraints the user already provided.
- Immediate next action: the first concrete step the agent can take.
- Validation criteria: how the user or agent will know the next step worked.

Treat the project as Defined Mode only when all three are identifiable:

- Project goal.
- Desired output or deliverable.
- Immediate next action.

Treat the project as Exploratory Mode when two or more are missing, or when the user is brainstorming instead of asking for execution.

If the user already has a plan, do not replace it with a new plan. Ask only for missing details that materially affect execution, then convert the user's plan into `NEXT_TASK.md`.

If the user does not have a clear plan, design the next step through conversation. Ask one to three intake questions about:

- Goal.
- Desired output.
- Current idea or constraints.
- First priority.

Good intake questions are concrete:

- "What should exist at the end of the first version?"
- "Who is this for?"
- "Do you want me to plan first, implement first, or explore options first?"
- "Are there any files, technologies, or directions I must avoid?"

After the user answers, summarize the chosen direction in one short paragraph. If the user agrees or the direction is safe to infer, proceed.

After the mode and first task are clear enough, run:

```bash
python scripts/init_context.py --root <project-root> --mode <defined|exploratory> --project-name "<name>" --project-description "<summary>" --current-task "<first task>"
```

Then edit the created files narrowly:

- Fill `PROJECT_STATE.md` with confirmed project truth: goal, mode, current understanding, constraints, decisions, and open questions.
- Fill `NEXT_TASK.md` with the first executable or exploratory step: current task, status, remaining steps, next action, scope boundaries, and validation criteria.
- Leave `TASK_LOG.md` as an append-only history; the initialization script already creates the first entry.

Run validation again before executing project work.

### 4. Resume Workflow

Use this when core files already exist.

Read:

- `PROJECT_STATE.md`
- `NEXT_TASK.md`

Do not read `TASK_LOG.md` by default.

Read recent `TASK_LOG.md` entries only when needed for:

- Debugging.
- Recovering interrupted work.
- Reviewing prior decisions.
- Understanding a conflict between current files and the user request.

If the user says only "continue this project", continue from `NEXT_TASK.md`.

If the user gives a new instruction, compare it with `PROJECT_STATE.md` and `NEXT_TASK.md`:

- If it is consistent, update `NEXT_TASK.md` and execute.
- If it changes the project goal, approach, or constraints, update `PROJECT_STATE.md` first.
- If it conflicts with old files, follow the user's latest explicit instruction and repair the files.
- If it is ambiguous, ask one concise question before editing project files.

### 5. Before Execution

Before substantial project changes, make sure `NEXT_TASK.md` states:

- Current task.
- Scope boundaries.
- Next action.
- Validation criteria.

If any of these are missing:

- Fill them from the user's request when safe.
- If unsafe to infer, ask one concise question.
- Do not start broad implementation while `NEXT_TASK.md` lacks a next action or validation criteria.

If the user asks a tiny one-step question, this update can wait until the end.

### 6. Execute The Task

Do the requested project work using the repository's normal tools and conventions.

Keep the state files as operational context, not as a substitute for reading the actual code or source files.

### 7. End Of Task

When meaningful progress occurred, update in this order:

1. Append a concise entry to `TASK_LOG.md`.
2. Update `NEXT_TASK.md` with current status and next action.
3. Update `PROJECT_STATE.md` only if project-level truth changed.
4. Run:

```bash
python scripts/validate_context.py --root <project-root>
```

In the final response, mention:

- What project work was completed.
- Which state files were updated.
- Any validation result or remaining blocker.

## Conflict Rules

- Latest explicit user instruction overrides stale project files.
- Project files override older conversation history.
- If project files are stale but the correct state is inferable, update them before continuing.
- Preserve user-written content. Make narrow edits and avoid full rewrites unless restructuring is required.
- Never overwrite existing state files with templates unless the user explicitly asks or `--force` is intentionally used.

## Update Rules

`PROJECT_STATE.md` changes only when project truth changes:

- Goal changes.
- Architecture or approach changes.
- Key decisions.
- Major progress milestones.
- New constraints, risks, or open questions.
- Refined understanding in Exploratory Mode.

`NEXT_TASK.md` changes when execution state changes:

- Task starts, progresses, completes, or is interrupted.
- Scope, priority, or direction changes.
- Work is split into subtasks.
- Validation criteria change.

`TASK_LOG.md` changes when meaningful progress occurs:

- Feature completion.
- Bug fix.
- Structural change.
- Validation result.
- Decision point.
- Important finding.
- Blocker that affects future work.

Do not log passive discussion, trivial file reads, or repeated failed commands unless they reveal a meaningful finding.
