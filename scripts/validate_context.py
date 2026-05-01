#!/usr/bin/env python3
"""Validate project context file presence and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_HEADINGS = {
    "PROJECT_STATE.md": [
        "# Project State",
        "## Project Description",
        "## Mode",
        "## Current Goals",
        "## Current Understanding",
        "## Technical Approach",
        "## System Structure",
        "## Key Constraints",
        "## Key Decisions",
        "## Current Progress",
        "## Known Limitations",
        "## Environment Notes",
        "## Open Questions",
    ],
    "NEXT_TASK.md": [
        "# Next Task",
        "## Current Task",
        "## Status",
        "## Completed Steps",
        "## Remaining Steps",
        "## Next Action",
        "## Scope Boundaries",
        "## Validation Criteria",
        "## Resume Instructions",
    ],
    "TASK_LOG.md": [
        "# Task Log",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate PROJECT_STATE.md, NEXT_TASK.md, and TASK_LOG.md."
    )
    parser.add_argument("--root", default=".", help="Project root containing context files.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat placeholder warnings as errors.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    files: dict[str, dict[str, object]] = {}

    if not root.exists():
        errors.append(f"Project root does not exist: {root}")
        result = {"ok": False, "root": str(root), "files": files, "warnings": warnings, "errors": errors}
        print(json.dumps(result, indent=2))
        return 1
    if not root.is_dir():
        errors.append(f"Project root is not a directory: {root}")
        result = {"ok": False, "root": str(root), "files": files, "warnings": warnings, "errors": errors}
        print(json.dumps(result, indent=2))
        return 1

    for filename, headings in REQUIRED_HEADINGS.items():
        path = root / filename
        info: dict[str, object] = {"exists": path.exists()}
        files[filename] = info
        if not path.exists():
            errors.append(f"Missing required file: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in headings if heading not in text]
        info["missing_headings"] = missing
        info["bytes"] = len(text.encode("utf-8"))
        if missing:
            errors.append(f"{filename} is missing headings: {', '.join(missing)}")
        if "TBD" in text:
            warnings.append(f"{filename} still contains TBD placeholders")
        if filename == "TASK_LOG.md" and text.count("\n## ") == 0:
            warnings.append("TASK_LOG.md has no dated entries yet")

    if args.strict and warnings:
        errors.extend(warnings)

    result = {
        "ok": not errors,
        "root": str(root),
        "files": files,
        "warnings": warnings,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
