"""La garde (`.claude/hooks/garde.py`) face aux gestes qu'elle refuse et à ceux qu'elle laisse."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
GARDE = RACINE / ".claude" / "hooks" / "garde.py"
LECON = "courses/zero-to-hero/01-micrograd"
MIEN = f"{LECON}/micrograd.py"


def garde(outil, tool_input, en_seance=False):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(RACINE)}
    env.pop("ML_SEANCE", None)
    if en_seance:
        env["ML_SEANCE"] = "1"
    entree = json.dumps({"tool_name": outil, "tool_input": tool_input, "cwd": str(RACINE)})
    p = subprocess.run(
        [sys.executable, str(GARDE)],
        input=entree,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    return p.returncode, p.stderr


def edition(chemin, en_seance=False, outil="Write"):
    cle = "notebook_path" if outil == "NotebookEdit" else "file_path"
    return garde(outil, {cle: str(RACINE / chemin)}, en_seance)


def bash(commande, en_seance=False):
    return garde("Bash", {"command": commande}, en_seance)


@pytest.mark.parametrize(
    "chemin",
    [
        MIEN,
        f"{LECON}/notes.md",
        f"{LECON}/explore.py",
        "courses/maths/01-linear-algebra/linalg.py",
        "core/nn.py",
        "papers/2003-bengio-nplm/repro.py",
        "papers/2003-bengio-nplm/notes.md",
        "rebuilds/01-micrograd-2026-12/micrograd.py",
    ],
)
def test_refuse_les_fichiers_de_lambert(chemin):
    for outil in ("Write", "Edit", "MultiEdit"):
        code, err = edition(chemin, outil=outil)
        assert code == 2 and "à Lambert" in err, (outil, chemin, err)


def test_refuse_un_notebook_de_lambert():
    code, err = edition(f"{LECON}/micrograd.ipynb", outil="NotebookEdit")
    assert code == 2 and "à Lambert" in err


@pytest.mark.parametrize(
    "chemin",
    [
        f"{LECON}/test_micrograd.py",
        f"{LECON}/plot.py",
        f"{LECON}/data.py",
        f"{LECON}/README.md",
        f"{LECON}/exercises.md",
        f"{LECON}/ref/micrograd.py",
        "papers/2003-bengio-nplm/test_repro.py",
        "glossary.md",
        "questions.md",
        "README.md",
    ],
)
def test_laisse_les_fichiers_de_claude(chemin):
    assert edition(chemin)[0] == 0


def test_laisse_le_journal_hors_depot(tmp_path):
    assert garde("Write", {"file_path": str(tmp_path / "journal.md")})[0] == 0


@pytest.mark.parametrize(
    "commande",
    [
        f"cat {MIEN}",
        f"uv run pytest {LECON} -q",
        f"uv run pytest {LECON} -q 2>&1 | tail -20",
        f"uv run pytest {LECON} -q > /tmp/sortie.txt",
        "git status",
        "date",
        f"ls -la {LECON}/",
        "echo x > /dev/null",
        f"uv run ruff format {MIEN}",
        "mkdir -p courses/zero-to-hero/02-makemore-bigram",
        f"echo 'see {MIEN}' > questions.md",
        f"cat > questions.md <<'EOF'\n- 2026-11-07 · 01-micrograd · why does {MIEN} need += ?\nEOF",
        f"cat > ~/notes/projets/ml/journal.md <<'EOF'\n- Reprendre ici : {MIEN}, test 3.\nEOF",
        f"cat > {LECON}/test_micrograd.py <<'EOF'\nx\nEOF",
        f"cat > {LECON}/ref/micrograd.py <<'EOF'\nx\nEOF",
        f"cp {LECON}/test_micrograd.py rebuilds/01-micrograd-2026-12/",
        f"cp {LECON}/test_micrograd.py rebuilds/01-micrograd-2026-12/test_micrograd.py",
        f"cp {MIEN} /tmp/copie.py",
        f"git commit -m '01-micrograd: backward on {MIEN} (3/5)'",
    ],
)
def test_bash_passe(commande):
    code, err = bash(commande)
    assert code == 0, (commande, err)


@pytest.mark.parametrize(
    "commande",
    [
        f"cat > {MIEN} <<'EOF'\nx\nEOF",
        f"cat >{MIEN} <<'EOF'\nx\nEOF",
        f"echo x >> {LECON}/notes.md",
        f"echo x | tee {LECON}/notes.md",
        f"echo x | tee -a {MIEN}",
        f"cp {LECON}/ref/micrograd.py {MIEN}",
        f"cp {LECON}/ref/micrograd.py {LECON}/",
        f"sed -i '' 's/a/b/' {MIEN}",
        f"rm {MIEN}",
        f"rm -rf {LECON}",
        f"git mv {MIEN} core/micrograd.py",
        f"git rm {MIEN}",
        f"uv run pytest -q && cat > {MIEN} <<'EOF'\nx\nEOF",
    ],
)
def test_bash_refuse(commande):
    code, err = bash(commande)
    assert code == 2 and "à Lambert" in err, (commande, err)


@pytest.mark.parametrize(
    "chemin",
    [
        "CLAUDE.md",
        ".claude/agents/tuteur.md",
        ".claude/hooks/garde.py",
        "bin/ml",
        "tests/test_garde.py",
        "pyproject.toml",
        "uv.lock",
    ],
)
def test_methode_fermee_en_seance_seulement(chemin):
    assert edition(chemin)[0] == 0
    code, err = edition(chemin, en_seance=True)
    assert code == 2 and "méthode" in err, err


def test_methode_bash_en_seance():
    assert bash("cat CLAUDE.md", en_seance=True)[0] == 0
    assert bash("cat > CLAUDE.md <<'EOF'\nx\nEOF", en_seance=True)[0] == 2
    assert bash("cat > CLAUDE.md <<'EOF'\nx\nEOF")[0] == 0


def test_entree_illisible_laisse_passer():
    p = subprocess.run(
        [sys.executable, str(GARDE)],
        input="pas du json",
        capture_output=True,
        text=True,
        check=False,
    )
    assert p.returncode == 0
