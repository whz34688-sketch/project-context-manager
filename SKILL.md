---
name: project-context-manager
description: Use when managing a long-running, iterative, or multi-session project where project state should be persisted in PROJECT_STATE.md, TASK_LOG.md, and NEXT_TASK.md instead of relying on conversation history. Use for ongoing coding, writing, research, product, or exploratory work that needs reliable resume context across sessions; do not use for simple one-off tasks.
---

# Project Context Manager

This skill keeps project memory in files, not in the conversation.

Core principle: do not rely on conversation history as the source of truth for project state. Preserve the current project state in structured files at the project root.

## Core Files

Maintain these files in the project root:

- `PROJECT_STATE.md`: current truth of the project.
- `NEXT_TASK.md`: active execution pointer.
- `TASK_LOG.md`: historical progress log.

## Conflict Rules

- If project files conflict with older conversation history, trust the files.
- If project files conflict with the user's latest explicit instruction, follow the latest user instruction and update the files.
- If the files appear stale, incomplete, or internally inconsistent, repair them before continuing when the correct state can be inferred.
- Ask the user only when the next action or project goal cannot be inferred safely.
- Preserve user-written content. Make narrow edits to state files and avoid rewriting entire files unless restructuring is necessary.

## Startup Workflow

At the start of an invoked task:

1. Check whether `PROJECT_STATE.md`, `NEXT_TASK.md`, and `TASK_LOG.md` exist in the project root.
2. If none exist, treat this as a new managed project:
   - Run the Project Intake workflow below.
   - Create all three files using the templates below.
   - Fill `PROJECT_STATE.md` with the confirmed or inferred project direction.
   - Fill `NEXT_TASK.md` with the first concrete action or exploration step.
   - Create `TASK_LOG.md` as the historical log.
3. If some but not all files exist, create the missing files and reconcile them with the existing files.
4. Read `PROJECT_STATE.md` and `NEXT_TASK.md`.
5. Do not read `TASK_LOG.md` by default. Read only recent entries when needed for debugging, recovery, review, or understanding prior decisions.
6. Determine whether the project is in Defined Mode or Exploratory Mode.
7. Execute the user's task.

## Project Intake

Use this workflow when starting a managed project with no existing core files.

First assess whether the user's project request is clear enough to start.

Treat the project as clear enough to start when:

- The goal is specific enough to act on.
- The desired output is identifiable.
- The immediate next action can be chosen without guessing.
- Missing details can be resolved while working.

For a clear project:

- Ask only for missing requirements that would materially affect execution.
- Create `PROJECT_STATE.md` from the confirmed or inferred requirements.
- Create `NEXT_TASK.md` with the first actionable task.
- Create `TASK_LOG.md` as the historical log.
- Begin guiding or executing the project.

Treat the project as unclear when:

- The goal is vague or still forming.
- The desired output is unknown or has several plausible forms.
- The user is brainstorming rather than requesting execution.
- The next action would require guessing the user's intent.

For an unclear project:

- Ask one to three concise intake questions about the user's goal, current idea, desired output, constraints, and first priority.
- Summarize the clarified direction.
- Create `PROJECT_STATE.md` from that summary.
- Create `NEXT_TASK.md` with the next exploration step.
- Create `TASK_LOG.md` as the historical log.
- Continue guiding the project from the clarified state.

If the mode is unclear after reading the user's request, ask one to three concise intake questions before creating or updating `PROJECT_STATE.md`.

## Project Modes

### Defined Mode

Use when the project has clear goals, stable requirements, and execution-focused incremental work.

Update frequency:

- `PROJECT_STATE.md`: low frequency; update only for project-level changes.
- `NEXT_TASK.md`: update when task state, priority, or direction changes.
- `TASK_LOG.md`: append when meaningful progress occurs.

### Exploratory Mode

Use when goals are evolving, assumptions are still being tested, or the project requires iterative clarification.

Update frequency:

- `PROJECT_STATE.md`: medium to high frequency; capture evolving understanding.
- `NEXT_TASK.md`: update when exploration direction or immediate next steps change.
- `TASK_LOG.md`: append for meaningful findings, decisions, and validation.

## File Responsibilities

### PROJECT_STATE.md

Purpose: current state, not history.

Read at the start of each managed task. Update only when the project-level truth changes, such as:

- Goal changes.
- Architecture or approach changes.
- Key decision changes.
- Major progress milestones.
- Refined understanding in Exploratory Mode.
- New constraints, risks, or open questions.

Do not update for minor implementation details.

### NEXT_TASK.md

Purpose: current task and resume pointer.

Read at the start of each managed task. Update when:

- The active task progresses significantly.
- The active task completes.
- Work is interrupted.
- Scope, priority, or direction changes.
- Work is split into subtasks.
- Validation criteria change.

### TASK_LOG.md

Purpose: historical record of meaningful progress.

Do not read by default. When needed, prefer recent entries only.

Append an entry when there is meaningful progress, such as:

- Bug fixes.
- Feature completion.
- Structural changes.
- Validation steps.
- Decision points.
- Important findings.
- Blockers or failed approaches that affect future work.

Do not log trivial file reads, passive discussion, idle exploration, or repeated failed commands unless they reveal a meaningful finding.

## End Workflow

At the end of a managed task:

1. Append to `TASK_LOG.md` if meaningful progress occurred.
2. Update `NEXT_TASK.md` if the task state changed.
3. Update `PROJECT_STATE.md` if project-level state changed.
4. Keep updates concise and scannable.
5. In the final user response, mention any state files updated.

## Templates

Use these templates when initializing missing files. Keep headings stable unless there is a strong reason to adapt them.

### PROJECT_STATE.md

```markdown
# Project State

## Project Description

TBD

## Current Goals

- TBD

## Current Understanding

- TBD

## Technical Approach

- TBD

## System Structure

- TBD

## Key Constraints

- TBD

## Key Decisions

- TBD

## Current Progress

- TBD

## Known Limitations

- TBD

## Environment Notes

- TBD

## Open Questions

- TBD

## Exploratory Notes

- Initial assumptions: TBD
- Corrected misunderstandings: TBD
- Discarded approaches: TBD
- Current exploration direction: TBD
```

### NEXT_TASK.md

```markdown
# Next Task

## Current Task

TBD

## Status

Not started

## Completed Steps

- TBD

## Remaining Steps

- TBD

## Next Action

TBD

## Scope Constraints

- TBD

## Validation Criteria

- TBD

## Resume Instructions

TBD
```

### TASK_LOG.md

```markdown
# Task Log

Historical record of meaningful progress. Newest entries may be appended at the top or bottom, but keep one consistent order.

## YYYY-MM-DD - Initial Project Setup

- Task performed: Initialized project context files.
- Files or components affected: `PROJECT_STATE.md`, `NEXT_TASK.md`, `TASK_LOG.md`.
- Changes made: Created baseline context management files.
- Validation or outcome: Project can be resumed from file-based state.
- Outstanding issues: TBD.
- New findings: TBD.
```

## Practical Update Rules

- Prefer concise bullets over long narrative.
- Keep `PROJECT_STATE.md` deduplicated and current.
- Keep `NEXT_TASK.md` specific enough that another session can resume immediately.
- Keep `TASK_LOG.md` append-only unless correcting a factual error.
- If a task spans many steps, update `NEXT_TASK.md` during the task, not only at the end.
- If the repository already has its own planning or state files, ask before replacing them; otherwise, map this skill's files to the existing convention when the mapping is obvious.
