#!/usr/bin/env python3
"""La garde du dépôt ml : ce que Claude n'écrit pas (`CLAUDE.md`, « Qui écrit quoi »).

Hook PreToolUse (`.claude/settings.json`) sur Edit, Write, MultiEdit, NotebookEdit et Bash. Lit sur
l'entrée standard le JSON de Claude Code et refuse, sortie 2 et raison sur stderr :
- un outil d'édition sur un fichier de Lambert : sous `courses/`, `core/`, `papers/` et `rebuilds/`,
  tout fichier qui n'est pas à Claude (`README.md`, `test_*.py`, `conftest.py`, `data.py`, `plot.py`,
  `exercises.md`, `__init__.py`, et tout ce qui est sous un dossier `ref/`) ;
- une ligne Bash dont un geste d'écriture vise un fichier de Lambert : la cible d'un `>` ou `>>`,
  les fichiers de `tee` et de `sed -i`, la destination de `cp` et `mv` (ou, si c'est un dossier, le
  fichier qui y naîtrait), les cibles de `rm`, de `git rm` et de `git mv`. Un chemin seulement nommé
  (`uv run pytest courses/…`, le corps d'un heredoc, un message de commit) n'est pas un geste ;
- en séance (`ML_SEANCE=1`, posé par `bin/ml seance`), les mêmes gestes sur la méthode :
  `CLAUDE.md`, `.claude/`, `bin/`, `tests/`, `pyproject.toml`, `uv.lock` (`CLAUDE.md`, « Changer la
  méthode »).
Hors du dépôt (le journal dans `~/notes`), tout passe.

Trous connus, tenus par le prompt du tuteur : un script Python qui ouvre le fichier lui-même, un
heredoc donné à `python`, un chemin construit par variable ou par glob, une cible entre guillemets
qui contient une espace, un `cd` suivi d'un chemin relatif (la ligne est jugée depuis le `cwd` de la
session). Python 3.9 et bibliothèque standard, comme les hooks d'equipe.
Relevé du 6 novembre 2026 : la première version jugeait chaque mot de la ligne dès qu'un `>` s'y
trouvait, et refusait un `README.md` qui citait le dossier d'une leçon ; d'où le jugement par geste.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Iterator
from pathlib import Path

ZONES = ("courses", "core", "papers", "rebuilds")
A_CLAUDE = {"README.md", "conftest.py", "data.py", "plot.py", "exercises.md", "__init__.py"}
METHODE = ("CLAUDE.md", ".claude", "bin", "tests", "pyproject.toml", "uv.lock")
# Une ligne se coupe en commandes simples aux séparateurs du shell et aux sauts de ligne : le corps
# d'un heredoc devient des « commandes » qui ne commencent par aucun verbe d'écriture.
SEPARATEURS = re.compile(r"\|\||&&|[;|\n()`]")
# La cible d'une redirection : `> f`, `>f`, `>> f`. `2>&1` et `>&2` n'en ont pas.
REDIRECTION = re.compile(r">>?\s*([^\s>&|;]+)")
ECRIVAINS = ("tee", "sed", "cp", "mv", "rm")


def racine() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


def relatif(chemin: str, cwd: Path) -> Path | None:
    """Le chemin depuis la racine du dépôt, ou None s'il est dehors."""
    p = Path(os.path.expanduser(chemin.strip("'\"")))
    if not p.is_absolute():
        p = cwd / p
    try:
        return p.resolve().relative_to(racine())
    except ValueError:
        return None


def a_lambert(rel: Path) -> bool:
    if not rel.parts or rel.parts[0] not in ZONES:
        return False
    if "ref" in rel.parts[1:-1]:
        return False
    nom = rel.name
    return not (nom in A_CLAUDE or (nom.startswith("test_") and nom.endswith(".py")))


def methode(rel: Path) -> bool:
    return bool(rel.parts) and rel.parts[0] in METHODE


def refus(rel: Path, en_seance: bool) -> str | None:
    if a_lambert(rel):
        return (
            f"`{rel}` est à Lambert : il l'écrit lui-même (CLAUDE.md, « Qui écrit quoi »). "
            "Explique, pose une question, ou écris une référence dans `ref/` sur le mot « solution »."
        )
    if en_seance and methode(rel):
        return (
            f"`{rel}` est la méthode, fermée en séance (CLAUDE.md, « Changer la méthode ») : "
            "une règle change dans une session `claude` sans agent."
        )
    return None


def cibles(commande: str) -> Iterator[str]:
    """Les chemins que la ligne écrit, déplace ou efface, commande simple par commande simple."""
    for simple in SEPARATEURS.split(commande):
        for m in REDIRECTION.finditer(simple):
            yield m.group(1)
        mots = simple.split()
        if not mots:
            continue
        verbe, args = mots[0], mots[1:]
        if verbe == "git" and args and args[0] in ("rm", "mv"):
            verbe, args = args[0], args[1:]
        if verbe not in ECRIVAINS:
            continue
        if verbe == "sed" and not any(a.startswith("-i") for a in args):
            continue
        args = [a for a in args if not a.startswith("-") and a not in ("''", '""')]
        if verbe == "sed":
            args = args[1:]  # l'expression d'abord, puis les fichiers
        if verbe in ("cp", "mv") and len(args) >= 2:
            dest, sources = args[-1], args[:-1]
            if dest.endswith("/") or not Path(dest).suffix:
                for s in sources:
                    yield str(Path(dest.strip("'\"")) / Path(s.strip("'\"")).name)
            else:
                yield dest
            continue
        for a in args:
            yield a


def refus_bash(commande: str, cwd: Path, en_seance: bool) -> str | None:
    for cible in cibles(commande):
        rel = relatif(cible, cwd)
        if rel is None:
            continue
        message = refus(rel, en_seance)
        if message:
            return message
    return None


def main() -> None:
    try:
        entree = json.load(sys.stdin)
        outil = entree["tool_name"]
        tool_input = entree.get("tool_input") or {}
        cwd = Path(entree.get("cwd") or os.getcwd())
    except Exception:  # noqa: BLE001 : entrée illisible, on laisse passer, comme equipe
        sys.exit(0)
    en_seance = os.environ.get("ML_SEANCE") == "1"
    if outil == "Bash":
        commande = tool_input.get("command")
        message = refus_bash(commande, cwd, en_seance) if isinstance(commande, str) else None
    else:
        fichier = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not isinstance(fichier, str):
            sys.exit(0)
        rel = relatif(fichier, cwd)
        message = refus(rel, en_seance) if rel is not None else None
    if message:
        print(f"Garde ml : {message}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
