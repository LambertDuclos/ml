#!/usr/bin/env python3
"""The guard of the ml repo: what Claude does not write (`CLAUDE.md`, "Who writes what").

PreToolUse hook (`.claude/settings.json`) on Edit, Write, MultiEdit, NotebookEdit and Bash. Reads
Claude Code's JSON on stdin and refuses, exit 2 with the reason on stderr:
- an editing tool on one of Lambert's files: under `courses/`, `core/`, `papers/` and `rebuilds/`,
  every file that is not Claude's (`README.md`, `test_*.py`, `conftest.py`, `data.py`, `plot.py`,
  `exercises.md`, `__init__.py`, and everything under a `ref/` folder);
- a Bash line whose write gesture targets one of Lambert's files: the target of a `>` or `>>`, the
  files of `tee` and `sed -i`, the destination of `cp` and `mv` (or, when it is a folder, the file
  that would be born there), the targets of `rm`, `git rm` and `git mv`. A path merely mentioned
  (`uv run pytest courses/…`, the body of a heredoc, a commit message) is not a gesture;
- in a session (`ML_SESSION=1`, set by `bin/ml session`), the same gestures on the method:
  `CLAUDE.md`, `.claude/`, `bin/`, `tests/`, `pyproject.toml`, `uv.lock` (`CLAUDE.md`, "Changing the
  method").
Outside the repo (the journal in `~/notes`), everything passes.

Known holes, held by the tutor's prompt: a Python script that opens the file itself, a heredoc
given to `python`, a path built from a variable or a glob, a quoted target with a space in it, a
`cd` followed by a relative path (the line is judged from the session's `cwd`). Python 3.9 and the
standard library, like equipe's hooks.
Record of 6 November 2026: the first version judged every word of the line as soon as a `>` was in
it, and refused a `README.md` that mentioned a lesson folder; hence judging by gesture.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Iterator
from pathlib import Path

ZONES = ("courses", "core", "papers", "rebuilds")
CLAUDE_FILES = {"README.md", "conftest.py", "data.py", "plot.py", "exercises.md", "__init__.py"}
METHOD = ("CLAUDE.md", ".claude", "bin", "tests", "pyproject.toml", "uv.lock")
# A line is cut into simple commands at the shell separators and at newlines: the body of a heredoc
# becomes "commands" that start with no writing verb.
SEPARATORS = re.compile(r"\|\||&&|[;|\n()`]")
# The target of a redirect: `> f`, `>f`, `>> f`. `2>&1` and `>&2` have none.
REDIRECT = re.compile(r">>?\s*([^\s>&|;]+)")
WRITERS = ("tee", "sed", "cp", "mv", "rm")


def root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


def relative(path: str, cwd: Path) -> Path | None:
    """The path from the repo root, or None when it is outside."""
    p = Path(os.path.expanduser(path.strip("'\"")))
    if not p.is_absolute():
        p = cwd / p
    try:
        return p.resolve().relative_to(root())
    except ValueError:
        return None


def is_lamberts(rel: Path) -> bool:
    if not rel.parts or rel.parts[0] not in ZONES:
        return False
    if "ref" in rel.parts[1:-1]:
        return False
    name = rel.name
    return not (name in CLAUDE_FILES or (name.startswith("test_") and name.endswith(".py")))


def is_method(rel: Path) -> bool:
    return bool(rel.parts) and rel.parts[0] in METHOD


def refusal(rel: Path, in_session: bool) -> str | None:
    if is_lamberts(rel):
        return (
            f'`{rel}` belongs to Lambert: he writes it himself (CLAUDE.md, "Who writes what"). '
            'Explain, ask a question, or write a reference in `ref/` on the word "solution".'
        )
    if in_session and is_method(rel):
        return (
            f'`{rel}` is the method, closed during a session (CLAUDE.md, "Changing the method"): '
            "a rule changes in a plain `claude` session, without an agent."
        )
    return None


def targets(command: str) -> Iterator[str]:
    """The paths the line writes, moves or deletes, simple command by simple command."""
    for simple in SEPARATORS.split(command):
        for m in REDIRECT.finditer(simple):
            yield m.group(1)
        words = simple.split()
        if not words:
            continue
        verb, args = words[0], words[1:]
        if verb == "git" and args and args[0] in ("rm", "mv"):
            verb, args = args[0], args[1:]
        if verb not in WRITERS:
            continue
        if verb == "sed" and not any(a.startswith("-i") for a in args):
            continue
        args = [a for a in args if not a.startswith("-") and a not in ("''", '""')]
        if verb == "sed":
            args = args[1:]  # the expression first, then the files
        if verb in ("cp", "mv") and len(args) >= 2:
            dest, sources = args[-1], args[:-1]
            if dest.endswith("/") or not Path(dest).suffix:
                for s in sources:
                    yield str(Path(dest.strip("'\"")) / Path(s.strip("'\"")).name)
            else:
                yield dest
            continue
        yield from args


def bash_refusal(command: str, cwd: Path, in_session: bool) -> str | None:
    for target in targets(command):
        rel = relative(target, cwd)
        if rel is None:
            continue
        message = refusal(rel, in_session)
        if message:
            return message
    return None


def main() -> None:
    try:
        entry = json.load(sys.stdin)
        tool = entry["tool_name"]
        tool_input = entry.get("tool_input") or {}
        cwd = Path(entry.get("cwd") or os.getcwd())
    except Exception:  # noqa: BLE001 : unreadable input lets the tool through, like equipe
        sys.exit(0)
    in_session = os.environ.get("ML_SESSION") == "1"
    if tool == "Bash":
        command = tool_input.get("command")
        message = bash_refusal(command, cwd, in_session) if isinstance(command, str) else None
    else:
        file = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not isinstance(file, str):
            sys.exit(0)
        rel = relative(file, cwd)
        message = refusal(rel, in_session) if rel is not None else None
    if message:
        print(f"ml guard: {message}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
