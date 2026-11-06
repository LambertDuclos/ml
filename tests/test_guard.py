"""The guard (`.claude/hooks/guard.py`) against the gestures it refuses and the ones it lets through."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / ".claude" / "hooks" / "guard.py"
LESSON = "courses/zero-to-hero/01-micrograd"
MINE = f"{LESSON}/micrograd.py"


def guard(tool, tool_input, in_session=False):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)}
    env.pop("ML_SESSION", None)
    if in_session:
        env["ML_SESSION"] = "1"
    entry = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": str(ROOT)})
    p = subprocess.run(
        [sys.executable, str(GUARD)],
        input=entry,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return p.returncode, p.stderr


def edit(path, in_session=False, tool="Write"):
    key = "notebook_path" if tool == "NotebookEdit" else "file_path"
    return guard(tool, {key: str(ROOT / path)}, in_session)


def bash(command, in_session=False):
    return guard("Bash", {"command": command}, in_session)


@pytest.mark.parametrize(
    "path",
    [
        MINE,
        f"{LESSON}/notes.md",
        f"{LESSON}/explore.py",
        "courses/maths/01-linear-algebra/linalg.py",
        "core/nn.py",
        "papers/2003-bengio-nplm/repro.py",
        "papers/2003-bengio-nplm/notes.md",
        "rebuilds/01-micrograd-2026-12/micrograd.py",
    ],
)
def test_refuses_lamberts_files(path):
    for tool in ("Write", "Edit", "MultiEdit"):
        code, err = edit(path, tool=tool)
        assert code == 2 and "belongs to Lambert" in err, (tool, path, err)


def test_refuses_a_notebook_of_lamberts():
    code, err = edit(f"{LESSON}/micrograd.ipynb", tool="NotebookEdit")
    assert code == 2 and "belongs to Lambert" in err


@pytest.mark.parametrize(
    "path",
    [
        f"{LESSON}/test_micrograd.py",
        f"{LESSON}/plot.py",
        f"{LESSON}/data.py",
        f"{LESSON}/README.md",
        f"{LESSON}/exercises.md",
        f"{LESSON}/ref/micrograd.py",
        "papers/2003-bengio-nplm/test_repro.py",
        "glossary.md",
        "questions.md",
        "README.md",
    ],
)
def test_lets_claudes_files_through(path):
    assert edit(path)[0] == 0


def test_lets_the_journal_outside_the_repo_through(tmp_path):
    assert guard("Write", {"file_path": str(tmp_path / "journal.md")})[0] == 0


@pytest.mark.parametrize(
    "command",
    [
        f"cat {MINE}",
        f"uv run pytest {LESSON} -q",
        f"uv run pytest {LESSON} -q 2>&1 | tail -20",
        f"uv run pytest {LESSON} -q > /tmp/out.txt",
        "git status",
        "date",
        f"ls -la {LESSON}/",
        "echo x > /dev/null",
        f"uv run ruff format {MINE}",
        "mkdir -p courses/zero-to-hero/02-makemore-bigram",
        f"echo 'see {MINE}' > questions.md",
        f"cat > questions.md <<'EOF'\n- 2026-11-07 · 01-micrograd · why does {MINE} need += ?\nEOF",
        f"cat > ~/notes/projets/ml/journal.md <<'EOF'\n- Resume here: {MINE}, test 3.\nEOF",
        f"cat > {LESSON}/test_micrograd.py <<'EOF'\nx\nEOF",
        f"cat > {LESSON}/ref/micrograd.py <<'EOF'\nx\nEOF",
        f"cp {LESSON}/test_micrograd.py rebuilds/01-micrograd-2026-12/",
        f"cp {LESSON}/test_micrograd.py rebuilds/01-micrograd-2026-12/test_micrograd.py",
        f"cp {MINE} /tmp/copy.py",
        f"git commit -m '01-micrograd: backward on {MINE} (3/5)'",
    ],
)
def test_bash_passes(command):
    code, err = bash(command)
    assert code == 0, (command, err)


@pytest.mark.parametrize(
    "command",
    [
        f"cat > {MINE} <<'EOF'\nx\nEOF",
        f"cat >{MINE} <<'EOF'\nx\nEOF",
        f"echo x >> {LESSON}/notes.md",
        f"echo x | tee {LESSON}/notes.md",
        f"echo x | tee -a {MINE}",
        f"cp {LESSON}/ref/micrograd.py {MINE}",
        f"cp {LESSON}/ref/micrograd.py {LESSON}/",
        f"sed -i '' 's/a/b/' {MINE}",
        f"rm {MINE}",
        f"rm -rf {LESSON}",
        f"git mv {MINE} core/micrograd.py",
        f"git rm {MINE}",
        f"uv run pytest -q && cat > {MINE} <<'EOF'\nx\nEOF",
    ],
)
def test_bash_refuses(command):
    code, err = bash(command)
    assert code == 2 and "belongs to Lambert" in err, (command, err)


@pytest.mark.parametrize(
    "path",
    [
        "CLAUDE.md",
        ".claude/agents/tutor.md",
        ".claude/hooks/guard.py",
        "bin/ml",
        "tests/test_guard.py",
        "pyproject.toml",
        "uv.lock",
    ],
)
def test_method_closed_during_a_session_only(path):
    assert edit(path)[0] == 0
    code, err = edit(path, in_session=True)
    assert code == 2 and "method" in err, err


def test_method_bash_during_a_session():
    assert bash("cat CLAUDE.md", in_session=True)[0] == 0
    assert bash("cat > CLAUDE.md <<'EOF'\nx\nEOF", in_session=True)[0] == 2
    assert bash("cat > CLAUDE.md <<'EOF'\nx\nEOF")[0] == 0


def test_unreadable_input_lets_through():
    p = subprocess.run(
        [sys.executable, str(GUARD)],
        input="not json",
        capture_output=True,
        text=True,
        check=False,
    )
    assert p.returncode == 0
