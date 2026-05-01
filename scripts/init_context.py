#!/usr/bin/env python3
"""Initialize project context files from bundled templates."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
import sys


ROOT_FILES = {
    "PROJECT_STATE.template.md": "PROJECT_STATE.md",
    "NEXT_TASK.template.md": "NEXT_TASK.md",
    "TASK_LOG.template.md": "TASK_LOG.md",
}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create PROJECT_STATE.md, NEXT_TASK.md, and TASK_LOG.md from templates."
    )
    parser.add_argument("--root", default=".", help="Project root where context files should live.")
    parser.add_argument(
        "--mode",
        choices=["defined", "exploratory", "unknown"],
        default="unknown",
        help="Project mode to write into PROJECT_STATE.md.",
    )
    parser.add_argument("--project-name", default=None, help="Human-readable project name.")
    parser.add_argument("--project-description", default="TBD", help="Short project summary.")
    parser.add_argument("--current-task", default="TBD", help="Initial current task.")
    parser.add_argument("--create-root", action="store_true", help="Create the root directory if missing.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing context files.")
    parser.add_argument("--dry-run", action="store_true", help="Report actions without writing files.")
    return parser.parse_args()


def render_template(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        if args.create_root:
            if not args.dry_run:
                root.mkdir(parents=True, exist_ok=True)
        else:
            print(json.dumps({"ok": False, "errors": [f"Project root does not exist: {root}"]}, indent=2))
            return 2
    if root.exists() and not root.is_dir():
        print(json.dumps({"ok": False, "errors": [f"Project root is not a directory: {root}"]}, indent=2))
        return 2

    templates_dir = skill_root() / "templates"
    if not templates_dir.is_dir():
        print(json.dumps({"ok": False, "errors": [f"Missing templates directory: {templates_dir}"]}, indent=2))
        return 2

    today = _dt.date.today().isoformat()
    project_name = args.project_name or root.name
    values = {
        "DATE": today,
        "MODE": args.mode,
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": args.project_description,
        "PROJECT_ROOT": str(root),
        "CURRENT_TASK": args.current_task,
    }

    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []
    errors: list[str] = []

    for template_name, target_name in ROOT_FILES.items():
        template_path = templates_dir / template_name
        target_path = root / target_name
        if not template_path.is_file():
            errors.append(f"Missing template: {template_path}")
            continue
        if target_path.exists() and not args.force:
            skipped.append(target_name)
            continue
        content = render_template(template_path.read_text(encoding="utf-8"), values)
        if not args.dry_run:
            target_path.write_text(content, encoding="utf-8", newline="\n")
        if target_path.exists() and args.force:
            overwritten.append(target_name)
        else:
            created.append(target_name)

    ok = not errors
    print(
        json.dumps(
            {
                "ok": ok,
                "root": str(root),
                "mode": args.mode,
                "created": created,
                "skipped": skipped,
                "overwritten": overwritten,
                "errors": errors,
                "dry_run": args.dry_run,
            },
            indent=2,
        )
    )
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
