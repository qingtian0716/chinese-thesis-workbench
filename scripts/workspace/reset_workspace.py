#!/usr/bin/env python3
"""Reset generated thesis workspace layers while preserving original materials."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MODES = {"reset-output", "reset-evidence", "full-reset"}


@dataclass
class ResetResult:
    root: Path
    mode: str
    archive_dir: Path
    planned_paths: list[Path]
    archived_paths: list[Path]
    dry_run: bool


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def _existing(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.exists()]


def _without_descendants(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in sorted(paths, key=lambda item: len(item.parts)):
        if any(path != parent and path.is_relative_to(parent) for parent in result):
            continue
        result.append(path)
    return result


def _reset_file(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def planned_reset_paths(root: Path, mode: str) -> list[Path]:
    if mode not in MODES:
        raise ValueError(f"Unknown reset mode: {mode}")

    paper_context = root / "paper-context"
    context_paths = (
        [path for path in paper_context.iterdir() if path.name != "archive"]
        if paper_context.exists()
        else []
    )
    output_paths = [
        root / "paper-output",
        root / "thesis-ai-standard" / "templates" / "thesis-ai-spec.yaml",
        root / "thesis-ai-standard" / "templates" / "figure-registry.yaml",
        root / "paper-context" / "workflow" / "chapter-progress.md",
        root / "paper-context" / "workflow" / "workflow-status.md",
    ]
    evidence_paths = [
        root / "paper-context" / "evidence",
        root / "paper-context" / "literature",
        root / "paper-context" / "workflow",
    ]
    full_paths = [root / "thesis-ai-standard"]

    if mode == "reset-output":
        return _without_descendants(_existing(output_paths))
    if mode == "reset-evidence":
        return _without_descendants(_existing(output_paths + evidence_paths))
    return _without_descendants(_existing(output_paths + context_paths + full_paths))


def _archive_and_remove(path: Path, archive_dir: Path, root: Path) -> Path:
    relative = path.relative_to(root)
    target = archive_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"Archive target already exists: {target}")
    shutil.move(str(path), str(target))
    return target


def _recreate_mode_state(root: Path, mode: str) -> None:
    if mode == "reset-output":
        (root / "paper-output").mkdir(parents=True, exist_ok=True)
        _reset_file(root / "thesis-ai-standard" / "templates" / "thesis-ai-spec.yaml")
        _reset_file(root / "thesis-ai-standard" / "templates" / "figure-registry.yaml")
        _reset_file(root / "paper-context" / "workflow" / "chapter-progress.md")
        _reset_file(
            root / "paper-context" / "workflow" / "workflow-status.md",
            "phase: spec_confirmed\nstatus: pending\n",
        )
    elif mode == "reset-evidence":
        (root / "paper-output").mkdir(parents=True, exist_ok=True)
        (root / "paper-context" / "evidence").mkdir(parents=True, exist_ok=True)
        (root / "paper-context" / "literature").mkdir(parents=True, exist_ok=True)
        (root / "paper-context" / "workflow").mkdir(parents=True, exist_ok=True)
    elif mode == "full-reset":
        (root / "paper-output").mkdir(parents=True, exist_ok=True)
        (root / "paper-context").mkdir(parents=True, exist_ok=True)


def reset_workspace(root: Path | str, mode: str, confirm: bool = False) -> ResetResult:
    root = Path(root).resolve()
    if mode not in MODES:
        raise ValueError(f"Unknown reset mode: {mode}")

    planned = planned_reset_paths(root, mode)
    archive_dir = root / "paper-context" / "archive" / _timestamp()
    if not confirm:
        return ResetResult(root, mode, archive_dir, planned, [], dry_run=True)

    archived: list[Path] = []
    archive_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(planned, key=lambda item: len(item.parts), reverse=True):
        if not path.exists():
            continue
        if path.parts[-1] in {"papers", "assets"}:
            raise PermissionError(f"Refusing to reset original material directory: {path}")
        archived.append(_archive_and_remove(path, archive_dir, root))

    _recreate_mode_state(root, mode)
    return ResetResult(root, mode, archive_dir, planned, archived, dry_run=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reset generated thesis workspace layers without deleting papers/ or assets/."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Thesis workspace root.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--reset-output", action="store_true", help="Clear generated outputs only.")
    group.add_argument("--reset-evidence", action="store_true", help="Clear evidence and generated outputs.")
    group.add_argument("--full-reset", action="store_true", help="Clear all generated workspace state.")
    args = parser.parse_args()

    mode = (
        "reset-output"
        if args.reset_output
        else "reset-evidence"
        if args.reset_evidence
        else "full-reset"
    )
    root = Path(args.workspace).resolve()
    dry_run = reset_workspace(root, mode, confirm=False)

    print(f"Workspace: {root}")
    print(f"Mode: {mode}")
    print("The following generated paths will be archived and reset:")
    if dry_run.planned_paths:
        for path in dry_run.planned_paths:
            print(f"- {path}")
    else:
        print("- No existing generated paths found.")
    print(f"Archive target: {dry_run.archive_dir}")
    print("Original material directories papers/ and assets/ are never deleted.")

    if input("Type yes to continue: ").strip() != "yes":
        print("Cancelled. No files changed.")
        return 1

    result = reset_workspace(root, mode, confirm=True)
    print(f"Reset complete. Archived {len(result.archived_paths)} path(s) to {result.archive_dir}")
    print("Next step: resume the workflow from the phase appropriate to the selected reset mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
